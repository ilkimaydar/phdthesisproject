#!/usr/bin/env python3
"""Validate work/<LABEL>/rows.jsonl against the catalog schema and the verification ledger.

Usage:
  python scripts/rows_check.py <LABEL>          validate and print counts and problems
  python scripts/rows_check.py <LABEL> --csv    also write catalog/P2_<LABEL>_catalog.csv

Schema and allowed values: catalog/README.md. The verification state of a row is computed here from
work/<LABEL>/verify_ledger.jsonl (written by scripts/lit_verify.py); nobody types it by hand.
Exit code 0 when no row has a schema problem, 1 otherwise.
"""
import csv
import difflib
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCKS = {"LIT_A1": 100, "LIT_A2": 200, "LIT_A3": 300, "LIT_A4": 400, "LIT_A5": 500, "LIT_X": 600, "LIT_IEEE": 700, "SELFTEST": 900,
          **{f"LIT_X{n}": 900 + 100 * n for n in range(1, 15)}, "DECK_SRC": 2400, "EMBED_1": 2500, "LIT_OPT": 2600}
FIELDS = ["paper_id", "category", "role", "title", "first_author", "venue", "year", "doi", "arxiv_id", "url", "key_idea", "method",
          "data", "reported_result", "relation_to_project", "relevance", "code_or_data", "read_level", "peer_review", "notes"]
REQUIRED = ["paper_id", "category", "role", "title", "first_author", "venue", "year", "url", "key_idea", "relation_to_project",
            "relevance", "read_level", "peer_review"]
ENUMS = {
    "role": {"ATTACK", "DEFENSE", "DETECTION", "DATASET", "BENCHMARK", "SURVEY", "TOOL", "METHOD"},
    "relevance": {"High", "Medium", "Low"},
    "read_level": {"abstract", "metadata-only", "full-text"},
    "peer_review": {"peer-reviewed", "preprint", "unknown"},
}
EXTRA = ["verification_status", "verified_via", "verified_at_utc", "citations", "citations_retrieved_utc"]


def norm(text):
    text = unicodedata.normalize("NFKD", str(text or ""))
    return re.sub(r"[^a-z0-9]+", "", "".join(c for c in text if not unicodedata.combining(c)).lower())


def norm_doi(text):
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", str(text or "").strip(), flags=re.I)
    return re.sub(r"^doi:\s*", "", text, flags=re.I).lower()


def norm_arxiv(text):
    text = re.sub(r"^https?://arxiv\.org/(abs|pdf)/", "", str(text or "").strip(), flags=re.I)
    return re.sub(r"v\d+$", "", re.sub(r"^arxiv:\s*", "", text, flags=re.I))


def load_ledger(folder):
    ledger = {}
    path = folder / "verify_ledger.jsonl"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                ledger[(record["source"], record["key"])] = record
    return ledger


def title_match(a, b):
    a, b = norm(a), norm(b)
    if not a or not b:
        return False
    if len(min(a, b, key=len)) >= 20 and (a in b or b in a):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.9


def verify(row, ledger):
    keys = []
    if row.get("doi"):
        keys.append(("crossref", norm_doi(row["doi"])))
    if row.get("arxiv_id"):
        keys.append(("arxiv", norm_arxiv(row["arxiv_id"])))
    best = ("UNVERIFIED", "no ledger record for this row" if keys else "row has no DOI and no arXiv id", "")
    for source, key in keys:
        record = ledger.get((source, key))
        if record is None:
            continue
        if record["status"] == "NOT_FOUND":
            best = ("NOT_FOUND", f"{source} {key}", record["at"])
            continue
        author_a, author_b = norm(record.get("first_author")), norm(row.get("first_author"))
        checks = {
            "title": title_match(row.get("title"), record.get("title")),
            "author": bool(author_a) and bool(author_b) and (author_a in author_b or author_b in author_a),
            "year": any(y.isdigit() and str(row.get("year", "")).isdigit() and abs(int(y) - int(row["year"])) <= 1 for y in record.get("years", [])),
        }
        if all(checks.values()):
            name = "Crossref works record" if source == "crossref" else "arXiv API record"
            state = "VERIFIED" if source == "crossref" else "ARXIV_API_VERIFIED"
            return state, f"{name} {key} via scripts/lit_verify.py; title, first author and year match", record["at"]
        best = ("MISMATCH", f"{source} {key} differs in: " + ", ".join(k for k, ok in checks.items() if not ok), record["at"])
    return best


def citations(row, ledger):
    for source in ("openalex", "crossref"):
        record = ledger.get((source, norm_doi(row.get("doi")))) if row.get("doi") else None
        if record and record.get("cited_by") is not None:
            return str(record["cited_by"]), record["at"]
    return "", ""


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = [a for a in sys.argv[1:] if a != "--csv"]
    if len(args) != 1 or args[0] not in BLOCKS:
        print(__doc__)
        print("known labels: " + ", ".join(BLOCKS))
        return 2
    label = args[0]
    folder = ROOT / "work" / label
    rows_path = folder / "rows.jsonl"
    if not rows_path.exists():
        print(f"missing {rows_path}")
        return 2
    ledger = load_ledger(folder)
    problems, out_rows, seen_ids, seen_keys = [], [], set(), {}
    counts = {"state": {}, "role": {}, "relevance": {}}
    base = BLOCKS[label]
    for number, line in enumerate(rows_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as error:
            problems.append(f"line {number}: not valid JSON ({error})")
            continue
        pid = str(row.get("paper_id", ""))
        where = f"line {number} {pid}"
        for key in REQUIRED:
            if not str(row.get(key, "")).strip():
                problems.append(f"{where}: missing {key}")
        unknown = [k for k in row if k not in FIELDS]
        if unknown:
            problems.append(f"{where}: unknown keys {unknown}")
        match = re.match(r"^P2-P(\d{3,4})$", pid)
        if not match or not (base < int(match.group(1)) < base + 100):
            problems.append(f"{where}: paper_id must be P2-P{base + 1:03d} to P2-P{base + 99:03d}")
        if pid in seen_ids:
            problems.append(f"{where}: duplicate paper_id")
        seen_ids.add(pid)
        for key, allowed in ENUMS.items():
            if row.get(key) not in allowed:
                problems.append(f"{where}: {key} must be one of {sorted(allowed)}")
        if not re.match(r"^\d{4}$", str(row.get("year", ""))):
            problems.append(f"{where}: year must be 4 digits")
        if len(str(row.get("key_idea", "")).split()) > 35:
            problems.append(f"{where}: key_idea is longer than 35 words")
        for kind, value in (("doi", norm_doi(row.get("doi"))), ("title", norm(row.get("title")))):
            if value:
                if (kind, value) in seen_keys:
                    problems.append(f"{where}: same {kind} as {seen_keys[(kind, value)]}")
                seen_keys[(kind, value)] = pid
        state, via, at = verify(row, ledger)
        cited, cited_at = citations(row, ledger)
        counts["state"][state] = counts["state"].get(state, 0) + 1
        for key in ("role", "relevance"):
            counts[key][str(row.get(key))] = counts[key].get(str(row.get(key)), 0) + 1
        out_rows.append({**{k: row.get(k, "") for k in FIELDS}, "verification_status": state, "verified_via": via,
                         "verified_at_utc": at, "citations": cited, "citations_retrieved_utc": cited_at})
    print(f"ROWS {len(out_rows)}; schema problems {len(problems)}")
    for key in ("state", "role", "relevance"):
        print(f"by {key}: " + ", ".join(f"{k} {v}" for k, v in sorted(counts[key].items())))
    for row in out_rows:
        if row["verification_status"] in ("MISMATCH", "NOT_FOUND"):
            print(f"{row['verification_status']}\t{row['paper_id']}\t{row['verified_via']}")
    for problem in problems[:60]:
        print("PROBLEM\t" + problem)
    if "--csv" in sys.argv:
        target = (folder if label == "SELFTEST" else ROOT / "catalog") / f"P2_{label}_catalog.csv"
        with open(target, "w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS + EXTRA)
            writer.writeheader()
            writer.writerows(out_rows)
        print(f"wrote {target.relative_to(ROOT)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
