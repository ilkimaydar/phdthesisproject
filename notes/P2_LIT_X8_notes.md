# P2_LIT_X8 notes - evaluation methodology for attack detectors

Status: written by the LIT_X8 worker agent. NOT AUDITED: writer's own work; a fresh-agent audit is required. Nothing here is a result of ours; every card states a hypothesis.

## 0. Status, read depth and limits

- Rows: 26 in work/LIT_X8/rows.jsonl (X8-F1 8, X8-F2 6, X8-F3 2, X8-F4 10), one above the target of 25. Verification states are computed by scripts/rows_check.py; see catalog/P2_LIT_X8_catalog.csv.
- Read depth: abstracts only for 25 rows (arXiv API or Crossref record), metadata-only for 1 row (P2-P1724). No full text was read. Statements about the body of a paper are labelled as memory leads or as not read.
- Search route: websearch answered "No search results found" to both calls made, so no websearch result was read in this run (section 8.4). Candidates came from memory leads confirmed through scripts/lit_verify.py (arXiv id batches, Crossref DOI lookups, Crossref title and topic searches) and from 5 arXiv keyword searches before the arXiv host was stopped.
- Cross-references of the form "LIT_A5 row P2-P510" point to staging rows of other tasks as read in work/LIT_A*/rows.jsonl during this run. They are those agents' paraphrases, not re-read by this task, and those files were still changing.
- Uncomfortable findings first:
  1. The evaluation stance of the slide footer (matched false-alarm operating points, adaptive testing) is established practice, not a contribution: fixed-FPR reporting before and after a defense-aware attack already exists for digital detectors (P2-P1715), and guideline papers demand adaptive evaluation (P2-P1701, P2-P1702, P2-P1711).
  2. Consistency checks have published evasion attacks: context-consistency checks are bypassed by attacks that keep the checked relation satisfied (P2-P1717; ADC, LIT_A5 row P2-P516), and control-based intrusion detection on robotic vehicles, including three real vehicles, was evaded by stealthy attacks (P2-P1726).
  3. Detection is not an easy shortcut: ten detectors were bypassed in one study (P2-P1711), four detection defenses fell to a joint-constraint attack (P2-P1713), and a reduction ties robust detection to robust classification (P2-P1714).
  4. Fusing several weak checks did not resist an adaptive adversary (P2-P1712), and explanations can be attacked together with the prediction (P2-P1716). Both hit slide 05 and the explanation branch of every slide.

## 1. Problem map (evaluation failure modes and the papers that define them)

| No. | Problem | Defining rows | Note |
|---|---|---|---|
| E1 | Detector tested only against attacks that ignore it | P2-P1711, P2-P1713, P2-P1715, P2-P1702 | Attacker adds the detector to the objective or mimics benign statistics |
| E2 | Attack failure caused by the evaluation (masked gradients, weak or mis-tuned attacks) | P2-P1703, P2-P1707, P2-P1704, P2-P1708 | Applies strongly to OpenCV-style cue pipelines, which are not differentiable (inference) |
| E3 | Consistency check evaded by keeping the checked relation satisfied | P2-P1717, P2-P1726; LIT_A5 row P2-P516 (same paper as LIT_A1 row P2-P127) | Shown for object-context checks on static images and for control-based monitors on robotic vehicles |
| E4 | Several weak checks combined and assumed strong | P2-P1712 | Direct warning for multi-cue fusion |
| E5 | Explanation manipulated together with the prediction | P2-P1716 | Saliency-type interpreters on classifiers |
| E6 | Threat model abstract, unstated or unrealistic | P2-P1706, P2-P1710 | Physical attacker constraints (access, line of sight, cost) must be written down |
| E7 | Wrong operating point or ignored base rate | P2-P1718, P2-P1719; LIT_A5 row P2-P514 (baselines at unequal false-positive rates) | Average metrics hide the low false-alarm region |
| E8 | Sequence-level scoring artefacts; delay ignored | P2-P1721, P2-P1720 | One flagged frame credited as a whole detected segment |
| E9 | Benign conditions break the detector without any attack | P2-P1722, P2-P1723 | Detector failure alone is not an attack signal |
| E10 | General pitfalls of learning-based security evaluation | P2-P1705 | Pitfall names are in the body, not read |
| E11 | Claims larger than the state of the art allows | P2-P1714 | Sanity check on detection claims |

## 2. Solution map (evaluation practices and tools)

| No. | Practice | Rows | Limits seen |
|---|---|---|---|
| S1 | Guideline checklist for defense evaluation | P2-P1701, P2-P1709 | Checklist items not read in this run |
| S2 | Methodology for building an adaptive attack per defense | P2-P1702, P2-P1711, P2-P1713 | Digital classifier setting |
| S3 | Parameter-free attack ensemble; automatic indicators of attack failure; gradient-free attacks | P2-P1704, P2-P1708, P2-P1707 | Norm-bounded attacks; no physical setting in the abstracts |
| S4 | Theoretical sanity check of detection claims | P2-P1714 | Norm-bounded; logic transfers by inference only |
| S5 | Operating-point reporting: TPR at a fixed low FPR; same point before and after the adaptive attack; worst case across attacks at a fixed threshold | P2-P1719, P2-P1715, P2-P1725 | P2-P1719 is from another task domain |
| S6 | False-alarm budget framing: base rate; detection delay under a false-alarm constraint; attacker impact while undetected | P2-P1718, P2-P1720, P2-P1724 | P2-P1724 not read (metadata-only) |
| S7 | Benign hard-negative sets with controlled conditions | P2-P1722, P2-P1723 | Simulated conditions and synthetic corruptions |
| S8 | Realistic, cost-aware threat models | P2-P1706, P2-P1710 | Position papers |
| S9 | Certified detection as an alternative to empirical adaptive tests | Verified lead PatchGuard++ (arXiv 2104.12609, not catalogued); LIT_A5 row P2-P519 (DetectorGuard) | Bounded patch on classification or static detection only |

## 3. Answers to the three questions of the brief

### 3.1 What the guideline papers require from a detection defense
Supported by the abstracts read (row ids in brackets):
1. Test against an attacker who knows the detector and targets it. All ten detectors studied were defeated by constructing new loss functions (P2-P1711); adaptive attacks are called the de facto standard, and adaptive evaluations done by defense authors were still incomplete for thirteen defenses (P2-P1702); the evasion target is an input that is misclassified and judged non-adversarial at once (P2-P1713).
2. Show that an attack failure is not an artefact of the evaluation: obfuscated gradients (P2-P1703), improper tuning of attack hyperparameters and gradient masking (P2-P1704), obscurity to the attack used, checked with gradient-free attacks (P2-P1707), automatic failure indicators (P2-P1708).
3. State the threat model in concrete terms: attacker motivations, constraints and abilities (P2-P1706); precise and cost-driven threat modelling (P2-P1710).
4. Report at a fixed false-positive operating point, before and after the adaptive attack (P2-P1715 uses TPR at 1% and 5% FPR); prefer TPR at low FPR over average metrics (P2-P1719); remember the base rate (P2-P1718).
5. For a detector with a reject threshold, attack the reject score itself and report the worst case across several attacks and restarts (P2-P1725).
6. Do not rely on stacking weak checks (P2-P1712).
7. Sanity-check the size of the claim against what robust classification achieves (P2-P1714).
8. Count the inference cost of test-time procedures as part of the evaluation (P2-P1709).
9. Avoid the general pitfalls of learning-based security evaluation (P2-P1705; the list itself was not read).
Not available from the abstracts: the item-by-item checklists of P2-P1701 and P2-P1711. A memory version is in section 7 (lead C1), UNVERIFIED.
Limit: every guideline row concerns norm-bounded digital attacks on image classifiers. To our knowledge (abstract-level reading in this task) none addresses physical attack detectors on video; transfer to the slides is our inference.

### 3.2 How an adaptive attacker would target a consistency check
Recipes in the records read:
| Recipe | Evidence | Read depth |
|---|---|---|
| Add the check to the attack objective | P2-P1711 (a loss per detector); ADC joint objective, LIT_A5 row P2-P516: above 85 percent fooling while bypassing the context check in over 80 percent of cases (figures as paraphrased in that row) | abstract; other task's row |
| Treat detector output and check as two simultaneous constraints | P2-P1713 (orthogonalised gradients; four detectors at 0% accuracy and 0% detection rate) | abstract |
| Plan the attack so the checked relation stays satisfied, with no query to the victim | P2-P1717 (context-consistent attack plans) | abstract |
| Mimic the benign statistics of the checked signal | P2-P1715 (logit mimicry; retraining on mimicry examples evaded again) | abstract |
| Get past non-differentiable or masked steps | P2-P1703; gradient-free search P2-P1707 | abstract |
| Attack all checks jointly | P2-P1712 | abstract |
| Attack the explanation as well | P2-P1716 | abstract |
| Make the manipulation robust over a distribution of viewing transformations | Verified lead arXiv 1707.07397 (expectation over transformations, 3D-printed objects), not catalogued; LIT_A5 row P2-P502 reports a temporal-consistency detector as almost unchanged under an adaptive attack of this type (authors' own evaluation per that row) | abstract; other task's row |
| Stay inside what the monitor accepts and still cause damage (stealthy attacker) | P2-P1726 (three stealthy attack types evade control-based intrusion detection on eight robotic vehicle systems, three of them real; missions deviate or crash); P2-P1724 | abstract for P2-P1726; metadata-only for P2-P1724 (memory lead C2) |

Per cue (hypotheses built from the recipes plus rows of other tasks; to our knowledge no record read in this task studies an adaptive attack on a shape, shadow, reflection or light check):
| Cue | Likely adaptive move | Supporting cross-reference (other tasks' rows, not re-read) |
|---|---|---|
| Shape, slide 01 | Keep the outer contour and class-typical edges intact and place the manipulation inside the sign face or off the object; optimise over viewpoints so no view-dependent mismatch remains | LIT_A1 progress log names an edge-patch attack and screen patches off the target as threats (leads of that task) |
| Shadow, slide 02 | Choose shadow shapes and motion that a real occluder could cast, so the plausibility gate passes | The slide's own critical failure case; LIT_A2 rows on shadow attacks |
| Reflection, slide 03 | Use reflected light that resembles benign glare and follows the expected view dependence | LIT_A3 row P2-P303 (triangle light patches that resemble natural glare) |
| Light, slide 04 | Model ambient brightness and exposure in the attack; time the light to the camera so the wrong output is stable | LIT_A4 rows P2-P434 (brightness-aware transformation model) and P2-P405 (emission timing adapted so the wrong class persists over frames) |
| Temporal, slide 05 | Keep the attack consistent across frames, or concentrate it in the few frames that matter | LIT_A3 row P2-P313 (authors argue frame-consistency defences have limited effect when the attack is consistent over most frames); LIT_A5 rows P2-P522 (persistent trajectory manipulation) and P2-P520 (one to three frames suffice for tracker hijacking) |
Reading: the common adaptive strategy is to make the attack satisfy the physical relation the check tests. The useful question for each slide is therefore the price of that constraint for the attacker (lost attack success, more equipment, less stealth), measured at a matched false-alarm point (card X8-1).

### 3.3 Which papers report false alarms per hour or per kilometre, and on what benign data
- Found in this task: none. To our knowledge, limited to the records this task could read.
- What was searched: (a) pattern scan of every staging row present in work/ (LIT_A1 to LIT_A5, LIT_X12) for per hour, per kilometre, per km, per mile, per minute: 0 hits outside this task's own rows; (b) arXiv keyword search "false alarms per hour autonomous driving perception": 1 record, arXiv 2610.07882 (title names CUSUM-governed alarms for off-road navigation; abstract not read; lead C8); (c) a second arXiv search on false alarms per hour in attack detection was not answered (host stopped); (d) one Crossref topic search on false alarms per hour or per kilometre in camera-based driver assistance: 6 records, none on driving (one 2026 preprint from underwater acoustic monitoring carries a false-positives-per-hour constraint in its title); (e) websearch: 2 calls, both answered "No search results found" (section 8.4), so the web was not searched.
- How the catalogued camera attack-detection papers measure false alarms instead (all figures as paraphrased in other tasks' rows):
| Row | Benign data | Reporting unit |
|---|---|---|
| LIT_A3 P2-P309 | 75 benign and 75 attack images per time of day | per-image true and false positive rate, day and night |
| LIT_A3 P2-P313 | 54 benign static images, 476 benign moving-vehicle images | F1 per setting |
| LIT_A3 P2-P312 | more than 180k images | true-negative and true-positive rate |
| LIT_A4 P2-P402 | authors' own sign crops | TPR at FPR 0 |
| LIT_A5 P2-P501 | 100 clean videos from BDD100K | accuracy, precision, recall; no fixed false-alarm point |
| LIT_A5 P2-P510 | real-world and simulated data | FPR 5 percent with TPR 99 percent |
| LIT_A5 P2-P512 | 30 benign physical videos | false positives in heavy rain, fog and one bumpy-road video |
| LIT_A5 P2-P514 | clips of nuScenes, KITTI, BDD100K | threshold set for under 5 percent benign false positives; baselines at unequal rates |
| LIT_A5 P2-P530 | trajectory benchmarks (not a camera attack setting) | delay at a mean-time-to-false-alarm constraint |
- Consequence: a per-hour or per-kilometre false-alarm figure on long benign driving video would be new relative to these rows (hypothesis, card X8-2). The claim needs a web search and full-text checks before it is written anywhere.
- Unread leads that may hold time-based or per-image false-alarm protocols: C3, C4, C5 and C8 in section 7.

## 4. Closest prior work to the owner's design slides (ranked for this task's angle: the evaluation stance)

| Rank | Row | Why it is close | What it leaves open |
|---|---|---|---|
| 1 | P2-P1715 | Same reporting format as the slide footer: one detector, fixed FPR, before and after a defense-aware attack | Digital, CIFAR-10 classifier logits |
| 2 | P2-P1717 (with ADC, LIT_A5 row P2-P516) | A consistency check is the attacked object; the attack keeps the relation consistent | Object-context relation on static images, not physical cues or video |
| 3 | P2-P1726 | A runtime monitor that uses control algorithms to check vehicle behaviour is evaded by stealthy attacks, also on real vehicles; nearest analogue found of a physics-gated check under an adaptive attacker (analogy is ours) | Sensors and actuators, not camera perception |
| 4 | P2-P1711, P2-P1713 | Standard proof that detectors fall to joint objectives | Digital |
| 5 | P2-P1712 | Fusion of weak checks tested and found not strong; the nearest published warning for slide 05 | Digital ensembles; names of the defenses not in the abstract |
| 6 | P2-P1716 | Flag-with-explanation designs attacked jointly | Saliency interpreters, not cue-level evidence |
| 7 | P2-P1718, P2-P1720, P2-P1724 | False-alarm budget as the governing quantity; delay under a false-alarm constraint; undetected impact | Other domains; P2-P1724 unread |
| 8 | LIT_A1 row P2-P143 (other task) | Unified evaluation of patch defenses on detectors with adaptive attacks, in the project's own domain; per that row adaptive attacks substantially bypass existing defenses | Not re-read here; patch defenses only |
| 9 | LIT_A5 rows P2-P510 and P2-P514 (other task) | Operating points and adaptive results reported for spatiotemporal consistency; one compares baselines at unequal false-positive rates | Not re-read here |

## 5. Gaps and what is left to test

1. To our knowledge (abstract-level reading), no published adaptive-attack study targets a shape, shadow, reflection or light consistency check for camera attack detection; the analogues are context checks (P2-P1717, ADC), control-based monitors on robotic vehicles (P2-P1726) and temporal checks (other tasks' rows).
2. No row in the project staging files reports false alarms per hour or per kilometre for a camera attack detector (section 3.3). Web search still needed.
3. Benign hard negatives are not standard in attack-detection test sets; the controlled-condition sign set found here is simulated (P2-P1722) and the corruption sets are synthetic single images (P2-P1723).
4. The guideline literature read is about norm-bounded digital attacks on classifiers. A guideline for physical attack detectors on video (event definition, per-hour alarms, delay, abstentions, physical attacker constraints) was not found in this task.
5. Event-level scoring rules for attack segments in video are unsettled; the point-adjustment problem (P2-P1721) shows how such rules can inflate results.
6. Comparison at matched false-alarm points is not uniform in the closest prior work (LIT_A5 row P2-P514).
7. Not checked in this task: any full text; the checklists of P2-P1701 and P2-P1711; the content of P2-P1724; published versions of 13 arXiv-only rows (venue leads V1 to V13; 3 further arXiv-only rows are labelled preprint); licences of all datasets named; code repositories (none opened); citation counts (no OpenAlex call).

## 6. Datasets, benchmarks and code seen (none opened; licences not checked)

| Item | Where named | Use for the project |
|---|---|---|
| CURE-TSD-Real, repository olivesgatech/CURE-TSD on GitHub | abstract of P2-P1722 | Sign detection video under controlled simulated conditions with metadata; benign hard negatives |
| CURE-TSR, more than two million sign images, site named in the abstract | arXiv 1712.02463 (verified lead, not catalogued) | Sign crops under challenging conditions for sign-level checks |
| Pascal-C, Coco-C, Cityscapes-C | abstract of P2-P1723 (public per the abstract, location not given) | Benign corruption sets for detectors |
| ImageNet-C and ImageNet-P | arXiv 1903.12261 (verified lead) | Common-corruption benchmark for classifiers; background only |
| ImageNet-A and ImageNet-O | arXiv 1907.07174 (verified lead) | Natural, unmodified hard images; conceptual hard-negative reference |
| IndicatorsOfAttackFailure, repository pralab/IndicatorsOfAttackFailure on GitHub | abstract of P2-P1708 | Debugging of gradient-based attack runs |
| RobustBench library and leaderboard | arXiv 2010.09670 (verified lead) | Classifier robustness leaderboard; background only |
| DoTA, 4,677 egocentric traffic anomaly videos, STAUC metric, repository named in the abstract | arXiv 2004.03044 (verified lead) | Example of a spatio-temporal detection metric for driving video; not attack data |
| Numenta Anomaly Benchmark | arXiv 1510.03336 (verified lead) | Scoring rule that rewards early detection and penalises false alarms on streams |
| APDE patch-defense benchmark | LIT_A1 row P2-P143 (other task) | Unified patch-defense evaluation with adaptive attacks |
Licence question for every dataset above: open. Record the licence before any download (deck rule).

## 7. Leads not confirmed

Content leads (from memory unless stated; UNVERIFIED until the full text is read):
- C1. Checklist content of P2-P1701 and P2-P1711: state a precise threat model; run adaptive attacks aimed at the defense; report clean accuracy and, for detectors, a ROC curve or TPR at a stated FPR; take the per-example worst case over attacks; add gradient-free and transfer attacks to expose masking; check that attacks converge and that an unbounded attack succeeds; release code. Tried: abstracts only; the abstracts do not list the items.
- C2. P2-P1724 proposes a metric that relates the damage a stealthy attacker can cause to an upper bound on false alarms (expected time between false alarms), and the companion survey (Giraldo et al., DOI 10.1145/3203245) recommends it. Tried: Crossref records (no abstract for P2-P1724; the survey abstract does not state the metric).
- C3. Gavrila and Munder, Multi-cue Pedestrian Detection and Tracking from a Moving Vehicle, International Journal of Computer Vision (DOI 10.1007/s11263-006-9038-7, Crossref record found): may report false classifications per minute for a vehicle-mounted system. Tried: Crossref (no abstract).
- C4. Dollar et al., Pedestrian Detection: An Evaluation of the State of the Art, IEEE TPAMI 2012 (DOI 10.1109/tpami.2011.155, Crossref record found): per-image false-positive evaluation protocol on long driving video. Tried: Crossref (no abstract).
- C5. Kalra and Paddock, Driving to safety: How many miles of driving would it take to demonstrate autonomous vehicle reliability?, Transportation Research Part A 2016 (DOI 10.1016/j.tra.2016.09.010, Crossref record found): statistics of demonstrating a low failure rate from driven distance, usable for sizing a benign test. Tried: Crossref (no abstract); figures not read.
- C6. Sommer and Paxson, Outside the Closed World: On Using Machine Learning for Network Intrusion Detection, IEEE S&P 2010 (DOI 10.1109/sp.2010.25, Crossref record found): guidance on the cost of false positives for anomaly detectors. Tried: Crossref (no abstract).
- C7. Feature Squeezing (arXiv 1704.01155, record found) is one of the combined defenses broken in P2-P1712; MagNet bypass (arXiv 1711.08478, record found). Tried: abstracts; the P2-P1712 abstract does not name the defenses.
- C8. arXiv 2610.07882, CUSP: CUSUM-Governed Survival Hazard Alarms at the Perception Onset for Off-Road Navigation (record found by keyword search): may report alarms under a false-alarm budget in a perception setting. Abstract not read; arXiv host stopped.
- C9. arXiv 2505.12586, A Few Large Shifts: Layer-Inconsistency Based Minimal Overhead Adversarial Example Detection (record found by keyword search): a recent low-overhead detector; evaluation practice not read.
- C10. Shen et al., Constructive Noise Defeats Adversarial Noise: Adversarial Example Detection for Commercial DNN Services, NDSS 2026 (DOI 10.14722/ndss.2026.230250, record found as a side hit of a Crossref title search): recent detection paper; evaluation practice not read.
- C11. Li et al., WIP: Adversarial Object-Evasion Attack Detection in Autonomous Driving Contexts: A Simulation-Based Investigation Using YOLO, Symposium on Vehicle Security and Privacy 2024 (DOI 10.14722/vehiclesec.2024.23059, Crossref record found, no abstract): detection of object-evasion attacks in simulation; how it measures false alarms is not read. In the scope of LIT_A1 and LIT_A5.
- C12. Dash et al., Out of control, Annual Computer Security Applications Conference 2019 (DOI 10.1145/3359789.3359847, Crossref record found, no abstract): earlier conference version of P2-P1726; whether its content differs was not read.
Venue leads (memory; the rows carry venue "arXiv preprint" and peer_review "unknown" until a record confirms them):
- V1 P2-P1702 NeurIPS 2020. V2 P2-P1703 ICML 2018. V3 P2-P1704 ICML 2020. V4 P2-P1705 USENIX Security 2022. V5 P2-P1707 ICML 2018. V6 P2-P1708 NeurIPS 2022. V7 P2-P1709 ICML 2022. V8 P2-P1712 USENIX WOOT 2017. V9 P2-P1713 ICLR 2022. V10 P2-P1714 ICML 2022. V11 P2-P1716 USENIX Security 2020. V12 P2-P1723 NeurIPS 2019 workshop. V13 P2-P1725 ICML 2020.
- Venue leads confirmed during the run through Crossref and now in the rows: P2-P1710, P2-P1717, P2-P1719, P2-P1720, P2-P1721, P2-P1722.
Count: 12 content leads and 13 venue leads.

## 8. Exclusions and items verified but not catalogued

### 8.1 Verified in the ledger, not catalogued because the row target was reached (candidates for promotion)
- Hussain et al., Reconstruction-Based Adversarial Attack Detection in Vision-Based Autonomous Driving Systems, Machine Learning and Knowledge Extraction 2023, DOI 10.3390/make5040080: autoencoder-based detector for perturbation attacks on regression models of driving systems; the abstract reports a true positive rate of 93% and names an online evaluation framework, with no false-positive figure in the abstract. Medium; an example of a detection rate reported without its operating point.
- Aldahdooh et al., Adversarial example detection for DNN models: a review and experimental comparison, Artificial Intelligence Review 2022, DOI 10.1007/s10462-021-10125-w, arXiv 2105.00203: experimental comparison of eight detectors on four datasets (abstract). Medium.
- Lorenz et al., arXiv 2112.01601: strong standard attacks are easy to detect, other attacks with similar success are much harder (abstract). Medium; a caution for detection benchmarks.
- Guerin et al., arXiv 2211.16158 (AAAI 2023 per the arXiv record): monitors should be judged on discarding incorrect predictions, not on out-of-distribution detection (abstract). Medium; likely in LIT_X13 scope.
- Xiang et al., PatchGuard++, arXiv 2104.12609: provable attack detection for patches (abstract). Medium; patch family belongs to LIT_A1.
- Athalye et al., Synthesizing Robust Adversarial Examples, arXiv 1707.07397. Medium; attack core list of LIT_A1.
- Lu et al., arXiv 1707.03501: physical adversarial signs did not disrupt detection from a moving platform over distances and angles (abstract, 2017). Medium; evaluation over an approach sequence.
- Hendrycks et al., Natural Adversarial Examples, arXiv 1907.07174. Medium.
- Giraldo et al., ACM Computing Surveys, DOI 10.1145/3203245 (folded into the notes of P2-P1724).
- Cai et al., Context-Aware Transfer Attacks for Object Detection, arXiv 2112.03223 (folded into the notes of P2-P1717).
- Temel et al., CURE-TSR, arXiv 1712.02463 (folded into the notes of P2-P1722).
- Kalra and Paddock, Dollar et al., Sommer and Paxson, Gavrila and Munder: Crossref records found, no abstract read (leads C3 to C6).

### 8.2 Excluded as outside the subject or Low relevance
- RobustBench, arXiv 2010.09670: classifier leaderboard; Low for this project.
- Hendrycks and Dietterich, arXiv 1903.12261: classifier corruption benchmark; covered for detection by P2-P1723.
- Kapoor and Narayanan, Leakage and the Reproducibility Crisis in ML-based Science, arXiv 2207.07048: general ML methodology outside the subject; supports the split-by-recording rule only by analogy.
- Lavin and Ahmad (Numenta Anomaly Benchmark), arXiv 1510.03336, and Yao et al. (DoTA), arXiv 2004.03044: generic stream or traffic-anomaly evaluation, not attack detection; kept in section 6 only.
- Feature Squeezing, arXiv 1704.01155, and the MagNet bypass, arXiv 1711.08478: detector and bypass from the digital classifier literature; no evaluation point beyond P2-P1711 and P2-P1712.
- Side hits of keyword, title and topic searches with no relation to the subject or outside this task's angle: a deepfake detection paper, a multi-agent reinforcement learning paper for cyber-physical security, a 2014 traffic sign detection paper, three quickest-change-detection papers on energy constraints, a 2026 zero-query attack paper on detectors (title only), an attack on anomaly detection in industrial systems, an audio adversarial-example paper, two aerial-imagery patch attack papers, a dissertation on noise-based defenses, a 2025 survey of defenses for object detection (LIT_X1 scope), records from forensic testing and underwater acoustic monitoring, supplementary-file and figure records.
- Segment and Complete and Segment and Recover (returned by a topic search): already LIT_A1 rows or leads, not rebuilt here.
- Patch attack papers returned by the arXiv keyword search (ShapeShifter and two 2026 transferable-patch preprints): core list of LIT_A1, not rebuilt here.

### 8.3 Scope notes
- Rows P2-P1718, P2-P1719, P2-P1720, P2-P1721, P2-P1724 and P2-P1726 come from other domains (intrusion detection, privacy attacks, change detection, time-series anomaly detection, industrial control, robotic vehicles). They are catalogued for the evaluation method only, as the task brief asks, and each row says so.
- SoK and system-level evaluation papers for autonomous-driving security were left to LIT_X1 and LIT_X9.

### 8.4 Tool notes for this run
- websearch: 2 calls, both answered with the text "No search results found" and no limit text: one topical query (false alarms or false positives per hour in physical attack detection for driving cameras) and one control query naming a well-known paper (P2-P1701). The tool was therefore treated as not working in this run and not called again. Progress logs of other agents report the same and one quota text for this network. Result: no web discovery and no abstract reading through search snippets. Both calls are Q lines in progress/LIT_X8.log.
- arXiv API: STOP_HOST (shared stop after an earlier 4xx or bot check) on the sixth keyword search; not called again. No written row was affected.
- Crossref: 3 lookup calls with 12 DOIs, 8 title searches and 4 topic searches, all answered. The topic searches (adaptive attacks evading consistency-based detection in autonomous driving; adaptive attacks against patch-detection defenses; false alarms per hour or per kilometre in camera-based driver assistance; false positives of adversarial-example detectors on naturally corrupted images) returned no paper on an adaptive attack against a camera consistency check and none on time-based false alarms in driving; side hits are in sections 7, 8.1 and 8.2. Crossref searches match titles, so this is weak evidence of absence.
- Calls used: lit_verify 25 of 50, websearch 2 of 40.

## 9. Problem cards (hypotheses, not results)

### Card X8-1 - The detector is only tested against attacks that ignore it
- Problem: a consistency check that flags known attacks may fail once the attacker optimises against the check itself; published detectors were bypassed this way.
- Contribution to test: a check-aware evaluation protocol for each cue (shape, shadow, reflection, light, temporal). With the alarm threshold fixed on held-out benign recordings, the attacker searches for manipulations that change the frozen detector output while the cue residual stays under the threshold. Reported: attack recall at the fixed false-alarm point before and after, and the largest detector damage reachable without an alarm.
- Prior work already covering it: the protocol elements exist for digital classifier detectors (P2-P1711, P2-P1713, P2-P1715), for context checks (P2-P1717; ADC in LIT_A5) and for control-based monitors on robotic vehicles (P2-P1726). To our knowledge (abstract-level reading) it has not been applied to physical cue checks. The protocol itself is not a contribution; the measured price of consistency for the attacker would be.
- Open-source starting point: no attack code was confirmed in this task. The repository named in P2-P1708 (not opened) targets gradient-attack debugging. Check-aware search over few physical parameters can be written as gradient-free search with restarts (P2-P1707); official attack code is inventoried by LIT_X3.
- Data and laptop fit: digital simulation only. Attack parameters are low-dimensional (shadow polygon, light spot position and colour, patch placement), so each query is one forward pass of a small frozen detector plus OpenCV cue extraction; expected to fit the 10-core CPU, 32 GB RAM and the 6 GB GPU, to be confirmed by a measured fit test (deck rule). Licence question: the base sign and driving data (for example GTSRB, LISA, BDD100K, CURE-TSD) must have their licences recorded before download. Physical validation is outside the laptop scope and must be stated as a limitation.
- Experiment workflow: (1) freeze detector, cue check and threshold on held-out benign recordings at a stated false-alarm point; (2) run attacks that ignore the check and record recall; (3) run check-aware attacks: joint constraint, gradient-free search with restarts, plus failure checks of the attack run in the sense of P2-P1708; (4) report recall at the fixed point before and after, the undetected-damage curve, and the worst case over attacks per clip (P2-P1725).
- Success measure: change in attack recall at the matched false-alarm point between check-ignoring and check-aware attacks, and the detector damage left to an undetected attacker. A bypass at no cost is a valid, reportable outcome.
- Sources: P2-P1701, P2-P1702, P2-P1703, P2-P1707, P2-P1708, P2-P1711, P2-P1713, P2-P1715, P2-P1717, P2-P1724 (not read), P2-P1725, P2-P1726.

### Card X8-2 - Per-frame false-positive rates hide the alarm burden of real driving
- Problem: the catalogued detection papers report false positives per image, frame or video on small benign sets; with rare attacks, the number of alarms per hour of ordinary driving and its uncertainty stay unknown.
- Contribution to test: an event-level false-alarm protocol. Alarm events per hour on long held-out benign recordings, by condition (day, night, rain), with a confidence interval; all detectors compared at one matched alarm budget; detection delay reported under that budget.
- Prior work already covering it: the base-rate argument (P2-P1718), reporting at low false-positive rates (P2-P1719), delay under a false-alarm constraint (P2-P1720), scoring pitfalls for segments (P2-P1721), and an autonomous-driving example with a mean-time-to-false-alarm constraint outside camera attacks (LIT_A5 row P2-P530). To our knowledge no camera attack-detection row in the project staging files reports alarms per hour (section 3.3); this needs a web search before it is claimed.
- Open-source starting point: none confirmed. The protocol is a scoring script over cached per-frame scores (own code, Python standard library).
- Data and laptop fit: long benign video is needed; the deck names BDD100K video and ACDC. Scoring is CPU-only and threshold sweeps run on cached scores. The benign hours needed follow from the target alarm rate and a binomial or Poisson bound, to be fixed in the analysis plan (the question posed in the title of lead C5). Licence question: BDD100K and ACDC terms must be recorded before download (LIT_X2 scope).
- Experiment workflow: (1) define an alarm event (merge rule, refractory time) before any result is seen; (2) calibrate thresholds on a calibration split of benign recordings, split by recording; (3) run on held-out benign recordings by condition and on attack clips, count alarm events per hour and detection delay; (4) compare detectors at the matched alarm budget and add random-score and untrained baselines (P2-P1721).
- Success measure: alarms per hour with interval on held-out benign video by condition; attack recall and delay at the matched budget; count of abstentions and of clips with no usable evidence.
- Sources: P2-P1705, P2-P1718, P2-P1719, P2-P1720, P2-P1721.

### Card X8-3 - Benign look-alikes are missing from the test set
- Problem: detectors fail without any attack under corruptions, weather and challenging sign conditions, so a consistency check tuned on clean data may alarm on benign hard cases; benign sets in attack papers are small.
- Contribution to test: a benign hard-negative suite per cue (controlled-condition sign video, corruption sets, natural shadows, glare and exposure jumps collected by the other tasks), with false alarms reported per condition and severity and with benign detector failures counted separately from attacks.
- Prior work already covering it: controlled challenging conditions with metadata for sign detection (P2-P1722) and corruption benchmarks for detectors (P2-P1723). Neither contains attacks or cue-specific look-alikes. Natural shadow, glare and night sets belong to LIT_A2 to LIT_A4, LIT_X2 and LIT_X7.
- Open-source starting point: the CURE-TSD repository named in the abstract of P2-P1722 (not opened); corruption benchmark code is public per the abstract of P2-P1723 (location not confirmed).
- Data and laptop fit: dataset sizes are not in the abstracts; check size and licence before download and start with a subset by condition and level (deck rule: CPU baselines and frozen features first, expand after a measured fit test). Corruption generation runs on the CPU.
- Experiment workflow: (1) record licences and sizes, choose a subset by condition and level; (2) run the frozen detector and mark frames where it fails without an attack; (3) run each cue check and count alarms per condition and level, separately for detector-failure frames and detector-correct frames; (4) recalibrate per condition if needed and report the cost in attack recall at the matched budget.
- Success measure: false alarms per condition and severity at the matched budget; share of benign detector failures wrongly flagged as attacks; abstention counts.
- Sources: P2-P1705, P2-P1718, P2-P1722, P2-P1723.

### Card X8-4 - Fusing cues and showing explanations may add attack surface
- Problem: combining several weak checks is not automatically strong, and the explanation shown with a flag can be manipulated together with the prediction.
- Contribution to test: (a) a joint adaptive attack against the fused multi-cue score compared with each single cue, to see whether fusion raises the attacker's cost at a matched false-alarm point; (b) explanation faithfulness under attack: whether the flagged region and cue still point at the manipulated region when the attacker optimises against the explanation.
- Prior work already covering it: ensembles of weak defenses broken by an adaptive adversary (P2-P1712, digital classifiers); joint attacks on prediction and interpretation (P2-P1716, saliency interpreters). To our knowledge (abstract-level reading) not on physical multi-cue detectors with cue-level explanations. Explanation evaluation is LIT_X4 scope.
- Open-source starting point: none confirmed in this task.
- Data and laptop fit: same simulation set-up as card X8-1; fusion is logistic regression or boosting on cached cue scores (deck route A), CPU-only. Licence question as in card X8-1.
- Experiment workflow: (1) train single-cue and fused scores on cached cue features, split by recording; (2) attack each single cue and the fusion with the same check-aware search budget (P2-P1713); (3) compare attack recall at the matched false-alarm point and the detector damage left to the attacker; (4) on flagged attack clips measure the overlap between the explained region and the true manipulated region, before and after an explanation-aware attack.
- Success measure: gain of fusion over the best single cue under the joint attack at matched false alarms (zero gain is a valid outcome); explanation localisation accuracy under attack.
- Sources: P2-P1702, P2-P1712, P2-P1713, P2-P1716.
