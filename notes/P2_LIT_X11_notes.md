# P2_LIT_X11 notes - phantom and fabricated-object attacks, and methods that reject them

Status: written by the LIT_X11 worker agent. NOT AUDITED. Nothing here is a result of ours; cards state hypotheses.
Catalog rows: work/LIT_X11/rows.jsonl, paper_id P2-P2001 to P2-P2025 (25 rows; states computed by scripts/rows_check.py: VERIFIED 16, ARXIV_API_VERIFIED 9, MISMATCH 0). The id P2-P2026 was used for a short time for a concept paper that was then moved to section 9 (outside the subject); that id is not reused.
Read depth: 21 rows at abstract level, 4 rows metadata-only (P2-P2003, P2-P2008, P2-P2012, P2-P2017). No full text was read. Row P2-P2001 rests on a one-sentence record abstract.
Rows of other tasks are cited by their paper_id and task label; their content was read from the staging files of those tasks and is unaudited model output.

## 0. Limits of this run (read before using anything below)

1. websearch: 6 calls, 0 results each (the tool answered that it found no results; logs of other tasks name a used-up search quota). No search-engine discovery took place.
2. arXiv API: 3 id-lookup calls and 1 keyword search succeeded; the next call printed a shared STOP_HOST and the host was not called again. arXiv-only candidates found after that point could not be confirmed.
3. Discovery therefore came from (a) leads recalled from memory and then confirmed in an arXiv or Crossref record, (b) Crossref keyword searches, which are noisy (8 topical searches contributed no row: they gave the DOI of 1 row already found, P2-P2024, 1 concept paper used as a pointer in section 1.3, and a few title-level pointers), (c) one arXiv keyword search (1 row, P2-P2015). Work from 2024 to 2026 is under-sampled. A fresh search pass is needed before any claim about what does not exist.
3a. Crossref: the last call of the run printed a shared STOP_HOST and the host was not called again. All 25 rows had been checked before that point; one more question 3 search (false activation rates of emergency braking in field data) did not run.
4. Statements marked "from memory, UNVERIFIED" were not read in any record during this run.
5. Numbers in this file are copied from the record named next to them. Where a record is an arXiv preprint of a published paper, the published text may differ.

## 1. Answers to the three questions of the brief

### 1.1 Which attacks create objects, and by which medium

| Medium | What is created | Rows | Evidence read |
|---|---|---|---|
| Projected light or screen (projector, drone-carried projector, digital billboard) | Depthless road signs, persons, lanes shown for a short time | P2-P402 (LIT_A4), P2-P2002; projector-made phantom floods P2-P525 (LIT_A5) | P2-P2002 abstract: a Mobileye unit read a drone-projected sign as real; no rates |
| Light aimed into the lens or stereo pair | Fake obstacle depth; flare ghosts; infrared-made objects | P2-P2010; P2-P409 and P2-P431 (LIT_A4); P2-P311 (LIT_A3) | P2-P2010 abstract: fake depth up to 15 m at night and up to 8 m in daytime; a drone was stopped |
| Print: poster, sticker, advertisement, logo, lenticular print | A detector box or a sign class where no such object exists | P2-P2004, P2-P2005, P2-P2006, P2-P2007, P2-P2003, P2-P2013, P2-P2017; P2-P102 (LIT_A1) and P2-P524 (LIT_A5) | P2-P2004 arXiv abstract: appearing attack, success up to 92.4% over 1 m to 25 m and -60 to 60 degrees. P2-P2006 abstract: above 95% in physical and virtual tests. P2-P2003 and P2-P2017: title only |
| Sound injected into the camera | Distortion that makes detectors create, hide or alter objects; a printed patch that acts only while the distortion is present | P2-P2008, P2-P2009 | P2-P2009 abstract names hiding, creating and altering attacks on YOLO V3, YOLO V5 and Faster R-CNN; no rates. P2-P2008: title only |
| Image-space perturbation (digital stand-ins, no physical carrier) | Fabricated boxes, single or in floods | P2-P2011, P2-P2013 (also shown with printed posters), P2-P2014, P2-P2015, P2-P2016 | P2-P2013 arXiv abstract: false positive rate 99.9%, mean average precision 0 |
| Camera-only 3D detection space | Objects in bird-eye-view 3D detection | P2-P2012 | Title only; medium unknown |
| Real but harmless objects (not fabricated) | Needless stops through over-cautious planning | P2-P2023 | Abstract: 9 planning vulnerabilities found in 3 planning implementations |
| LiDAR spoofing (outside the camera scope, analogue only) | Forged cars and other ghost objects in point clouds | attacks named in P2-P2020 and P2-P2021 | Abstracts only |

Reading: creation attacks are not one family. Print carriers leave no light signature. Projected and lens-directed light leave a light signature and no carrier geometry. Sound and triggered patches leave a frame-distortion signature. Floods leave an output-statistics signature. One cue cannot cover all four.

### 1.2 Which plausibility checks reject fabricated objects, and what they cost

| Check | Cue | Sensor | Effect stated in the record read | Cost stated in the record read | Row |
|---|---|---|---|---|---|
| Per-object committee of four small CNNs for light, context, surface and depth (description taken from row P2-P402 of LIT_A4) | Appearance of the detected crop and its surroundings | Camera | See row P2-P402 of LIT_A4 (not re-read here). P2-P2001 abstract: one sentence, no numbers | Not read | P2-P402 (LIT_A4), P2-P2001 |
| Edge consistency between image, predicted depth and predicted segmentation | Structure agreement across tasks | Camera | Up to 100% of perturbed images detected at an assumed 5% false positive rate, depending on strength (abstract) | Needs a multi-task network with depth and segmentation outputs; run time not in the abstract | P2-P2018 |
| Context consistency (one auto-encoder per class) | Does the object fit its scene | Camera | ROC-AUC over 0.95 in most cases on PASCAL VOC and MS COCO (abstract) | One auto-encoder per class; run time not in the abstract | P2-P2019 |
| Context consistency by a language model | Object co-occurrence | Camera | See P2-P126 (LIT_A1) | Not read | P2-P126 (LIT_A1) |
| Ghost overlap plus spatiotemporal consistency | Flare ghost position against detected object, over time | Camera | See P2-P431 (LIT_A4) | Not read | P2-P431 (LIT_A4) |
| Class against motion consistency | Track kinematics | Camera | See P2-P510 (LIT_A5) | Needs several frames (statement in that row) | P2-P510 (LIT_A5) |
| 3D shadow invariant | A real object must cast a LiDAR shadow | LiDAR | More than 94% accuracy on anomalous shadows, KITTI (arXiv abstract) | 0.003 s to 0.021 s per object on commodity hardware (arXiv abstract) | P2-P2020 |
| Local objectness with a depth and point-density relation | Part-level realness, distance-dependent prior | LiDAR | At least 70% of forged cars eliminated in most cases, against under 30% for the best earlier defence (abstract) | Lower loss of car AP and precision than earlier defences; no number in the abstract | P2-P2021 |
| Occlusion patterns as invariant physical features (CARLO) | Free space behind and in front of an object | LiDAR | Mean attack success rate reduced to 5.5%; a learned variant to around 2.3% (abstract of arXiv 2006.16974; in the ledger, not catalogued) | Not in the abstract | none |
| Bounded admission (cap on detections passed to the tracker) | Output count | Camera | Largely restores end-to-end latency under a detection flood (abstract) | A non-trivial loss of admitted clean detections; no number in the part read | P2-P2015 |
| Formal sanity rules over detector output streams | Spatial and temporal logic formulas | Any | Sanity checks without ground truth in some cases; no detection numbers (abstract) | A fragment is monitorable offline in polynomial time; online cost not in the abstract | P2-P2022 |
| Scene-perspective prior (box size and position against camera geometry) | Geometry | Camera | From memory, UNVERIFIED (Hoiem 2008, DOI 10.1007/s11263-008-0137-5, record in the ledger, no abstract) | Not read | none |

Reading on cost: among the records read, one check states a time per object (P2-P2020) and one states what it loses in true detections (P2-P2015, without a number). The camera-only checks state accuracy-type figures and no time, memory or false alarms per hour. The operating points differ (5% per-image false positive rate, ROC-AUC, accuracy, share of forged objects removed), so the published figures cannot be compared with each other. A 5% per-image false positive rate is unlikely to fit a per-hour false-alarm budget of the kind used on the deck (our judgement); no record read converts its figure to false alarms per hour.

Checks can be attacked. Depth: P2-P2010 makes a stereo camera report an obstacle that is not there, so depth cannot be treated as an attack-free referee. Context: row P2-P516 of LIT_A5 reports attacks built to pass context checks. Shadow invariant: P2-P2020 tests an invalidation attack against itself and reports robustness. Edge consistency: P2-P2018 builds a multi-task attack against its own scheme (outcome not in the part of the abstract read beyond the headline figure).

### 1.3 How false braking risk is measured, if at all

Finding: in the records read, no paper reports a false-braking rate (needless brake events per hour or per kilometre) for a camera-based creation attack or for a detector of such attacks. To our knowledge, within the limits of section 0, that measure is open. NEEDS_VERIFY against full texts, in the first place P2-P402 (LIT_A4), P2-P2001 and P2-P2021.

What is measured instead:
1. Detector-level success of the attack: success rate (P2-P2004, P2-P2006), false positive rate and mean average precision (P2-P2013), counts per detector (P2-P2016).
2. Reactions of a real system, as demonstrations: a driver-assistance unit accepting a projected sign (P2-P2002); a drone brought to a sudden stop (P2-P2010); field tests on production systems (row P2-P402 of LIT_A4, not re-read here).
3. Closed-loop simulation for LiDAR appearing attacks and their defence on Baidu Apollo (P2-P2021; outcome figures not in the abstract).
4. System-level templates for other attack goals: traffic-rule violation rate for sign evasion (P2-P2024: prior attacks reach no system-level effect; a system-driven design raises the violation rate by around 70%); vehicle crash rate for latency attacks (arXiv 2312.09520 abstract, in the ledger, not catalogued: around 95% on average against around 30% for earlier attacks; see also P2-P525 of LIT_A5); planning invariants as oracles for needless stops caused by harmless objects (P2-P2023); driving-safety metrics that are decoupled from detection precision (P2-P2025; the metric list is not in the abstract).
5. One out-of-scope record (arXiv 2507.09095, network timing attack on sensor fusion, in the ledger, not catalogued) names phantom braking and collisions as impacts seen in end-to-end simulation.
6. Vehicle-testing side, title-level pointers only, content not read: "Test and evaluation research on false reaction scenarios of automatic emergency braking system" (Liu, 2026, DOI 10.1109/iseae69422.2026.11544251) and the standard "Automatic Emergency Braking (AEB) System Performance Testing" (SAE J3087, DOI 10.4271/j3087_202504). Both are Crossref records in the ledger.
7. The phenomenon itself is framed, not measured, in a human-factors concept paper (Hegna Berge, 2024, DOI 10.54941/ahfe1005212, Crossref abstract read, in the ledger, not catalogued): phantom braking is described as sudden and unexpected deceleration and read through signal detection theory, with accident avoidance favoured at the price of possible rear-end accidents. The paper has one simulator participant and reports no braking rate.
8. A monitor judged on an emergency-braking case study exists for another problem (out-of-distribution inputs, not fabricated objects): the abstract of DOI 10.1049/cps2.12034 (Cai, 2022, in the ledger, not catalogued, family of LIT_X6) reports a small detection delay, a very small number of false alarms and an execution time comparable to the monitored component, in simulation. Its measures (detection delay, number of false alarms, execution time) are the nearest published pattern to what a phantom-object check would have to report.

Consequence for Paper 2: contribution 7 of the owner list names false alarms and controlled attack scenarios. A false-braking proxy with a frozen trigger rule (card 3) would be a measured quantity that the records read do not report.

## 2. Problem map (attack families and the papers that define them)

| Family | Defining records | Notes |
|---|---|---|
| A. Split-second phantoms by projection or screen | P2-P402 (LIT_A4), P2-P2002; flood variant P2-P525 (LIT_A5) | Depthless object, short exposure; light medium |
| B. Printed appearing or creating attacks on detectors | P2-P2004, P2-P2005, P2-P2012 (title only), P2-P102 (LIT_A1), P2-P524 (LIT_A5); data P2-P2017 (title only) | Designed to stay detected from far to near (P2-P2004); per-frame persistence is not given in the abstract |
| C. Non-sign carriers read as signs | P2-P2006, P2-P2007, P2-P2003 (title only) | Advertisements, logos, arbitrary images, lenticular prints; classifier-level in the abstracts read |
| D. Creation through the camera channel, no scene object | Sound: P2-P2008 (title only), P2-P2009. Light into the lens: P2-P2010, P2-P409 and P2-P431 (LIT_A4). Infrared: P2-P311 (LIT_A3) | Footprint is a frame distortion, a flare or a spectral response |
| E. Fabrication at scale | P2-P2013, P2-P2014, P2-P2015, P2-P2016; effect taxonomy P2-P2011 | Targets non-maximum suppression, the tracker and the latency budget |
| F. Consequence layer | P2-P2023, P2-P2024, P2-P2025; pointer DOI 10.54941/ahfe1005212 | Needless stops, system-level effects, driving-safety metrics, the phantom-braking concept |

## 3. Solution map (defense and detection families)

| Family | Records | Covers | Open point |
|---|---|---|---|
| S1. Learned per-object realness committee | P2-P402 (LIT_A4), P2-P2001 | Projected phantoms (per the LIT_A4 row) | Print carriers, night, cost, abstain state: not read |
| S2. Cross-task consistency residual | P2-P2018 | Image-level digital perturbations at a fixed false positive rate | Physical fabricated objects; per-object decision |
| S3. Context consistency | P2-P2019, P2-P126 (LIT_A1) | Objects out of place in general scenes | Driving scenes; adaptive attacks (P2-P516 of LIT_A5) |
| S4. Temporal and motion consistency | P2-P510 and P2-P513 (LIT_A5), P2-P431 (LIT_A4) | Misclassified or ghost objects over frames | Persistent printed phantoms that move consistently with the scene |
| S5. Physical invariants in 3D sensing | P2-P2020, P2-P2021, CARLO (ledger only) | LiDAR ghost and appearing attacks | Camera analogue untested |
| S6. Output-rate limiting | P2-P2015 | Detection floods | Price in lost true detections; crowded benign scenes |
| S7. Formal sanity rules | P2-P2022; pointers DOI 10.1007/978-3-030-03769-7_23 and DOI 10.1007/978-3-030-88494-9_18 | Explainable rule violations on output streams | Offline in the abstract read; no attack evaluation read |
| S8. Scene-perspective prior | Hoiem 2008 (ledger only, UNVERIFIED content) | Implausible size or position | Never read as an attack defence here |
| S9. Sensor and system-level measures | Named in the abstract of P2-P2009; mitigation part of P2-P2010 cut off | Not read | Not read |

## 4. Closest prior work to the owner's design slides (ranked, fabricated-object angle)

1. The phantom countermeasure by Nassi and co-authors: P2-P402 (LIT_A4) and P2-P2001. Reason: same pipeline shape as all five slides (frozen detector, independent cues per detected object, decision), camera-only, aimed at fake objects, with a light cue (slide 04), a context cue and a depth cue (cue list per the LIT_A4 row; P2-P2001 itself was read only as a one-sentence abstract). This is the strongest threat to any novelty claim about telling real from fake objects with cheap camera cues. Differences that remain to be shown, not assumed: an abstain state, an explanation output beyond per-expert scores, print carriers, night data, matched false-alarm points, cost. Both rows need a full-text read.
2. P2-P2018 (edge consistency across image, depth and segmentation at a fixed 5% false positive rate). Reason: the consistency residual between independent cues with a fixed operating point is already published, for digital perturbations. The owner design differs by using physical cues and per-object decisions; that difference must carry the claim.
3. P2-P431 (LIT_A4): ghost-object overlap plus spatiotemporal consistency for flare ghosts. Reason: a fabricated-object test that is geometric and temporal, close to slides 04 and 05.
4. P2-P510 (LIT_A5): class against motion consistency. Reason: a physical-plausibility test per track with an operating point. It targets misclassification; its behaviour on created objects was not read.
5. P2-P2019 and P2-P126 (LIT_A1): context consistency. Reason: the "does this object belong here" test for a fabricated sign or obstacle; known to be evadable (P2-P516 of LIT_A5).
6. P2-P2022: spatio-temporal perception logic. Reason: an existing explainable format for plausibility rules, which overlaps with contribution 6 of the owner list (explain which inconsistency caused the flag).
7. P2-P2015: bounded admission. Reason: a lightweight rule against fabricated detections with its price stated; relevant to contribution 5 (lightweight) and to latency claims.
8. P2-P2020 and P2-P2021: LiDAR analogues. Reason: P2-P2020 uses a shadow as a physical invariant for ghost objects, the idea of slide 02 in another sensor; P2-P2021 scores a per-object filter by forged objects removed and by precision lost.

Uncomfortable points, stated first for the coordinator:
- A camera-only, lightweight, multi-cue check for fake objects with light, context, surface and depth cues was published in 2020 (per the LIT_A4 row). A 2023 journal article by the same first author on separating real from fake objects (P2-P2001) is probably the same line of work (not read beyond one sentence). The red-marked cue list of Paper 2 overlaps with it.
- A depth cue is itself attackable (P2-P2010).
- Print-medium creation attacks (P2-P2004, P2-P2006) put a physical carrier in the scene that moves consistently with it, and P2-P2004 is designed to stay detected from far to near, so temporal inconsistency (slide 05) may not fire on them (hypothesis; per-frame persistence was not read).

## 5. Gaps and what is left to test

G1. False-braking rate: not reported for camera-based creation attacks or their detectors in the records read (section 1.3).
G2. Print carriers against the learned committee: no record read says whether the committee of P2-P402 and P2-P2001 was tested on printed advertisements or posters (P2-P2003 is by the same first author; title only). NEEDS_VERIFY.
G3. A physics-only, training-light baseline for phantom rejection (planarity or parallax, size against ground position, shadow or contact cue) was not found for cameras in this run. To our knowledge, within the limits of section 0.
G4. Benign look-alikes of fabricated objects (people on billboards and bus advertisements, signs printed on trucks, reflections in shop windows, statues) are not named as a hard-negative set in any record read. The benign-or-abstain branch of the slides needs such a set.
G5. Matched operating points: the published figures use different measures (section 1.2). A comparison at one false-alarm rate per hour is missing.
G6. Depth as a referee: P2-P2010 shows a depth cue can be fed a fake obstacle; a check that relies on depth needs its own plausibility gate.
G7. Triggered and camera-channel creation (P2-P2008, P2-P2009): no detection result was read. The frame-distortion footprint is a candidate cue (card 4).
G8. Floods: an admission cap loses true detections (P2-P2015). An explainable flood alarm tested on crowded benign scenes was not found.
G9. Illumination split: P2-P2010 reports a longer fake-depth range at night (15 m against 8 m); P2-P2005 includes night tests. Attack strength depends on ambient light, so results must be reported by illumination.
G10. Adaptive attacks against a multi-cue check: P2-P2018 and P2-P2020 test attacks against their own defence; the context family has a published evasion (P2-P516 of LIT_A5). Any new check needs the same test.

## 6. Datasets, benchmarks and code seen

| Item | Where seen | Possible use | Licence or fit note |
|---|---|---|---|
| APRICOT | P2-P2017 (title only); APRICOT-Mask per P2-P110 (LIT_A1) | Candidate real-photo set of printed patches | Not checked; record before download |
| KITTI | P2-P2018, P2-P2020 abstracts | Depth and 3D data for consistency checks | Not checked |
| Cityscapes | P2-P2018 abstract | Segmentation and depth consistency | Not checked |
| PASCAL VOC, MS COCO | P2-P2011, P2-P2016, P2-P2019 abstracts | General-scene detection and context | Not checked |
| BDD100K | Deck (state/DECK_DIGEST.md); P2-P420 (LIT_A4) | Benign driving video for hard negatives | Not checked; record before download |
| Code of P2-P2018 | Repository named in the abstract, not opened | Reference implementation of an edge-consistency detector | Not checked |
| Code of the phantom countermeasure | Named in row P2-P402 of LIT_A4 as UNVERIFIED | Baseline committee | Not checked |
| Baidu Apollo, LGSVL | Abstracts of P2-P2021 and arXiv 2312.09520 | Closed-loop simulation | Too heavy for the laptop without a fit test (assumption; not measured) |
| NVIDIA Jetson AGX Orin, Nvidia NX | Abstracts of P2-P2015 and arXiv 2304.05370 | Embedded timing reference points | Hardware, not data |

No dataset of benign look-alikes of fabricated objects and no dataset of recorded phantom or print-creation attack video was found in this run.

## 7. Problem cards

Hardware assumed (coordinator update 1): 10-core CPU, 32 GB RAM, one laptop GPU with 6 GB of memory. Deck rules carried over: CPU baselines and frozen features before anything else; split by recording; licence recorded before download.

### Card 1. A flat phantom passes as a real object
Problem: a detector reports a sign, person or vehicle that is only a projection or a print, and nothing in a single box says that the object has no body.
CONTRIBUTION TO TEST: a per-object physicality score from three cheap camera cues with an abstain state: (a) planarity, the residual of the object motion against the motion of the surface that carries it over a short window; (b) size against ground position under camera geometry; (c) contact or shadow evidence at the base of the object. Compare it with a small crop classifier and, if its code can be run, with the published committee, at matched false-alarm points. Prior work already covers the general idea of a camera-only real-versus-fake check (P2-P402 of LIT_A4, P2-P2001) and of a cross-cue consistency residual (P2-P2018). What is left is whether geometry-only cues with no learned appearance model add signal on print carriers and at night, and whether an abstain state lowers false alarms.
OPEN-SOURCE STARTING POINT: tools named on the deck (YOLOX-Nano, OpenCV optical flow and homography, scikit-learn, frozen Depth Anything V2 Small); the repository named in the abstract of P2-P2018 (not opened).
DATA AND LAPTOP FIT: positives made by inserting flat pictures of signs and persons onto planar surfaces of benign driving clips with a frame-consistent homography (a stand-in, not a recorded attack), plus APRICOT photographs if the licence allows; negatives from benign driving video with hand-picked look-alikes (advertisements with people, signs on trucks). CPU-only cue extraction; the frozen depth model must pass a fit test on the 6 GB GPU first. Licence questions: BDD100K, APRICOT, KITTI.
EXPERIMENT WORKFLOW: (1) freeze the detector, the cue definitions and the split by recording; (2) build the inserted-phantom clips and the look-alike negative list; (3) compute the three cues per track and fit a calibrated logistic model with an abstain band on the calibration recordings; (4) compare with detector-only, crop classifier and single-cue variants on held-out recordings.
SUCCESS MEASURE: true positive rate at a fixed false-alarm rate, false alarms per hour on long benign clips, share of abstentions, ms per frame on the CPU, results split by day and night.
SOURCES: P2-P2001, P2-P2004, P2-P2005, P2-P2006, P2-P2018, P2-P2010, P2-P2020.

### Card 2. A box flood eats the latency budget
Problem: an attacker makes the detector emit a flood of false boxes, which slows suppression and tracking and breaks any ms-per-frame promise.
CONTRIBUTION TO TEST: a constant-time monitor on output statistics (box count, density, size distribution, births per frame) that raises an explainable flood alarm and bounds downstream work, compared with a plain admission cap. Prior work already covers the attack (P2-P2013, P2-P2014, P2-P2015, P2-P525 of LIT_A5) and a cap as defence with its price named (P2-P2015). What is left is separating a flood from a crowded benign scene and reporting the true detections lost.
OPEN-SOURCE STARTING POINT: YOLOX-Nano and ONNX Runtime (deck); a fabrication attack in the style of P2-P2011 re-implemented on the small detector (no official code location was seen in this run).
DATA AND LAPTOP FIT: benign clips with dense traffic and crowds as hard negatives; attacked frames produced digitally on the laptop GPU (small detector, 6 GB is expected to suffice; fit test first). Licence question: the driving video set used for the benign clips.
EXPERIMENT WORKFLOW: (1) reproduce one flood attack on the frozen small detector and log per-frame output statistics; (2) log the same statistics on crowded benign clips; (3) calibrate the alarm on calibration recordings at a fixed false-alarm rate per hour; (4) measure p95 latency and true detections lost with the monitor, with a plain cap and with neither.
SUCCESS MEASURE: flood recall at the fixed false-alarm rate, p95 end-to-end latency under attack, true detections lost against the plain cap.
SOURCES: P2-P2011, P2-P2013, P2-P2014, P2-P2015, P2-P2016.

### Card 3. Nobody reports the false brake
Problem: creation attacks and their detectors are scored per image or per frame, while the harm is a needless brake; the records read give no false-braking rate.
CONTRIBUTION TO TEST: an offline false-braking proxy with a rule frozen before any run: an object counts as a brake trigger when it stays inside the ego corridor below a time-to-collision threshold for a set number of frames. Report needless triggers per hour with and without the check, and missed triggers on real obstacles. Prior work already covers system-level measurement for sign evasion (P2-P2024), planning invariants for needless stops (P2-P2023), driving-safety metrics (P2-P2025) and closed-loop tests for LiDAR appearing attacks (P2-P2021). What is left, to our knowledge, is a rate for camera-based fabricated objects and for the false alarms of the check itself.
OPEN-SOURCE STARTING POINT: the timestamped replay harness of deck card 6; OpenCV Kalman filter for tracks; a constant-deceleration longitudinal model written in Python.
DATA AND LAPTOP FIT: benign driving video with ego speed if the set provides it (to be checked), with the inserted phantoms of card 1. No simulator is required for the proxy; a closed-loop simulator is outside the laptop limits until a fit test says otherwise. Licence question: the driving video set and its ego-motion data.
EXPERIMENT WORKFLOW: (1) write and freeze the trigger rule and its thresholds; (2) run detector, tracker and trigger rule on benign clips to get the baseline needless-trigger rate; (3) add inserted phantoms and count triggers with and without the plausibility check; (4) count missed triggers on real obstacles caused by the check and by its abstentions.
SUCCESS MEASURE: needless triggers per hour removed by the check at no increase in missed triggers on real obstacles, with the rule fixed in advance.
SOURCES: P2-P2021, P2-P2023, P2-P2024, P2-P2025, P2-P2010.

### Card 4. The attack is switched on for a few frames
Problem: a triggered patch or a camera-channel injection creates an object only while a distortion is present, so a scan of ordinary frames finds nothing.
CONTRIBUTION TO TEST: a birth-context gate: when a new object track is born, test whether the same frames carry a global blur or distortion event that the estimated camera motion does not explain. This rests on the abstract of P2-P2009 (the patch acts under an injected distortion) and on an unread paper (P2-P2008); the mechanism details are from memory and UNVERIFIED, so the card depends on a full-text read. No detection result for this attack family was read.
OPEN-SOURCE STARTING POINT: OpenCV sharpness measures (variance of Laplacian), optical flow magnitude, ECC alignment (deck card 12).
DATA AND LAPTOP FIT: benign clips with natural motion blur, potholes and vibration as hard negatives; distortion events synthesised by blur kernels on benign clips as a stand-in until recorded attack video exists. CPU only. Licence question: the driving video set.
EXPERIMENT WORKFLOW: (1) read P2-P2008 and P2-P2009 in full and fix the distortion model; (2) synthesise distortion bursts and inserted objects on benign clips; (3) compute blur-against-motion residuals at track births and calibrate with an abstain band; (4) test on held-out recordings with natural blur.
SUCCESS MEASURE: recall of distortion-coincident object births at a fixed false-alarm rate per hour, with natural-blur clips reported separately.
SOURCES: P2-P2008, P2-P2009.

## 8. Leads not confirmed

No record was read for the items below in this run; all are recalled from memory and UNVERIFIED.
1. An earlier report-style version of the phantom attack paper (cryptology preprint server, 2020): not searched; no DOI or arXiv id known.
2. A workshop paper on spoofing a Mobileye 630 camera with a projector (2021): not searched.
3. GlitchHiker, electromagnetic interference on the camera signal path: no DOI known; arXiv host stopped.
4. VOGUES, validation of an object class through its estimated components: no DOI known.
5. Model assertions for monitoring machine-learning models (flicker and multi-box assertions on video detections): no DOI known.
6. KEMLP, a knowledge-enhanced pipeline with sign shape and content rules: arXiv host stopped.
7. A defence that compares a sign with historical street-level imagery of the same place: arXiv host stopped.
8. Data fabrication attacks in collaborative vehicular perception and an occupancy-based countermeasure: arXiv host stopped; outside the camera-only scope.
9. The 2019 LiDAR spoofing paper with an emergency-brake case study in simulation: not looked up; outside the camera-only scope.
10. False-activation test scenarios in a national emergency-braking regulation: not a scholarly record; not looked up.
11. Follow-up papers that re-test or improve the phantom committee: 3 Crossref keyword searches and 1 arXiv keyword search found none; websearch was unavailable. Open.
Published venue recalled from memory and not confirmed by any record (10 items; a recalled name is written only where a row labels it UNVERIFIED): P2-P2009, P2-P2010 and P2-P2021 (security conferences), P2-P2006 (workshop), P2-P2016 (conference), P2-P2017, P2-P2019 and P2-P2020 (conference names of the three book chapters), arXiv 2304.05370 and arXiv 2312.09520.
One recalled DOI was wrong: 10.1145/3582570 resolves to an unrelated software-engineering paper; the correct DOI of P2-P2001 came from a Crossref title search.

## 9. Exclusions

Read in a record and not catalogued, with the reason:
- arXiv 1906.11897 (patch that suppresses all detections) and arXiv 1910.00068 (context patches that blind a detector to a class): hiding attacks, family of LIT_A1.
- arXiv 1806.02299 (DPatch): classic detector patch; its abstract does not state false detections; family of LIT_A1.
- arXiv 2304.05370 (Overload) and arXiv 2312.09520 (SlowTrack): latency attacks whose abstracts do not state fabricated objects; the latency family is represented by P2-P2014, P2-P2015 and P2-P525 (LIT_A5). SlowTrack is used in section 1.3 for its crash-rate measure.
- arXiv 2006.16974 (CARLO): LiDAR only; used in section 1.2; not catalogued so that LiDAR analogues stay at two rows.
- arXiv 2507.09095: in-vehicle network timing attack, not a visual attack; used in section 1.3 only.
- arXiv 2603.14124: attack fingerprints on small self-driving platforms measured as steering deviation; phantom projection is one of five attack classes; not object detection.
- DOI 10.1109/ijcnn64981.2025.11228721 and DOI 10.1109/ijcnn60899.2024.10650435: backdoor attacks (training time), outside physical visual attacks.
- DOI 10.1145/3503161.3548362 and DOI 10.1109/iccv51701.2025.02267: patch defences, family of LIT_A1; title only.
- DOI 10.14722/vehiclesec.2024.23059: evasion-attack detection in simulation, family of LIT_A5; title only.
- DOI 10.3390/make5040080: reconstruction-based attack detection for vision-based driving; not specific to fabricated objects; title only.
- DOI 10.1007/s11263-008-0137-5 (Hoiem 2008), DOI 10.1007/978-3-030-03769-7_23 and DOI 10.1007/978-3-030-88494-9_18: no abstract in Crossref; kept as pointers in sections 1.2 and 3.
- DOI 10.1109/iseae69422.2026.11544251 and DOI 10.4271/j3087_202504: title-level pointers for question 3; content unknown.
- DOI 10.1109/tps-isa50397.2020.00042: probably the published version of P2-P2011 (same first author, near-identical title); identity not confirmed, so the DOI is not in the row.
- DOI 10.1145/3488932.3497771 (Koehler, 2022, signal injection attacks against CCD image sensors): record confirmed, no abstract in Crossref, content not read; camera-channel injection (family D of the problem map), sensor type CCD per the title; belongs with the camera-pipeline family of LIT_A4.
- DOI 10.1049/cps2.12034 and DOI 10.1109/iccps48487.2020.00024 (Cai, 2022 and 2020, real-time out-of-distribution detection with an emergency-braking case study): monitoring family of LIT_X6; the 2022 abstract is used in section 1.3 only.
Already catalogued by another task and not repeated: P2-P402, P2-P409, P2-P431 (LIT_A4); P2-P311 (LIT_A3); P2-P102, P2-P126 (LIT_A1); P2-P510, P2-P516, P2-P524, P2-P525 (LIT_A5). One deliberate overlap: P2-P2020 repeats P2-P234 of LIT_A2 with an abstract-level read.
- DOI 10.54941/ahfe1005212 (Hegna Berge, 2024, phantom braking concept paper with a cycling simulator): human-factors paper, not an attack or detection paper, outside the subject of the common brief; it was staged for a short time as row P2-P2026 and then removed from the staging file before the catalog was built; used in section 1.3 only.
Rows filed under family F1 that are not fabricated-object papers: P2-P2023, P2-P2024, P2-P2025 (evidence for question 3 of the brief).
