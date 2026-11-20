# P2 LIT_X13 notes - runtime monitoring of perception (X13-F1 to X13-F3)

Status: writer's own work, not audited. 25 rows in work/LIT_X13/rows.jsonl (P2-P2201 to P2-P2225): 18 read at abstract level, 7 metadata-only (title-level; no abstract read). No full text read. Families: X13-F1 16 rows, X13-F2 7, X13-F3 2. Every statement below comes from the abstract or record named; where it is this agent's reading, it says so. "To our knowledge" means: within these 25 rows and the other tasks' staging rows grepped during this run.

## 0. Uncomfortable findings first
1. The monitoring literature already has cheap monitors that sit beside a frozen network or detector and raise alarms on missed traffic signs (P2-P2204), on window-level performance drops of a detector (P2-P2205) and on out-of-distribution objects (P2-P2209, P2-P2210). Adding physical attacks to their target list is a small step, and one of them, SAFE (P2-P2210), already trains its detector monitor on adversarially perturbed samples. A reviewer from this community may read the slides' "frozen detector plus checker" as a known monitor architecture with a new input.
2. One feature-statistics score already detects both out-of-distribution and adversarial inputs (P2-P2215, classifiers, digital attacks). Feature monitors are the natural baseline any physical-cue checker must beat at the same false-alarm rate (card M1).
3. Guerin et al. (P2-P2208) show that good out-of-distribution scores can give a false impression of safety, because what matters is whether a monitor discards wrong predictions. The same objection applies to attack detectors scored only on attacked versus clean inputs (card M2).
4. A system-level monitor for perception with fault detection, fault identification, guarantees and negligible overhead exists for an autonomous-driving stack (P2-P2206, simulator only). Identification of the faulty module is a form of explanation, which overlaps with contribution 6 at the module level.
5. Runtime detectors for physical adversarial inputs already exist in other tasks' rows (Kantaros et al., LIT_A1 P2-P147 and LIT_A5 P2-P505; video version P2-P504; ego-motion state machine P2-P512). The runtime-monitoring framing is therefore not new for attacks; what this task adds is the monitor families, the evaluation frameworks and the safety framing around them.

## 1. Problem map
This task's angle is monitoring, so the map lists the failure families monitors are built for. Attack families themselves are defined in the LIT_A1 to LIT_A5 rows.

| Failure family a monitor targets | Rows that define it here | Is a physical attack inside it? |
|---|---|---|
| Silent misses of a detector (false negatives, hidden or discarded objects) | P2-P2204 (missed traffic signs), P2-P2205 (window-level drop of detection quality) | Not tested in the abstracts; attacks that hide a sign produce exactly this failure |
| Inputs not covered by training (novel classes, out-of-distribution objects) | P2-P2201, P2-P2202, P2-P2203, P2-P2209, P2-P2210, P2-P2211, P2-P2216; survey P2-P2212 | Digital perturbations only, as test target (P2-P2215) or as surrogate training data (P2-P2210) |
| Faults across perception modules | P2-P2206 | Not discussed in the abstract |
| Misbehaviour of the whole driving system, predicted ahead of time | P2-P2214 (abstract), P2-P2224 and P2-P2225 (title-level) | Injected anomalous contexts, not attacks (P2-P2214) |
| Deep-learning perception weaknesses as safety concerns | P2-P2217, P2-P2218 | Not stated in the abstracts |

## 2. Solution map
| Monitor family | Mechanism (from the abstracts) | Rows |
|---|---|---|
| Activation-abstraction monitors | Stored activation patterns with a Hamming-distance test; per-neuron boxes from training values; active updating with human labels; extension to object detectors | P2-P2201, P2-P2202, P2-P2203, P2-P2209; title-level P2-P2213, P2-P2222, P2-P2223 |
| Feature-statistics monitors | Class-conditional Gaussians on intermediate features scored by Mahalanobis distance | P2-P2215 |
| Learned introspection on detector features | Second network on internal features of a frozen detector: missed-sign alarm, sliding-window mAP prediction, per-object MLP trained on clean versus adversarially perturbed samples | P2-P2204, P2-P2205, P2-P2210 |
| System-level diagnosis | Diagnostic graph over perception modules; deterministic, probabilistic and learned fault detection and identification | P2-P2206 |
| Input reconstruction and time series | Autoencoder reconstruction plus time-series anomaly detection to predict misbehaviour seconds ahead | P2-P2214; title-level P2-P2224 (uncertainty), P2-P2225 (attention maps) |
| Training-time shaping of detectors | Virtual outliers sampled in feature space plus an unknown-aware loss (needs retraining) | P2-P2216 |
| Zero-cost OOD for automotive classification | Replacement of softmax confidence with no added inference cost, meant to trigger a fallback | P2-P2211 |
| Evaluation frameworks | Safety Gain, Residual Hazard, Availability Cost; out-of-model-scope instead of OOD; surveys organised by threat, requirement, detection, reaction, evaluation | P2-P2207, P2-P2208, P2-P2219; title-level P2-P2220, P2-P2221 |
| Safety-standard framing | Safety concerns of deep-learning perception and their mitigations, aligned with ISO 21448 and informing ISO PAS 8800 | P2-P2217, P2-P2218 |

## 3. Closest prior work to the owner's design slides (ranked)
Shared pipeline of all five slides: frozen detector, independent cue, consistency check, calibrated decision with explanation or abstain.
1. P2-P2206 (Antonante et al., Artificial Intelligence 2023): diagnostic information across perception modules is used to detect faults and identify the faulty module, with guarantees and negligible overhead, tested in LGSVL with Apollo. Closest to the consistency-check-plus-explanation shape at system level. Whether its diagnostic tests are cross-module consistency checks is this agent's expectation, not read. Faults, not attacks.
2. P2-P2204 (Rahman et al., IROS 2019): alarm on a frozen traffic-sign detector's features when a sign was missed; at 80% recall, 89.9% precision on the Belgian dataset and 90.8% on GTSRB (abstract). Closest to contribution 2 and to slide 01's frozen sign detector. Natural misses only, no physical cue, no explanation.
3. P2-P2210 (SAFE, ICCV 2023): per-object features of a frozen detector plus an MLP trained on clean versus adversarially perturbed samples. Same per-object, frozen-detector layout as the slides; trained with digital perturbations and aimed at OOD objects.
4. P2-P2205 (Rahman et al., IROS 2021): sliding-window prediction of detector mAP from internal features. Window-level analogue of slide 05; no cause located.
5. P2-P2215 (Lee et al., 2018 preprint record): one Mahalanobis score for OOD and adversarial inputs. Baseline for any feature-level comparison.
6. P2-P2207 and P2-P2208 (Guerin et al.): evaluation, not detection; they change how the slides' "matched false-alarm" rule should be read (card M2).
Outside this task's rows and closer to attacks: Kantaros et al. runtime detectors (P2-P147, P2-P505), VG* (P2-P504), VisionGuard (P2-P512), conformal plus CUSUM detection of deception attacks on camera sequences (P2-P534).

## 4. Gaps and what is left to test
1. To our knowledge, no monitor in these 25 rows is evaluated on physical patch, shadow, reflected-light or projected-light attacks against a detector. Since other tasks' rows hold runtime detectors for physical inputs, the open point is narrower: feature monitors from this literature (P2-P2201, P2-P2202, P2-P2210, P2-P2215) have not, to our knowledge, been compared with physical-cue checks on the same physical-attack recordings at a matched false-alarm rate (card M1).
2. Alarm rates per hour of driving: none of the 18 abstracts read reports them; metrics are precision at fixed recall, FPR95, predicted mAP, share of misbehaviours predicted and lead time. Consistent with LIT_X8 notes section 3.3.
3. Harm-based scoring (Safety Gain, Residual Hazard, Availability Cost; out-of-model-scope) has not, to our knowledge, been applied to physical-attack detectors (card M2).
4. Missed-object monitors are trained and tested on natural misses; attack-induced misses may also remove the internal evidence those monitors read (card M3).
5. Explanation: monitors here output an unmatched pattern, a predicted score or a faulty module; none in these rows names a physical cause such as a shadow or glare. The slides' cue-level explanation is the part not covered here.
6. Safety framing: the F3 search was cut short (section 9). Whether SOTIF-aligned safety concerns include malicious inputs, and how ISO 21448 and the automotive cybersecurity standard divide physical attacks on perception, is not answered by any record read.

## 5. Answers to the brief's three questions
1. How monitors are evaluated, and on what data:
   - Operating-point metrics: precision at 80% recall for missed-sign alarms on the Belgian traffic-sign detection set and GTSRB (P2-P2204); FPR95 on OOD object-detection benchmarks including OpenImages (P2-P2210, P2-P2216); share of misclassifications flagged at a small false-positive rate (P2-P2201); tunable false-warning trade-offs (P2-P2202).
   - Window-level: predicted mAP over a sliding window of frames on driving datasets (P2-P2205).
   - Lead time: 77% of misbehaviours predicted, up to 6 seconds ahead, in the Udacity simulator (P2-P2214).
   - System level: failure modes recreated in LGSVL with Apollo (P2-P2206).
   - Safety-oriented: Safety Gain, Residual Hazard, Availability Cost across classification, drone landing and driving use cases (P2-P2207); discarding wrong predictions instead of OOD detection (P2-P2208).
   - Alarms per hour of driving: not found in the abstracts read.
2. Which monitors are light enough for embedded use:
   - Stated in abstracts: no added inference cost (P2-P2211); negligible computational overhead (P2-P2206); efficient (P2-P2202). Implied by the mechanism but without a figure: Hamming-distance pattern lookup (P2-P2201), class-mean distances (P2-P2215), an MLP on per-object features of a frozen detector (P2-P2210).
   - No abstract read gives latency or memory on embedded hardware. VOS (P2-P2216) needs detector retraining, which conflicts with the frozen-detector design.
   - The online-applicability attribute of the anomaly survey (P2-P2212) and the design factors of P2-P2219 are the next reads for a cost comparison.
3. Where the monitoring literature already treats adversarial inputs:
   - P2-P2215: one score for OOD and adversarial samples (classifiers, digital attacks).
   - P2-P2210: adversarial perturbations used to train a detector OOD monitor (attacks as training signal, not as test target).
   - P2-P2213: provably-robust activation monitoring (title-level; what the robustness covers was not read).
   - Other tasks: runtime detectors for physical adversarial inputs (P2-P147, P2-P505, P2-P504, P2-P512), deception-attack detection with conformal scores and CUSUM (P2-P534), and stealthy attacks that evade control-based monitors on robotic vehicles (P2-P1726).

## 6. Datasets, benchmarks and code seen
- Belgium Traffic Sign Detection dataset and GTSRB (P2-P2204). Licences not checked here; LIT_X2 notes record conflicting licence tags for GTSRB.
- OpenImages as an OOD object-detection benchmark (P2-P2210).
- LGSVL simulator with Baidu Apollo Auto (P2-P2206); Udacity driving simulator (P2-P2214).
- Code: VOS at github.com/deeplearning-wisc/vos, named in the abstract, not opened (UNVERIFIED). No other code location appeared in the records read.

## 7. Problem cards
Ranking criteria: fit to the red-marked focus (lightweight, explainable, the five cue families), laptop feasibility, measurability, novelty margin against verified prior work. Order: M1 (direct baseline question every slide faces), M3 (contribution 2, small data need), M2 (evaluation, cheap, but a methods point rather than a detector).

### Card M1 - Feature monitors versus physical-cue checks on the same attacks
- Problem: cheap feature monitors already run beside frozen detectors, but it is unknown whether they flag physical patch, shadow or light attacks, so the added value of a physical cue is unmeasured.
- Contribution to test: on held-out physical-attack recordings, a physical-cue consistency residual reaches higher attack recall than a feature monitor (Mahalanobis distance or box abstraction on detector features) at the same benign false-alarm rate, and the two combined beat each alone. It fails if the feature monitor already catches the attacks.
- Prior coverage: P2-P2215 covers OOD plus digital attacks on classifiers; P2-P2210 trains a detector OOD monitor on adversarial perturbations; runtime detectors for physical inputs exist (P2-P147, P2-P505). To our knowledge the head-to-head comparison on physical attacks against detectors is not reported.
- Open-source starting point: YOLOX-Nano frozen; PyTorch forward hooks for per-object features; NumPy and scikit-learn for Gaussian fits and per-neuron intervals; OpenCV for the cue residual.
- Data and laptop fit: physical-attack images and videos catalogued by LIT_A1 to LIT_A5 (for example AdvNet, named in P2-P505, location not seen); benign driving video (BDD100K named on the deck). Licence question: each set's terms must be recorded before download. Feature caching fits the 6 GB GPU or CPU; monitors fit on CPU.
- Experiment workflow: (1) cache per-object features and cue residuals for benign and attack recordings, split by recording; (2) fit the feature monitors on benign training recordings only; (3) set every threshold for the same false-alarm rate on a benign calibration split; (4) compare attack recall, delay in frames, ms per frame and the combination.
- Success measure: attack recall per attack family at matched benign false alarms, plus alarms per hour on long benign clips and p95 added latency.
- Sources: P2-P2215, P2-P2210, P2-P2202, P2-P2201, P2-P2209; other tasks: P2-P147, P2-P505.

### Card M2 - Score attack flags by the harm they prevent
- Problem: attack detectors are scored on attacked versus clean inputs, yet an attack that leaves the detector output unchanged causes no harm and a benign condition that hides a sign does; the OOD lesson of P2-P2208 suggests such scoring can mislead.
- Contribution to test: the ranking of candidate detectors (detector confidence only, feature monitor, physical-cue check) changes when they are scored with Safety Gain, Residual Hazard and Availability Cost on detector-error labels instead of ROC on attack labels. It fails if the two rankings agree.
- Prior coverage: P2-P2207 defines the metrics; P2-P2208 shows ranking changes for OOD monitors. To our knowledge not applied to physical-attack detectors.
- Open-source starting point: the P2-P2207 metric definitions written as a short Python module; scikit-learn metrics; cached outputs of card M1.
- Data and laptop fit: same recordings as card M1 plus ground-truth boxes to label detector errors; CPU only; licence questions as card M1.
- Experiment workflow: (1) label each object and frame for attack presence and for detector error (missed, false, wrong class); (2) score each candidate by ROC on attack labels; (3) score by the three safety metrics with return functions stated explicitly; (4) compare rankings and report attacks that caused no detector error separately.
- Success measure: rank agreement between the two scorings, the count of disagreeing frames, and Residual Hazard at matched Availability Cost.
- Sources: P2-P2207, P2-P2208, P2-P2219, P2-P2204.

### Card M3 - Missed-sign alarm under physical attack
- Problem: a missed-sign alarm built on a frozen detector's features works for natural misses, but stickers, shadows or light that hide a sign may also suppress the internal evidence the alarm reads.
- Contribution to test: an alarm trained on natural misses loses recall on attack-induced misses, and adding a detector-independent cue (sign shape and colour evidence, slide 01) restores recall at the same false-alarm rate. It fails if the alarm already transfers to attack-induced misses.
- Prior coverage: P2-P2204 (natural misses; 89.9% and 90.8% precision at 80% recall on two sign datasets, abstract) and P2-P2205 (window-level performance). To our knowledge not tested on attack-induced misses.
- Open-source starting point: a frozen sign detector (YOLOX-Nano trained once on a public sign set, or an SSD as in P2-P2204); a small MLP alarm in scikit-learn; OpenCV contour and colour cues.
- Data and laptop fit: GTSRB and the Belgian detection set for natural misses (licence question open, see LIT_X2); physical-attack sign images from the LIT_A1 rows; alarm training on CPU, feature caching on the 6 GB GPU.
- Experiment workflow: (1) reproduce a false-negative alarm on natural misses; (2) create attack-induced misses with the physical attack sets; (3) measure alarm recall on both kinds of misses at a fixed benign false-alarm rate; (4) add the independent cue, repeat, and count abstentions where the cue is unreliable.
- Success measure: recall on attack-induced misses at matched false alarms; precision at 80% recall for comparison with P2-P2204; added ms per frame.
- Sources: P2-P2204, P2-P2205, P2-P2201.

## 8. Leads not confirmed (10)
1. Detection Latency as a Constraint on the Architectural Complexity of Real-Time AI-based Adversarial Detectors (SSRN posted content 2026, DOI 10.2139/ssrn.7042279): Crossref record seen in a title search; content and domain not read, so relevance is unknown; not catalogued.
2. Unifying Runtime Monitoring Approaches for Safety-Critical Machine Learning: Application to Vision-Based Landing (Lecture Notes in Computer Science, 2026 or 2027, DOI 10.1007/978-3-032-31666-0_40): Crossref record seen; its first-author field reads like a given name; aviation use case; content not read.
3. Papers on SOTIF triggering conditions for camera perception: one Crossref topic search hit a shared stop; websearch returned nothing; none confirmed.
4. Whether ISO 21448 leaves malicious attacks to the automotive cybersecurity standard: agent's background expectation; no standard text or record read.
5. ISO PAS 8800: named in the P2-P2218 abstract; the standard was not read.
6. A benchmark of safety monitors for image classifiers (memory lead, Ferreira and co-authors, about 2021): not searched, both hosts stopped.
7. An activation-based framework that flags anomalous operation of deep networks including adversarial inputs (memory lead, name FACER, about 2020): not searched.
8. Learned monitors for operational design domains of camera perception (memory lead, Torfah and co-authors, about 2022): not searched.
9. Online SOTIF risk quantification for driving (memory lead, "SOTIF entropy", about 2022 to 2023): not searched.
10. Safety analysis methods for perceptual components in automated driving (memory lead, Salay, Czarnecki and co-authors, about 2019): not searched.
Failed lookup (not a lead): an arXiv id tried from memory for ThirdEye (P2-P2225) returned an unrelated mathematics paper; that id is not used anywhere.

## 9. Exclusions
Side hits of the title searches, not catalogued (reason in brackets):
- A survey on machine learning for robotic emotion monitoring, Applied Sciences 2022 (outside the subject).
- A book prologue on emerging trends in machine learning, 2020 (outside the subject).
- A dissertation on Thai traffic sign classification (classification only, no monitoring or attacks).
- A 2011 paper on false-alarm filtering in a vision traffic sign recognition system with AdaBoost and texture (pre-deep-learning recognizer; Low).
- The doctoral thesis record whose author family name matches the Rahman monitoring papers (the papers themselves are catalogued).
- Towards Dependability Metrics for Neural Networks, MEMOCODE 2018 (metric definitions, not a runtime monitor; Low).
- Evaluating Merging Strategies for Sampling-based Uncertainty Techniques in Object Detection, ICRA 2019 (uncertainty estimation: LIT_X6 angle).
- Hyperdimensional Feature Fusion for Out-of-Distribution Detection, WACV 2023 (classifier OOD: LIT_X6 angle).
- Gaussian-Based Runtime Detection of Out-of-distribution Inputs for Neural Networks, RV 2021 (classifier-level predecessor of P2-P2209; not a separate row).
- How Do We Fail? Stress Testing Perception in Autonomous Vehicles, IROS 2022 (offline stress testing, not runtime monitoring; may serve a triggering-condition or simulation angle).
- Multimodal Detection of Unknown Objects on Roads for Autonomous Driving, SMC 2022, and a 2022 anomaly experiment with forward-backward style transfers (multimodal or exploratory; Low for a camera attack angle).
- SiMOOD: Evolutionary Testing Simulation With Out-Of-Distribution Images, PRDC 2022 (testing, not runtime monitoring; Low).
- An indoor air-quality OOD poster, a spatiotemporal occupancy-prediction paper, an avionics visual-programming paper, a UAV construction-safety paper and a 2023 textbook chapter on test-time evasion attacks (outside the subject or generic).
- Duplicate records of catalogued work: the AAAI 2024 abstract reprint of P2-P2206, the IROS 2021 precursor of P2-P2206, the 2023 journal extension of P2-P2203, the WACV Workshops 2021 companion of P2-P2205 (DOIs in the row notes).
No instruction-like text was seen in any record read.

## 10. Overlap with other tasks (not rebuilt here)
- Kantaros et al., real-time detectors for digital and physical adversarial inputs (ICCPS 2021): LIT_A1 P2-P147 and LIT_A5 P2-P505; video extension LIT_A5 P2-P504.
- Klingner et al., detecting adversarial perturbations in multi-task perception (IROS 2022): LIT_X11 P2-P2018.
- Cai et al. 2023, real-time detection of deception attacks in cyber-physical systems: LIT_A5 P2-P534.
- Runtime OOD monitors with calibrated false alarms (2020, CODiT 2023, inductive conformal assurance monitoring 2021): LIT_X6 P2-P1509, P2-P1510, P2-P1512.
- Sequential tests for perception monitoring: LIT_A5 P2-P529, P2-P530, P2-P533.
- Over-activation analysis of physical patches (Z-Mask, AAAI 2023): LIT_X14 P2-P2323; attention-based multi-frame defense: LIT_A5 P2-P508 and LIT_X5 P2-P1414.
- Control-based runtime monitors evaded by stealthy attacks on robotic vehicles: LIT_X8 P2-P1726.

## 11. Search record
- websearch: 5 calls, all answered "No search results found"; the web was not searched.
- Crossref: 16 title searches answered (query strings in work/LIT_X13/query_log.tsv); the 17th call, a SOTIF topic query, and the 18th met a shared stop (HTTP 429 set by another agent). No further Crossref call in this run.
- arXiv: calls made only after the coordinator's shared stop expired; 2 id-list lookups (18 ids; 17 matched their leads, 1 id from memory was wrong) and 1 title search answered; the 4th call met a new shared stop. No further arXiv call.
- lit_verify calls: 22 of 50. websearch calls: 5 of 40. OpenAlex citation call skipped (budget kept; Crossref cited-by counts are in the ledger).
- Family shortfall: X13-F3 has 2 rows, because the SOTIF searches were cut off by the host stops and empty websearch.
