# README - exp/P2_oa

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
