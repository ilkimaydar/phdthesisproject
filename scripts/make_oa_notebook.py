#!/usr/bin/env python3
"""Write the Colab notebook that collects open-access PDFs into Drive (run by the owner in Colab, never here).

Usage: python scripts/make_oa_notebook.py
Writes exp/P2_oa/P2_oa_01_pdf_collector.ipynb and exp/P2_oa/README.md. An existing file is never overwritten:
the next free name with a _vNN suffix is used instead. Every code cell is checked with ast.parse first.
"""
import ast
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "exp" / "P2_oa"

INTRO = r"""# P2 open-access PDF collector (run in Google Colab by the owner)

Status: written by the coordinator. NOT RUN. Not audited.

What it does: reads the list of open-access PDF locations built by `scripts/oa_resolve.py` (file `work/OA_RESOLVE/oa_manifest.csv` in the project folder), downloads each PDF inside this Colab runtime (a Google computer, not your laptop), checks that it is a real PDF, and saves it into a Google Drive folder.

Built-in rules:
- Open-access copies only: the arXiv export host and the open-access locations listed by OpenAlex. No library proxy, no paywalled site, no shadow library.
- One request every 5 seconds to arXiv and every 6 seconds to any other host.
- A host that answers 401, 403, 420 or 429 is stopped for the rest of the run. Three answers in a row from one host that are not a PDF also stop that host.
- Files already in the folder are skipped. Rows marked as duplicates in the list are skipped.
- A download log is written next to the PDFs: `_download_log.csv`.

How to run:
1. In Google Drive, right-click this file, choose Open with, then Google Colaboratory.
2. Menu Runtime, then Run all.
3. Approve the Google Drive access dialog for your own account.
4. The first run fetches LIMIT = 20 items. Look at the folder. Then set LIMIT = None in the settings cell and run all again.

Where the files go: the folder in TARGET (settings cell). By default it sits next to the opencode folder, inside your PhD research folder, and it inherits that folder's sharing (anyone with the link at the time this notebook was written). With Drive for desktop in stream mode (the G: drive on your laptop) the PDFs stay online until you open them, unless the folder is marked available offline.

Copyright: these are personal research copies of open-access papers. Do not redistribute them.
"""

SETTINGS = r"""PROJECT = '/content/drive/MyDrive/US/Documents/Projects/PhD_Thesis_Research_UDC_CS'
MANIFEST = PROJECT + '/Opencode_PhD_Thesis_Research_UDC_CS/work/OA_RESOLVE/oa_manifest.csv'
TARGET = PROJECT + '/P2_open_access_PDFs'
LIMIT = 20          # first run: 20 items; set to None to process every row
PACE = {'export.arxiv.org': 5}
DEFAULT_PACE = 6    # seconds between requests to any other host
"""

MOUNT = r"""from google.colab import drive
drive.mount('/content/drive')
"""

COLLECT = r"""import csv, datetime, os, re, time, unicodedata, urllib.error, urllib.parse, urllib.request

os.makedirs(TARGET, exist_ok=True)
LOG = os.path.join(TARGET, '_download_log.csv')
UA = 'P2-open-access-collector/0.1 (academic research use; one request every few seconds)'
HARD_STOP = {401, 403, 420, 429}

def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

def ascii_name(text):
    text = unicodedata.normalize('NFKD', text or '')
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return re.sub('[^A-Za-z0-9]+', '', text) or 'Anon'

def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/pdf,*/*;q=0.5'})
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return response.status, response.headers.get('Content-Type', ''), response.read(60000000)
    except urllib.error.HTTPError as error:
        return error.code, '', b''
    except Exception as error:
        return 'network ' + type(error).__name__, '', b''

with open(MANIFEST, encoding='utf-8') as handle:
    rows = [r for r in csv.DictReader(handle) if r['pdf_url'] and not r.get('dup_of')]
if LIMIT:
    rows = rows[:LIMIT]

stopped, misses_in_row, results = set(), {}, []
new_log = not os.path.exists(LOG)
with open(LOG, 'a', newline='', encoding='utf-8') as log_handle:
    log = csv.writer(log_handle)
    if new_log:
        log.writerow(['utc', 'paper_id', 'url', 'status', 'bytes', 'result', 'file'])
    for row in rows:
        name = '%s_%s_%s.pdf' % (row['paper_id'], ascii_name(row['first_author']), row['year'] or 'nd')
        path = os.path.join(TARGET, name)
        if os.path.exists(path):
            results.append('already_in_folder')
            continue
        outcome = 'no_usable_url'
        for url in (row['pdf_url'], row.get('alt_pdf_url', '')):
            if not url:
                continue
            host = urllib.parse.urlsplit(url).netloc
            if host in stopped:
                outcome = 'host_stopped'
                continue
            status, ctype, data = fetch(url)
            if status == 200 and data[:5] == b'%PDF-' and len(data) >= 30000:
                with open(path, 'wb') as out:
                    out.write(data)
                outcome = 'saved'
                misses_in_row[host] = 0
            elif status in HARD_STOP:
                stopped.add(host)
                outcome = 'host_stopped_%s' % status
            else:
                misses_in_row[host] = misses_in_row.get(host, 0) + 1
                outcome = 'not_a_pdf_%s' % status
                if misses_in_row[host] >= 3:
                    stopped.add(host)
            log.writerow([utc_now(), row['paper_id'], url, status, len(data), outcome, name if outcome == 'saved' else ''])
            log_handle.flush()
            time.sleep(PACE.get(host, DEFAULT_PACE))
            if outcome == 'saved':
                break
        results.append(outcome)
        print(row['paper_id'], outcome)
"""

SUMMARY = r"""from collections import Counter
print('items in this run:', len(results))
for result, count in Counter(results).most_common():
    print('  ', result, count)
print('hosts stopped in this run:', ', '.join(sorted(stopped)) or 'none')
print('PDF files now in the folder:', sum(1 for f in os.listdir(TARGET) if f.lower().endswith('.pdf')))
print('log file:', LOG)
"""

README = r"""# README - exp/P2_oa

## Purpose
Collect open-access PDFs of catalogued papers into Google Drive for later reading and Colab work, without the IEEE library route (dropped by the owner) and without writing PDFs to the owner's laptop.

## Contents
| File | What it is |
|---|---|
| P2_oa_01_pdf_collector.ipynb | Colab notebook. The owner opens it from Drive with Google Colaboratory and runs it. Not run by any agent |
| ../../work/OA_RESOLVE/oa_manifest.csv | Input: one line per catalog row with its open-access PDF location, built by scripts/oa_resolve.py from OpenAlex and arXiv metadata |

## Status
Written by the coordinator, not run, not audited. The manifest is rebuilt each time scripts/oa_resolve.py runs, so later catalog rows are added by rerunning it before the notebook.

## Rules
Open-access copies only; paced requests; a host is stopped on 401, 403, 420 or 429, or after three non-PDF answers in a row; files already present are skipped. Personal research copies: do not redistribute.

## Change log (append only)
- first version written by scripts/make_oa_notebook.py.
"""


def lines(text):
    return text.splitlines(keepends=True)


def free_name(stem, suffix):
    target = OUT / f"{stem}{suffix}"
    number = 2
    while target.exists():
        target = OUT / f"{stem}_v{number:02d}{suffix}"
        number += 1
    return target


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    OUT.mkdir(parents=True, exist_ok=True)
    cells = [("markdown", INTRO), ("code", SETTINGS), ("code", MOUNT), ("code", COLLECT), ("code", SUMMARY)]
    notebook_cells = []
    for index, (kind, source) in enumerate(cells, 1):
        if kind == "code":
            ast.parse(source)
            notebook_cells.append({"cell_type": "code", "id": f"p2oa{index:02d}", "metadata": {}, "execution_count": None,
                                   "outputs": [], "source": lines(source)})
        else:
            notebook_cells.append({"cell_type": "markdown", "id": f"p2oa{index:02d}", "metadata": {}, "source": lines(source)})
    notebook = {"nbformat": 4, "nbformat_minor": 5, "cells": notebook_cells,
                "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3"},
                             "language_info": {"name": "python"}, "colab": {"provenance": []}}}
    nb_path = free_name("P2_oa_01_pdf_collector", ".ipynb")
    nb_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    readme = OUT / "README.md"
    if not readme.exists():
        readme.write_text(README, encoding="utf-8", newline="\n")
    json.loads(nb_path.read_text(encoding="utf-8"))
    print(f"wrote {nb_path.relative_to(ROOT)} ({len(notebook_cells)} cells, {sum(1 for k, _ in cells if k == 'code')} code cells parsed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
