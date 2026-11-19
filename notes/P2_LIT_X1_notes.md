# P2_LIT_X1_notes - surveys and systematizations (task LIT_X1)

Status: written by LIT_X1 (continuation agent). Not audited. Read depth: abstracts, publisher-page extracts and search-result extracts of full texts; no paper was read in full. Rows: work/LIT_X1/rows.jsonl; catalog build: catalog/P2_LIT_X1_catalog.csv. Rows P2-P1022, P2-P1023 and P2-P1024 are arXiv preprints that were not checked against the arXiv API in this run (shared arXiv stop in force for the whole run): state UNVERIFIED, NEEDS_VERIFY; P2-P1023 and P2-P1024 carry first_author UNVERIFIED because no record read showed the authors. P2-P1025 is verified through its ICCV 2025 DOI. Hardware facts used on the cards: 10-core CPU, 32 GB RAM, one 6 GB laptop GPU (00_COMMON update 1).

## 0. Findings first (uncomfortable ones on top)
1. Consistency checking is already a named defense class at survey level. The sensor-attack SoK (P2-P1024) lists spatial, temporal or contextual consistency checks as defense class D5 and gives the rationale the owner's slides rely on: many attacks lack precision or continuity, so their outputs break short-horizon spatial, temporal or semantic relations; its camera examples flag patches through temporal incoherence or scene-context mismatch. The IEEE S&P magazine article (P2-P1021) presents spatiotemporal consistency as a general defense, and the semantic AI security SoK (P2-P1022) tabulates camera-side consistency defenses (driving context and physics, driving context, reflected lights) with deployability columns. A Paper 2 claim must rest on the specific cheap cue, the gate and abstain state, the cost and the matched false-alarm evaluation, not on consistency checking as such.
2. The 2026 traffic-sign survey (P2-P1009) already names the slide 01 and slide 05 ideas as directions: rule-based verification of sign shape, colour and symbol (rated low cost and highly real-time feasible, but liable to miss valid-looking adversarial signs) and temporal consistency across frames plus road-context checks (its section 6.1.2, because most traffic-sign attack papers test single images).
3. The D5 rationale has a built-in weak point: it works because attacks lack continuity. An attacker who keeps the perturbation stable across frames (high continuity in the attribute scheme of P2-P1024) removes the signal a temporal check uses. The coordinator lead on a sequence-aware shadow attack for video (CVPR 2026 workshop, UNVERIFIED, notes/P2_COORD_leads.md) is such a case. This is an inference from the SoK attributes, not a result in any record read.
4. Physical attacks may be weaker in black-box practice than white-box papers suggest: a 2025 review finds all three deployment classes transfer poorly across models and modalities (P2-P1003), and a defense comparison on OpenPilot found that no single defense covers all attacks (P2-P1011). Every controlled attack scenario must state its threat model.
5. Certified patch defenses do not yet cover what a driving camera needs: per P2-P1018 most handle image classification and one small patch, not detection, tracking, several patches or patches that grow as the vehicle approaches; it also notes that some reported clean accuracy ignored false alerts on clean images.

## 1. Problem map (attack families and the surveys that define them)
| Taxonomy axis | Classes | Row |
|---|---|---|
| Adversarial medium (the artifact that carries the perturbation) | sticker, patch and other media; four steps: perturbation generation, medium manufacturing, threat-image capture, attack | P2-P1001 |
| Attack form, task, knowledge | adversarial patches, optical attacks, 3D-printed objects; tasks incl. self-driving; white, black, gray box | P2-P1002 |
| Physical deployment (object detection) | 2D physical objects, injected adversarial signals, 3D camouflage; perceptibility visible, natural, stealthy, imperceptible; transfer cross-model and cross-modal | P2-P1003 |
| Optical attacks | invasive versus non-invasive physical attacks; optical attacks in three groups by where the perturbation is generated (light source, light path, light capture, as P2-P1005 describes them) | P2-P1004 |
| Light transmission pipeline | light sources, transmission channel (visible or infrared), capture | P2-P1005 |
| Manufacturing and re-sampling process | touchable (2D, 3D) versus untouchable attacks (light, projection, reflected light); re-sampling by cameras and other samplers under changing environments | P2-P1023 |
| Traffic-sign specific | medium (digital or physical), objective, access, phase; threats: digital changes, patches, shadows, lighting effects, sensor-level | P2-P1009 |
| AD semantic AI security | physical-layer vectors: object texture, shape, position, laser or IR light, translucent patch; plus sensor spoofing and cyber-layer vectors | P2-P1022 |
| Sensor-attack error propagation | camera attack nodes: physical patch, projected patch, laser, infrared light, strong light; camera error nodes incl. false positive, false negative, misclassification, displacement, sign, signal and lane misdetection, latency; attributes precision, continuity, intensity, dynamic target and impact | P2-P1024 |
| Setting, sensor, traffic element | real world, simulator, digital; camera, LiDAR, fusion; traffic elements | P2-P1010 |
| Fusion | single-sensor attacks (camera, LiDAR, radar, GPS) cascading through fusion logic | P2-P1017 |

Where the five cue families sit (brief question 2):
- Object appearance (slide 01): the best covered class: patches, stickers, 2D objects and 3D camouflage (P2-P1001, P2-P1002, P2-P1003), touchable attacks (P2-P1023), texture and shape vectors (P2-P1022).
- Shadows (slide 02): named as a threat of its own only in the traffic-sign survey (P2-P1009). In the general taxonomies read, a shadow falls under optical or untouchable attacks; no general survey read gives shadows a class of their own (abstract-level reading).
- Reflections (slide 03): reflected light appears as an untouchable attack example (P2-P1023, extract) and as the target of a reflected-light consistency defense in the SoK table (P2-P1022); the light-pipeline review (P2-P1005) covers the light path.
- Lighting (slide 04): optical attacks (P2-P1002, P2-P1004, P2-P1005), signal injection (P2-P1003), laser, infrared, strong-light and projector nodes (P2-P1024), laser or IR light vector (P2-P1022).
- Video frames (slide 05): no taxonomy read treats time as a medium. Time enters as an attribute: continuity of the induced error (P2-P1024), temporal attacks on video (P2-P1020), single-image evaluation as a gap (P2-P1009), video and multimodal inputs as new surfaces (P2-P1006). Slide 05 is a check that spans media, not a medium of its own.

## 2. Solution map (defense and detection families named by the surveys)
| Family | What the surveys say | Rows |
|---|---|---|
| Input pre-processing and purification (smoothing, squeezing, reconstruction, diffusion) | cheap variants weak against patches, shadows, occlusion and viewpoint (P2-P1009 Table 8); diffusion reconstruction strongest in the OpenPilot comparison but heavy (P2-P1011); generative defenses as a class (P2-P1016) | P2-P1002, P2-P1008, P2-P1009, P2-P1011, P2-P1016 |
| Patch localisation and removal | 11 defenses benchmarked; patch-mask accuracy does not predict defense outcome (P2-P1025) | P2-P1002, P2-P1008, P2-P1025 |
| Adversarial training, model modification | strong for known attacks, limited for unseen physical attacks (P2-P1009) | P2-P1008, P2-P1009, P2-P1011 |
| Certified defenses (masking, randomized smoothing) | narrow threat models (P2-P1018); sampling cost (P2-P1019) | P2-P1002, P2-P1018, P2-P1019 |
| Inference-time detection (feature, reconstruction, auxiliary model, uncertainty, steganalysis, attention) | ranked by timeliness; novel attacks poorly detected (P2-P1020); anomaly detection medium feasibility and open to adaptive attacks (P2-P1009) | P2-P1009, P2-P1010, P2-P1020 |
| Consistency checking (spatial, temporal, contextual, physics, fusion, reflected light, trajectory) | established class D5 (P2-P1024); general defense view (P2-P1021); SoK table with deployability (P2-P1022); temporal consistency detector scored for real time (P2-P1014) | P2-P1009, P2-P1014, P2-P1021, P2-P1022, P2-P1024 |
| Rule-based and structure-aware verification (sign shape, colour, symbol, semantics, ILP) | low cost, high real-time feasibility; misses valid-looking adversarial signs | P2-P1009 |
| System level (maps, fusion, system-level evaluation) | map or sensor consistency depends on calibration and map freshness (P2-P1009); fusion redundancy paradox (P2-P1017); system-level evaluation gap (P2-P1022) | P2-P1009, P2-P1017, P2-P1022 |

## 3. Closest prior work to the owner's design slides (ranked; survey level only)
P2-P1022 and P2-P1024 are preprints whose arXiv records were not API-checked in this run (NEEDS_VERIFY).
1. P2-P1024 (SoK of sensor attacks, preprint): states the shared hypothesis of all five slides (attacks break short-horizon consistency) and its limit (continuity). Closest for slides 02, 04, 05.
2. P2-P1009 (traffic-sign survey 2026): names rule-based sign-structure verification (slide 01) and temporal plus context consistency (slide 05) as cheap or future defenses, with a deployment trade-off table. Closest for slide 01.
3. P2-P1022 (SoK of semantic AI security, preprint): tabulates camera-side consistency defenses (driving context and physics, driving context, reflected lights) with timing, resource, training and adaptive-attack columns; its reflected-light entry is the closest to slide 03.
4. P2-P1021 (IEEE S&P magazine 2025): spatiotemporal consistency as a general defense; limitations section not read.
5. P2-P1014 (Artificial Intelligence Review 2025): AS-ADS scoring; a temporal consistency detector with majority voting scored as partly real-time with fixed thresholds: a ready baseline frame for slide 05.
6. P2-P1025 (ICCV 2025 benchmark, arXiv id): the evaluation protocol slide 01 needs (distance, light and angle bins in the physical world; adaptive attacks; outcome metrics rather than patch-mask metrics).
Primary defense papers closer still (for example the physics-aware 2026 defense, P2-P514 in LIT_A5) are catalogued by the cue-family tasks.

## 4. Open problems named by surveys (one line each)
- P2-P1022: general lack of system-level evaluation is the most critical of six scientific gaps; component-level success need not mean system-level effect.
- P2-P1009: most traffic-sign attack studies test single images; temporal consistency and road-context reasoning are proposed future defenses.
- P2-P1009: metrics beyond attack success rate are needed, including detection and system-oriented measures.
- P2-P1009: rule-based verification may miss valid-looking adversarial signs; anomaly detection is open to adaptive attacks; XAI inspection is not a standalone defense.
- P2-P1018: certified patch defenses mostly cover classification and one small patch; detection, tracking, segmentation, several patches and growing patches remain open.
- P2-P1018: some reported clean accuracy did not count false alerts on clean images as errors.
- P2-P1008: balance of robustness and model utility; adaptive attackers; physical-world resilience.
- P2-P1003: weak transfer of all three deployment classes across models and modalities; trade-off between ease of deployment and visibility.
- P2-P1002: transfer of physical attacks under domain shift and architecture change.
- P2-P1006: standardised evaluation protocols for detector attacks; video and multimodal inputs as new attack surfaces.
- P2-P1020: poor detection of novel attacks; compute burden on edge devices; video-stream attacks under-studied compared with still images; weak integration with alerting; adaptive attacks.
- P2-P1013: feasibility under real-time computing limits and lightweight robust pipelines are under-explored; snow, rain and fog affect the data.
- P2-P1019: certified defenses need fewer randomized-smoothing samples and more data sources.
- P2-P1017: fusion does not remove camera risk; single-modality attacks can cascade through fusion logic.
- P2-P1011: no single defense covers all attacks; purification is partial.
- P2-P1016: gaps between conventional and generative defenses in scalability, adaptability and resilience.
- P2-P1024: precise, reproducible physical execution limits attacks (precision, continuity); model-level defenses are mostly uncertified and adaptive attacks remain a challenge (extract).
- P2-P1025: patch-detection accuracy does not predict defense performance; physical-world and adaptive-attack evaluation is needed.
- P2-P1014: defenses should be scored for real time, adaptability, interpretability and efficiency together.
- P2-P1023: no open-problem list read (abstract not read); its extract stresses that light and weather at re-sampling strongly change physical attack performance.

## 5. Defenses judged practical in real time, and what is missing (brief question 3)
- P2-P1009 Table 8 (extract): high real-time feasibility for pre-processing and feature squeezing, data augmentation and simulation, and rule-based verification; medium-high for adversarial training; medium for anomaly detection, map or sensor consistency and ILP; low-medium for ensembles and certified robustness; low for XAI inspection. The same table marks the cheap options as weak for patches, shadows, occlusion and viewpoint change, or for valid-looking adversarial signs.
- P2-P1014 AS-ADS (extract): a temporal consistency defense with majority voting gets 0.5 for real time (143 ms LSTM inference), 0.25 for adaptability (fixed thresholds), 0.25 for interpretability (entropy logs), 0.5 for efficiency (embedded compatible); a dynamic 3D modelling defense gets 1.0 for real time (12 ms) and 4.375 overall.
- P2-P1020 (abstract): an LSTM-based detector within 0.001 s at about 90 percent accuracy; NutNet adds about 8 percent inference time.
- P2-P1025 (extract): among 11 defenses SAC had the smallest time cost and NutNet the best defense performance.
- P2-P1022: deployability columns per defense (timing and resource overhead, no training, no extra data, no hardware change, robust to adaptive attack); values not transcribed because the extract lost the check marks.
- Missing, in the surveys' own terms: end-to-end latency on embedded hardware (P2-P1013, P2-P1020); robustness to adaptive attackers (P2-P1008, P2-P1009, P2-P1020, P2-P1024); detection on video streams (P2-P1009, P2-P1020); system-level effect (P2-P1022); honest false-alert accounting (P2-P1018). None of the abstracts read reports benign look-alikes (tree shadows, glare, auto-exposure jumps) as a standard hard-negative set; to our knowledge from abstract-level reading this protocol element is open.

## 6. Gaps and what is left to test
1. A cheap camera-only cue with an explicit abstain state, compared with one survey-named consistency baseline at a matched false-alarm rate on benign look-alike clips: not found as a protocol in the surveys read.
2. Temporally coherent attacks (high continuity) against temporal checks: the surveys name adaptive attacks as open but describe no stress test of this kind (abstract level).
3. Light-borne attacks are rated the least perceptible deployment class (P2-P1003), yet no survey read evaluates real-time camera-side detection across light attack types; the lightweight laser-attack detector seen in search (Laser Guard, IEEE Access 2025) is left to LIT_A4.
4. System-level effect: frame and clip metrics need at least a per-track decision measure; closed-loop simulation (PASS, P2-P1022) is likely beyond the laptop budget.

## 7. Survey-of-surveys (for a related-work table)
| Row | Focus | Year | Attacks | Defenses | Driving-specific |
|---|---|---|---|---|---|
| P2-P1001 | physical attacks, all vision tasks | 2024 | yes | no (per P2-P1002) | partly |
| P2-P1002 | physical attacks and defenses, vision | 2026 | yes | yes | partly |
| P2-P1003 | physical attacks on object detection | 2025 | yes | no (abstract) | partly |
| P2-P1004 | optical physical attacks | 2024 | yes | not read | partly |
| P2-P1005 | light-pipeline physical attacks | 2026 | yes | not read | partly |
| P2-P1006 | attacks on object detection, with evaluation | 2025 | yes | yes (section list) | partly |
| P2-P1007 | physical attacks, camera-based systems | 2023 | yes | not read | partly |
| P2-P1008 | patch attacks and defenses | 2025 | yes | yes | no |
| P2-P1009 | traffic-sign recognition threats and defenses | 2026 | yes | yes | yes |
| P2-P1010 | physical vulnerabilities of driving systems | 2025 | yes | yes | yes |
| P2-P1012 | traffic-sign recognition attacks | 2023 | yes | no (abstract) | yes |
| P2-P1013 | AV attacks and defenses, safety view | 2024 | yes | yes | yes |
| P2-P1014 | vision-based autonomous systems | 2025 | yes | yes, scored | yes |
| P2-P1015 | image classification in driving systems | 2025 | yes | yes | yes |
| P2-P1016 | generative defenses for AV cybersecurity | 2026 | partly | yes | yes |
| P2-P1017 | single-modality to fusion attacks | 2026 | yes | yes | yes |
| P2-P1018 | certified patch defenses | 2023 | no | yes | yes |
| P2-P1019 | certified robustness in driving perception | 2025 | no | yes | yes |
| P2-P1020 | real-time attack detection (surveillance) | 2026 | yes | yes | no |
| P2-P1021 | spatiotemporal consistency defenses | 2025 | partly | yes | partly |
| P2-P1022 | SoK semantic AI security in driving | 2022 preprint | yes | yes | yes |
| P2-P1023 | physical adversarial examples | 2023 preprint | yes | not read | partly |
| P2-P1024 | SoK sensor attacks, error propagation | 2025 preprint | yes | yes | yes |
P2-P1011 (DSN-W 2025) and P2-P1025 (ICCV 2025) are evaluation studies, not surveys.

## 8. Datasets, benchmarks and code seen
- P2-P1025: patch-defense benchmark with 2 attack goals, 13 patch attacks, 11 detectors, 11 defenses and 4 metrics; dataset of 94 patch types and 94,000 images (arXiv extract). Code and data location not seen; licence unknown.
- P2-P1022: PASS evaluation platform. The AutoSec 2022 PASS paper (seen, not catalogued) lists 45 stop-sign and almost 1,000 traffic-light scenarios and an open-source plan; location and licence not read.
- P2-P1011: code named as github.com/DepCPS/revisiting_adversarial_ADS (UNVERIFIED); uses OpenPilot (licence not read).
- P2-P1001: paper list named as github.com/weihui1308/PAA (UNVERIFIED).
- Seen, not catalogued (UNVERIFIED): PADetBench (Knowledge-Based Systems 2025): 23 physical attacks and 48 detectors under simulated physical dynamics; APRICOT-Mask, pixel-level masks of physical patches introduced with the SAC defense (CVPR 2022); the Laser Guard benchmark of laser-based adversarial examples (IEEE Access 2025).
- Licence question: no licence was read. Record each licence before any download (DECK_DIGEST section 4).

## 9. Problem cards (hypotheses, not results)

### Card 1 - Consistency checks are an established defense class: what does a cheap camera-only check add?
- Problem: surveys already list spatial, temporal and contextual consistency checking as a defense family, so the owner's pipeline must show what a lightweight camera-only cue adds over existing consistency detectors at the same false-alarm rate.
- Contribution to test: a frozen detector plus one cheap per-track cue residual (contour versus box, exposure or flicker) with an explicit abstain state reaches recall comparable to a heavier consistency defense at equal FPR and lower latency.
- Open-source starting point: the OpenPilot and YOLO comparison code of P2-P1011 (location UNVERIFIED); OpenCV for cues; the PASS platform of P2-P1022 only if it fits.
- Data and laptop fit: public sign and driving video plus controlled attack clips; detector inference and OpenCV cues fit the 6 GB GPU and 32 GB RAM; closed-loop simulation probably does not. Licence question: video sets and OpenPilot code licences must be recorded first.
- Experiment workflow: (1) fix detector and tracker; (2) implement two or three cue residuals and an abstain rule; (3) compare with detector-only and one survey-named consistency baseline at matched FPR on benign look-alike clips; (4) time every stage per frame on the laptop.
- Success measure: TPR at fixed FPR; false alarms per hour; p95 ms per frame; abstention rate.
- Sources: P2-P1024, P2-P1021, P2-P1022, P2-P1009, P2-P1011, P2-P1014.
- Prior work: the idea is covered at survey level; only the cue choice, gate, abstention, cost and protocol can be new.

### Card 2 - Temporally coherent attacks against frame-consistency checks
- Problem: the D5 rationale rests on attacks lacking precision or continuity (P2-P1024); an attack kept stable across frames removes that signal, and most traffic-sign attack studies test single images (P2-P1009), so this case is weakly measured.
- Contribution to test: a temporal check combined with a per-frame physical cue (shadow geometry or exposure residual) keeps recall against temporally coherent attacks where a temporal-only check loses it.
- Open-source starting point: tracker plus OpenCV cues; the sequence-aware shadow attack lead (CVPR 2026 workshop, UNVERIFIED) as attack generator if code exists.
- Data and laptop fit: short sign video sequences with synthetic and printed attacks; CPU-feasible; licence of each video set to be recorded.
- Experiment workflow: (1) build single-frame and temporally coherent versions of the same attack; (2) run temporal-only and temporal-plus-physical checks; (3) match FPR on benign clips with natural shadows and glare; (4) report the recall gap and warning delay.
- Success measure: recall at fixed FPR for coherent versus incoherent attacks; warning delay in frames.
- Sources: P2-P1024, P2-P1009, P2-P1020, P2-P1014.
- Prior work: temporal consistency defenses exist (P2-P1014 scores one; LIT_A5 rows); a coherent-attack stress test is what is left, to our knowledge from abstract-level reading.

### Card 3 - Patch defenses are ranked by the wrong metric
- Problem: patch-defense evaluations are inconsistent; patch-localisation accuracy does not track defense performance (P2-P1025), and some certified defenses did not count false alerts on clean images (P2-P1018).
- Contribution to test: evaluating the slide 01 contour-versus-box check with object AP, attack success and TPR at fixed FPR (false alerts on clean sign clips included), binned by distance, light and angle, changes its ranking against localise-and-remove defenses compared with patch-mask metrics.
- Open-source starting point: the P2-P1025 benchmark patches and defenses (code location UNVERIFIED); SAC and APRICOT-Mask seen in search (not catalogued).
- Data and laptop fit: the 94,000-image set can be subsampled; licence unknown and to be read before download.
- Experiment workflow: (1) take benchmark patches on sign images; (2) run detector-only, one localise-and-remove defense and the contour check; (3) compute AP, attack success and TPR at fixed FPR; (4) bin by distance, light and angle.
- Success measure: rank changes between metric families; TPR at fixed FPR; ms per frame.
- Sources: P2-P1025, P2-P1018, P2-P1008, P2-P1009.
- Prior work: P2-P1025 already makes the metric point for localise-and-remove defenses; extending it to a detection-side shape check is what is left.

## 10. Leads not confirmed
| Lead | Where seen | What was tried | State |
|---|---|---|---|
| Published venue of the SoK on semantic AI security (P2-P1022) | arXiv page; a UC Irvine page calls it a preprint journal article | search results only | not found; row kept as preprint |
| SoK: The Next Frontier in AV Security (arXiv 2604.20621) | search result | not verified (row cap of the brief) | UNVERIFIED |
| Runtime Safety Monitoring of Deep Neural Networks for Perception: A Survey (arXiv 2511.05982) | search result | not verified (row cap) | UNVERIFIED |
| A Taxonomy of System-Level Attacks on Deep Learning Models in Autonomous Vehicles (arXiv 2412.04510) | search result | not verified (row cap) | UNVERIFIED |
| Adversarial Examples in Environment Perception for Automated Driving (arXiv 2504.08414) | search result | not verified (row cap) | UNVERIFIED |
| A Survey on Physical Adversarial Attack in Computer Vision (arXiv 2209.14262) | search result | not verified (row cap); published venue unknown | UNVERIFIED |
| SoK: Rethinking Sensor Spoofing Attacks against Robotic Vehicles from a Systematic View (EuroS&P 2023, DOI shown as 10.1109/EuroSP57164.2023.00067) | IEEE CSDL page | not verified (row cap) | UNVERIFIED |
| PASS platform paper (NDSS AutoSec workshop 2022) | NDSS and NSF pages | not verified | UNVERIFIED |
| PADetBench (Knowledge-Based Systems 2025, DOI shown as 10.1016/j.knosys.2025.114395) | publisher page | not verified (benchmark, other tasks) | UNVERIFIED |

Verified by Crossref but not catalogued (row cap of the brief): Deng et al. 2021, IEEE Transactions on Industrial Informatics, 10.1109/tii.2021.3071405 (metadata only); Fawole et al. 2025, ACM Computing Surveys, 10.1145/3729167 (vision transformers in traffic-sign recognition). Both can be added by the coordinator from the ledger.

## 11. Exclusions
- Aerial patch and camouflage review (Sensors 2026, 10.3390/s26196057): UAV and remote-sensing domain. Its finding that viewpoint is modelled mostly as scale is background for slide 01.
- LiDAR-only surveys (arXiv 2409.20426; arXiv 2411.13778): outside the camera scope.
- Surveillance physical-attack survey (TNNLS 2023, arXiv 2305.01074): surveillance domain; seen only as a reference.
- Self-driving security review (IET ITS 2026, 10.1049/itr2.70237): network, privacy and general cybersecurity, not perception attacks.
- IoT adversarial-example detection review (PMC 2026) and hardware side-channel detectors (power analysis, GPU monitoring): outside camera perception.
- Temporal misalignment attacks and their defense on camera-LiDAR fusion (ICLR 2026, arXiv 2507.09095): timestamp attacks, not visual physical attacks.
- General surveys of digital adversarial-example detection (a 2022 CRAD survey) and off-topic Crossref hits (perception survey, Neurocomputing 2022; cybersecurity-systems survey, ESWA 2024).
- Recovery-method benchmark for adversarial traffic signs (IET ITS 2025): digital attacks only per the extract; Low.
- Primary attack and defense papers seen in searches (ControlLoc CCS 2025, SysAdv ICCV 2023, PhySense CCS 2024, physics-aware defense Sensors 2026, Laser Guard IEEE Access 2025, natural-light attack WACV 2024, fluorescent patch NeurIPS 2025, traffic-sign perturbation study CVPR 2025 workshop): belong to the cue-family tasks; not catalogued here.

## 12. Notes on method
- 17 of 40 websearch calls (the last 4 returned no results, as other agents reported) and 11 of 50 lit_verify calls; queries in progress/LIT_X1.log and work/LIT_X1/query_log.tsv. Crossref answered every DOI checked (24 target DOIs FOUND, 0 NOT_FOUND). The arXiv host was under a shared stop for the whole run, so no arXiv call was made: 3 rows wait for the arXiv check (NEEDS_VERIFY), and the arXiv ids on 5 DOI-verified rows (P2-P1001, P2-P1002, P2-P1006, P2-P1011, P2-P1025) were taken from arXiv pages in search results and are not API-checked.
- No instruction-like text was met in search results.
