# P2_LIT_X14 notes - other camera targets: lanes and road markings, traffic lights, pedestrians, vehicles

Status: written by the LIT_X14 worker agent (a continuation; the first LIT_X14 agent stopped on a provider rate limit before writing any row). NOT AUDITED: fresh-agent audit required. Rows: work/LIT_X14/rows.jsonl, 25 rows, P2-P2301 to P2-P2325 (scripts/rows_check.py: VERIFIED 25, MISMATCH 0, NOT_FOUND 0, schema problems 0; High 12, Medium 13). Read depth: abstract level 5 (P2301 and P2308 from websearch snippets of the paper PDFs; P2319, P2320 and P2323 from Crossref abstracts), metadata-only 20 (Crossref record without abstract; their key ideas paraphrase the title and say so). No full text read. Ids of this task are written without the P2- prefix (P2301 = P2-P2301); ids of other tasks keep the prefix and name the task.

Tool state during the run (limits completeness):
- websearch: 17 calls for this task (7 by the first agent, 10 by this one); 1 returned results (the first call of this agent), all others returned "no search results". Every "none found" below means "none found with these searches", not proof of absence.
- export.arxiv.org was under a shared stop at launch and was not called. Papers that exist only on arXiv are listed as leads with NEEDS_VERIFY.
- Crossref: 30 lit_verify calls (27 title searches, 3 DOI batches with 30 lookups). Crossref carried an abstract for 4 of the 30 DOIs looked up, which is why most rows are metadata-only.
- No instruction-like text was found in search results or API records.

## Findings first (uncomfortable ones first)
1. For pedestrians and vehicles the slide 05 idea (check the detector's class against the physics of its track) is already published: P2-P510 (LIT_A5, 2023) cross-checks the class of a track against its spatiotemporal behaviour and ego context, tested with physical patches shown on a monitor or a projector on a moving vehicle. A Paper 2 claim for these classes has to be an increment over it (vanishing rather than misclassification, cheaper cues, an explicit abstain state), not the consistency idea itself.
2. Defenses tested on more than one class or task exist, but none in the records read combines physical attacks with lanes, lights, pedestrians and vehicles. The multi-class or multi-task evaluations read are digital (P2-P128 in LIT_A1, P2-P2018 in LIT_X11), static images (P2-P519 in LIT_A5: VOC, COCO, KITTI), task-level (P2323 Z-Mask: segmentation and detection with digital and printed patches) or two targets (P2-P1011 in LIT_X1: stop sign and lead vehicle on OpenPilot, where no single defense covered all attacks per that row). This gap holds only to our knowledge: 20 of the 25 rows here are metadata-only.
3. Real-vehicle camouflage is weaker than lab results suggest: P2319 (preprint, 2026, not peer reviewed) reports a gap between digital and physical effect on a full-size car, attenuated by texture transfer loss, environmental interference and detector robustness. Vehicle positives made only in simulation would overstate the threat; Paper 2 should say so if it uses them.
4. Traffic lights: few attack papers and no attack detector found. One patch attack (P2307), one robustness evaluation in a Level-4 stack (P2306, content not read) and the laser attack catalogued by LIT_A4 (P2-P407). The cheapest independent cues for lights (prior map, lit-lamp position versus colour, phase order) lie outside the five cue families of the design slides.
5. Lanes: one lane-specific defense found (P2302, content not read). The USENIX Security 2021 road-patch lane attack named in the brief could not be confirmed in a primary record during this run (lead 1).
6. A cross-task, time-aware attack framework exists (P2322, Pattern Recognition 2025, content not read). Any check that compares tasks or frames must be tested against an attacker who keeps them in agreement.

## 1. Problem map (attack families with the papers that define them)
| Target | Attack family | Rows here | Rows in other tasks |
|---|---|---|---|
| Lanes and road markings | Road-surface patches and drawn lines against lane detectors | P2301 (study of 3 physical attacks on 4 lane-detector types) | Leads 1 and 2 (USENIX Security 2021) |
| Lanes | Natural illusions: shadows, reflections, tire marks | - | P2-P204, P2-P241 (LIT_A2) |
| Lanes | Simple physical perturbations against end-to-end driving models | P2304 | - |
| Lanes | Training-time backdoor with a physical trigger | P2305 | - |
| Traffic lights | Patches | P2307 | - |
| Traffic lights | Robustness evaluation inside a Level-4 stack | P2306 | - |
| Traffic lights | Laser through the rolling shutter | - | P2-P407 (LIT_A4), P2-P321 (LIT_A3) |
| Pedestrians | Patches and wearable textures that hide people | P2309, P2310, P2311, P2312, P2313, P2314 | P2-P104, P2-P105 (LIT_A1) |
| Pedestrians | Night, reflective and near-infrared attacks | - | P2-P319, P2-P320 (LIT_A3) |
| Vehicles | Full-body camouflage | P2315, P2316, P2317, P2318 | P2-P106 FCA, P2-P107 ACTIVE (LIT_A1) |
| Vehicles | Real-world strength of camouflage | P2319 | - |
| Vehicles | Vehicle as carrier: screen patch aimed at another object | P2308 | - |
| Vehicles | Light projection that makes a car vanish | - | P2-P426 (LIT_A4) |
| Tracked road users | Tracker hijacking and ID transfer | - | P2-P521, P2-P523 (LIT_A5) |
| All targets | Cross-task, time-aware attack | P2322 | - |
| All targets | System-level effect of evasion attacks | P2321 | - |
| Taxonomy | 2D objects, injected signals, 3D camouflage | P2320 (review) | - |

## 2. Solution map (defense and detection families)
- Lane-specific defense: P2302 (model-agnostic per the title; mechanism not read).
- Feature statistics that flag and mask the attack region across task types: P2323 Z-Mask (the flagged region doubles as an explanation); multi-frame attention variant by the same first author, P2-P508 (LIT_A5).
- Cross-task consistency: P2-P128 (LIT_A1; detection versus instance segmentation, BDD100K, PGD); P2-P2018 (LIT_X11; edges, depth and segmentation, Cityscapes and KITTI). Digital perturbations in both records.
- Track and trajectory consistency: P2-P510 (class versus motion, LIT_A5); P2324 (Kalman-filter defense for multi-target tracking, content not read); P2-P518 (deviation clipping inside Kalman trackers, LIT_A5); P2-P512 (ego-motion residuals with a Normal, Warning, Attack state machine, LIT_A5).
- Map and context priors: P2325 (traffic-light mapping, localisation and state detection; not an attack paper).
- Evaluation lenses: P2321 (system-level effect), P2303 (driving-oriented lane metric), P2-P1011 (defense comparison on a production driving stack, LIT_X1).

## 3. Closest prior work to the design slides for these targets (ranked, with the reason)
1. P2-P510 (LIT_A5): the slide 05 shape (frozen detector and tracker, independent spatiotemporal cue, consistency check) already applied to pedestrians and vehicles with physical patches. Main novelty threat for any non-sign extension.
2. P2-P1011 (LIT_X1): defense comparison on a sign target and a lead-vehicle target; ready baseline set, and evidence that purification defenses are partial.
3. P2323 Z-Mask: deterministic detector of physical patches on two task types with an explicit flagged region; strongest slide 01 baseline beyond signs among the rows read.
4. P2324: Kalman-filter defense for tracked road users; likely the cheapest temporal baseline (content not read).
5. P2302: the only lane defense found (content not read).
6. P2325: prior map for traffic lights; not a defense, but the cheapest independent cue for lights.

## 4. Gaps and what is left to test
1. One cheap consistency layer evaluated with physical attacks across signs, lights, lanes, pedestrians and vehicles: none found (to our knowledge).
2. Traffic lights: no attack detector found; lit-lamp position versus colour, prior map and phase order are untested as attack cues in what was read (card X14-1).
3. Lanes: no check of lane geometry against ego motion found; P2302 unread (card X14-2).
4. Pedestrians: wearable textures deform with the body, so rigid shape priors such as the sign contour of slide 01 do not apply; natural-looking textures (P2313) weaken appearance cues. Vanishing is a different failure from the misclassification that P2-P510 targets per its key idea (card X14-3).
5. Vehicles: threat realism (P2319). Report positives by source: simulated, composited, recorded.
6. Adaptive attackers that keep tasks or frames consistent (P2322).
7. Evaluation should reach the driving decision (P2321, P2303), not stop at per-frame detection.

## 5. Datasets, benchmarks and code seen
- comma2k19 and TuSimple: named in the P2301 snippet (lane studies). Licences not checked.
- LanEvil++ (P2-P241, LIT_A2): CARLA-generated lane-illusion benchmark.
- From other tasks' rows: KITTI tracking traces (P2-P518), BDD100K validation set (P2-P128), Cityscapes and KITTI (P2-P2018).
- Physical setups: two robot cars, one carrying a screen (P2308); one real car with transferred camouflage (P2319); no data release seen.
- No code location seen in the records read by this task.

## 6. Leads not confirmed (9)
1. Dirty Road Can Attack: Security of Deep Learning based Automated Lane Centering under Physical-World Attack (Sato and co-authors, USENIX Security 2021). Seen only in reference lists of two preprints returned by websearch (arXiv 2511.14876 and 2511.08015) and in the P2301 snippet, which describes the dirty road patch attack. Tried: 4 targeted websearch queries (3 by the first agent, 1 by this one), no primary page; USENIX papers carry no DOI; arXiv host stopped. NEEDS_VERIFY on the USENIX Security 2021 programme page or the arXiv API.
2. Too Good to Be Safe: Tricking Lane Detection in Autonomous Driving with Crafted Perturbations (USENIX Security 2021, from memory). Tried: 1 websearch query, empty; no DOI. NEEDS_VERIFY.
3. Attacking Autonomous Driving Agents with Adversarial Machine Learning: A Holistic Evaluation with the CARLA Leaderboard (arXiv 2511.14876, preprint). Seen as a websearch result; arXiv host stopped. NEEDS_VERIFY.
4. Invisible Triggers, Visible Threats! Road-Style Adversarial Creation Attack for Visual 3D Detection in Autonomous Driving (arXiv 2511.08015, preprint): road-surface posters that create false 3D detections (snippet). Phantom family (LIT_X11). NEEDS_VERIFY.
5. Transferable Physical-World Adversarial Patches Against Object Detection in Autonomous Driving (arXiv 2604.23105, preprint): patch optimised over several detectors (snippet). NEEDS_VERIFY.
6. CAMOU vehicle camouflage (ICLR 2019, from memory): no DOI; not searched.
7. RAUCA vehicle camouflage (ICML 2024, from memory): possibly the conference version of P2318.
8. Adversarial YOLO person-patch defense (arXiv, from memory): not searched.
9. Traffic-light datasets for card X14-1 (Bosch Small Traffic Lights, LISA Traffic Light, DriveU Traffic Light): names from memory; LIT_X2 owns datasets.

Confirmed in Crossref but not catalogued (records are in work/LIT_X14/verify_ledger.jsonl):
- Detecting Adversarial Perturbations in Multi-Task Perception, IROS 2022, DOI 10.1109/iros47612.2022.9981559: peer-reviewed version of P2-P2018 (LIT_X11, catalogued from arXiv). The coordinator may attach this DOI there.
- Revisiting Adversarial Perception Attacks and Defense Methods on Autonomous Driving Systems, DSN-W 2025: already catalogued as P2-P1011 (LIT_X1).
- Generate Transferable Adversarial Physical Camouflages via Triplet Attention Suppression, IJCV 2024, DOI 10.1007/s11263-024-02098-4: likely follow-up of P2316 (titles only).
- Invisible Pedestrians: Synthesizing Adversarial Clothing Textures To Evade Industrial Camera-Based 3D Detection, ICME 2024, DOI 10.1109/icme57554.2024.10687467: setting unclear from the title.
- Defending Physical Adversarial Attack on Object Detection via Adversarial Patch-Feature Energy, ACM MM 2022, DOI 10.1145/3503161.3548362: patch defense (LIT_A1 core), no abstract in the record.
- Demo: Security of Camera-based Perception for Autonomous Driving under Adversarial Attack, AutoSec 2021, DOI 10.14722/autosec.2021.23018: no abstract; content unknown.
- Demo version of P2321, VehicleSec 2024, DOI 10.14722/vehiclesec.2024.25014.
- Traffic light mapping and detection, ICRA 2011, DOI 10.1109/icra.2011.5980164: companion of P2325.
- AdvGLOW: Covert adversarial attacks against autonomous driving perception, ETS-Data 2026, DOI 10.26599/etsd.2026.9190001: dataset record, content unknown; for LIT_X2.

## 7. Exclusions (not catalogued, with reasons)
- Reconstruction-Based Adversarial Attack Detection in Vision-Based Autonomous Driving Systems (MDPI MAKE 2023, abstract read): autoencoder detector for digital perturbations on regression models; no physical attack and no object target. Candidate for LIT_X5 (lightweight detectors).
- Adversarial Driving: Attacking End-to-End Autonomous Driving (IV 2023): the title gives no physical element; not read.
- Adversarial Attack Detection for Deep Learning Driving Maneuver Classifiers in Connected Autonomous Vehicles (ICCCN 2024): manoeuvre classifiers, not camera targets.
- LSM: A Comprehensive Metric for Assessing the Safety of Lane Detection Systems in Autonomous Driving (VTC2024-Fall): no attack in the title.
- Traffic-sign defenses returned by the searches (2022, 2025, 2026 records): signs belong to LIT_X12 and LIT_A1.
- Aerial-imagery attacks (Neurocomputing 2023, TrustCom 2024, a TGRS supplement record): not vehicle cameras.
- LiDAR backdoor attacks (SenSys 2022, IJCNN 2026): not camera.
- UniCamo multispectral camouflage (ICASSP 2026): multispectral detector, outside the RGB camera scope assumed here.
- Physically Realizable Adversarial Creating Attack against Vision-based BEV Space 3D Object Detection (TIP 2025; only a supplement record seen): phantom creation, LIT_X11.
- Dissertations without a year, Crossref component and peer-review records, standards documents.

## 8. Answers to the three questions of the brief
1. Physical attacks by target: table in section 1. Lanes: road-surface patches, drawn lines, shadows and other illusions, end-to-end model attacks, physical backdoor triggers. Traffic lights: patches, laser stripes. Pedestrians: patches, T-shirt and clothing textures, dynamic patches, night and infrared attacks. Vehicles: full-body camouflage, light projection, and vehicles that carry a screen patch aimed at other objects.
2. Defenses tested on more than one class or task, from records read: P2323 (segmentation and detection), P2-P510 (people and vehicles by design), P2-P519 (VOC, COCO, KITTI), P2-P502 (AdvIT: several video tasks), P2-P128, P2-P2018 and P2-P1011 (stop sign and lead vehicle). Unknown: P2302, P2324. None read evaluates physical attacks on lanes, lights, pedestrians and vehicles together.
3. Cue family by target (hypotheses unless a row is cited):

| Target | Appearance (slide 01) | Shadows (02) | Reflections (03) | Lighting (04) | Video frames (05) | Cue outside the five |
|---|---|---|---|---|---|---|
| Lanes | Weak: patches and drawn lines imitate ordinary marks (P2301); geometry priors (width, parallel lines) are stronger | Strong threat: shadows are the most disruptive illusion in LanEvil++ (P2-P241); negative shadows (P2-P204) | Reflections are among the LanEvil++ illusions (P2-P241) | Low | Strong: lane geometry should move smoothly with ego motion | Ego motion, map |
| Traffic lights | Housing, lamp layout, position of the lit lamp versus the reported colour | Low | Sun reflection on a lens can make an unlit lamp look lit (benign hard negative) | Strong: LED flicker is normal (P2-P430, LIT_A4); laser stripes (P2-P407) | Phase order and timing | Prior map (P2325) |
| Pedestrians | Weak for wearable and natural-looking textures (P2310, P2313) | A person still casts a shadow when the detector misses them (LiDAR analogue: P2-P235, LIT_A2) | Reflective attacks at night (P2-P319) | Night and near-infrared (P2-P320) | Strong: tracks should not vanish mid-scene (P2-P510, P2324) | Scene context |
| Vehicles | Camouflage covers the whole body, no compact patch (P2315 to P2318) | The cast shadow stays when the box is lost | Paint highlights change with view | Headlights; projection vanishing (P2-P426) | Strong: track continuity and plausible motion (P2324, P2-P518) | Other cameras of the vehicle |

## 9. Problem cards (hypotheses, not results; laptop: 10-core CPU, 32 GB RAM, one laptop GPU with 6 GB)

### Card X14-1. A traffic-light state that contradicts its own lamp layout, the map and the phase order
- Problem: a patch (P2307) or a light attack (P2-P407) can make the detector miss a light or report the wrong state; sign-specific cues do not cover lights.
- Contribution to test: a traffic-light consistency residual from (a) the position of the lit lamp inside the housing versus the reported colour, (b) presence of a light where earlier frames or a prior map (P2325) place one, (c) plausibility of the state sequence and its timing; abstain when the lamp region is saturated or occluded. Prior coverage: none found in this pass; P2306 is unread and may include defenses.
- Open-source starting point: a frozen small detector (the deck names YOLOX-Nano); OpenCV colour and blob features; a hand-written finite-state machine; scikit-learn calibration.
- Data and laptop fit: CPU-only features. Benign data: traffic-light datasets to be confirmed by LIT_X2 (lead 9, UNVERIFIED) and BDD100K clips with lights. Attack positives: digital composites of patch textures near the housing and simulated colour stripes, because no attack data or code was seen. Licence question: terms of each traffic-light dataset and of BDD100K for derived frames.
- Experiment workflow: (1) freeze the detector and crop lights over time on benign clips split by recording; (2) compute and cache the three residuals; (3) composite attack cases and fit a small calibrated head with recording-grouped validation; (4) compare with detector confidence only and with each residual alone at a fixed false-alarm rate, with LED flicker and sun glare as hard negatives.
- Success measure: attack recall at a fixed false-alarm rate per hour; false alarms on flicker and glare clips; p95 ms per frame on CPU; abstention count.
- Sources: P2306, P2307, P2325; related P2-P407 (LIT_A4), P2-P321 (LIT_A3), P2-P430 (LIT_A4).

### Card X14-2. Lane geometry that moves against the vehicle's own motion
- Problem: road-surface patches, drawn lines and shadows shift the detected lane (P2301, P2304, P2-P204), and lane following acts on the shifted lane.
- Contribution to test: a residual between the lane offset change predicted from ego motion (speed and yaw rate, or visual odometry) and the detected change, plus geometry priors (lane width, parallel lines), accumulated over a bounded window; abstain during lane changes, on worn markings and in construction zones. Prior coverage: P2302 is unread; P2-P512 (LIT_A5) already uses ego-motion residuals against other physical attacks, so the residual idea is not new; the lane-specific check is what is left to test.
- Open-source starting point: an open lane detector (not chosen here); OpenCV; an OpenCV Kalman filter for the predicted offset.
- Data and laptop fit: comma2k19 (named in P2301; whether it carries vehicle signals is from memory, UNVERIFIED) and TuSimple; LanEvil++ (P2-P241) for shadow and reflection illusions; attack positives from composites of dirty-road-style patches. Lane detector on the 6 GB GPU at reduced resolution, residuals on CPU. Licence question: comma2k19, TuSimple and LanEvil++ terms not checked.
- Experiment workflow: (1) run the frozen lane detector on benign drives and store lane polylines with ego signals; (2) predict the offset change from ego motion and compute residuals; (3) inject composite attacks and illusions and set the threshold on held-out recordings; (4) measure lead time before the lateral deviation that a driving-oriented metric (P2303) would count as a failure.
- Success measure: attack recall at a fixed false-alarm rate per hour on long benign drives; lead time; p95 latency; abstentions during lane changes.
- Sources: P2301, P2302, P2303, P2304, P2305; related P2-P204, P2-P241 (LIT_A2), P2-P512 (LIT_A5).

### Card X14-3. A pedestrian or vehicle that vanishes from detection but not from the scene
- Problem: adversarial clothing and vehicle camouflage hide road users (P2309 to P2318); patch localisers expect compact regions that full-body textures do not have.
- Contribution to test: track-level evidence that an object is still present after the detector drops it: Kalman track continuation plus two cheap cues inside the predicted box (optical-flow motion that keeps the track velocity; a dark ground-contact region consistent with the object's cast shadow); abstain on true occlusion by another tracked object. Prior coverage: P2-P510 checks class against motion for misclassification and P2-P518 bounds tracker drift; vanishing with cue evidence is the increment to test, and P2322 warns that a coherent attacker may defeat it.
- Open-source starting point: a frozen small detector (YOLOX-Nano per the deck), a simple Kalman tracker, OpenCV Farneback optical flow, scikit-learn.
- Data and laptop fit: BDD100K video (deck) for benign tracks with occlusions; positives from published clothing and camouflage textures composited onto people and cars where the authors' terms allow (no code seen here), plus a small own recording with a printed pattern. P2319 shows real-world strength is lower, so report positives by source. Flow on CPU at reduced resolution; detector on the 6 GB GPU. Licence question: BDD100K terms for derived frames; reuse terms of published textures.
- Experiment workflow: (1) run detector and tracker on benign clips and log each track end with its cause (occlusion, exit, miss); (2) compute the flow and shadow cues in the predicted box for a bounded number of frames after each track end; (3) inject vanishing attacks by compositing textures and fit the accumulation rule with recording-grouped validation; (4) compare with tracker-only and detector-confidence-only rules at a matched false-alarm rate.
- Success measure: vanishing-attack recall at a fixed false-alarm rate per hour; time from attack onset to alarm; p95 latency; abstentions on occlusion.
- Sources: P2309, P2310, P2313, P2315, P2316, P2319, P2322, P2324; related P2-P510, P2-P518 (LIT_A5).
