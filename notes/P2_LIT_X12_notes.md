# P2_LIT_X12 notes - traffic-sign standards, priors and sign-specific defenses

Status: written by the LIT_X12 worker (first run stopped on a provider rate limit; this file was written by the continuation). NOT AUDITED: fresh-agent audit required. All problem cards are hypotheses, not results.

Catalogue: work/LIT_X12/rows.jsonl, 25 rows (P2-P2101 to P2-P2125), rows_check 0 problems. Verification states (computed by scripts/rows_check.py, never typed): VERIFIED 16, ARXIV_API_VERIFIED 5, UNVERIFIED 4 (P2-P2110, P2-P2111, P2-P2113, P2-P2115: Crossref and the arXiv API both answered HTTP 429 in this run, so no Crossref or arXiv record exists; OpenAlex matches title and year for the first three). Read depth: every row is abstract level; 10 rows also had parts of the paper text read in search-result excerpts (stated in each row's notes). Families: F1 5 rows, F2 5 rows, F3 15 rows.

## Problem map (attack families with the papers that define them)
| Attack family | Papers in this catalogue | What it means for a sign-prior check |
|---|---|---|
| Printed stickers or patches on the sign face | Jia 2022 NDSS (P2-P2125, detector-based TSR, production vehicle); Bayzidi 2022 (P2-P2124, realistic stickers on 11 classifiers); REAP 2023 (P2-P2121, realistic rendering benchmark) | The face changes; outline and mounting stay. A check of class against outline sees a contradiction only if the attack changes the predicted class to one with another standard shape or colour |
| Rectangular occlusion as a threat model | Wu 2019 DOA (P2-P2105); Rangsikunpum 2026 (P2-P2109) | Occluders cover class-critical features (Bayzidi: the digit of a speed limit); shape of the outline is untouched |
| Retroreflective patches visible only under headlights | Tsuruoka 2024 (P2-P2120) | Abuses the standardised retroreflective sheeting itself; daylight checks see nothing |
| Hiding and appearance attacks on detectors | Jia 2022 (P2-P2125) | With no box, there is nothing to check; needs a track, a map or a location prior |
| Digital Lp attacks on sign classifiers | Khan 2022 (P2-P2103), Yocam 2026 (P2-P2116), KEMLP (P2-P2101) | Not physical; useful only as a sanity baseline |
| Shadow and natural-light attacks (defined by LIT_A2 and LIT_A4 papers) | evaluated as targets in LAMDA 2026 (P2-P2115) | Colour and brightness cues shift; outline usually stays |
| Benign look-alikes | vandal stickers (Bayzidi, P2-P2124); 12 simulated conditions (CURE-TSD, P2-P2123) | Source of false alarms for any prior check |

## Solution map (defense and detection families)
| Family | Rows | Cue | Output |
|---|---|---|---|
| A. Structure-aware checks using sign priors | KEMLP (P2-P2101), Rangsikunpum (P2-P2109), ILP rules (P2-P2111), SAFER-Sign (P2-P2110), Khan OCR mapper (P2-P2103); survey category in Andleeb 2026 (P2-P2112) | Shape class, colour class, text or pictogram, logic rules or grammar | Corrected label (KEMLP, Rangsikunpum, Khan), rule decision (ILP), disagreement score with abstention (SAFER-Sign) |
| B. Prior injected at training time | LAMDA (P2-P2115) | VLM descriptions of shape, colour, border as text prototypes | Plain classifier, no run-time alarm |
| C. Redesign of the standard | Shua 2024 (P2-P2102) | Optimised pictograms and colours under constraints | More robust future signs |
| D. Location and multi-view priors | Etim 2024 (P2-P2106) historical street images; Timofte 2014 (P2-P2122) multi-view geometric consistency (recognition, not defense) | Same physical sign seen before or from other views | Majority vote; 3D hypothesis selection |
| E. Learned attack detectors beside an unchanged recogniser | Mumcu 2024 ViLAS (P2-P2108), PatchGuard-Freq 2026 (P2-P2113), detector head of Rangsikunpum (P2-P2109) | Label-text agreement; frequency spectrum; mid-layer features | Alarm score (AUC, false positives reported) |
| F. Restoration | Enan 2026 GAN (P2-P2107) | Generative reconstruction | Cleaned image |
| G. Robust training | BlurNet (P2-P2104), DOA (P2-P2105), IYOLO-TS (P2-P2114), Yocam (P2-P2116) | Training data and regularisers | More robust model |
| H. Physical measurement of standard sign properties (not defenses) | Maldonado-Bascon 2007 (P2-P2117), Siegmann 2008 (P2-P2118), Balali 2015 (P2-P2119) | Colour-to-shape tree; calibrated luminance and retroreflectivity | Sign class; retroreflectivity estimate |

## Closest prior work to the owner's design slides (ranked)
1. SAFER-Sign, Fayzullaev 2026 (P2-P2110, UNVERIFIED, abstract only). Uncomfortable finding first: it already scores disagreement among shape, colour and pictogram channels against a grammar of valid sign attribute tuples, with per-channel abstention and a reliability gate, and it treats attacks and benign degradation as one signature. This covers the core of slide 01 (class-specific structural disagreement plus abstain) on single crops. What the abstract does not show: viewpoint tracking over video, detector boxes, a training-free variant, matched false-alarm rates, latency. Full text must be read before slide 01 claims anything.
2. KEMLP (P2-P2101) and its lightweight hardware descendant Rangsikunpum 2026 (P2-P2109). Class-implies-shape logic with shape and content auxiliary models. They correct labels instead of raising a calibrated alarm; Rangsikunpum adds a learned attack detector and runs at over 9,000 fps on a low-cost FPGA (abstract), a hard latency baseline.
3. ILP stop-sign rules, Chaghazardi 2023 (P2-P2111, UNVERIFIED). OpenCV colour masks, polygon fit and OCR text turned into logic facts; fully explainable. Covers the explanation part of slide 01; limited to stop signs and text, no adaptive attack, no benign-video false-alarm rate.
4. ViLAS, Mumcu 2024 (P2-P2108). Same pipeline shape as all five slides (unchanged recogniser plus independent detector, AUC and latency reported); the cue is learned label-text agreement, not a physical prior.
5. Andleeb 2026 survey (P2-P2112). Names structure-aware reasoning over geometry, colour and semantics as a defense category, so the category itself is not new; novelty has to come from viewpoint conditioning, detector-level operation, calibrated abstention and matched false-alarm evaluation.
Slide 03: Tsuruoka 2024 (P2-P2120) defines the retroreflective night attack; no defense in this catalogue checks the night response of sheeting. A 2025 follow-up with defenses exists as an index record only (lead below) and must be checked first.

## Answers to the brief's three questions
1. Standardised and checkable from one camera (to our knowledge, from the records read):
   - Shape class per sign category: the octagon is reserved for STOP in the US MUTCD (FHWA 2009 section 2A.09 and Table 2A-4; 11th edition 2023 Chapter 2A guidance that exclusive shapes such as the STOP octagon should not be obscured). Under the 1968 Vienna Convention, danger warning signs are an equilateral triangle (white or yellow ground, red border) or a diamond (yellow ground, black rim), with black or dark blue symbols (UN Treaty Series text). Checkable from one camera as an outline class, with perspective tolerance (REAP fits ellipses or polygons to sign masks; Maldonado-Bascon treats an octagon as a circle at distance).
   - Colour class of ground, border and legend: fixed per category in both systems; daylight chromaticity boxes exist (EN 12899-1 classes CR1 and CR2; a US alternative colour method in 23 CFR 655 Subpart F). Only approximately checkable: white balance, exposure and illumination move colours (CURE-TSD: one detector lost all performance under decolorization; Maldonado-Bascon needed separate handling of white signs at night).
   - Border: red border for warning and prohibitory classes (Vienna text read for warning signs); white border on STOP (MUTCD wording seen only in a secondary handbook).
   - Retroreflectivity: minimum maintained levels per colour at a fixed measurement geometry (MUTCD 2023 table at 0.2 degree observation and -4.0 degree entrance angle, for example white on red signs W at least 35 and R at least 7 cd/lx/m2, official Chapter 2A text in a search excerpt). From one camera this is checkable only as a relative night-time response (legend versus background, change with distance and angle); absolute values need photometric calibration (P2-P2118, P2-P2119).
   - Size: minimum sizes exist (MUTCD and Vienna), but size is checkable only with a range estimate (tracking or ego-motion).
   - Not a standard but a physical fact used by several papers: a sign is a rigid planar object at a fixed position (perspective keypoints in REAP; multi-view consistency in Timofte; location prior in Etim).
2. Papers that use such priors: recognition: Maldonado-Bascon 2007, Timofte 2014, REAP 2023 (shape fit cross-checked with a classifier); defense: KEMLP 2021, Rangsikunpum 2026, Chaghazardi 2023, SAFER-Sign 2026, Khan 2022 (OCR content), LAMDA 2026 (training-time descriptions), Shua 2024 (redesign of the standard), Etim 2024 (location prior), Yocam 2026 (MUTCD retroreflectivity thresholds as labels).
3. Sign-specific defenses and how they were evaluated (abstract level):
| Defense | Task | Attacks | Data | Reported measures | False alarms | Latency |
|---|---|---|---|---|---|---|
| KEMLP (P2-P2101) | classification | physical, Lp, unforeseen, corruptions | road signs | robust accuracy | no | no |
| BlurNet (P2-P2104) | classification | RP2 stickers | LISA | attack success 90% to 20% (adaptive) | no | no |
| DOA (P2-P2105) | classification | rectangular occlusion | not named in abstract | robust accuracy | no | no |
| Khan hybrid (P2-P2103) | classification | FGSM, PGD, MIM, C&W | not named | accuracy | no | no |
| Etim (P2-P2106) | classification | one recent attack | Street View history | effectiveness | no | no |
| Shua (P2-P2102) | classification | patches | synthesised signs | robust accuracy, user study | no | no |
| Enan (P2-P2107) | classification | patches | sign classes | accuracy | no | relative only |
| Mumcu ViLAS (P2-P2108) | attack detection | four attacks | not named | AUC 0.94 | via AUC | 4.4 ms |
| Rangsikunpum (P2-P2109) | classification plus detector head | white-box stickers | LISA, GTSRB | accuracy | not in parts read | over 9,000 fps, 2.8 W |
| SAFER-Sign (P2-P2110) | classification with abstention | adaptive attacks and degradation | not in part read | not in part read | not in part read | not in part read |
| ILP rules (P2-P2111) | stop-sign recognition | RP2, AdvCam | Wikimedia images | accuracy 100% | no | no |
| PatchGuard-Freq (P2-P2113) | attack detection plus fine-tuning | patches, adaptive | stop sign, LISA, COCO | AUC 1.0, zero false positives | yes | not on embedded |
| IYOLO-TS (P2-P2114) | detection | patches | LISA, LISA-Mask | mAP | no | real time, no figure |
| LAMDA (P2-P2115) | classification | shadow, natural light, RP2 | GTSRB, LISA | robust accuracy | no | no added overhead |
Pattern: almost all evaluate cropped classification on GTSRB or LISA; two work on detectors; two report false positives; two report latency; adaptive attacks appear in BlurNet, PatchGuard-Freq and SAFER-Sign only.

## Standards and regulations (no DOI rows; notes table per the brief)
| Name | Issuing body | What it fixes (as read) | State |
|---|---|---|---|
| Manual on Uniform Traffic Control Devices, 2009 edition, Chapter 2A | US FHWA | Exclusive shapes (Table 2A-4, octagon for STOP); minimum maintained retroreflectivity keyed to ASTM D4956-04 sheeting types | Official FHWA page, search excerpt only |
| MUTCD 11th edition (2023), Chapter 2A | US FHWA | Exclusive shapes must not be obscured; agencies keep retroreflectivity at or above Table 2A-5 levels, measured at 0.2 degree observation and -4.0 degree entrance angle | Official FHWA PDF, search excerpt only |
| Convention on Road Signs and Signals, Vienna 1968, Annex 1 | United Nations (UNECE administers) | Danger warning sign models (triangle, diamond), ground, border and symbol colours; circular standing and parking signs | UNTS record in the ledger (several DOIs 10.18356/...); text read as a search excerpt of the UN Treaty Series; later amendments not checked |
| ASTM D4956 Standard Specification for Retroreflective Sheeting for Traffic Control | ASTM committee D04 | Sheeting types and performance (types I to III named in MUTCD 2009) | Crossref records for editions 01, 05, 11a, 17 in the ledger; content beyond the title UNVERIFIED |
| ASTM D8379 practice for nighttime retroreflective sheeting effectiveness (positive-contrast textual signs) | ASTM committee D04 | Night legibility evaluation of sheeting | Crossref record in the ledger; content UNVERIFIED |
| EN 12899-1 Fixed, vertical road traffic signs, Part 1 Fixed signs | CEN (BSI editions in Crossref) | Daylight chromaticity classes CR1 and CR2 and luminance factor; retroreflection classes RA1 and RA2 by observation and entrance angle | BSI records in the ledger; content seen only in a non-official copy in search results: UNVERIFIED, numbers deliberately not copied |
| 23 CFR 655 Subpart F, appendix (alternate method for colour of retroreflective sign materials) | US federal regulation | CIE 1931 colour boxes and daytime luminance factors | Seen on a secondary legal page; UNVERIFIED until read on the official eCFR |
| CIE 39.2 (surface colours for visual signalling) and CIE 54.2 (retroreflection measurement) | CIE | Colour limits and measurement method referenced by EN 12899-1 | Named inside EN 12899-1 text; UNVERIFIED |
| Czech national annex to EN 12899-1 | Czech road agency | Adds a microprismatic class RA3 | Official national page, search excerpt; UNVERIFIED |

## Gaps and what is left to test
1. To our knowledge no record read checks the detector's class against the standard outline and colours of a tracked sign across viewing angles, with an abstain state, on detector boxes, at matched false-alarm rates on benign video. SAFER-Sign (full text unread) may cover part of it on crops.
2. No defense found that tests whether a sign's night-time retroreflective response matches uniform standard sheeting; the retroreflective patch attack (P2-P2120) shows a strong angle dependence that such a check could exploit.
3. False alarms of prior checks on vandalised, faded or damaged signs are not reported by any row; Bayzidi (P2-P2124) suggests most random stickers do not flip classifiers, so an alarm on every sticker would be costly.
4. Hiding attacks remove the box; a prior check needs a track, a map or a location prior (Etim, P2-P2106) to notice a missing sign.
5. Colour priors fail under exposure and colour shifts (P2-P2123, P2-P2117); colour checks need a reliability gate, which links to slide 04.
6. A class-to-standard table (GTSRB, LISA and MTSD classes to shape, ground, border and legend colours) is needed by any of these checks and was not found as a published resource (REAP groups signs by shape and size; Bayzidi uses five classes in three shapes).

## Datasets, benchmarks and code seen
- GTSRB: Stallkamp 2012, 10.1016/j.neunet.2012.02.016 (ledger FOUND; not catalogued here). GTSDB: Houben 2013, 10.1109/ijcnn.2013.6706807 (ledger FOUND). LISA: introduced with the Mogelmose 2012 survey, 10.1109/tits.2012.2209421 (ledger FOUND; the dataset link not checked).
- BelgiumTS: P2-P2122, public according to the paper; official page not opened.
- CURE-TSD-Real: P2-P2123, https://github.com/olivesgatech/CURE-TSD (licence not checked). VIP Cup 2017 summary: Temel 2018, 10.1109/msp.2017.2783449 (ledger FOUND).
- REAP: P2-P2121, https://github.com/wagner-group/reap-benchmark; built on Mapillary Vistas and MTSD (licences to be recorded before any download).
- LISA-Mask (P2-P2114) and the MAD benchmark (Peng 2025 RPF-MAD, 10.3390/electronics14102044, ledger FOUND): availability unknown.
- Code: ILP rules https://github.com/Chaghazardi/Traffic-Sign-Detection-using-ILP (P2-P2111); LAMDA https://github.com/pedram-mohajer/LAMDA (P2-P2115). No code location seen for KEMLP, SAFER-Sign, Rangsikunpum or PatchGuard-Freq.

## Problem cards
### Card X12-1: The predicted class contradicts the sign standard, but nobody checks it along the track
- Problem: a patched sign can be labelled as a class whose standard outline and colours do not match the observed sign, yet structure-aware defenses found so far judge single crops, not tracked detector boxes across viewing angles.
- Contribution to test: a training-free lookup from detector class to standard shape and colour classes, compared with the tracked ROI's fitted outline and dominant colours over several frames, with a viewpoint-dependent tolerance and an abstain state when the outline is unreliable. Prior work already covers the single-crop version (SAFER-Sign, KEMLP, Rangsikunpum, ILP rules); the test is whether tracking and viewpoint conditioning add recall at a fixed false-alarm rate.
- Open-source starting point: frozen sign detector (licence to check), OpenCV contour, ellipse and polygon fitting as in REAP and the ILP code, a class-to-standard table built from MUTCD Table 2A-4 and Vienna Annex 1 categories.
- Data and laptop fit: REAP renderings (Mapillary licence question), GTSDB, LISA clips, CURE-TSD benign conditions; OpenCV features on CPU, detector on the 6 GB laptop GPU; record each licence before download.
- Experiment workflow: (1) build the class-to-standard table for the chosen label set; (2) run the frozen detector and a tracker on clean, benign-degraded and attacked clips; (3) compute a per-frame outline and colour residual against the table with viewpoint tolerance and accumulate it along the track; (4) compare with detector-only, a spectral check in the style of PatchGuard-Freq, and a single-frame version of the same residual.
- Success measure: attack recall at a matched false-alarm rate per hour of benign driving; count of abstentions; p95 ms per frame.
- Sources: P2-P2110, P2-P2101, P2-P2109, P2-P2111, P2-P2117, P2-P2121, P2-P2124.

### Card X12-2: Retroreflective patches appear only under the victim's headlights
- Problem: the retroreflective patch attack turns the standard sheeting into an attack surface that is nearly invisible by day; no defense in this catalogue checks whether the night response of a sign matches uniform sheeting.
- Contribution to test: whether the local night-time luminance of a tracked sign, as distance and angle change under the vehicle's own headlights, departs from the smooth profile expected for uniform sheeting; flag localized excess return, abstain when exposure saturates. The 2025 follow-up with defenses (lead, unconfirmed) may already cover this and must be read first; the topic overlaps LIT_A3.
- Open-source starting point: OpenCV luminance statistics on tracked ROIs; camera response ideas from Siegmann 2008 and Balali 2015; frozen detector.
- Data and laptop fit: no public dataset of such patches found; needs controlled night recordings of a sign with retroreflective tape (owner decision: physical experiment and safety) or a rendering based on the paper's setup; CURE-TSD darkening and exposure as benign negatives; CPU only.
- Experiment workflow: (1) record or render night approach sequences of clean and patched signs at several angles; (2) extract per-region luminance profiles against distance and angle; (3) fit the clean-sheeting profile on held-out clean sequences; (4) score residuals and compare with brightness-only and texture-only checks.
- Success measure: recall at a fixed false-alarm rate on night clips with benign glare and wet roads; p95 latency.
- Sources: P2-P2120, P2-P2118, P2-P2119, P2-P2116, P2-P2123.

### Card X12-3: Benign damage and stickers versus attacks, the false-alarm side of sign priors
- Problem: outline and colour checks also fire on faded, vandalised, damaged or partly occluded signs, while most random stickers do not change classifier output (P2-P2124), so an alarm on every anomaly would add false alarms without matching real risk.
- Contribution to test: measure how often prior-check residuals fire on benign degradations versus attacks that cover class-critical features, and test a residual weighted by the features that separate the predicted class from its neighbours (for example the digit of a speed limit). SAFER-Sign treats attacks and degradation as one signature; this card tests whether separating them lowers false alarms.
- Open-source starting point: the features of card X12-1; CURE-TSD conditions; sticker placement ideas from Bayzidi 2022.
- Data and laptop fit: CURE-TSD, GTSRB, LISA (licences to record); CPU features.
- Experiment workflow: (1) build a benign set (CURE-TSD levels, natural sticker images if a licensed source exists) and an attack set (RP2-style and critical-feature placements); (2) compute residuals; (3) add class-critical weighting; (4) report false alarms per hour and recall at matched operating points.
- Success measure: false alarms per hour at matched attack recall, by condition type.
- Sources: P2-P2124, P2-P2123, P2-P2110, P2-P2117.

## Leads not confirmed (what was tried)
- arXiv ids from memory of the first run, batch closed by HTTP 429 before any record: 2503.12567 (a third-party page names it for the Enan GAN defense), 1712.09327, 1712.02463, 1707.03501, 1710.03337, 2308.11894, 2201.06192 (titles not confirmed). 1908.11262 and 2212.05680 were seen on arXiv pages in search results and are attached to P2-P2123 and P2-P2121; 1902.06857 (CURE-TSD reliability assessment) seen in a search result only.
- AR-GAN defense for sign classification: Crossref title search in the first run returned no match.
- Loy 2004, fast shape-based road sign detection, 10.1109/iros.2004.1389331: Crossref record has no year, so a row would fail the year check; not catalogued.
- Pavlitska 2023 survey of attacks on TSR, arXiv 2307.08278: seen in search results; arXiv closed. Its discussion says defenses for TSR received much less attention than attacks.
- SoutheastCon 2025 survey of TSR threats and defenses, 10.1109/southeastcon56624.2025.10971663: first author not seen.
- Sarwatt 2025, benchmark of recovery methods for adversarial traffic signs (IET Intelligent Transport Systems, 10.1049/itr2.70115): abstract seen; Crossref closed.
- Sensors 2026, sequence-preserving dual field-of-view defense for sign and light recognition, 10.3390/s26051737: first author not seen.
- Gao 2025, N-version voting for TSR, arXiv 2507.06907; VISAT benchmark with colour and shape attributes, arXiv 2510.26833; NeuroShield neuro-symbolic shape and colour rules, arXiv 2601.13162: seen in search results; arXiv closed; authors partly unseen.
- Neural-symbolic follow-up of the ILP work (2024) and a 2026 Surrey thesis, 10.15126/thesis.902331: search results only.
- Retroreflective patch follow-up on commercial vehicles with defenses (2025): index record only.
- NDSS 2025 paper on physical attacks against commercial TSR (spatial memorization): open PDF excerpt seen, authors not seen; likely LIT_X9 scope.
- Coordinator leads checked: the Andleeb survey is confirmed (P2-P2112); LAMDA is catalogued as UNVERIFIED (P2-P2115). Its claim of structure-aware defenses is confirmed at abstract level; the defenses it reviews were not read.

## Ledger-confirmed records not catalogued (row cap of 25, or abstract not read)
- F1 classical colour and shape pipelines: de la Escalera 1997 (10.1109/41.649946), Barnes 2008 radial symmetry (10.1109/tits.2008.922935), Bahlmann 2005 colour, shape and motion (10.1109/ivs.2005.1505111), Gao 2006 (10.1016/j.jvcir.2005.10.003), Gomez-Moreno 2010 segmentation evaluation (10.1109/tits.2010.2054084), Greenhalgh 2012 (10.1109/tits.2012.2208909), Fleyeh 2006 shadow and highlight invariant colour segmentation (10.1109/iccis.2006.252225, relevant to slide 02), Escalera 2010 (10.1007/s00138-008-0145-z), Fleyeh 2008 (10.1109/ivs.2008.4621172), Lee 2014 image-based retroreflectivity (10.12652/ksce.2014.34.1.0185).
- Retroreflectivity management: Khalilikhah 2015 (10.1016/j.measurement.2015.07.049), Ai 2016 mobile LiDAR (10.1016/j.trc.2015.12.002), Saleh 2024 lifespan models (10.1016/j.ijtst.2024.02.008), Asamoah 2025 joint detection and retroreflectivity estimation, SSRN (10.2139/ssrn.5127319), Carlson 2012 NCHRP synthesis (10.17226/14663), Bischoff 2002 report (10.5703/1288284313313).
- F2: Woitschek 2021 feasibility study (10.1109/iv48863.2021.9575935), Apostolidis 2023 (10.1007/978-3-031-44127-1_13), Babic 2021 market-ready TSR field test (10.3390/en14123697), Wali 2019 and Liu 2019 reviews (10.3390/s19092093, 10.1109/access.2019.2924947), Wang 2023 system-level effect (10.1109/iccv51070.2023.00407, LIT_X9 scope), Khalilikhah 2017 vandalism prediction (10.3846/16484142.2016.1252946), Ersu 2024 sign damage detection (10.1109/icarcv63323.2024.10821546), Lengyel 2021 sticker collection (10.1515/auto-2020-0115), Suo 2026 nighttime attack, SSRN (10.2139/ssrn.6173277).
- F3: Peng 2025 RPF-MAD (10.3390/electronics14102044; Crossref abstract read: meta-adversarial pre-training and fine-tuning; reported gains of 1.53% standard and 2.64% robust accuracy), Kavi Rohith 2026 dual-stage patch mitigation (10.1109/nelex69209.2026.11590354, metadata only), Fawakherji 2026 domain transfer (10.1109/southeastcon63549.2026.11476037, metadata only), Patil 2026 FALCONS, SSRN (10.2139/ssrn.6000017, metadata only), Lin 2025 simulated attacks with a YOLO defense (10.3390/engproc2025092015), Yang 2020 (arXiv 2003.00120) and CARE 2022 (arXiv 2209.05055) logic-reasoning certified robustness (arXiv records FOUND in the first run; content not re-read).

## Exclusions
- Network traffic classifier defense supplement (Crossref component record): network traffic, not road signs.
- Graffiti copyright law (SSRN) and sign-vandalism advertising (1996 book chapter): not computer vision.
- Acoustic detection of occluded vehicles: not camera based.
- Generic deep-learning TSR papers without a robustness or prior angle (several 2017 to 2026 records from the discovery searches): no link to attack detection.
- Weather-robust TSR classifiers (several 2024 to 2026 records): benign robustness, left to the lighting and weather tasks; not read.
- Aerial patch review, embodied-agent patch purification, traffic-light camouflage poster: outside the sign scope of this task.
- GhostStripe rolling-shutter stripes on signs and its defense: in scope for slide 04 and left to LIT_A4.
