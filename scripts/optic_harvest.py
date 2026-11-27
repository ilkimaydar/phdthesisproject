#!/usr/bin/env python3
"""Harvest candidate papers on LIGHT and OPTIC attacks from the arXiv API (no LLM, metadata and abstracts only).

Usage: python scripts/optic_harvest.py
Writes work/OPTIC/candidates.tsv (arxiv_id, year, first_author, title, score, in_catalog, abstract_excerpt) and
work/OPTIC/query_log.tsv. Requests go through scripts/lit_verify.py (shared spacing and shared stop after any 4xx).
Candidates are NOT catalog rows: relevance is a keyword score; a person or agent still reads each record and writes
the row (skill lit-verify), after which scripts/lit_verify.py arxiv <id> verifies it.
"""
import csv
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lit_verify as lv  # noqa: E402

ROOT = lv.ROOT
OUT = ROOT / "work" / "OPTIC"
QUERIES = [
    'all:laser AND all:adversarial AND (all:camera OR all:"traffic sign" OR all:detection)',
    'all:infrared AND all:adversarial AND (all:camera OR all:driving OR all:detection)',
    '(all:projector OR all:projection) AND all:adversarial AND (all:detection OR all:driving OR all:camera)',
    '(all:"rolling shutter" OR all:flicker) AND (all:attack OR all:adversarial) AND all:camera',
    '(all:reflection OR all:reflective OR all:retroreflective) AND all:adversarial AND (all:physical OR all:"traffic sign")',
    'all:"adversarial light" OR all:"adversarial illumination" OR all:"adversarial laser" OR all:"optical adversarial"',
    'all:shadow AND all:adversarial AND (all:"traffic sign" OR all:detection)',
    '(all:glare OR all:headlight OR all:"lens flare") AND (all:attack OR all:adversarial OR all:robustness) AND all:detection',
    '(all:"auto-exposure" OR all:exposure) AND all:attack AND all:camera',
    '(all:phantom OR all:"fake object" OR all:ghost) AND all:attack AND (all:ADAS OR all:driving)',
    'all:camera AND (all:"sensor attack" OR all:"signal injection") AND all:driving',
    'all:adversarial AND all:night AND (all:detection OR all:"traffic sign")',
    'all:"physical-world" AND all:adversarial AND (all:light OR all:optical)',
    'all:spotlight AND all:adversarial',
    '(all:"traffic light" OR all:"traffic signal") AND all:adversarial AND all:physical',
    'all:"physical adversarial" AND all:defense AND (all:detection OR all:camera) AND (all:light OR all:illumination)',
    'all:adversarial AND (all:thermal OR all:infrared) AND (all:pedestrian OR all:vehicle) AND all:physical',
    'all:light AND all:attack AND all:"sign recognition"',
]
KEY = re.compile(r"(laser|infrared|\bIR\b|projector|projection|flicker|rolling.?shutter|\bLED\b|reflect|retroreflect|glare|headlight|exposure|flare|optical|light|illumin|shadow|ghost|phantom|spotlight|lens|image sensor|invisible|stealth)", re.I)
ATT = re.compile(r"(adversarial|attack|spoof|inject|perturb|evasion|malicious|manipulat)", re.I)
DOM = re.compile(r"(autonomous|driving|vehicle|traffic|ADAS|object detect|camera|perception|road|sign|lane)", re.I)


def catalog_ids():
    ids, dois = set(), set()
    for path in (ROOT / "catalog").glob("P2_*_catalog.csv"):
        with open(path, encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("arxiv_id"):
                    ids.add(lv.norm_arxiv(row["arxiv_id"]))
                if row.get("doi", "").lower().startswith("10.48550/arxiv."):
                    ids.add(row["doi"].lower().split("arxiv.", 1)[1])
    return ids


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    known = catalog_ids()
    found = {}
    with open(OUT / "query_log.tsv", "a", encoding="utf-8", newline="\n") as qlog:
        for number, query in enumerate(QUERIES, 1):
            url = ("https://export.arxiv.org/api/query?max_results=40&sortBy=relevance&search_query="
                   + urllib.parse.quote(query))
            entries = lv.arxiv_entries(lv.get(url))
            qlog.write("\t".join([lv.now(), "arxiv", f"Q{number}", query.replace("\t", " "), str(len(entries))]) + "\n")
            for entry in entries:
                text = entry["title"] + " " + entry["abstract"]
                score = (2 if KEY.search(text) else 0) + (1 if ATT.search(text) else 0) + (1 if DOM.search(text) else 0) + (1 if KEY.search(entry["title"]) else 0)
                if entry["key"] not in found or found[entry["key"]]["q"] > number:
                    found[entry["key"]] = {**entry, "score": score, "q": number}
            print(f"Q{number}: {len(entries)} results, {len(found)} unique so far")
    rows = sorted(found.values(), key=lambda r: (-r["score"], r["key"]))
    with open(OUT / "candidates.tsv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["arxiv_id", "year", "first_author", "title", "score", "in_catalog", "query", "abstract_excerpt"])
        for r in rows:
            writer.writerow([r["key"], (r["years"] or [""])[0], r["first_author"], r["title"], r["score"],
                             1 if r["key"] in known else 0, r["q"], r["abstract"][:300]])
    new = [r for r in rows if r["key"] not in known]
    print(f"candidates {len(rows)}; not in catalog {len(new)}; score >= 4 and not in catalog {sum(1 for r in new if r['score'] >= 4)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
