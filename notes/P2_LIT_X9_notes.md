# P2_LIT_X9 notes - system-level impact of perception attacks, simulation and benchmark platforms, digital-to-physical gap

Label LIT_X9 (wave 2, continuation run). Brief: briefs/LIT_X9.md. Rows: work/LIT_X9/rows.jsonl (paper_id block P2-P1801 to P2-P1899). Status: writer's own work, not audited.

## How this list was built
- Websearch returned no results for 5 of 5 queries (Q: lines in progress/LIT_X9.log), so discovery ran through `search-crossref` title and keyword queries (work/LIT_X9/query_log.tsv).
- Crossref: 35 calls, then STOP_HOST from a shared stop set by another agent; Crossref ended for this run. arXiv: the shared stop seeded by the coordinator was in force at the start; 2 batch calls with abstracts after it expired (21 of 21 ids found). No other host used. lit_verify 37 of 50 calls, websearch 5 of 40.
- 26 rows, all passing rows_check: VERIFIED 18 (Crossref), ARXIV_API_VERIFIED 8. Read depth: abstract 24, metadata-only 2 (P2-P1804, P2-P1805). No full text was read.
- Duplicates with other tasks, kept on purpose because they are core to these families and this run read their abstracts or confirmed their venue: P2-P1806 (= P2-P2024, P2-P2321), P2-P1807 (= P2-P2025), P2-P1808 (= P2-P339, arXiv only there), P2-P1816 (= P2-P1110, metadata-only there), P2-P1817 (= P2-P1108, P2-P2017, metadata-only there), P2-P1819 (= P2-P2315, metadata-only there), P2-P1826 (= P2-P2317, metadata-only there). 19 rows are new to the project as far as a title search of work/*/rows.jsonl showed.
- All three brief leads are confirmed: the ICCV 2023 system-level study (P2-P1806), simulator-based attack benchmarks (Q2 table), and optimisation over transformations (P2-P1821, P2-P1824).

## Uncomfortable findings first
1. The question behind card X9-C1 is already answered for attacks: all representative STOP-sign evasion attacks showed no system-level effect in the ICCV 2023 measurement (P2-P1806); driving-safety damage was decoupled from detection precision (P2-P1807); success against commercial sign recognition was much lower than academic results suggest (P2-P1808). Two consequences for Paper 2: the threat a detector guards against may be weaker in practice than per-frame numbers imply, and reviewers can ask for decision-level evidence that the detector helps. What stays open, to our knowledge from the records read, is the same question asked of attack detectors and their false alarms.
2. Simple digital pasting misstates attack strength: success on simple digital simulations does not predict realistic success (REAP, P2-P1816); real-world patches are notably less effective than digital ones (P2-P1818); adversarial strength is hard to keep in uncontrolled settings (APRICOT, P2-P1817). A detector validated only on pasted patches stands on weak ground (card X9-C2).
3. Attack detectors inside a simulated driving loop already exist: P2-P1803, P2-P1804, AD2 (P2-P507) and VisionGuard (P2-P512). P2-P1804 is the closest in setting and was read at title level only; read it before any novelty claim for card X9-C1.

## Answers to the brief questions

### Q1. Studies that measure the effect of an attack on driving decisions rather than detector accuracy
| Row | Driving-level measure in the record read | Setting |
|---|---|---|
| P2-P1806 | traffic-rule violation rate; prior STOP-sign attacks: no system-level effect; SysAdv: violation rate up by around 70% | full AD pipeline with vehicle plant model (simulator not named in the abstract) |
| P2-P1807 | driving-safety performance metrics, decoupled from detection precision | stereo 3D detection, end-to-end evaluation framework |
| P2-P1808 | system-level success metrics that model spatial memorization | commercial traffic sign recognition, physical tests |
| P2-P1809 | vehicle crash rate around 95% (SlowTrack) against around 30% (earlier latency attacks) | Baidu Apollo with LGSVL, two scenarios; digital attack |
| P2-P1810 | time to leave the lane, as little as 1.3 s (preliminary) | one lane-keeping system; physical road patch |
| P2-P1811 | driving-level success objectives; right-turn failures; path hijacking | end-to-end driving in simulation; open code |
| P2-P1812 | chance, size and duration of steering-angle errors during a drive-by | steering models; digital and physical |
| P2-P1813 | crash into an undetected 3D-printed object; simulation safety assessment (results not read) | camera plus LiDAR fusion |
| P2-P1825 | steering-angle deviation up to 23.06 degrees digital, up to 19.17 degrees real | steering models |
| P2-P1803 | attack detector also judged online, end to end at runtime | regression models; digital attacks |
Other tasks: AD2 (P2-P507, driving scores in CARLA closed loop), VisionGuard (P2-P512, LGSVL and CARLA), SlowPerception (P2-P525, collision rate), LanEvil++ (P2-P241, closed-loop lane perception). Measures in use: violation rate, crash or collision rate, time to lane departure, steering deviation. None of the records read scores an attack detector by false alarms per hour of benign driving at the decision level, to our knowledge.

### Q2. Simulators and benchmarks that can inject patches, shadows or light effects
| Platform | What it injects, per the record read | Licence stated in a record |
|---|---|---|
| CARLA (P2-P1814) | configurable sensors and environmental conditions; attacks are added by the studies below | abstract: open-source code and assets that "can be used freely"; licence names not stated |
| LGSVL (P2-P1815) | full-stack simulation hooked to Autoware and Apollo; custom sensors, controllable objects | not stated |
| PASS (P2-P1805) | system-driven safety and security evaluation (title only) | not stated |
| DCI pipeline (P2-P1801) | three physical attacks on vehicles in CARLA, static and continuous scenes, weather | not stated |
| AttackScenes (P2-P1819) | virtual 3D scenes for comparing camouflage attacks | not stated |
| DTA (P2-P1826) and Nesti et al. (P2-P1818) | vehicle camouflage rendered in CARLA; billboard patches optimised in CARLA | not stated |
| CARLA-GeAR (P2-P544) and PADetBench (P2-P543), LIT_A5 | patches on billboards and truck backs with clean clones; 20 physical attack methods under weather, view and distance control | PADetBench MIT per the README read by LIT_A5; CARLA-GeAR not read |
| LanEvil++ (P2-P241), LIT_A2 | natural illusions including shadows and reflections, lane perception | not read |
| REAP (P2-P1816) | patches on over 14,000 real sign images with geometric and lighting transforms (digital on real images) | not stated; Mapillary Vistas terms apply |
| APRICOT (P2-P1817) | photographs of printed patches (physical) | not stated |
Patches, billboards and camouflage textures are covered. Shadows and reflections appear only for lane perception (LanEvil++). No record read injects projected, reflected or laser light attacks into a driving simulator, to our knowledge. Only PADetBench has a licence stated in a record seen; the rest is NEEDS_VERIFY.

### Q3. Attacks that work digitally and fail physically
- Classifier era: a large fraction of adversarial images still fooled a classifier through a phone camera (P2-P1820); photos at varied distances and angles were mostly classified correctly, which the authors put down to sensitivity to viewing scale (P2-P1822); physical stop signs that fooled a crop-and-classify proxy did not fool YOLO or Faster R-CNN (P2-P1823).
- Attackers' answer: optimisation over transformation distributions (P2-P1821) and its detector form (P2-P1824); learned digital-to-physical models (print-and-capture translation P2-P1802, renderer imitation P2-P1826); GAN-generated physical examples (P2-P1825).
- Later measurements still find a gap: notably lower real-world effectiveness for segmentation patches (P2-P1818); digital-simulation success not predictive of realistic success (P2-P1816); adversarial strength hard to keep in uncontrolled settings (P2-P1817); reliable success on certain commercial functions but much lower overall (P2-P1808); no system-level effect for prior STOP-sign attacks, with physically inconsistent object sizes in pixel sampling named as one cause (P2-P1806); steering deviation up to 23.06 degrees digital and up to 19.17 degrees real (P2-P1825).
- In simulation, DCI (P2-P1801) reports an average AP drop of 6.59% for YOLO v6 and of 14.51% under the ASA attack, and its authors suggest attack advances may be near a limit.

## Closest prior work to the owner's design slides (ranked)
1. P2-P1804 (VehicleSec 2024 WIP): detecting object-evasion attacks on YOLO in simulated driving contexts. Closest in setting to slides 01 and 05 and to card X9-C1; title-level reading only, so its metrics and simulator are unknown.
2. P2-P1806 and P2-P1807: the system-level evaluation template card X9-C1 would reuse for detectors; they measure attacks, not detectors.
3. P2-P1817 (APRICOT): physical photographs with anomaly-detection baselines that flag patches; the closest physical-data evaluation of a slide 01 style detector.
4. P2-P1803 (MAKE 2023): an attack detector judged online, end to end at runtime; digital attacks on regression models.
5. P2-P1816 (REAP) and P2-P1818: realistic and three-stage attack evaluation for card X9-C2; they measure attacks, not detectors.

## Gaps and what is left to test (to our knowledge, from the records read)
- Decision-level scoring of attack detectors: alarm before the reaction point and false alarms per hour of benign driving, against frame-level TPR at matched FPR (card X9-C1).
- Detector transfer across digital, transformation-robust and physical renderings of the same attack (card X9-C2).
- Simulator injection of light attacks (projected, reflected, laser) and of matched benign look-alikes (card X9-C3); whether simulated light matches real camera response is untested in the records read.
- Closed-loop feedback: the lane-keeping attack (P2-P1810) has to handle dependence between consecutive frames; if that dependence runs through the vehicle's own motion (full text needed), replaying fixed video cannot reproduce it, and an offline evaluation in Paper 2 would miss it.
- Latency attacks (P2-P1809; P2-P525) make the timing of an added detector stage part of the attack surface.

## Datasets, benchmarks and code seen
| Item | Row | Location as read | Licence |
|---|---|---|---|
| CARLA | P2-P1814 | open source per the abstract; location not read | NEEDS_VERIFY |
| LGSVL | P2-P1815 | not read | NEEDS_VERIFY |
| PASS | P2-P1805 | not read | NEEDS_VERIFY |
| DCI dataset | P2-P1801 | not read | NEEDS_VERIFY |
| REAP benchmark | P2-P1816 | github.com/wagner-group/reap-benchmark (arXiv abstract) | not read; Mapillary Vistas terms |
| APRICOT | P2-P1817 | not read | NEEDS_VERIFY |
| UPC code and AttackScenes | P2-P1819 | mesunhlf.github.io/index_physical.html (arXiv abstract) | not read |
| AdverseDrive code | P2-P1811 | github.com/xz-group/AdverseDrive (arXiv abstract) | not read |
| Cityscapes; Mapillary Vistas | P2-P1818; P2-P1816 | named in abstracts | not read |

Note for the coordinator: Crossref confirms journal versions of two LIT_A5 rows whose DOIs were marked not Crossref-verified. CARLA-GeAR (P2-P544): IEEE Transactions on Intelligent Transportation Systems 2024, DOI 10.1109/tits.2024.3412432, Crossref title "CARLA-GeAR: A Dataset Generator for a Systematic Evaluation of Adversarial Robustness of Deep Learning Vision Models". PADetBench (P2-P543): Knowledge-Based Systems 2025, DOI 10.1016/j.knosys.2025.114395, Crossref title "PADetBench: Towards benchmarking texture- and patch-based physical attacks against object detection". Both records are in work/LIT_X9/verify_ledger.jsonl.

## Leads not confirmed
Tried: Crossref title search (host stopped after call 35), websearch (5 of 5 empty). Rows keep the records that were read.
1. A peer-reviewed USENIX Security 2021 version of P2-P1810 (dirty road patches): recalled, not confirmed.
2. ICML 2018 version of P2-P1821: recalled, not confirmed.
3. ICLR 2017 workshop version of P2-P1820: recalled, not confirmed.
4. CoRL 2017 version of P2-P1814 (CARLA): recalled, not confirmed.
5. Licences of CARLA code and assets and of LGSVL, and whether LGSVL is still maintained: recalled, not read; NEEDS_VERIFY.

## Problem map (attack families seen from the system level, with the papers that define them)
| Family | What changes for the driving task | Rows |
|---|---|---|
| Object evasion against signs and objects, judged at system level | A missed STOP sign or object matters only if the plan changes before the vehicle can still react | P2-P1806, P2-P1807, P2-P1808 |
| Perception latency attacks | Extra detections or tracker work delay the output, so a correct detection arrives too late | P2-P1809 (digital); SlowPerception P2-P525 (physical, LIT_A5) |
| Attacks on driving functions through road surface or roadside content | Painted road marks, dirty-road patches or billboards steer lane keeping or end-to-end models | P2-P1810, P2-P1811, P2-P1812, P2-P1825 |
| Physical objects against fused camera and LiDAR perception | A printed 3D object is missed by both sensors, so fusion gives no second opinion | P2-P1813 |
| Transformation-robust physical attacks (the digital-to-physical bridge) | Attacks optimised over viewpoint, lighting, print and camera changes so that they survive capture | P2-P1802, P2-P1820, P2-P1821, P2-P1824, P2-P1825, P2-P1826 |

## Solution map (evaluation and detection routes seen from this angle)
| Route | Rows |
|---|---|
| System-level measurement studies and platforms | P2-P1805, P2-P1806, P2-P1807, P2-P1808 |
| Simulators and scenario generators that place attacks in driving scenes | P2-P1801, P2-P1814, P2-P1815, P2-P1819; CARLA-GeAR P2-P544 and PADetBench P2-P543 (LIT_A5); LanEvil++ P2-P241 (LIT_A2) |
| Benchmarks and datasets of physical attacks on real images | P2-P1816, P2-P1817, P2-P1818 |
| Attack detectors judged in a driving loop | P2-P1803, P2-P1804; AD2 P2-P507 and VisionGuard P2-P512 (LIT_A5) |
| Studies that measure the digital-to-physical gap | P2-P1806, P2-P1808, P2-P1816, P2-P1817, P2-P1818, P2-P1820, P2-P1822, P2-P1823 |

## Problem cards (hypotheses, not results; house layout of state/DECK_DIGEST.md section 3)

### X9-C1 A per-frame alarm score does not say whether the drive was protected (all slides, evaluation)
- Problem: attack detectors are scored per frame (TPR at a fixed FPR), but one system-level measurement found that the representative published STOP-sign evasion attacks left the driving outcome unchanged, and another found detection-level damage and driving-safety damage decoupled; a frame-level ranking of detectors may therefore not match their value on the road.
- Contribution to test: H: scoring the owner's consistency check at the decision level (alarm raised before the last point where the vehicle can still react, false alarms per hour on benign drives) ranks detector variants differently from frame-level TPR at matched FPR. Prior work covers system-level evaluation of attacks (P2-P1806, P2-P1808, platform P2-P1805) and of detection precision versus driving safety (P2-P1807); detectors judged inside a driving loop exist (P2-P1803, P2-P1804; AD2 P2-P507 and VisionGuard P2-P512 from LIT_A5). A matched-FPR comparison of frame-level and decision-level rankings for the same detectors was not seen in the records read, to our knowledge.
- Open-source starting point: CARLA (P2-P1814) with patch placement as in CARLA-GeAR (P2-P544) or PADetBench pipelines (P2-P543); a frozen YOLO-family detector and tracker; a simple kinematic stopping model in place of a full planner, following the plant-model idea of P2-P1806.
- Data and laptop fit: rendering CARLA sequences on the 6 GB laptop GPU is a fit question to measure first (low quality preset, reduced resolution, offline rendering; CPU-only detection replay afterwards). Licence question: CARLA code and asset licences and the terms of any generated data must be recorded before release (not stated in the records read).
- Experiment workflow: (1) render approach sequences toward signs with and without physical-style patches, plus benign look-alikes (tree shadows, glare), at fixed seeds and held-out routes; (2) run frozen detector, tracker and cue check per frame; (3) compute frame-level TPR at fixed FPR and run-level outcomes (alarm before the reaction point, false alarms per hour of benign driving); (4) compare the detector rankings under both measures.
- Success measure: rank agreement between frame-level and decision-level scores across detector variants; warning margin in seconds before the reaction point at matched false alarms per hour.
- Sources: P2-P1803, P2-P1804, P2-P1805, P2-P1806, P2-P1807, P2-P1808, P2-P1814.

### X9-C2 A detector tuned on pasted or rendered attacks may not transfer to printed ones (slides 01 and 05, data)
- Problem: attack strength changes between digital, simulated and physical settings (the gap papers of family X9-F3), so a detector tuned on pasted or rendered attacks may key on rendering artefacts and miss printed attacks, or flag artefacts in benign renders.
- Contribution to test: H: the cue-consistency check keeps its TPR at a fixed FPR within a set margin across three renderings of the same attack: digital paste, transformation-robust rendering (expectation over transformation or a learned print-and-capture model), and real photographs. The gap papers read measure attack success, not detector transfer; APRICOT (P2-P1817) tests patch flagging on physical photographs only. A detector compared across the three renderings was not seen in the records read, to our knowledge.
- Open-source starting point: REAP (P2-P1816) for patches on real sign images, APRICOT (P2-P1817) for photographs of printed patches, the transformation sampling of P2-P1821 and the print-and-capture model idea of P2-P1802.
- Data and laptop fit: still images and short clips; fits the CPU and the 6 GB GPU. Licence question: APRICOT and REAP terms, and the base imagery REAP builds on, are not stated in the records read and must be checked before use.
- Experiment workflow: (1) build matched attack sets for the same sign classes in the three renderings; (2) run the frozen detector and the cue check; (3) report TPR at fixed FPR per rendering on one shared benign set; (4) list the cues whose values shift between renderings.
- Success measure: drop in TPR at fixed FPR from digital to physical rendering; share of alarms whose explanation names the same cue across renderings.
- Sources: P2-P1802, P2-P1816, P2-P1817, P2-P1818, P2-P1821, P2-P1824.

### X9-C3 Simulation benchmarks inject patches, rarely light, and never the matched benign look-alike (slides 02 to 04, data)
- Problem: the platforms read inject patches and textures (P2-P1801, P2-P1819, P2-P544, P2-P543) and natural shadows or reflections for lane perception (LanEvil++, P2-P241 from LIT_A2), but none of the records read injects projected or reflected light attacks. Clean clones of attacked scenes exist (P2-P544, P2-P543); a matched benign look-alike per attack (a natural shadow for a crafted one, glare for a light pattern) for false-alarm measurement was not seen.
- Contribution to test: H: a scripted simulator scenario set with light-pattern and shadow attacks plus matched benign look-alikes (tree shadows, headlight glare, wet-road reflections) predicts the false alarms per hour that the owner's cue checks show on real benign night clips. Whether the renderer reproduces projector or laser light faithfully is itself a gap question.
- Open-source starting point: CARLA (P2-P1814) weather and lighting controls; scenario generators of P2-P544 and P2-P543.
- Data and laptop fit: as X9-C1; the real benign comparison uses BDD100K night clips (licence question as on the deck).
- Experiment workflow: (1) define attack and look-alike scene parameters; (2) render with fixed seeds and held-out maps; (3) run the cue checks; (4) compare simulated and real false alarms per hour on benign material.
- Success measure: false alarms per hour on look-alikes; recall on light and shadow attacks; gap between simulated and real benign false-alarm rates.
- Sources: P2-P1801, P2-P1814, P2-P1815, P2-P1818, P2-P1819, P2-P1826.

## Exclusions
| Record seen (Crossref) | Reason not catalogued |
|---|---|
| ML-Driven Malware that Targets AV Safety (DSN 2020, 10.1109/dsn48063.2020.00030) | Attack vector is malware inside the vehicle software, not a physical visual attack; outside the Paper 2 subject |
| Adversarial Attack Detection for Deep Learning Driving Maneuver Classifiers in Connected Autonomous Vehicles (ICCCN 2024) | Manoeuvre classifiers on connected-vehicle data, not camera-based detection |
| WIP: On Robustness of Lane Detection Models to Physical-World Adversarial Attacks (AutoSec 2022) | Lane detection follow-up; the lane-centering system-level study is kept as the one lane example |
| Demo records of catalogued papers (VehicleSec 2024 demos of the ICCV 2023 system-level study and of SlowTrack; VehicleSec 2023 demo of tracker hijacking; AutoSec 2021 copy of the SPW 2021 demo) | Duplicates of main papers |
| CarFree (Applied Sciences 2021) and two CARLA object-detection papers (ICOSEC 2021, ICECCT 2021) | CARLA data generation or detection without attacks |
| LLM-Attacker closed-loop adversarial scenario generation (T-ITS 2025, supplement record only) | Adversarial traffic agents, not visual perception attacks |
| Lima (SSRN 2025), attack-space GAN for traffic signs (SSRN 2024), AE-Sign (CIML 2026), traffic-sign attack demonstration (ICCE-Taiwan 2025) | Attack generation without a system-level or simulation angle; cue-family scope of LIT_A1 and LIT_X12 |
| AlphaDog (NDSS 2025), adversarial translucent patch (Pattern Analysis and Applications 2025), UAV patch attack (IROS 2023) | Attack methods outside this angle; UAV imagery outside scope |
| Adversarial Driving: Attacking End-to-End Autonomous Driving (IV 2023) | Digital real-time perturbation of an end-to-end model, not a physical attack |
| Dissertation records (Security and Robustness of Autonomous Driving Systems Against Physical Adversarial Attack; noise-based defenses) | No year or venue in the record; theses not catalogued |
| Adversarial Imaging Pipelines (CVPR 2021, 10.1109/cvpr46437.2021.01579) | Crossref record without abstract; camera-pipeline attacks belong to the lighting family of LIT_A4 |
| SITAR, traffic light recognition in Level-4 driving (IV 2024); Human Drivers' Situation Awareness under physical-world attacks (VehicleSec 2023); Driving into Danger, patch attack on end-to-end driving (ISCC 2023); Demo: Security of Camera-based Perception under Adversarial Attack (SPW 2021); Demo: A Simulator for Cooperative and Automated Driving Security (AutoSec 2022) | Crossref title-level records only, no abstract; relevance to the three questions not established from the record read; candidates for a later pass |
| Towards Benchmarking and Assessing Visual Naturalness of Physical World Adversarial Attacks (CVPR 2023) | Naturalness to human observers, not system-level effect or simulation |
| Physical Hijacking Attacks against Object Trackers (CCS 2022); Seeing isn't Believing (CCS 2019) | Already catalogued by LIT_A5 (P2-P521) and LIT_X11 (P2-P2004) |
| Patch-feature energy defense (ACM MM 2022); blinding patch (Information Sciences 2021); Adversarial Camera Patch (ICCWS 2024) | Defense or attack methods inside the cue-family tasks, no system-level or simulation angle |
