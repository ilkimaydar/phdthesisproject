#!/usr/bin/env python3
"""Harvest candidate papers on LIGHT and OPTIC attacks from the Crossref works API (metadata only, no LLM).

Usage: python scripts/crossref_harvest.py
Writes work/OPTIC2/candidates.tsv (doi, year, first_author, title, venue, type, cited_by, score, in_catalog, publisher_group, query)
and work/OPTIC2/query_log.tsv. Requests go through scripts/lit_verify.py (shared spacing and shared stop after any 4xx).
Candidates are NOT catalog rows: the score is a keyword aid. A person or agent reads each record, writes the row
(skill lit-verify) and verifies it with scripts/lit_verify.py crossref <doi>.
publisher_group: ieee (DOI prefix 10.1109), acm (10.1145), usenix/ndss/other, springer (10.1007), elsevier (10.1016),
mdpi (10.3390), other. IEEE records are the leads for the owner's library session in Chrome (metadata only).
"""
import csv
import json
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lit_verify as lv  # noqa: E402

ROOT = lv.ROOT
OUT = ROOT / "work" / "OPTIC2"
SELECT = "DOI,title,author,issued,container-title,type,is-referenced-by-count"
FILTER = "from-pub-date:2017-01-01,type:journal-article,type:proceedings-article"
QUERIES = [
    "adversarial laser attack camera object detection autonomous driving",
    "projector adversarial light attack traffic sign recognition",
    "flicker rolling shutter attack camera detection",
    "adversarial illumination physical attack autonomous vehicle camera",
    "infrared adversarial attack physical object detector",
    "reflection light attack physical adversarial autonomous driving",
    "remote camera perception attack light injection",
    "phantom object attack projection ADAS",
    "lens flare glare headlight adversarial robustness detection",
    "auto exposure attack camera perception",
    "high dynamic range fusion attack pulsed light camera",
    "optical adversarial attack camera lens sticker",
    "light-based defense detection of physical attacks traffic sign",
    "defense against laser and projector attacks on vision systems",
    "traffic light recognition adversarial physical attack light",
    "adversarial shadow attack traffic sign detection",
    "night time physical adversarial attack detection autonomous vehicle",
    "camera sensor spoofing blinding attack autonomous vehicle",
    "emergency vehicle lighting object detection failure",
    "benign illumination change versus adversarial attack detection camera",
    "lightweight detector adversarial physical attack real-time embedded vehicle",
    "consistency check temporal detection physical adversarial attack tracking",
]
KEY = re.compile(r"(laser|infrared|projector|projection|flicker|rolling.?shutter|\bLED\b|reflect|retroreflect|glare|headlight|exposure|flare|optical|\blight|illumin|shadow|ghost|phantom|spotlight|lens|blind|dazzle|strobe|pulse|HDR)", re.I)
ATT = re.compile(r"(adversarial|attack|spoof|inject|perturb|evasion|malicious|manipulat|defen[cs]e|detect|robust)", re.I)
DOM = re.compile(r"(autonomous|driving|vehicle|traffic|ADAS|object detect|camera|perception|road|sign|lane|vision)", re.I)


def group(doi):
    d = doi.lower()
    for prefix, name in (("10.1109/", "ieee"), ("10.1145/", "acm"), ("10.1007/", "springer"), ("10.1016/", "elsevier"),
                         ("10.3390/", "mdpi"), ("10.48550/", "arxiv"), ("10.14722/", "ndss"), ("10.1049/", "iet")):
        if d.startswith(prefix):
            return name
    return "other"


def catalog_dois():
    dois = set()
    for path in (ROOT / "catalog").glob("P2_*_catalog.csv"):
        with open(path, encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("doi"):
                    dois.add(lv.norm_doi(row["doi"]))
    return dois


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    known = catalog_dois()
    found = {}
    with open(OUT / "query_log.tsv", "a", encoding="utf-8", newline="\n") as qlog:
        for number, query in enumerate(QUERIES, 1):
            url = ("https://api.crossref.org/works?rows=40&select=" + SELECT + "&filter=" + FILTER
                   + "&query.bibliographic=" + urllib.parse.quote(query))
            try:
                body = lv.get(url)
            except Exception as error:  # noqa: BLE001
                print(f"Q{number}: stopped ({error})")
                qlog.write("\t".join([lv.now(), "crossref", f"Q{number}", query, "STOP"]) + "\n")
                break
            try:
                items = json.loads(body)["message"]["items"]
            except Exception:  # noqa: BLE001
                items = []
            qlog.write("\t".join([lv.now(), "crossref", f"Q{number}", query, str(len(items))]) + "\n")
            for item in items:
                doi = lv.norm_doi(item.get("DOI", ""))
                title = lv.clean((item.get("title") or [""])[0])
                if not doi or not title:
                    continue
                authors = item.get("author") or []
                first = (authors[0].get("family") or authors[0].get("name") or "") if authors else ""
                parts = (item.get("issued") or {}).get("date-parts") or [[None]]
                year = str((parts[0] or [""])[0] or "")
                venue = lv.clean((item.get("container-title") or [""])[0])
                score = (2 if KEY.search(title) else 0) + (1 if ATT.search(title) else 0) + (1 if DOM.search(title) else 0)
                if doi not in found:
                    found[doi] = {"doi": doi, "year": year, "first": first, "title": title, "venue": venue,
                                  "type": item.get("type", ""), "cited": item.get("is-referenced-by-count", ""),
                                  "score": score, "q": number}
            print(f"Q{number}: {len(items)} results, {len(found)} unique so far")
    rows = sorted(found.values(), key=lambda r: (-r["score"], r["doi"]))
    with open(OUT / "candidates.tsv", "w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t")
        writer.writerow(["doi", "year", "first_author", "title", "venue", "type", "cited_by", "score", "in_catalog",
                         "publisher_group", "query"])
        for r in rows:
            writer.writerow([r["doi"], r["year"], r["first"], r["title"], r["venue"], r["type"], r["cited"], r["score"],
                             1 if r["doi"] in known else 0, group(r["doi"]), r["q"]])
    new = [r for r in rows if r["doi"] not in known]
    print(f"candidates {len(rows)}; not in catalog {len(new)}; score >= 4 and not in catalog {sum(1 for r in new if r['score'] >= 4)}; "
          f"ieee not in catalog {sum(1 for r in new if group(r['doi']) == 'ieee')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
