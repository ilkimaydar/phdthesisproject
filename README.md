# PhD thesis research: detecting physical visual attacks on object detection in autonomous vehicles

Repository description: udcphdthesisrepository

Working title of the current paper: **Lightweight and Explainable AI for Detecting Adversarial Attacks on Object Detection in Autonomous Vehicles.**

Physical attacks such as altered signs, stickers, shadows, reflected or projected light, and manipulations that unfold over video frames can make a camera-based detector miss, mislabel or invent objects. This project asks whether cheap, explainable consistency checks placed around an unchanged detector can flag such attacks, including at night and in poor visibility, without slowing the vehicle's perception.

**Status: work in progress, literature-mapping phase. No experiment has been run, so this repository reports no results. Nothing here is peer reviewed or independently audited.**

## Live

- Website: [ilkimaydar.github.io/phdthesisproject](https://ilkimaydar.github.io/phdthesisproject/) (GitHub Pages, deployed from `main` by `.github/workflows/pages.yml` once Pages is enabled with the source "GitHub Actions").

## Contents

| Path | What it is |
|---|---|
| `site/` | The website: overview, research design, searchable literature map, about page. Static HTML, CSS and JavaScript, light mode, no external scripts |
| `catalog/` | Literature catalogs, one CSV per search task. Schema and verification states in `catalog/README.md` |
| `notes/` | Notes per search task: problem map, solution map, closest prior work, gaps, problem cards. Written with AI assistance, not audited |
| `work/` | Provenance: staging rows, verification ledgers (raw Crossref and arXiv answers with timestamps), query logs, and `work/OA_RESOLVE/oa_manifest.csv` with open-access PDF locations |
| `scripts/` | `lit_verify.py` (metadata checks with a ledger), `rows_check.py` (schema and verification check, CSV builder), `oa_resolve.py` (open-access locations from OpenAlex and arXiv), `build_site.py` (builds `site/`), `make_oa_notebook.py`, `plog.py`. This repository is exported from a private working folder by a script that copies an allow list of files and runs a leak scan before every commit |
| `exp/P2_oa/` | Colab notebook that collects open-access PDFs into the owner's Google Drive (not into this repository) |
| `exp/P2_nb/` | Colab notebook skeletons for a CPU-first pilot on synthetic frames. Not run |

## How a paper enters the catalog

A candidate is looked up by DOI in Crossref or by identifier in the arXiv API. It counts as verified only when the title, first author and year of that record match the catalog row; `scripts/rows_check.py` computes this from the ledger, nobody types it. Summaries are short paraphrases, not copied abstracts. PDFs are never stored in this repository.

## Rebuild the site

```
python scripts/build_site.py site
```

Python 3.10 or newer, standard library only.

## Licence

Not chosen yet; until a licence file is added, all rights are reserved by the owner. Bibliographic data and titles belong to their publishers and authors.

## AI-use disclosure

The literature search, verification scripts, summaries, notebooks and website were produced with assistance from AI models (Anthropic Claude, run through the OpenCode agent tool) under the direction of the project owner. Catalog rows carry a machine-computed verification state; notes and summaries have not yet been independently audited.
