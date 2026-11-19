#!/usr/bin/env python3
"""Find legal open-access PDF locations for catalog rows. Metadata only: no PDF is fetched here.

Usage: python scripts/oa_resolve.py [LABEL ...]
  default: every work/<LABEL>/rows.jsonl except SELFTEST
Writes work/OA_RESOLVE/oa_manifest.csv (one line per catalog row, rebuilt on each run) and appends every
OpenAlex answer to work/OA_RESOLVE/oa_ledger.jsonl (reused later, so each DOI is asked only once).

Choice of location per row:
  pdf_url      OpenAlex best open-access location with a PDF link when there is one, otherwise the arXiv copy
               at https://export.arxiv.org/pdf/<id> (arXiv asks automated tools to use the export host)
  alt_pdf_url  the arXiv copy when pdf_url came from OpenAlex and the row has an arXiv id
  route        openalex, arxiv, landing (open-access landing page without a PDF link) or none
Network rules come from scripts/lit_verify.py: shared spacing per host and the shared stop after a 4xx.
"""
import csv
import json
import pathlib
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lit_verify as lv  # noqa: E402

ROOT = lv.ROOT
OUT = ROOT / "work" / "OA_RESOLVE"
FIELDS = ["paper_id", "dup_of", "label", "title", "first_author", "year", "doi", "arxiv_id", "route", "pdf_url", "alt_pdf_url",
          "landing_url", "oa_status", "license", "version", "host", "note"]


def load_rows(labels):
    rows = []
    for folder in sorted((ROOT / "work").iterdir()):
        if not folder.is_dir() or folder.name in ("SELFTEST", "OA_RESOLVE") or (labels and folder.name not in labels):
            continue
        path = folder / "rows.jsonl"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            row["_label"] = folder.name
            rows.append(row)
    return rows


def load_ledger():
    known = {}
    path = OUT / "oa_ledger.jsonl"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                known[record["doi"]] = record
    return known


def ask_openalex(dois, known):
    todo = [d for d in dois if d not in known and "," not in d]
    for start in range(0, len(todo), 50):
        batch = todo[start:start + 50]
        flt = "|".join("https://doi.org/" + d for d in batch)
        url = ("https://api.openalex.org/works?per-page=50&select=doi,open_access,best_oa_location&filter=doi:"
               + urllib.parse.quote(flt, safe=":/|"))
        try:
            data = json.loads(lv.get(url))
        except SystemExit:
            print("openalex stopped; rows not asked yet keep route none for this run")
            return
        seen = set()
        with open(OUT / "oa_ledger.jsonl", "a", encoding="utf-8", newline="\n") as handle:
            for work in data.get("results", []):
                access = work.get("open_access") or {}
                best = work.get("best_oa_location") or {}
                record = {"at": lv.now(), "doi": lv.norm_doi(work.get("doi") or ""), "is_oa": bool(access.get("is_oa")),
                          "oa_status": access.get("oa_status") or "", "pdf_url": best.get("pdf_url") or "",
                          "landing_url": best.get("landing_page_url") or "", "license": best.get("license") or "",
                          "version": best.get("version") or ""}
                known[record["doi"]] = record
                seen.add(record["doi"])
                handle.write(json.dumps(record, ensure_ascii=False) + "\n")
            for doi in batch:
                if doi not in seen:
                    record = {"at": lv.now(), "doi": doi, "is_oa": False, "oa_status": "no_record", "pdf_url": "",
                              "landing_url": "", "license": "", "version": ""}
                    known[doi] = record
                    handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_rows(set(sys.argv[1:]))
    known = load_ledger()
    dois = sorted({lv.norm_doi(r["doi"]) for r in rows if r.get("doi") and not lv.norm_doi(r["doi"]).startswith("10.48550/")})
    ask_openalex(dois, known)
    out, counts, first_seen = [], {}, {}
    for row in rows:
        doi = lv.norm_doi(row.get("doi")) if row.get("doi") else ""
        arxiv = lv.norm_arxiv(row.get("arxiv_id")) if row.get("arxiv_id") else ""
        if not arxiv and doi.startswith("10.48550/arxiv."):
            arxiv = doi.split("arxiv.", 1)[1]
        record = known.get(doi, {}) if doi else {}
        arxiv_pdf = "https://export.arxiv.org/pdf/" + arxiv if arxiv else ""
        route, pdf, alt, landing, note = "none", "", "", "", ""
        if record.get("pdf_url"):
            route, pdf, landing = "openalex", record["pdf_url"], record.get("landing_url", "")
            alt = arxiv_pdf if arxiv_pdf and "arxiv.org" not in pdf else ""
        elif arxiv_pdf:
            route, pdf, landing = "arxiv", arxiv_pdf, "https://arxiv.org/abs/" + arxiv
            note = "arXiv copy; licence not checked; may differ from the published version"
        elif record.get("is_oa") and record.get("landing_url"):
            route, landing = "landing", record["landing_url"]
            note = "open-access landing page without a PDF link"
        elif doi and doi not in known:
            note = "not asked yet"
        for prefix in ("https://arxiv.org/pdf/", "http://arxiv.org/pdf/", "https://www.arxiv.org/pdf/"):
            if pdf.startswith(prefix):
                pdf = "https://export.arxiv.org/pdf/" + pdf[len(prefix):]
        key = doi or ("arxiv:" + arxiv if arxiv else "title:" + "".join(c for c in row.get("title", "").lower() if c.isalnum()))
        dup_of = first_seen.setdefault(key, row.get("paper_id", ""))
        dup_of = "" if dup_of == row.get("paper_id", "") else dup_of
        if dup_of:
            counts["duplicate"] = counts.get("duplicate", 0) + 1
        counts[route] = counts.get(route, 0) + 1
        out.append({"paper_id": row.get("paper_id", ""), "dup_of": dup_of, "label": row["_label"], "title": row.get("title", ""),
                    "first_author": row.get("first_author", ""), "year": row.get("year", ""), "doi": doi,
                    "arxiv_id": arxiv, "route": route, "pdf_url": pdf, "alt_pdf_url": alt, "landing_url": landing,
                    "oa_status": record.get("oa_status", ""), "license": record.get("license", ""),
                    "version": record.get("version", ""), "host": urllib.parse.urlsplit(pdf).netloc if pdf else "",
                    "note": note})
    with open(OUT / "oa_manifest.csv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(out)
    hosts = {}
    for item in out:
        if item["host"]:
            hosts[item["host"]] = hosts.get(item["host"], 0) + 1
    print(f"ROWS {len(out)}; by route: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    print("top PDF hosts: " + ", ".join(f"{h} {n}" for h, n in sorted(hosts.items(), key=lambda kv: -kv[1])[:8]))
    print("wrote work/OA_RESOLVE/oa_manifest.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
