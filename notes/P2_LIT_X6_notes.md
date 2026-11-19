# P2_LIT_X6 notes - calibration, abstention and selective prediction

Label LIT_X6 (wave 2, continuation run). Staging file work/LIT_X6/rows.jsonl: 25 rows, P2-P1501 to P2-P1525. Verification state from scripts/rows_check.py: VERIFIED 23 (Crossref), UNVERIFIED 2 (arXiv-only, NEEDS_VERIFY: P2-P1524, P2-P1525). Read depth: abstract 21, metadata-only 4 (P2-P1505, P2-P1506, P2-P1514, P2-P1515), full-text 0. Status: written by this agent, not audited.

Continuation note: the first run of this label stopped on a provider rate limit after 12 logged queries. Its candidate lists were not saved, so this run rebuilt the candidates with 11 new queries and did not repeat the logged ones. The arXiv API host was under a shared stop for the whole run, so arXiv-only papers could not be script-checked.

## Answers to the three questions of the brief (uncomfortable findings first)

### 3. Does any attack detector use a calibrated three-way output (clear, suspected, insufficient evidence)?
Not found, to our knowledge, in the 23 queries logged for this label. Each ingredient exists separately:
- Same pipeline shape without calibration or an insufficient state: DetectorGuard (LIT_A1 row P2-P111) checks a frozen detector against an independent objectness cue and raises an alert; it has two outcomes (detections or alert).
- Calibrated abstention in AV perception without attacks: the dual-threshold conformal method of Kumar et al. (LIT_A5 row P2-P536) abstains under environmental perturbation; SAOD (P2-P1502) gives a detector calibrated detections plus an image-level reject, tested under domain shift.
- Calibrated credibility plus explanation plus adversarial-input detection, for classification only: Deep k-Nearest Neighbors (P2-P1525, NEEDS_VERIFY).
- Calibrated reject on traffic-sign recognition, not adversarial: Boursinos et al. (P2-P1512).
- Formal sources for a third outcome: reject option (Chow, P2-P1505), sequential tests with a continue outcome (Wald, P2-P1506), three-way decisions (Yao, P2-P1514); all three read at title level only.
Reading: the combination the design slides propose (physical attacks on detectors, a calibrated clear / suspected / insufficient output, evaluation at matched false-alarm rates) appears open. The uncomfortable side: every ingredient is mature, so a reviewer may call the combination incremental unless the insufficient-evidence state is shown to change outcomes, for example fewer false alarms on benign look-alikes at the same attack recall.

### 1. Which calibration measures exist for detectors, and how do they behave under shift?
Measures seen:
- D-ECE: precision against confidence, optionally binned over box position and size (Küppers 2020, P2-P1516).
- LaECE: confidence should reflect classification and localisation quality together (Oksuz 2023, P2-P1502).
- LaECE0 and LaACE0: confidence aligned with IoU to the matched object, read together with LRP at tuned thresholds (Kuzucu 2024, P2-P1503).
- Proper scoring rules, calibration plots and errors, entropy under shift (Huseljic 2024, P2-P1513); a survey of probabilistic detection metrics (Feng 2022, P2-P1511).
- A calibration error with a generic link function by Popordanoska et al. is named in the supplement of P2-P1503 (not checked).
Behaviour reported in the records read:
- Location: on COCO, D-ECE grows as detections approach the image border (figure caption, P2-P1516).
- Evaluation pitfalls: D-ECE plus AP comparisons and temperature scaling can mislead; post-hoc isotonic regression on D-DETR beats the train-time Cal-DETR by more than 7 D-ECE on COCO (abstract, P2-P1503).
- Shift: the BPC code README (D-DETR) lists D-ECE 12.8 in-domain (MS-COCO) and 10.8 out-of-domain (corrupted COCO) for the baseline, 10.3 and 9.4 with the BPC loss, and 14.2 and 12.3 with temperature scaling (P2-P1517; README, not the paper). Temperature scaling made calibration worse in both settings in that table.
- SAOD: tested detectors show LaECE of about 10-20% (CVPR slides); one figure shows 43.3% before and 17.7% after linear-regression calibration (P2-P1502). Numbers under shift were not read.
- Huseljic 2024 analyses calibration under distributional shift and on OOD data and improves it by last-layer fine-tuning (abstract); numbers not read.
- Seen but not catalogued (LiDAR): Feng et al. 2019 (arXiv 1909.12358) report averaged ECE on nuScenes of 0.218 uncalibrated, 0.120 with isotonic regression fitted on KITTI and 0.030 when fitted on 1% of nuScenes (table extract): a calibrator transfers only partly across datasets.
Gap: no record read reports detector calibration under night, glare or rain separately, or under physical attack. The slides need a calibrated consistency residual, not only calibrated detector confidence; no paper read calibrates such a residual.

### 2. Which abstention schemes report risk against coverage?
- Selective classification with guaranteed risk and risk-coverage curves: Geifman 2017 (P2-P1524, NEEDS_VERIFY); abstract: 2% top-5 ImageNet error guaranteed with probability 99.9% at almost 60% coverage.
- Error against reject rate: Chow 1970 (P2-P1505, title level).
- Accuracy at a fixed true positive rate of the rejector, adaptive attacks included: Pang 2022 (P2-P1518). Its table 1 shows 57.23% accuracy on PGD-10 inputs kept by a confidence rejector at 95% TPR against 88.75% for the true-label oracle: plain confidence is far from an ideal rejector under attack.
- Rejection tested against an attacker who knows the reject rule: Sotgiu 2020 (P2-P1504).
- Error rate against number of alarms: Boursinos 2021 (P2-P1512).
- Image-level accept or reject scored inside DAQ (harmonic mean of TPR and TNR for reliability of uncertainties): SAOD (P2-P1502).
Gap: no per-object or per-track risk-coverage evaluation for detectors was found; risk-coverage is defined for classification. Coverage must be defined (share of objects, tracks or frames decided) before a detection paper can claim it.

## Problem map
Attack families are catalogued by LIT_A1 to LIT_A5. This map lists the reliability failures this angle addresses.
| Problem | Rows that define or show it |
|---|---|
| Unknown objects detected as known classes with very high confidence | P2-P1523, P2-P1522 |
| Miscalibration that depends on object location and size | P2-P1516 |
| Misleading calibration evaluation (D-ECE with AP, temperature scaling) | P2-P1503 |
| Calibration that changes under domain shift | P2-P1517, P2-P1513, P2-P1502 |
| Pixel-level OoD scores give scattered false positives and frame-to-frame flicker | P2-P1501 |
| Conformal guarantees lost under adversarial perturbation | P2-P1521 |
| Reject rules evaded by attackers who know them | P2-P1504, P2-P1518 |
| Exchangeability assumption broken by consecutive frames | P2-P1519 (footnotes), P2-P1510 |

## Solution map
- Post-hoc detector calibration: Platt scaling and isotonic regression tailored to detectors (P2-P1503); box-sensitive calibration (P2-P1516); per-class calibrators inside SAOD (P2-P1502).
- Train-time calibration losses: BPC (P2-P1517); TCD and Cal-DETR by the same group (not catalogued).
- Selective prediction and reject options: guaranteed-risk selection (P2-P1524), error-reject theory (P2-P1505), rectified rejection (P2-P1518), multi-layer neural rejection (P2-P1504), conformal reject on signs (P2-P1512), three-way decisions (P2-P1514), sequential tests (P2-P1506).
- Conformal methods: tutorial (P2-P1508); conformal p-values with false discovery control and a uniform bound on any detector's false positive rate across thresholds (P2-P1507); conformal boxes (P2-P1519, P2-P1520); runtime OOD monitors with calibrated false-alarm rates (P2-P1509); windows of consecutive inputs (P2-P1510); robust conformal prediction under attack (P2-P1521); nearest-neighbour credibility (P2-P1525).
- Open-set and OOD road objects: object-level OoD boxes with temporal smoothing (P2-P1501); unknown-aware training from video (P2-P1522); open-set protocol (P2-P1523); corner-case data (P2-P1515).
- Surveys and tutorials: P2-P1511, P2-P1508.

## Closest prior work to the owner's design slides (ranked)
Target element: the calibrated decision with an explicit benign / insufficient / abstain branch shared by all five slides, the "calibrated uncertainty" of slide 01 and the "principled insufficient-evidence state" of slide 05.
1. P2-P1502 SAOD (Oksuz 2023): the only record read that joins calibrated detector confidences with an explicit reject decision for a detector, evaluated under shift with a driving use case. Missing: attacks, per-object abstention, a suspected state, explanation.
2. P2-P1510 CODiT and P2-P1509 Cai 2020: monitors for driving perception with bounded or calibrated false alarms; CODiT works on windows of consecutive frames (slide 05). Missing: attacks (a 2023 follow-up by Cai on deception attacks is LIT_A5 row P2-P534), explanation, abstain state.
3. LIT_A5 row P2-P536 (Kumar 2025): dual-threshold conformal abstention for camera and LiDAR perception under environmental perturbation. Missing: attacks, detection, video.
4. P2-P1512 Boursinos 2021: conformal reject with calibrated error on traffic-sign recognition. Missing: attacks, detection.
5. P2-P1525 Deep k-Nearest Neighbors: calibrated credibility, explanation and adversarial-input detection together. Missing: detection, physical attacks, laptop cost not shown.
6. LIT_A1 row P2-P111 DetectorGuard: same pipeline shape (frozen detector, independent cue, consistency check, alert). Missing: calibration and an insufficient-evidence state.
7. P2-P1520 Timans 2024: conformal label sets and box intervals on frozen detectors; a label set with more than one class is a possible insufficient-evidence signal (inference, not tested by the paper).

## Gaps and what is left to test
1. A calibrated three-way decision for physical-attack detection on detectors: not found.
2. Calibration of a consistency residual under benign shift (night, glare, rain) against attack: not found.
3. Risk-coverage for detection at object or track level: not defined in any record read.
4. Conformal guarantees on video: CODiT handles windows; recording-level splits are needed so that calibration and test frames are not neighbours (deck rule).
5. An attacker who targets the abstain band (forcing abstention as a denial of service) or the alarm threshold: P2-P1504, P2-P1518 and P2-P1521 show the need; no physical-attack study read.
6. Cost: SAOD, STUD and DetSeg retrain detectors or use large open-world models; post-hoc calibrators and conformal thresholds need only cached scores (inference from the method descriptions, not measured).

## Problem cards
Hypotheses, not results. Hardware for the fit lines: 10-core CPU, 32 GB RAM, one laptop GPU with 6 GB (COORDINATOR UPDATE 1). Deck rule: CPU baselines and frozen features first; split by recording.

### Card X6-1. Abstain with a guarantee: a calibrated three-way attack decision on a frozen detector
- Problem: a two-way attack flag must guess when cues are weak (night, occlusion, distance), which inflates false alarms or misses attacks; no record read gives physical-attack detection on detectors a calibrated insufficient-evidence state.
- Contribution to test: post-hoc calibration of the consistency residual plus two conformal thresholds gives clear, suspected and insufficient outputs whose false-alarm rate on held-out benign recordings stays at the target, with higher attack recall on decided cases than one threshold at the same false-alarm rate. Prior coverage: SAOD (P2-P1502) covers image-level reject for detectors under shift and LIT_A5 row P2-P536 covers dual-threshold abstention under environmental perturbation; neither tests attacks.
- Open-source starting point: fiveai/detection_calibration, fiveai/saod and alextimans/conformal-od (locations UNVERIFIED); a small frozen detector from LIT_X3.
- Data and laptop fit: detector inference on the 6 GB GPU or the CPU; calibrators and thresholds work on cached scores on the CPU (to be measured). Benign driving video (BDD100K is named on the deck) plus public physical-attack clips; licence question: read the research-use terms of each set before download (LIT_X2).
- Experiment workflow: (1) run the frozen detector and one cheap cue on benign and attack recordings and cache the residuals; (2) fit Platt or isotonic calibrators on a recording-level calibration split; (3) set the alarm threshold from conformal p-values at a target false-alarm level and the abstain band from a second level or a risk target; (4) report false alarms per hour on held-out benign recordings, recall on decided cases, the insufficient-evidence rate by condition and p50/p95 latency.
- Success measure: at a matched false-alarm rate, higher recall on decided cases than the single-threshold baseline, with the insufficient-evidence rate stated per condition and the held-out false-alarm rate inside the target.
- Sources: P2-P1502, P2-P1503, P2-P1507, P2-P1520, P2-P1505; P2-P1524 (NEEDS_VERIFY).

### Card X6-2. Bounded false alarms over frames: window-level conformal evidence for slide 05
- Problem: per-frame flags on video either fire on short benign glitches or miss attacks that persist; slide 05 asks for causal accumulation with bounded memory and an insufficient-evidence state.
- Contribution to test: per-frame conformal p-values of a consistency residual, combined over a bounded causal window (Fisher combination or merging functions as in CODiT and its 2024 extension) and compared with a sequential test that keeps a continue state, all at the same false-alarm rate as per-frame thresholds and fixed persistence rules. Prior coverage: CODiT (P2-P1510) already gives window-level OOD detection with bounded false alarms in driving, and LIT_A5 row P2-P534 combines conformal scores with CUSUM for deception attacks; physical attacks on detectors with an explained trigger cue remain open.
- Open-source starting point: kaustubhsridhar/time-series-OOD (location UNVERIFIED); frozen detector plus tracker.
- Data and laptop fit: only residual sequences are processed, CPU only; benign driving video plus attack clips (licence question as in card X6-1).
- Experiment workflow: (1) compute a per-frame residual per track on benign recordings; (2) turn it into conformal p-values against a held-out benign calibration set; (3) combine over windows of k frames, with k set by the latency budget, and compare Fisher, harmonic mean and a sequential test; (4) measure false alarms per hour, delay in frames, the share of tracks left undecided, memory and p95 latency.
- Success measure: false alarms per hour on held-out benign recordings at or below the bound, and shorter delay than per-frame thresholding at the same false-alarm rate.
- Sources: P2-P1510, P2-P1509, P2-P1507, P2-P1506.

### Card X6-3. Does calibration survive the attack and the night?
- Problem: calibrators and conformal thresholds are fitted on clean daytime data; physical patches and night or weather shift can both move detector scores, and no record read separates the two.
- Contribution to test: measure detector calibration (LaECE0, D-ECE) and conformal set coverage on clean, benign-shift and attacked images, and test whether the calibration gap or the label-set size separates attack from shift well enough to feed the suspected or insufficient split. Prior coverage: P2-P1513 and P2-P1517 measure calibration under benign shift; P2-P1521 restores coverage under norm-bounded digital attacks; none covers physical patches on detectors.
- Open-source starting point: fiveai/detection_calibration and alextimans/conformal-od (locations UNVERIFIED).
- Data and laptop fit: inference only; night or weather subsets of public driving sets (ACDC and BDD100K are named on the deck) and physical-attack image sets listed by LIT_X2; licence question per source.
- Experiment workflow: (1) calibrate a frozen detector post hoc on clean validation data; (2) evaluate LaECE0, D-ECE and per-class coverage on clean, night or weather, and attacked sets; (3) count how often attacked objects get multi-label sets or low credibility against confident wrong labels; (4) compare those counts with the benign-shift sets.
- Success measure: a table of calibration and coverage by condition and a stated answer whether attack-induced and shift-induced miscalibration can be told apart (either answer is a result).
- Sources: P2-P1503, P2-P1516, P2-P1517, P2-P1513, P2-P1520, P2-P1521, P2-P1523.

## Datasets, benchmarks and code seen
Code locations come from abstracts, papers or repository pages in search results; none was opened or tested, so all are UNVERIFIED.
- github.com/fiveai/saod: SAOD code and test sets (P2-P1502).
- github.com/fiveai/detection_calibration: detector calibrators and evaluation (P2-P1503).
- github.com/fabiankueppers/calibration-framework (P2-P1516).
- github.com/akhtarvision/bpc_calibration: the repository page shows an MIT licence (P2-P1517).
- github.com/alextimans/conformal-od (P2-P1520).
- github.com/kaustubhsridhar/time-series-OOD: code, data and trained models per the abstract (P2-P1510).
- github.com/huachao0124/DetSeg-official (P2-P1501).
- github.com/P2333/Rectified-Rejection (P2-P1518).
- Data: CODA (P2-P1515); SAOD test sets; road anomaly benchmarks named in a third-party summary of P2-P1501 (RoadAnomaly, Fishyscapes, SegmentMeIfYouCan, LostAndFound); OoDIS (lead). No licence was read in this run.

## Leads not confirmed (14)
1. Cal-DETR (named in the abstract of P2-P1503): not checked.
2. TCD, Towards Improving Calibration in Object Detection Under Domain Shift (NeurIPS 2022): abstract read on the NeurIPS page; no DOI and arXiv stopped, so not catalogued.
3. Calibration error by Popordanoska et al. (named in the supplement of P2-P1503): not checked.
4. Conformal object detection for railway signalling by Andéol et al. (memory lead): not searched, budget.
5. OoDIS anomaly instance segmentation and detection benchmark (arXiv 2406.11835): seen in a search result; arXiv check impossible.
6. Out-of-Distribution Segmentation in Autonomous Driving: Problems and State of the Art (CVPRW 2025): seen; not checked.
7. Can We Trust You? On Calibration of a Probabilistic Object Detector for Autonomous Driving (arXiv 1909.12358, LiDAR): table extract read; not checked.
8. Uncertainty-based mitigation of adversarial attacks on automated lane centering (arXiv 2103.00345): seen; lane target outside this angle (LIT_X14).
9. Confidence Calibration for Object Detection and Segmentation (Springer book chapter, doi 10.1007/978-3-031-01233-4_8): seen; not script-checked.
10. Confidence-calibrated adversarial training (named in the related work of P2-P1518): not checked.
11. PatchGuard++ and Minority Reports (named in a query string of the first run): not checked in this run.
12. The Road to Safety: A Review of Uncertainty and Applications to Autonomous Driving Perception (Entropy 2024): seen; not checked.
13. ST-OOD spatio-temporal OOD detection with a martingale-based conformal test (Journal of Systems Architecture 2025): seen; not checked.
14. Detection of Physical Adversarial Attacks on Traffic Signs for Autonomous Vehicles (IEEE IAICT 2023, autoencoder reconstruction error): seen; attack detection without calibration, left to LIT_A1 or LIT_X12.

Verified in the ledger but not catalogued, to stay inside the 25-row target: Kaur et al. 2024, ACM Transactions on Cyber-Physical Systems, doi 10.1145/3648005 (CODiT extension, noted in P2-P1510); Miller et al. 2018, ICRA, doi 10.1109/icra.2018.8460700 (dropout sampling for open-set detection; P2-P1523 reports it did worse); Pathiraja et al. 2023, CVPR, doi 10.1109/cvpr52729.2023.01890 (train-time multiclass confidence and localisation calibration; abstract not read).

## Exclusions
- Search noise from title searches: a dissertation on motion forecasting, a journal paper benchmarking YOLO versions (venue not assessed, not read), a 2026 conference paper on uncertainty-aware calibration (not read), an NLP paper on influence functions, and two dissertation records.
- Outside the camera scope: Spotting the Unexpected (STU), a LiDAR anomaly dataset (CVPR 2025).
- Inside the subject but outside this angle, left to other tasks: a VehicleSec 2024 work-in-progress paper on large multimodal models as a verification layer for adversarial signs; a commercial traffic-sign recognition attack study (arXiv 2409.09860); an NDSS 2022 paper on physical attacks against traffic-sign recognition.

## Notes for the coordinator
- No instruction addressed to agents was found in search results, API answers or pages.
- NEEDS_VERIFY: P2-P1524 (arXiv 1705.08500) and P2-P1525 (arXiv 1803.04765) need the arXiv API check after the shared stop ends.
- Counts: websearch 23 of 40 for this label (12 in the first run, 11 here); lit_verify 17 of 50 (all in this run).
