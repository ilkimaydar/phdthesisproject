# P2 LIT_X10 notes - cross-sensor, multi-view and context consistency

Status: written by the LIT_X10 worker agent (continuation run). NOT AUDITED: a fresh-agent audit is required. Rows: work/LIT_X10/rows.jsonl (P2-P1901 to P2-P1918), catalog/P2_LIT_X10_catalog.csv. Verification states are computed by scripts/rows_check.py from work/LIT_X10/verify_ledger.jsonl.

Counts: 18 rows (VERIFIED 12, ARXIV_API_VERIFIED 6); High 6, Medium 12; X10-F1 9, X10-F2 7, X10-F3 2. Read depth: 12 abstract, 6 metadata-only. No full text read. Every number below comes from the abstract of the row named, or from another task's row where that row is named; nothing here is an independent measurement.

Run limits that shaped the result: websearch returned nothing for 4 of 4 queries; Crossref was under a shared stop written at 23:49:47Z after a 429 that this agent did not receive, and was not called again; arXiv answered 429 to the third search call at 00:07Z, so arXiv was closed for the rest of the run. F3 (map and context) is thin for this reason, and the absence of a record is weak evidence, not proof that no such work exists.

## Uncomfortable findings first

1. Consistency checks are themselves a target. A frustum attack keeps camera and LiDAR semantics consistent and stays stealthy to the existing spoofing defenses it was tested against (P2-P1911). A patch placed in 3D so that it stays consistent across cameras and frames is benchmarked against BEV detectors (P2-P1917). One 3D-printed object attacks camera and LiDAR at the same time (P2-P1906). Together with ADC (P2-P516, LIT_A5) and the zero-query context-consistent attacks (P2-P1717, LIT_X8), the pattern is the same in every family: an attacker who knows the checked relation keeps it true. Any cue residual on slides 01 to 05 needs an adaptive-attack test where the attacker preserves the cue.
2. Adding sensors does not remove the camera threat. Camera-only patches compromised six camera-LiDAR fusion detectors and one camera-only detector (P2-P1910); in a physically realisable multi-sensor attack the failures came mainly from easily corrupted image features (P2-P1909); a single attacked modality could override correct information from the other modalities in standard fusion (P2-P1908). A 2026 review catalogued by LIT_X1 calls this a redundancy paradox of fusion designs (P2-P1017, as recorded in that row). This supports the owner's camera-side focus.
3. The closest structural match to the slide pipeline in this family is a learned fusion layer that compares independent sources, detects the inconsistent one and passes only the consistent ones (P2-P1908). It needs a second modality and a retrained fusion model, and it was tested on digital worst-case perturbations, not physical attacks.

## Answers to the brief questions

### Q1. Which consistency defenses need extra sensors or maps, and their reported cost
| Defense (row) | Extra input needed | Cost stated in the record read |
|---|---|---|
| Robust fusion that detects the inconsistent modality (P2-P1908) | Second modality; retrained fusion model | None in the abstract (training is implied by the method) |
| Adversarial training of camera-LiDAR fusion (P2-P1907) | LiDAR plus adversarial training | Qualitative: single-channel training can hurt the other channel; joint training does not raise robustness significantly |
| Adversarial training with feature denoising (P2-P1909) | LiDAR plus training | None numeric; false positives from LiDAR-pixel association remain |
| Runtime monitor over a consistency graph of modules (P2-P1912) | Several redundant modules | None numeric; the number of detectable faulty modules is bounded |
| Collaborative anomaly detection (P2-P1913) | Other vehicles and V2X | 91.5% of attacks detected at a 3% false-positive rate in simulation |
| ROBOSAC consensus sampling (P2-P1914) | Several agents | Trade-off stated: more sampled teammates, more sampling time |
| MADE malicious agent detection (P2-P1915) | Collaborators | AP drop against an oracle 1.28% (V2X-Sim) and 0.34% (DAIR-V2X); false positives controlled by the Benjamini-Hochberg procedure |
| CP-Guard+ (P2-P1916), adversarial training plus consensus (P2-P1904) | Collaborators | Not read (title only) |
| Map matching plus sign recognition (P2-P1901); navigation plus vision for speed limits (P2-P1902) | Digital map and positioning | Not read (title only); non-adversarial work |
From other tasks, cited and not rebuilt: VisionGuard (CCS 2024) predicts ego motion from GPS and IMU (P2-P512, LIT_A5); PhyScout checks keypoints against predicted vehicle state (P2-P515); PhySense builds a 3D kinematic model and may use LiDAR attributes, not confirmed (P2-P1302, LIT_X4); traffic-light mapping gives a map prior for lights (P2-P2325, LIT_X14).
Gap: no abstract read in this family states per-frame latency or memory. A cost comparison between cross-sensor checks and a camera-only cue check cannot be made from these records.

### Q2. Which context-consistency methods work with one camera
None of the 18 rows of this task is a one-camera context check: the F3 rows need a map. One-camera methods found by other tasks, cited and not rebuilt:
- Context auto-encoders per object class flag objects that do not fit the scene (P2-P2019, LIT_X11); a language model of object co-occurrence does the same independently of the detector (P2-P126, LIT_A1). Both were tested on general multi-object image sets, and both have published evasion attacks (P2-P516, P2-P1717).
- Edge, depth and segmentation consistency inside one multi-task network, reported at an assumed 5% false-positive rate (P2-P2018, LIT_X11; abstract as recorded in that row).
- A committee of small CNNs judging light, context, surface and depth of a detected object, built against projected phantoms (P2-P402, LIT_A4).
- A vision-language check of a sign crop against class-label text (P2-P1305, LIT_X4).
- Track-based spatiotemporal plausibility plus ego-velocity context (P2-P510, LIT_A5); this needs ego speed, which a vehicle has anyway.
- Benign multi-frame input reduced attack effect on camera-based 3D detectors (P2-P1918), which supports temporal evidence in one camera.
Inference, not tested: a lone road sign offers little object co-occurrence context, so scene-context checks are weaker for signs than for cluttered scenes; the map prior (Q1) is the sign-specific context but it needs a map.

### Q3. What these papers say a single-camera check cannot do
The abstracts read do not make a direct statement about single-camera checks; they speak about fusion. What they support, with the inference marked:
1. A single camera has no independent physical measurement to compare with, so an attack that is physically consistent in the image (3D-consistent patch across views and time, P2-P1917) leaves no cross-view residual. Inference from P2-P1917 and P2-P1911.
2. With only a frozen detector and one cue, a disagreement shows that one of the two is wrong but not which. Diagnosability theory bounds the number of faulty modules a consistency graph can detect (P2-P1912); attributing a fault needs redundancy. Inference from the general theory, not read in the paper.
3. A camera-side check cannot stop an attack that hits all fused sources at once (P2-P1906), but neither can fusion. Conversely, fusion does not cover camera-only attacks (P2-P1910, P2-P1909), so the two are complements, not substitutes.
4. A 2025 perspective article on spatiotemporal consistency defenses lists their limits: telling attacks from sensor noise, occlusion and poor lighting, static thresholds, simulation versus real operation, and adaptive attackers (P2-P517, LIT_A5, as recorded in that row). These limits apply to a single-camera check as much as to multi-sensor ones.
5. From the owner's slide 03, outside this task: an IR-filtered RGB camera may not see an infrared attack. No row of this task covers that.

## Problem map (attack families and the papers that define them)
- A. Coordinated attack on all fused sources with one physical object: P2-P1906 (3D-printed object against camera and LiDAR); P2-P1909 (universal object on a car roof hides vehicles from LiDAR-image fusion).
- B. Single-modality attack that breaks fusion: P2-P1910 (camera-only patches against six fusion detectors); P2-P1908 (single-source adversaries across multimodal tasks); P2-P1907 (single-source attacks and training effects in camera-LiDAR fusion).
- C. Consistency-preserving attacks that evade cross-checks: P2-P1911 (frustum attack keeps camera-LiDAR semantics consistent); P2-P1917 (3D-consistent patch across views and time). Context analogues in other tasks: P2-P516 (ADC), P2-P1717 (zero-query context-consistent attack plans).
- D. Data fabrication by malicious collaborators: P2-P1913; threat models of P2-P1914, P2-P1915, P2-P1916, P2-P1904.
- E. Robustness of camera-based and BEV 3D detectors: P2-P1917, P2-P1918; P2-P1903 (title only).

## Solution map (defense and detection families)
- S1. Learned cross-modal inconsistency gating in fusion: P2-P1908. Adversarial training of fusion: P2-P1907, P2-P1909.
- S2. Runtime monitoring over a consistency graph of modules, with diagnosability bounds: P2-P1912.
- S3. Multi-agent consensus and malicious-agent detection: P2-P1914 (consensus sampling), P2-P1915 (hypothesis tests with false-positive control), P2-P1913 (joint anomaly detection), P2-P1916 and P2-P1904 (title only).
- S4. Map-prior fusion for sign recognition, non-adversarial: P2-P1901, P2-P1902; for traffic lights P2-P2325 (LIT_X14).
- S5. One-camera context and multi-task consistency (other tasks): P2-P2019, P2-P126, P2-P2018, P2-P402, P2-P1305, P2-P510.
- S6. Ego-motion and physical-state consistency using extra sensors (other tasks): P2-P512, P2-P515, P2-P1302.
- S7. Mining camera-LiDAR disagreements as a source of perception gaps: P2-P1905 (title only; preprint server unknown).

## Closest prior work to the owner's design slides (ranked)
1. P2-P1908, Yang et al., CVPR 2021: compares independent sources, detects the inconsistent one, and trusts only the consistent ones; the same logic as independent cue, consistency check and decision. Differs: second modality, retrained fusion, digital attacks, no abstain output in the abstract.
2. P2-P2018, Klingner et al., IROS 2022 (LIT_X11): one camera, cross-task edge consistency, fixed false-positive operating point. Differs: digital image-level perturbations, no per-object decision in the abstract.
3. P2-P402, Nassi et al., CCS 2020 (LIT_A4): one camera, committee over light, context, surface and depth of the detected object. Differs: built for projected phantoms; learned experts rather than physical residuals.
4. P2-P2019 and P2-P126 (LIT_X11, LIT_A1): one-image context consistency; evaded by P2-P516 and P2-P1717.
5. P2-P1915, Zhao et al., IROS 2024: consistency statistics turned into hypothesis tests with explicit false-positive control; a template for the decision stage at matched false alarms.
6. P2-P1912, Antonante et al., IROS 2021: formal monitoring and diagnosability; a frame for when the system must abstain.
7. P2-P1913, Zhang et al. (preprint record 2023): multi-view anomaly detection reported as detection rate at a fixed false-positive rate.
Threats to rank beside them: P2-P1911, P2-P1906, P2-P1917.

## Gaps and what is left to test
1. Adaptive attacks that preserve a cheap physical cue (contour, shadow, reflection, light) were not found in the records read; the analogues exist for scene context (P2-P516, P2-P1717), cross-sensor semantics (P2-P1911) and multi-view geometry (P2-P1917).
2. No record read evaluates a map prior as a detector of physical sign attacks. The search was cut short by host stops, so this is an open lead, not a confirmed gap.
3. No per-frame latency or memory figure was read for any cross-sensor, multi-agent or map-based consistency defense.
4. Calibrated false-positive control (P2-P1915) and the time-versus-assurance analysis of consensus sampling (P2-P1914) have not been seen applied to single-camera cue residuals, to our knowledge within the records read.
5. Attribution of a disagreement (attack versus cue failure) has theory (P2-P1912) but no attack evaluation in the abstract read.
6. Multi-frame benign evidence helps (P2-P1918) while 3D-consistent patches are built to survive view and time checks (P2-P1917); how this balance plays out for physical sign attacks in real video is untested here.

## Datasets, benchmarks and code seen
- V2X-Sim (simulated) and DAIR-V2X (real road), named in the MADE abstract (P2-P1915). V2X-Sim is also row P2-P2414 of DECK_SRC. Licences not read.
- Physical artefacts: 3D-printed adversarial objects captured by LiDAR and camera devices (P2-P1906).
- Code: the abstract of P2-P1910 says code is available; no location seen. No other code or data location was seen in the records read. code_or_data is empty on all 18 rows for this reason.
- No benchmark in this family combines physical camera attacks with a second sensor and benign look-alikes at matched false alarms, as far as the records read show.

## Problem cards
Ranking criteria: fit to the advisor's red focus (lightweight and explainable; the five cue families), laptop feasibility (10-core CPU, 32 GB RAM, 6 GB laptop GPU), measurability at matched false alarms, novelty margin against the closest verified prior work. Each card is a hypothesis, not a result.

### Card X10-C1 (rank 1) - A consistency residual that the attacker keeps true
- Problem: a cue residual (contour against box, shadow geometry, local light) flags an attack only if the attack breaks that relation; cross-sensor and context checks have already been evaded by attacks that keep the checked relation true.
- Contribution to test: under an adaptive patch attack that adds a penalty keeping one cue residual low, a residual built from two weakly correlated cheap cues loses less recall at a matched false-positive rate than either cue alone. The hypothesis fails if the combined residual drops as much as the best single cue, or if the attacker reaches the same success rate at no extra patch cost.
- Open-source starting point: a frozen small detector (YOLOX-Nano, as on the deck); OpenCV contour, edge and local-luminance features; scikit-learn logistic regression and calibration; a public patch-attack implementation, chosen later with its licence checked.
- Data and laptop fit: sign crops and clips from LISA, GTSRB or Mapillary (licence questions open; see notes/P2_LIT_X2_notes.md); cue features on CPU; patch optimisation on the 6 GB GPU at small input size, fit to be measured before scaling.
- Experiment workflow: (1) build each cue residual on clean signs and on standard patches; (2) build adaptive patches that also minimise one residual, following the evasion pattern of P2-P516 and P2-P1911; (3) measure recall at a matched false-positive rate for single and combined residuals; (4) report the attack success rate and patch area the attacker needed.
- Success measure: recall at matched false alarms under the adaptive attack, its drop from the non-adaptive case, ms per frame, and the extra attacker cost.
- Sources: P2-P1911, P2-P1917, P2-P1906; from other tasks P2-P516, P2-P1717. Prior work covers adaptive evasion of context and cross-sensor checks; no record read covers cheap physical-cue residuals of the slides.

### Card X10-C2 (rank 2) - One detector and one cue cannot say which one failed
- Problem: when the frozen detector and a single cue disagree, the cause may be an attack or a failing cue (night, glare, blur, occlusion); with two modules the disagreement cannot be attributed.
- Contribution to test: a per-condition cue-reliability estimate plus a third weak cue (temporal persistence of the detection) turns part of the disagreements into attributable decisions and lowers the abstain rate at a matched false-positive rate without lowering recall. The hypothesis fails if attribution accuracy does not exceed a reliability-only baseline.
- Open-source starting point: OpenCV cues; scikit-learn isotonic calibration; the diagnostic-graph idea of P2-P1912 as a design frame (no code seen); hypothesis-test thresholds with false-discovery control as in P2-P1915.
- Data and laptop fit: BDD100K night and adverse clips as benign confounders (licence question open), plus attacked sign clips made by the team; CPU only.
- Experiment workflow: (1) define two-module and three-module consistency graphs; (2) inject cue faults (glare, blur, exposure jumps) and attacks separately, with labels; (3) measure attribution accuracy and abstain rate; (4) compare at matched false alarms on held-out recordings.
- Success measure: share of disagreements correctly attributed, abstain rate and recall at matched false alarms, ms per frame.
- Sources: P2-P1912, P2-P1908, P2-P1915. P2-P1912 gives the theory without an attack evaluation in the abstract; P2-P1908 learns which source to trust but needs a second modality.

### Card X10-C3 (rank 3) - A map prior as an attack-independent check for signs
- Problem: a sticker or patch changes what the camera reads but not what a map stores for that location; driver-assistance work already fuses map and camera for speed limits, yet no record read uses this to detect attacks.
- Contribution to test: a map-versus-detector disagreement score for mapped stop and speed-limit signs flags physical sign attacks at a lower false-positive rate than an image-only detector, except at stale or unmapped signs. The hypothesis fails if benign map-camera disagreements (stale maps, temporary signs) alone exceed the false-alarm budget. Limits stated in advance: no help for unmapped signs, vanishing obstacles or projected phantoms; needs map and positioning, so it is a comparator for the camera-only design, not the main contribution.
- Open-source starting point: a frozen sign detector; open map sign tags (licence terms to read before use); GPS traces where a driving dataset provides them (availability and licence to check).
- Data and laptop fit: clips with positions plus mapped sign locations; CPU only; storage is the main cost.
- Experiment workflow: (1) align clips to mapped signs; (2) measure the benign disagreement rate per hour of driving; (3) apply sticker and patch attacks to mapped sign crops; (4) report detection at matched false alarms and the share of signs the map covers.
- Success measure: false alarms per hour from stale maps, recall on attacked mapped signs, map coverage.
- Sources: P2-P1901, P2-P1902; from other tasks P2-P2325. Both own sources are title-level reads of non-adversarial work. Outside the red focus, hence rank 3.

## Leads not confirmed
1. GCP: Guarded Collaborative Perception with Spatial-Temporal Aware Malicious Agent Detection (IEEE TDSC 2026): Crossref search returned only a supplementary-file record (10.1109/tdsc.2026.3693684/mm1); the article record was not read; Crossref then stopped.
2. DynamicPAE: Generating Scene-Aware Physical Adversarial Examples in Real-Time (IEEE TPAMI): only supplementary video records were returned (10.1109/tpami.2025.3626068/mm2, mm4, mm5). Relevant to F3 as a scene-aware attack on context checks; main record not read.
3. The earlier CP-Guard paper behind P2-P1916: arXiv search cut by the 429.
4. Map priors or HD maps used as detectors of physical sign attacks: one Crossref query returned only non-adversarial work; arXiv not searched.
5. Radar-camera and stereo or multi-camera consistency defenses inside one vehicle against physical camera attacks: one Crossref query each, nothing relevant; arXiv not searched.
6. Published venues recalled from memory for preprint rows, all UNVERIFIED: P2-P1909 (a robot-learning conference, 2021), P2-P1910 (a learning-representations conference, 2024), P2-P1911 (a security symposium, 2022), P2-P1913 (a security symposium, 2024), P2-P1917 (a vision conference, 2023), P2-P1918 (a machine-learning journal). Check the published versions before citing.
7. Code repositories for P2-P1906, P2-P1910, P2-P1913, P2-P1914, P2-P1917 and P2-P1918 are believed to exist (memory); no location was seen, so none is written in the rows.
8. Dissertation record Security and Robustness of Autonomous Driving Systems Against Physical Adversarial Attack (Crossref, no year): not read.

## Exclusions
- Already catalogued by other tasks, cited not rebuilt: P2-P2018 and P2-P2019 (LIT_X11); P2-P126 and P2-P127 (LIT_A1); P2-P510, P2-P512, P2-P513, P2-P515, P2-P516, P2-P517 (LIT_A5); P2-P1302 and P2-P1305 (LIT_X4); P2-P1717 (LIT_X8); P2-P402 (LIT_A4); P2-P2325 (LIT_X14); P2-P1017 (LIT_X1).
- Duplicate: the 2022 AutoSec demo of the multi-sensor fusion attack (10.14722/autosec.2022.23038), same work as P2-P1906.
- Training-time attack, outside test-time physical attack detection: depth-aware backdoor attack on LiDAR-camera fusion (IEEE Access 2026).
- No security content: a 2026 camera-LiDAR-radar fusion survey; a 2025 efficient multi-camera BEV detector; a 2018 BEV LiDAR and front-camera fusion method; a 2023 targetless LiDAR-camera calibration preprint; speed-limit and traffic-sign recognition systems without map or security component (2004, 2010, 2011, 2015, 2020); context-aware detection architectures for accuracy (2022, 2025).
- Other task families: patch localisation and patch-energy defenses (LIT_A1 family); system-level effect of evasion attacks (LIT_X9 family); sign attack and sign classifier defense records of 2026 (LIT_X12 family); a generic activation-space perturbation detector (2019).
- Unrelated hits returned by the searches (speech, humour, hate-speech, semantic-communication and graph-learning records).

## Run record
- websearch: 4 queries, 0 results (log lines Q:).
- search-crossref: 18 queries; crossref DOI lookup: 1 call, stopped by the shared stop; arXiv id-list: 1 call (10 of 10 records); search-arxiv: 3 calls (2 records, then 429). lit_verify calls 23 of 50; websearch 4 of 40.
- No instruction-like text was seen in search or API results.
