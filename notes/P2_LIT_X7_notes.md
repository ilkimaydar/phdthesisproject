# P2 LIT_X7 notes - night, low visibility and adverse weather (owner contribution 4)

Status: written by the LIT_X7 agents (first agent: rows P2-P1601 to P2-P1616; continuation agent: rows P2-P1617 to P2-P1624, corrections and this file). Not audited: a fresh-agent audit is required. Read depth: abstracts or metadata only; no full text was read. Every number is quoted from the abstract or record of the row named next to it. Rows of other tasks (ids outside P2-P1601 to P2-P1699) are cited as their task wrote them; this agent did not re-read those papers. Verification states come from scripts/rows_check.py and the ledger work/LIT_X7/verify_ledger.jsonl.

Rows: 24 (X7-F1 6, X7-F2 8, X7-F3 10); High 13, Medium 11; abstract 19, metadata-only 5. Verification and role counts: end line of progress/LIT_X7.log.

## Findings first (uncomfortable ones on top)
1. Closest prior work on the defense side of contribution 4: a sign and traffic-light recognition defense evaluated over highway, night, rain and urban domains (Dual-FoV, rows P2-P211 of LIT_A2 and P2-P509 of LIT_A5). Per P2-P509 it stacks feature squeezing, temperature scaling and entropy gating with causal voting over 5 to 7 frames, and attack success fell from 37.4 to 18.2 percent overall. The rows give no per-domain figures, no false alarms per hour and no abstain state. Night operation of a temporal attack defense is therefore not new; a per-condition, matched-false-alarm evaluation with an abstain state is not in the records seen.
2. Night is the best case for light-based attacks, not a corner case. Projected patches reach up to 100% success in low ambient light and weaken as light rises (P2-P411, LIT_A4); a UV-triggered fluorescent patch reports 98.31% success in low light (P2-P315, LIT_A3); simulated headlight and flashlight patterns exceed 70% digital success (P2-P345, LIT_A3). Slide 04 meets its strongest attacks in the conditions where benign headlights and auto-exposure jumps are also most frequent.
3. At night the attack signal can be a missing reflection, not an extra one. RDPA (P2-P1608) covers part of a retroreflective sign with low-reflectivity material: by day it blends in, under headlights it leaves a dark region that drives a targeted misclassification (preprint abstract: 85.25% physical success in low-light indoor tests, 91.82% on outdoor roads). Bright retroreflective patches exist for signs (P2-P317, P2-P318, LIT_A3) and reflective microprism patches on clothing defeat pedestrian detectors under headlights (P2-P319, LIT_A3: above 80% on RetinaNet with the authors set, 93.6% on KITTI). A slide 03 cue that looks only for excess brightness misses the dark-mask polarity.
4. A cheap reliability statistic for bad conditions already exists. Temel et al. (P2-P1602) report that the mean magnitude spectrum of frame-to-frame changes can indicate sign-detection performance under simulated challenging conditions, where precision fell by 29% and recall by 68% on average for two detectors. The reliability gate of slides 02 to 04 is not new as a condition estimator; its use to gate attack alarms is not in the records read.
5. Benign night and weather losses are large enough to swamp an object-vanishing alarm. Detectors keep only 30-60% of clean performance under synthetic corruptions (P2-P1601); rendered rain costs detection on the order of 15% (P2-P1604); sign sheeting grade changes YOLOv8 sign detection most at night (P2-P1606). A missed object at night is weak evidence of an attack unless the decision is conditioned on visibility.
6. Night does not disarm sticker attacks, and weather does not reliably weaken attacks. Jia et al. (P2-P1607) report a sign attack effective in sunny, cloudy and night conditions and against a 2021 production vehicle. For vehicle camouflage the records disagree: similar results across weather in a CARLA benchmark (P2-P1609), degraded success under weather and camera motion for CAMOU, RAUCA and FCA (P2-P1610), and camouflage trained with weather in the loop (P2-P1611).
7. Attacks can imitate weather: a raindrop sticker on the lens (P2-P1612), optimised rain streaks (P2-P1613) and optimised snow, rain or fog particles against optical flow (P2-P1614). The benign-rain branch of slides 04 and 05 has an adversarial tail. P2-P1614 reports that training with non-optimised weather raises robustness at almost no extra cost.
8. Synthetic night data can plant false objects: unpaired day-to-night translation hallucinates traffic signs, vehicles and light effects (P2-P1619), so a translated night test set could create false light cues for slides 03 and 04.

## Answers to the three questions of the brief

### Q1. How much detectors degrade at night or in rain, fog and snow, and on which data
| Row | Condition | Data | Reported effect (abstract) |
|---|---|---|---|
| P2-P1601 | Synthetic image corruptions at several severities | Pascal-C, COCO-C, Cityscapes-C | Detectors keep 30-60% of original performance; stylized training gives a substantial gain |
| P2-P1602 | Simulated challenging conditions on real sign video | CURE-TSD-Real, two detectors | Severe levels: precision -29%, recall -68% on average |
| P2-P1604 | Rendered rain | KITTI, Cityscapes, nuScenes with rain | Detection about -15%, segmentation about -60%, depth error 6-fold; finetuning on rendered rain +21% detection |
| P2-P1605 | Ten low-light types | ExDark | No detection numbers; under 2% of VOC, ImageNet and COCO images are low-light |
| P2-P1606 | Day versus night, sign sheeting grade | ZND, 16,500 images, YOLOv8 | Retroreflectivity tracks detection most at night; no numbers |
| P2-P1603 | Fog, night, rain, snow | ACDC | Described as challenging; no numbers |
| P2-P1619 | Day to night | BDD100K | Method gain of 15.5% mAP (a gain, not the size of the day-night gap) |

Gap: no record read gives the day-versus-night drop of one frozen detector on real driving video; the loss figures come from synthetic corruption, simulated conditions or rendered rain. The project has to measure the benign drop itself (ACDC paired adverse and normal frames of the same scenes; BDD100K night clips) before it claims any night gain.

### Q2. Which physical attacks were tested at night, and what changed
| Attack | Row | Night facts in the row | What changes at night |
|---|---|---|---|
| Printed sign attack, NDSS 2022 | P2-P1607 | Sunny, cloudy and night conditions; production vehicle | Still effective per the abstract; per-condition rates not read |
| RDPA dark mask on retroreflective signs | P2-P1608 | Built for night; 85.25% indoor low light, 91.82% on roads | The signal is missing return under headlights; the authors state that many physical attacks fail at night |
| Retroreflective patches on signs | P2-P317, P2-P318 (LIT_A3) | Not re-read here | Extra return under headlights |
| Reflective microprism patches on clothing | P2-P319 (LIT_A3) | Night tests; above 80% (RetinaNet), 93.6% (KITTI) | Pedestrian detectors fail under headlight return |
| Projected patches on 3D surfaces | P2-P411 (LIT_A4) | Up to 100% in low ambient light, indoors | Stronger as ambient light falls |
| UV-triggered fluorescent patch | P2-P315 (LIT_A3) | 98.31% in low light; 96.72% against five defences | Needs darkness for the trigger to show |
| Headlight and flashlight light patterns | P2-P345 (LIT_A3) | Above 70% digital | Mimics natural light |

Weather rather than night: similar results across weather (P2-P1609), degraded success (P2-P1610), weather-trained camouflage (P2-P1611); whether night is among the 9 ALLUDE weather settings is not stated. Near-infrared and thermal night attacks are outside the RGB scope (Exclusions) but back the slide 03 limitation that an IR-filtered RGB camera may not see an infrared attack.

### Q3. Low-cost enhancement or adaptation light enough for a laptop pipeline
| Row | Method | Cost facts read | Fit to the laptop (10-core CPU, 32 GB RAM, 6 GB GPU) |
|---|---|---|---|
| P2-P1616 | Zero-DCE++ curve estimation | About 10K parameters; 1000 FPS on one GPU, 11 FPS on a CPU at 1200x900x3 (authors hardware, not named) | Best fit found; 11 FPS means about 90 ms per frame of that size on the authors CPU (arithmetic on their figure) |
| P2-P1617 | IA-YOLO, differentiable image processing with a small parameter predictor | Size and runtime not in the abstract | Light, but trained jointly with the detector: conflicts with the frozen-detector design |
| P2-P1622 | FOLD, low-order enhancement plus YOLOv3 on an FPGA board | No numbers in the abstract | Supports a classical, non-learned baseline first |
| P2-P1615 | Learning to See in the Dark | Raw sensor input | No fit: the deck datasets are RGB (this agent's reading) |
| P2-P1618, P2-P1623, P2-P1624 | Day-to-night adaptation of the detector (ICCV 2025, CVPR 2023, CVPR 2024) | Not read | Training-time changes to the detector; comparison points, not front ends |
| P2-P1619 | Day-to-night translation with hallucination suppression | Not read | Training-data generation; heavy |

Open question: whether enhancement helps detection at all. P2-P1620 (ExDark, detection-oriented and cost-aware) and P2-P1621 (journal overview with empirical evaluation) address it; their findings were not read. Design consequence: an enhancement curve changes local contrast and saturation, the inputs of the slide 03 and 04 light cues, so cues should be computed on the raw frame or re-calibrated after enhancement.

## Problem map (attack families seen from the night and weather angle)
| Family | Defining rows | Note |
|---|---|---|
| Night reflectance attacks (headlight-dependent) | P2-P1608; P2-P317, P2-P318, P2-P319 (LIT_A3) | Two polarities: dark mask and bright patch; signs and pedestrians |
| Light-source attacks strongest in darkness | P2-P411 (LIT_A4); P2-P315, P2-P345 (LIT_A3) | Projection, UV fluorescence, light patterns |
| Daytime sticker attacks that survive night | P2-P1607 | Night among the tested conditions |
| Weather-aware vehicle camouflage (object hiding) | P2-P1611; evaluated by P2-P1609, P2-P1610 | Weather effect contested |
| Weather-mimicking perturbations | P2-P1612, P2-P1613, P2-P1614 | P2-P1613 and P2-P1614 digital; P2-P1612 needs lens access |
| Benign confounders | P2-P1601 to P2-P1606 | Night, rain, fog, snow and corruption losses; sheeting variability |
| Synthetic-data artefacts | P2-P1619 | Translation hallucinates signs, vehicles and lights |

## Solution map (defense, robustness and detection families)
| Family | Rows | What it offers the project |
|---|---|---|
| Temporal defense evaluated over night and rain domains | P2-P211 (LIT_A2), P2-P509 (LIT_A5) | Closest prior work; overall figures only in the rows |
| Robust training and augmentation | P2-P1601, P2-P1604, P2-P1613, P2-P1614 | Changes the detector; baseline for contribution 4 |
| Enhancement front ends | P2-P1616, P2-P1617, P2-P1622, P2-P1615 | Cheap night input repair; may interfere with light cues |
| Detector adaptation to night | P2-P1618, P2-P1619, P2-P1623, P2-P1624 | Comparison points for any night gain claim |
| Condition and reliability estimation | P2-P1602 (frame-change spectrum), P2-P1603 (uncertain-region masks) | Prior art for the reliability gate and abstain state |
| Enhancement-for-detection studies | P2-P1620, P2-P1621 | Decide whether an enhancement stage is worth its cost |

## Closest prior work to the owner's design slides (ranked)
1. Dual-FoV defense (P2-P509, P2-P211; other tasks) for contribution 4 and slide 05: temporal voting with an entropy gate, tested over night and rain domains. Left open: per-condition false alarms, abstain state, frozen-detector add-on, explanation.
2. RDPA (P2-P1608) against slide 03: a malicious night reflection can be a dark region; the cue must be two-sided.
3. Temel et al. (P2-P1602) against the reliability gate of slides 02 to 04: a cheap frame-change statistic already predicts detector performance in bad conditions.
4. Projection and fluorescent attacks (P2-P411, P2-P315; other tasks) for slide 04: the threat peaks in darkness.
5. Aldoski et al. (P2-P1606) for slide 03: benign night retroreflection varies with sheeting grade.
6. Jia et al. (P2-P1607) for slide 01 at night: sticker attacks work under headlight illumination.
7. Schmalfuss et al. (P2-P1614) for slide 05: optical flow can be driven wrong by weather-like particles.
8. ALLUDE, DCI and RAUCA (P2-P1610, P2-P1609, P2-P1611) for slide 05 object vanishing: weather effect on the threat unsettled; ALLUDE is a candidate generator of controlled clips (memory needs not read).
9. Michaelis et al. and Tremblay et al. (P2-P1601, P2-P1604): benign degradation baselines and a rain renderer for hard negatives.
10. Li et al. (P2-P1619): avoid translated night images as test data, or check them for hallucinated objects.

## Gaps and what is left to test
1. Per-condition attack detection with false alarms per hour, matched operating points and an abstain state: not found; the only defense seen with night and rain domains (P2-P211, P2-P509) has overall figures in the rows read.
2. ADAV (P2-P501, LIT_A5; the slide 05 baseline) was tested on BDD100K videos with pasted patches; that row reports no night split, so its night false-alarm rate is unknown.
3. Day-versus-night loss of one frozen detector on real driving video: not found (Q1).
4. A two-sided reflectance cue tested against both dark-mask and bright-patch night attacks: not found.
5. Weather effect on attack success: contested (P2-P1609 versus P2-P1610, P2-P1611).
6. Enhancement before detection: whether it helps (P2-P1620, P2-P1621 unread) and whether it hides or fakes light cues (untested hypothesis).
7. Lens-fixed artefacts: lens drops stay fixed in image coordinates while scene rain moves; whether that separates AdvRain-style stickers from benign drops is untested.

## Problem cards (hypotheses, not results)

### Card X7-C1. Night turns the reflection cue upside down
- Problem: under headlights a sign or a pedestrian is seen through retroreflection, and attacks can add return or remove it while benign sheeting quality also varies, so a brightness-excess residual misses half of the threat.
- Contribution to test: a two-sided, class-conditioned reflectance residual inside the tracked region (observed return against the expected return for that class, distance and exposure), with abstain when headlight geometry or exposure is unknown.
- Prior work coverage: the attacks are published (P2-P1608; P2-P317, P2-P318, P2-P319) and benign variability is measured (P2-P1606); no record seen tests one detector against both polarities.
- Open-source starting point: frozen sign detector (YOLOX-Nano as on the deck), OpenCV region statistics, scikit-learn calibration; CURE-TSD tools named in P2-P1602 (location UNVERIFIED).
- Data and laptop fit: SYSU-RTSD (P2-P1608; location and licence unknown), ZND (P2-P1606; availability unknown), CURE-TSD-Real (P2-P1602; licence not checked), BDD100K night clips (licence question with LIT_X2). Dark-mask and bright-patch perturbations simulated digitally first (a proxy, not a physical test). CPU statistics plus a nano detector fit the 6 GB GPU.
- Experiment workflow: (1) run the frozen detector on benign night sign tracks and fit the expected-return model per class; (2) inject digital dark-mask and bright-patch perturbations into held-out recordings; (3) score one-sided and two-sided residuals per frame and per track; (4) compare with brightness-only and texture-only checks at matched false-alarm points.
- Success measure: recall at a fixed false-alarm rate for each polarity; false alarms per hour of benign night driving; ms per region; abstain count.
- Sources: P2-P1608, P2-P1606, P2-P1607, P2-P1602.

### Card X7-C2. A missed object at night is weak evidence of an attack
- Problem: benign night and weather already remove many detections, so an object-vanishing alarm with one threshold will be dominated by benign misses after dark and in rain, fog or snow.
- Contribution to test: a condition-aware alarm and abstain rule driven by a cheap visibility descriptor (the frame-change spectrum of P2-P1602, global luminance statistics, or the per-frame processing parameters of an IA-YOLO style predictor), calibrated per condition on a separate calibration set.
- Prior work coverage: the descriptor exists (P2-P1602); a temporal defense was evaluated over night and rain domains (P2-P509, P2-P211) without per-condition false alarms in the rows read; the ADAV baseline (P2-P501) has no night split in its row.
- Open-source starting point: frozen detector (YOLOX-Nano), OpenCV statistics and FFT, scikit-learn calibration; IA-YOLO code named in P2-P1617 (location UNVERIFIED); ADAV as comparator.
- Data and laptop fit: ACDC (P2-P1603; 4006 adverse images with same-scene normal references in the extended version; licence and access not checked), BDD100K night and weather clips (licence question), CURE-TSD-Real (P2-P1602). Inference only; fits the laptop.
- Experiment workflow: (1) measure benign miss rates of the frozen detector per condition on ACDC paired frames and BDD100K night; (2) compute visibility descriptors per frame; (3) inject digital object-vanishing perturbations into held-out recordings; (4) compare a fixed-threshold alarm, ADAV and the condition-calibrated rule at matched false alarms.
- Success measure: false alarms per hour by condition; attack recall at a matched false-alarm rate by condition; abstain rate; p95 latency.
- Sources: P2-P1601, P2-P1602, P2-P1603, P2-P1604, P2-P1617.

### Card X7-C3. Weather that is not weather
- Problem: attacks can imitate rain on the lens, rain streaks or weather particles, so the benign-rain branch of slides 04 and 05 can be exploited, and optical-flow cues can be driven wrong.
- Contribution to test: physical-consistency features that separate lens-fixed artefacts from scene weather (fixed image position across camera motion, flow consistency between rain layer and scene), combined with a weather gate on the motion cues.
- Prior work coverage: the attacks are published (P2-P1612, P2-P1613, P2-P1614) and weather augmentation is reported as a cheap robustness fix (P2-P1614); no record seen detects weather-mimicking attacks.
- Open-source starting point: OpenCV optical flow and temporal statistics; Distracting Downpour code named in P2-P1614 (location UNVERIFIED); rain renderer of P2-P1604 (location not seen).
- Data and laptop fit: ACDC rain frames, rendered rain on held-out clips (base dataset licences to check), digital lens-drop overlays as in AdvRain. CPU-bound; fits.
- Experiment workflow: (1) build benign sets with rendered rain and random lens drops; (2) build adversarial sets with drops placed by random search against the frozen detector; (3) compute fixity and flow-consistency features; (4) compare with brightness-only and temporal-only baselines at matched false alarms on real rain clips.
- Success measure: true positive rate at a fixed false-positive rate for adversarial versus benign drops; false alarms on real rain; ms per frame.
- Sources: P2-P1612, P2-P1613, P2-P1614, P2-P1604, P2-P1603.

### Card X7-C4. Enhancement may help the detector and blind the light cues
- Problem: a low-light enhancement stage may raise night detection, but it rewrites the local contrast and saturation the light cues read, and whether it helps detection at all is an open question.
- Contribution to test: measure detection change and cue separability with and without enhancement, and test the split design "detector on the enhanced frame, light cues on the raw frame".
- Prior work coverage: enhancement-for-detection studies exist (P2-P1620, P2-P1621; findings not read); no record seen looks at the effect of enhancement on attack cues.
- Open-source starting point: Zero-DCE++ (project page named in P2-P1616, UNVERIFIED), a classical gamma or histogram baseline as in P2-P1622, frozen YOLOX-Nano.
- Data and laptop fit: ExDark (P2-P1605; licence not checked), BDD100K night (licence question). Zero-DCE++ has about 10K parameters per its abstract; about 90 ms per 1200x900 frame on the authors CPU, so GPU or downscaling is needed for real time.
- Experiment workflow: (1) run the frozen detector on raw, classical-enhanced and Zero-DCE++ frames; (2) compute the slide 03 and 04 light cues on each version; (3) inject digital light attacks into held-out recordings; (4) compare detection AP, cue AUROC at matched false alarms and added latency.
- Success measure: AP change at night; cue recall at a matched false-alarm rate; added ms per frame and peak memory.
- Sources: P2-P1616, P2-P1617, P2-P1620, P2-P1621, P2-P1622, P2-P1605.

## Datasets, benchmarks and code seen
| Item | Row | Location as stated in the record (not opened) | Licence |
|---|---|---|---|
| ACDC (fog, night, rain, snow with same-scene normal references) | P2-P1603 | acdc.vision.ee.ethz.ch, UNVERIFIED | Not checked |
| ExDark (ten low-light types) | P2-P1605 | github.com/cs-chan/Exclusively-Dark-Image-Dataset, UNVERIFIED | Not checked |
| CURE-TSD-Real (simulated conditions on real sign video) | P2-P1602 | github.com/olivesgatech/CURE-TSD, UNVERIFIED | Not checked |
| Pascal-C, COCO-C, Cityscapes-C | P2-P1601 | Public per the abstract; location not seen | Not checked |
| Rain-augmented KITTI, Cityscapes, nuScenes | P2-P1604 | Project page per the conference abstract; location not seen | Base dataset licences apply; not checked |
| ZND sign set (16,500 images) | P2-P1606 | Not seen | Not checked |
| SYSU-RTSD night reflective sign set | P2-P1608 | Not seen | Not checked |
| DCI vehicle benchmark (CARLA) | P2-P1609 | Not stated | Not checked |
| ALLUDE evaluation system | P2-P1610 | Open source per the abstract; location not seen | Not checked |
| Zero-DCE++ | P2-P1616 | li-chongyi.github.io/Proj_Zero-DCE++.html, UNVERIFIED | Not checked |
| IA-YOLO | P2-P1617 | github.com/wenyyu/Image-Adaptive-YOLO, UNVERIFIED | Not checked |
| Distracting Downpour | P2-P1614 | github.com/cv-stuttgart/DistractingDownpour, UNVERIFIED | Not checked |
| Night data catalogued by other tasks | P2-P415 and P2-P2417 (provident vehicle detection at night), P2-P421 (NightOwls), P2-P418 and P2-P419 (Flare7K, Flare7K++), P2-P337 (night road glare set), P2-P1118 and P2-P1119 (nighttime segmentation sets), P2-P2408 (raw low-light set of P2-P1615) | See those rows | See those rows |

## Leads
Confirmed by rows of other tasks (not re-read here): the reflective night pedestrian attack seen in a websearch result of the first agent is P2-P319 (LIT_A3, Symmetry 2024, DOI 10.3390/sym16101262); the retroreflective patch work-in-progress paper is P2-P317 (LIT_A3); the two deck links of the brief appear as deck-source rows P2-P2407 (Debiased Teacher, same paper as P2-P1618) and P2-P2408 (same paper as P2-P1615); the nighttime flare sets are P2-P418 and P2-P419 (LIT_A4).
Not confirmed (1): RAUCA conference version (ICML 2024, from memory); not checked; noted on P2-P1611.

## Duplicates across tasks (for the coordinator)
P2-P1601 = P2-P1723 (LIT_X8); P2-P1603 = P2-P416 (LIT_A4) and P2-P2416 (deck sources); P2-P1605 = P2-P417 (LIT_A4); P2-P1607 = P2-P2005 (LIT_X11); P2-P1609 has a journal version P2-P1801 (LIT_X9); P2-P1612 = P2-P423 (LIT_A4, title case differs); P2-P1615 = P2-P2408 and P2-P1618 = P2-P2407 (deck sources).

## Records found but not catalogued (row target reached, no abstract read, or another task's area)
Crossref, no abstract: GDIP, ICRA 2023 (10.1109/icra48891.2023.10160356); Similarity Min-Max zero-shot day-night adaptation, ICCV 2023 (10.1109/iccv51070.2023.00744); Cooperative Students night adaptation, ICME 2024 (10.1109/icme57554.2024.10688290); SCI low-light enhancement, CVPR 2022 (10.1109/cvpr52688.2022.00555); WIP adversarial object-evasion attack detection in simulation, VehicleSec 2024 (10.14722/vehiclesec.2024.23059); effect of rain, snow, fog and hail on a self-driving car, IEEE Vehicular Technology Magazine 2019 (10.1109/mvt.2019.2892497); AdvLensPolluter camera contamination attack, IJCNN 2025 (10.1109/ijcnn64981.2025.11229089); YOLOv8 with Zero-DCE enhancement, ICRM 2025 (10.1109/icrm66809.2025.11349035).
Crossref with abstract: NUDN nighttime unsupervised domain adaptation with knowledge distillation and the LightImg augmentation, Applied Sciences 2024 (10.3390/app14188109).
Crossref metadata from the earlier agent (abstracts not read; Crossref stopped in this run): low-light synthesis for nighttime sign detection (SSRN preprint 2026, 10.2139/ssrn.7306026); RBL-YOLO nighttime detection (SSRN preprints 2026, 10.2139/ssrn.7312100 and 10.2139/ssrn.7324895); nighttime sign detection and classification, CVCI 2022 (10.1109/cvci56766.2022.9964980); Fog-YOLO11n, Applied Sciences 2026 (10.3390/app16168059); YOLOv8-SCS adverse weather, IEEE Access 2025 (10.1109/access.2025.3602211); joint-teacher nighttime adaptation, Measurement Science and Technology 2026 (10.1088/1361-6501/ae958c); haze removal and classification, ECCV 2018 (10.1007/978-3-030-01249-6_42).
arXiv metadata only: fakeWeather lens masks (2205.13807); AdvHaze (2104.13673); CURE-TSR (1712.02463); Foggy Cityscapes (1708.07819); BDD100K (1805.04687); Seeing Through Fog (1902.08913); DAWN (2008.05402); rainy-conditions detection review (2006.16471); SHIFT (2206.08367); IAT light adaptation transformer (2205.14871); MAET dark detection (2205.03346); FeatEnHancer (2308.03594); PE-YOLO (2307.10953); PADetBench (2408.09181, catalogued by LIT_A5 as P2-P543); day-to-night style transfer for vehicle detection (2412.16478); night pedestrian detection under illumination shift (2605.16406).

## Exclusions
- Near-infrared and thermal attacks and surveys (arXiv 2101.08154, 2205.05909, 2412.13709, 2603.21876, 2609.18133, 2604.06865, 2610.21034): sensors outside the RGB scope of the slides (2412.13709 is catalogued by LIT_A3 as P2-P320).
- Off-topic search hits: astronomy streak detection, satellite cyclone imagery, radar compression, deepfake defense, SAM corruption robustness, underwater enhancement, nighttime aerial tracking, thermal colorization, multispectral and surveillance image translation, 3D and point-cloud domain adaptation, fire-safety false-alarm studies, fatigue detection, a wheelchair simulator record, and supplement or table components without a paper record.
- Generic low-light enhancement networks without a detection result in the record (GAN, Retinex, invertible and transformer enhancers in the ledger): outside the detection focus of this task.

## Instructions found in data
None seen in the records, search results and files read by the continuation agent.
