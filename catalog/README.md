# README - catalog/

## Purpose
Literature catalogs for P2 (the owner's Paper 2). One CSV per literature task, built by `python scripts/rows_check.py <LABEL> --csv` from the task's staging file work/<LABEL>/rows.jsonl and its verification ledger. Nobody edits a CSV by hand: fix the staging row and rebuild.

## Status
Kickoff: no catalog built yet. Counts are appended to the Change log by the coordinator after each hand-back.

## Row schema (one JSON object per line in work/<LABEL>/rows.jsonl)
| Key | Rule |
|---|---|
| paper_id | `P2-P###`, never reused. Blocks: LIT_A1 101-199, LIT_A2 201-299, LIT_A3 301-399, LIT_A4 401-499, LIT_A5 501-599, LIT_X 601-699 (unused), LIT_IEEE 701-799. Wave 2, four digits: LIT_X1 1001-1099, LIT_X2 1101-1199, and so on in steps of 100 up to LIT_X14 2301-2399; DECK_SRC 2401-2499 |
| category | Claim-family code and name from the task brief, for example `A2-F1 Shadow attacks` |
| role | ATTACK, DEFENSE, DETECTION, DATASET, BENCHMARK, SURVEY, TOOL or METHOD |
| title | Verbatim from the record |
| first_author | Family name of the first author |
| venue | Journal, conference or `arXiv preprint` |
| year | 4 digits (issue or proceedings year) |
| doi | Lowercase, no URL prefix, or empty |
| arxiv_id | For example `1707.08945`, or empty |
| url | Landing page: the doi.org link, the arXiv abstract page or the official venue page |
| key_idea | Own words, at most 35 words |
| method | Own words, one line |
| data | Datasets or physical setup named in the record read, or empty |
| reported_result | Paraphrase. A number only if the record read states it. Otherwise empty |
| relation_to_project | Which design slide and which element it supports, baselines or threatens (state/PROJECT_BRIEF.md section 3) |
| relevance | High, Medium or Low |
| code_or_data | Official code or dataset location if seen, else empty. Write UNVERIFIED after it when not confirmed |
| read_level | abstract, metadata-only or full-text |
| peer_review | peer-reviewed, preprint or unknown |
| notes | Free text: year differences, retraction marks, licence remarks, NEEDS_VERIFY |

Every key is present on every row; use an empty string where there is nothing to say.

## Verification states (computed by scripts/rows_check.py from the ledger, never typed)
| State | Meaning |
|---|---|
| VERIFIED | Crossref returned the row's DOI and title, first author and year match |
| ARXIV_API_VERIFIED | The arXiv API returned the row's arXiv id and title, first author and year (within one year) match. Preprint record: check the published version before citing |
| MISMATCH | A record was found but title, author or year differ. Fix the row |
| NOT_FOUND | The DOI or arXiv id does not exist in the source. The row stays and counts as UNVERIFIED |
| UNVERIFIED | No DOI or arXiv id, or no ledger record. The coordinator checks these on the official page |

## Sharing and copyright
This folder inherits link sharing from the main folder. It holds metadata and paraphrased notes only. No publisher PDF is placed here.

## Change log (append only)
- kickoff: schema written by the coordinator.
