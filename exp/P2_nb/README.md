# exp/P2_nb - Colab notebook skeletons for the Paper 2 pilot

PILOT SKELETON - NOT RUN - synthetic data only - no result may be quoted from these notebooks. Not audited.

## Purpose

Two notebook skeletons that follow the deck's CPU-first route, so the first Paper 2 (P2) pilot can start in Google Colab from this Drive folder as soon as data is chosen. Nothing was installed or executed on the owner's computer, no notebook was run anywhere, and no dataset was downloaded. Brief: `briefs/NB_SKEL.md`. Progress log: `progress/NB_SKEL.log`.

## Files

| File | Contents | Cells (markdown + code) | Bytes |
|---|---|---|---|
| `P2_pilot_01_environment_and_data_manifest.ipynb` | Drive mount and one project path variable (`PROJECT_DIR`); runtime report (Python, CPU, RAM, GPU, free disk, library versions; reads only); data manifest; sha256 helpers and a split manifest by recording, with a demo on made-up file names; download placeholder without download code; status list | 14 (8 + 6) | 24013 |
| `P2_pilot_02_cue_features_synthetic.ipynb` | Five cue functions on frames the notebook draws itself (numpy and OpenCV, CPU only, fixed seed), one timing cell per function, and the list of what must replace the synthetic frames before any claim | 21 (9 + 12) | 25665 |
| `build_notebooks.py` | Writes both notebooks as nbformat 4.5 JSON and runs static checks. Standard library only. Never executes notebook code | - | - |
| `README.md` | This file | - | - |

sha256 of the files, from the build checked by the continuation agent:
- notebook 01: 0bf29e1450a485631130b4948d5fe8c759c69a7d4f7c2c10a02b6c193a356318
- notebook 02: 134461b275e1f05834986b2cfd8a928530bf22720ca85364a3995c45df3b9ea4
- builder: fdee7347e0a72211fbff421e5378d01295c5ce8ed072a151bc562b57334acb82

### Notebook 02 cue functions

| Function | Design slide (state/PROJECT_BRIEF.md section 3) | Synthetic input |
|---|---|---|
| `contour_box_agreement` | 01 Object Appearance | sign-like polygon on a textured background, with the drawn box and a loose box |
| `shadow_band_edge_stat` | 02 Shadows | dark slanted band through the frame centre |
| `saturated_region_stat` | 03 Reflections | bright blob clipped to white |
| `global_local_luminance_residual` | 04 Lighting | one gain on the whole frame; a blob inside the box |
| `flicker_stat` | 04 Lighting and 05 Video Frames | short sequences: static, one exposure step, horizontal stripes whose phase moves |

Each function returns raw statistics, sets no threshold and takes no decision. Its docstring states what it measures and what it does not show.

### Notebook 01 data manifest

Rows: BDD100K (video), PVDN, ACDC, Lost and Found, a low-light dataset the deck does not name, CODA (deck plan, state/DECK_DIGEST.md section 4); LISA and GTSRB (design slide 02). The names are labels from the owner's material, not confirmed facts. Every licence cell reads "to confirm from the official page" and every source address cell is empty. "APDE patch attacks" (design slide 01) has no row: the acronym is not identified (UNVERIFIED). Task LIT_X2 collects licences; the owner confirms each licence on the official page before any download.

## How to open a notebook in Colab from Drive

These steps were not tested by the agents that wrote the notebooks.

1. In Google Drive in the browser, open My Drive > US > Documents > Projects > PhD_Thesis_Research_UDC_CS > Opencode_PhD_Thesis_Research_UDC_CS > exp > P2_nb.
2. Right-click a notebook, then Open with > Google Colaboratory. If Colaboratory is not offered, connecting the Colab app to Drive is an owner action. Other route: in Colab, File > Open notebook > Google Drive, then search for the file name.
3. Run a copy, not the original: File > Save a copy in Drive. Colab saves outputs into the notebook it runs. The builder replaces a notebook only while its cells still match the digest stored in its metadata, so a run original is left alone and blocks a rebuild.
4. Notebook 01: Runtime > Run all and approve the Drive access prompt. The first code cell must print `project folder found: True` (it looks for this README); otherwise edit `PROJECT_DIR`. Nothing is saved while `SAVE_OUTPUTS` is False. When it is True, records go to new files under `exp/P2_nb/manifests/` and an existing file is never replaced.
5. Notebook 02: Runtime > Run all on a CPU runtime. It imports numpy and OpenCV (`cv2`); notebook 01 section 2 reports whether the runtime has them. It mounts no Drive and writes no file. Installing anything is an owner decision.

Third-party data goes to `DATA_DIR` (`/content/data` on the Colab disk), not into this link-shared Drive folder. The Colab disk does not persist between runtimes; where data is kept between sessions is an owner decision.

## Rebuild and check (on this computer, standard library only)

- `python exp/P2_nb/build_notebooks.py --check` builds both notebooks in memory, runs the checks, compares them with the files on disk and writes nothing.
- `python exp/P2_nb/build_notebooks.py` writes a notebook only when it is absent or an unmodified earlier build, then reads it back.
- Static checks: ast.parse and compile of every code cell; names read before any binding, cells taken in order; call arity of functions defined in the notebook; nbformat 4.5 layout; banner as first cell; licence cells pending and source address cells empty; no address-like text; no download code tokens; imports within an allowed set; a docstring on every function; one seeded timing cell per cue function; replacement list as last cell; size under 26000 bytes; ASCII only; no stored output. A self-test first feeds known-good and known-bad snippets to the checkers.

## Status

Fresh `--check` by the continuation agent (static checks only):
- checker self-test 18 of 18; RESULT: PASS; both notebooks on disk identical to the build.
- notebook 01: ast.parse 6 of 6 code cells, compile 6 of 6; undefined names 0; call arity problems 0; 15 functions, 15 with a docstring; manifest rows in code 8 and in the table 8, all licence cells pending and all source addresses empty; 1 download placeholder cell; 0 stored outputs; 0 problems.
- notebook 02: ast.parse 12 of 12 code cells, compile 12 of 12; undefined names 0; call arity problems 0; 16 functions, 16 with a docstring; 5 of 5 cue functions with a "Measures" and a "Does not show" part; 5 timing cells, one seeded cell per cue function; replacement list as last cell; 0 stored outputs; 0 problems.

Static checks do not show that a cell runs or that a statistic behaves as its docstring says. NOT RUN anywhere: numpy and OpenCV are not installed on this computer and were not installed. NOT AUDITED: written by agents with the NB_SKEL label; a fresh-agent audit is required.

## What is not done

- No notebook was executed, in Colab or elsewhere.
- `PROJECT_DIR` was derived from the Drive for desktop path of the project folder and was not checked in Colab.
- No dataset is chosen; no licence or source address is recorded; nothing is downloaded; no download cell exists.
- Library versions are reported, not pinned; there is no requirements file.
- `recording_of` assumes one folder per recording; each dataset needs its own recording or route key from its documentation. Split names and fractions are placeholders until an internal analysis plan, hashed before the first run, fixes them. The split helper has no stratification by condition.
- Not built: detector, tracker, viewpoint model, reliability gates, evidence accumulation of design slide 05, calibration, explanation output, abstain rule.
- A timing cell times one function on one small synthetic frame; it is not per-frame latency of a camera pipeline.
- What must replace the synthetic frames before any claim is made is the last cell of notebook 02.

## Review note (continuation agent; not applied to the notebooks; for the audit)

`shadow_band_edge_stat`: when an object mask is given, lit pixels on the mask edge can enter the dark/lit boundary set, and their 3x3 Sobel window then also covers the object-background edge. Eroding the mask by one pixel before the boundary set is formed would remove that term. With no dark band present, Otsu splits noise and `edge_sharpness` is a ratio of noise terms; read it together with `dark_fraction` and `luminance_ratio`.
