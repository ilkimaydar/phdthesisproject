# P2_LIT_A5_notes - changes across video frames (design slide 05)

Status: written by the LIT_A5 worker agent. Not audited. Row source: work/LIT_A5/rows.jsonl (45 rows, ids P2-P501 to P2-P545). Check result after the last batch: ARXIV_API_VERIFIED 35, VERIFIED 1, UNVERIFIED 9, 0 MISMATCH, 0 schema problems; High 17, Medium 28. Calls used: websearch 40 of 60, lit_verify 24 of 80.
Paper ids are written short: P501 means P2-P501.
Figures below come from search-result text extracts of the papers (arXiv HTML, PMC, PDF text) and from abstracts; no PDF was downloaded. An auditor should recheck the figures of P501, P511, P512 and P514 in the full papers.

## 0. Findings first

1. Prior work already covers most pieces of slide 05. Prior-frame consistency with a causal reference queue and an FPS figure: ADAV (P501). Kalman tracking, an abrupt-vanishing test, a 3-frame watch set, a failure warning, physical patch tests and a runtime overhead figure: AdROD-II (P511, arXiv 2608.16031, August 2026). A Normal, Warning, Attack state machine over accumulated residuals with per-frame runtime: VisionGuard of CCS 2024 (P512). Trajectory-versus-appearance conflict with a threshold set for a false-positive limit: the 2026 physics-aware defense (P514). Optical-flow consistency (P502), label-flip counts (P503) and window majority vote on physical-attack video (P504) are older still.
2. The slide wording "novel-attack recall or warning time beyond ADAV" is a low bar: ADAV reports no warning time, no false alarms per hour, no fixed false-alarm point and no memory figure in the text read (P501). The harder comparators are P511 and P512.
3. Consistency checks have a known counter: an attack that optimizes the detector and the check together (P516, static images). The physics-aware paper itself shows correction accuracy falling from 0.921 to 0.724 under a check-aware attacker (P514, Table 5 as read). AdROD-II cannot fire when an object is suppressed from first sight (P511, authors' own limitation).
4. Published comparisons are not at matched false-alarm rates. P514 lists PercepGuard at a false-positive rate of 0.236 against 0.041 for its own module; ADAV tunes a threshold on mAP (P501). Published numbers cannot be reused as baselines for a matched-FPR claim. Audit item: the text of P514 says its threshold keeps benign false positives below 5 percent, while its Table 2 lists values above 0.05 for its own module in several settings (up to 0.125); not reconciled in the extract read.
5. No record read applies a sequential test with an abstain state to physical-attack detection on camera detector outputs. Close analogues outside that setting: e-process test with a false-alarm bound on tracking failure (P533), SPRT with an undecided band on video anomaly scores (P529), CUSUM with a delay and false-alarm protocol (P530, P532), conformal plus CUSUM on camera sequences with delay in frames (P534), Warning and watch states (P512, P511), abstention designs (P535, P536).
6. Real attack video is scarce. Public sets found: Drive-By-Fly-By (P545, backdoor triggers, licence unread), AdROD companion sequences (P511, licence unread, patent notice), AdvNet images (P505). Simulated generators: PADetBench (P543, code MIT) and CARLA-GeAR (P544, licence unread). BDD100K data licence allows research and not-for-profit use (P542).
7. Both unverified lead labels on the slide are identified. "ADAV (2024)" is P501 (arXiv 2412.06215, single author, synthetic patch overlays on 200 BDD100K videos). "Physics-aware defense (2026)" is P514 (Sensors 26(3) 835).
8. Crossref returned HTTP 429 early in the run and was stopped for the rest of the run. Nine rows have no arXiv id and no Crossref record and stay UNVERIFIED (section 8).

## 1. Problem map (attack families and the papers that define them)

| Family | What it does over frames | Defining papers (paper_id) | Persistence facts read |
|---|---|---|---|
| Physical object vanishing (hiding) | Patch or sticker makes the detector miss an object | Disappearance Attack (P524); object-vanishing patch threat model of ADAV (P501); patch hiding (P519); pedestrian vanishing run length (P527); video patch benchmark with T-shirts (P506) | Fooled-frame share is below 100 percent: 63.5 to 85 percent of video frames in the stop-sign tests (P524); suppression works only inside a distance band and is rarely absolute (P511) |
| Object creation | Sticker or projection creates a detection that does not exist | Creation Attack, preliminary (P524); phantom objects for latency (P525); taxonomy (P517) | Few results read |
| Misclassification across frames | Wrong class over a sequence | Threat model of PercepGuard (P510); dynamic screen patches that change with distance (P526); sequence-consistent perturbations in the threat model of P509 | Dynamic patches change pixels frame to frame (P526) |
| Tracker hijacking | A few poisoned detections drag a track into or out of the vehicle path | P520 (1 to 3 frames), P521 (physical, CCS 2022), P522 (physical, CCS 2025), P523 (ID transfer by trajectory, no pixel change), P528 (tracker damage in CARLA); defense side P518 | One to three attacked frames can suffice (P520) |
| Latency and compute | Phantom objects inflate NMS and tracking work | SlowPerception (P525) | Seconds of added delay in physical tests (P525) |
| Adaptive attack on the check | Optimizes the attack and the consistency check jointly | ADC (P516, static images); adaptive rows of P514 and P510 | P514 adaptive correction accuracy 0.724 to 0.786 against 0.921 |
| Taxonomy and limits | Misclassification, deletion or creation, tracker hijacking, sensor spoofing | S&P Magazine overview (P517) | Names natural errors from noise, occlusion and poor lighting as a hard case |

Digital video attacks that older temporal detectors target: P502 (several tasks), P503 (video classification).

## 2. Solution map (defense and detection families)

| Family | Idea | Papers | Output states |
|---|---|---|---|
| A5-F1 prior-frame and temporal consistency | Compare detector output now with output 0.5 s ago (P501); optical-flow pseudo frame (P502); label flips between neighbours (P503); majority vote over a window (P504, P509); key frames plus flow (P506); channel-attention tracking across frames (P508); attention on frame pairs (P507); transform check per image (P505) | P501 to P509 | Binary (flag or not); P509 keeps objects after 3 frames of persistence |
| A5-F2 physics, trajectory, context | Track-class and context check (P510); ego-motion residuals with a Warning state (P512); spatial-temporal CRF (P513); spatio-temporal sensor consistency (P515); trajectory-appearance energy (P514); Kalman watch set (P511); deviation buffer inside a Kalman tracker (P518); objectness explained by boxes with alert (P519) | P510 to P519 | Warning and Attack (P512); watch and failure warning (P511); alert (P519) |
| A5-F4 sequential rules and abstention | SPRT with undecided band (P529); mode-aware CUSUM (P530); cumulative sign monitor with no stored sequence (P532); e-process with false-alarm bound (P533); conformal plus CUSUM on camera sequences (P534); abstain option in robustness (P535); conformal threshold plus abstention threshold (P536); theory survey (P531) | P529 to P536 | Undecided (P529); abstain (P535, P536) |
| A5-F5 streaming and lightweight temporal models | Streaming accuracy scores output against the world at output time (P537); next-frame prediction with a dual-flow module (P538); buffered long path of earlier frames at about 0.1 to 0.2 ms extra (P539); dual-path with distillation (P540); latency-aware metrics on synthetic video (P541) | P537 to P541 | Not attack related |

## 3. Closest prior work to slide 05, ranked

1. P511 AdROD (2026). Causal, bounded-window, tracker-based vanishing detector with a pending state and a failure warning, physical patch tests and a near-baseline overhead of 1.03 times before an attack. Slide 05 needs a test against it. Gap it leaves by its own account: no trigger without a prior track, and short tracking time at 40 km/h.
2. P512 VisionGuard (CCS 2024). Residual accumulation over a window with a Warning state, runtime of about 3 ms per frame, detection of 9 physical attacks in simulation and a physical run. Uses ego GPS and IMU motion in a closed loop, not frame cues; false positives in heavy rain, fog and a bumpy road.
3. P501 ADAV (named on the slide). Two-frame rule on detector outputs with a causal queue. Weakest comparator, synthetic overlays, no abstain.
4. P514 physics-aware defense (named on the slide). Trained module on backbone features and tracks, threshold set for under 5 percent benign false positives, 19 ms overhead against a 42 ms baseline, attacks inserted into clips of public sets.
5. P510 PercepGuard. Track-class plus context check with a reported operating point (false-positive rate 5 percent, true-positive rate 99 percent against adaptive attacks) and 96 percent detection on displayed and projected patches. A later paper says it needs 4 to 5 frames (P512).
6. P504 VG*. Fixed-window majority vote for physical-attack detection in video, with a perfect tracker assumed.
7. P502 AdvIT. Optical-flow consistency, above 95 percent frame detection on digital attacks (abstract).
8. P533 e-process test. Not an attack paper; the best template for a sequential statistic with a provable false-alarm bound.
9. P509 Dual-FoV. Bounded causal memory (15 frames), persistence rule (3 frames) and benign glare and rain in the same sequences.

## 4. Answers to the four questions of the brief

1. The two papers on the slide. P501 (ADAV): YOLOv5s trained on BDD100K; synthetic attacked videos made by pasting an optimized patch and moving it by a random walk; 100 clean plus 100 attacked videos, 240000 frames. Reported detection for patches above scale 0.8: accuracy 0.88, precision 0.83, recall 0.95; for smaller patches 0.67, 0.71, 0.52. Detector mAP at IoU 0.5 is 0.36 attacked and 0.44 clean with ADAV against 0.22 and 0.46 without. A false-alarm rate is not stated in the text read; the authors say a high recall matters more than low false positives because the second stage leaves clean frames unchanged. P514 (physics-aware): attacks RP2, CAPatch and SLAP applied to clips from nuScenes, KITTI and BDD100K; threshold 0.2 chosen so benign false positives stay below 5 percent; its Table 2 lists the module false-positive rate between about 0.015 and 0.125 depending on setting; a check-aware attacker lowers correction accuracy to 0.724 (P514).
2. Latency and memory, fixed false-alarm rate. Latency or run time: P501 (FPS on a T4: 56 clean, 20 attacked), P512 (about 3.1 ms per frame, 0.0013 s per iteration), P514 (19 ms overhead), P506 (hardware overhead named), P509 (voting delay 167 to 233 ms), P534 (embedded run time named), P539 (inference time and FLOPs), P511 (1.03 times overhead). Memory: no peak-RAM figure in any text extract read; abstract-only rows could not be checked. False-alarm control: P514 (threshold for under 5 percent), P510 (5 percent operating point), P534 (false positives per 100 runs). None of the records read compares methods at matched false-alarm rates or reports false alarms per hour of benign driving.
3. Sequential tests and abstain. For attack detection on camera detector outputs: none found in the records read. Nearest: majority vote over a window (P504); accumulated residuals with a Warning state (P512); watch set with failure warning (P511); CUSUM on conformal p-values of camera sequences for replay and stuck-camera attacks (P534). Outside attacks: e-process (P533), SPRT with undecided frames (P529), CUSUM variants (P530, P532). Abstain exists in P535 (images) and P536 (AV perception under perturbation).
4. Public video with physical or injected attacks and licences. P545 Drive-By-Fly-By (44 real scenarios, backdoor triggers, licence unread). P511 repository assets (road and laboratory sequences, patches; a licence and a patent notice exist, text unread). P505 AdvNet (physical sign images; location unread). P543 PADetBench (CARLA images, MIT per README). P544 CARLA-GeAR (CARLA datasets, licence unread). P509 benchmark (500 one-second sequences) built from four sources whose README lists research-only, CC BY-NC 4.0, MIT and by-request terms, combined non-commercial. P542 BDD100K carries no attacks; data licence: educational, research and not-for-profit use free, commercial use for BDD and BAIR Commons members, toolkit code BSD 3-Clause. A physical sign-attack paper (arXiv 2201.06192, seen in one search result only, not catalogued) says more than 1,000 video clips are on its demo site; licence unread.

## 5. Gaps and what is left to test (hypotheses, not results)

- Matched-FPR, held-out-recording comparison of a two-frame rule (P501), a tracker watch rule (P511) and a cue accumulator. None found in the records read.
- Warning time from attack onset in frames or seconds. Reported by P512, P511 (3 frames), P509, P534; not by P501.
- False alarms per hour on long benign driving, including benign look-alikes (occlusion, edge exit, glare, rain). P512 reports rain, fog and bump failures; P509 includes glare and rain; none gives a per-hour rate.
- Peak memory of a bounded-memory accumulator against a per-object tracker whose cost grows with injected boxes (P525).
- Abstain output: count of undecided cases, coverage against risk, for attack detection. Only analogues exist (P529, P536).
- First-sighting suppression (P511 limitation): a cue check that needs no prior track.
- Adaptive attacker against the accumulator itself (P516, P514 Table 5 show the check can be targeted).
- Real physical clips: how well a detector tuned on injected clips keeps its ranking on a small real set (P545, P511 assets).

## 6. Datasets, benchmarks and code seen

| Item | What | Licence or status as read |
|---|---|---|
| BDD100K (P542) | 100K dashcam videos, tracking subset 2,000 | Data and labels: UC Regents licence, educational, research, not-for-profit use free; code BSD 3-Clause (documentation page read) |
| Argoverse-HD | Streaming perception set used by P537 to P540 | Not read |
| nuScenes, KITTI | Used by P514 and others | Not read |
| PADetBench (P543) | CARLA physical-attack benchmark | Code MIT (README); datasets on Hugging Face; dataset terms unread |
| CARLA-GeAR (P544) | CARLA dataset generator | Not read |
| AdvNet (P505) | Clean and physical traffic-sign images | Not read |
| Drive-By-Fly-By (P545) | Real videos with physical triggers | Paper licence CC BY-NC-SA 4.0 per search record; dataset terms unread |
| AdROD repository (P511) | Patches and road and laboratory sequences; code withheld | Licence and patent notice exist, text unread |
| P509 benchmark | 500 sequences from aiMotive, Waymo, Udacity, Texas | README: research-only, CC BY-NC 4.0, MIT, by request; combined non-commercial |
| StreamYOLO, LongShortNet, DAMO-StreamNet code | GitHub repositories seen in results | Licence unread |
| Static patch-defense benchmark | arXiv 2508.00649 (94,000 images, 94 patch types); repository name APDE | Side finding for slide 01 (the APDE label); not catalogued here |

## 7. Leads of the brief and extra candidates

All eleven leads of the brief were identified from a record read (three of them, P502, P510 and P514, remain UNVERIFIED by the script):
- ADAV: P501. Physics-aware 2026: P514. PercepGuard: P510. AdvIT: P502. ICLR 2020 attack on tracking: P520. CCS tracker hijacking: P521 (2022) and P522 (2025). Towards Streaming Perception: P537. StreamYOLO: P538. arXiv 2401.04942: Latency-aware Road Anomaly Segmentation in Videos (P541). arXiv 2509.13181: Road Obstacle Video Segmentation (Rai et al., 2025; image and video obstacle segmentation, no attacks; recorded in section 9, not catalogued). BDD100K video: P542.

Leads not confirmed (extra candidates seen in results, 8):
1. F&F Attack against multiple object trackers (ICCV 2023, Zhou et al.): title and venue read from a CVF PDF in a search result; no arXiv hit, no DOI; not catalogued.
2. WIP paper on the practicality of attacks on object tracking (NDSS VehicleSec 2023): first author not seen.
3. Kalman-filter based patch-attack defense for multi-target tracking (ICIT 2023, DOI 10.1109/icit58465.2023.10143128): first author not seen.
4. AVMON (VehicleSec 2024, DOI 10.14722/vehiclesec.2024.23029): authors not seen.
5. Real-time adaptive sensor attack detection with CUSUM and a deadline (autonomous CPS): authors and venue not seen.
6. Adversarial resilience in sequential prediction via abstention (NeurIPS 2023): arXiv search found nothing; theory.
7. Attention-aware temporal adversarial shadows on traffic sign sequences (CVPR 2025 workshop): first author not seen; shadow track.
8. Defending driving perception against adversarial object-based attacks via motion planning (ACM, DOI 10.1145/3774906.3800480): authors not seen.
Tried and failed: arXiv title searches for AdvIT, AD2, PercepGuard, VisionGuard (CCS), PhySense, PhyScout and the physics-aware paper returned no preprints.

## 8. Verification and tool notes

- Crossref: search-crossref returned HTTP 429 (STOP_HOST) on the first AdvIT search; a second Crossref call issued in parallel had already returned three records (one used: P521). No Crossref call afterwards. Cause: two lit_verify calls issued in parallel; do not repeat.
- Nine rows are UNVERIFIED and carry NEEDS_VERIFY: P2-P502, P2-P507, P2-P510, P2-P512, P2-P513, P2-P514, P2-P515, P2-P517, P2-P534. DOIs in P510, P512, P513, P514, P515, P517 and P534 were read from URLs or PDF text in search results.
- OpenAlex cross-read (not counted as verification by the checker): the DOIs of P501, P506, P512, P513, P514, P515, P517, P521, P522, P534 and P543 resolved to the same title and year; the DOI of P510 (10.5555 prefix) had no OpenAlex record.
- ARXIV_API_VERIFIED rows: title, first author and year (within one year) match the arXiv record. Preprint records: check for a published version before citing. Year choices: P542 uses 2018 and P544 uses 2022 because the arXiv record year is the check basis.
- Name collisions: VisionGuard (Kantaros, P505), VG* (P504) and VisionGuard (Han, CCS 2024, P512) are three different works.
- Text in results: no instruction aimed at agents was seen; one irrelevant company-profile page appeared in a results list and was ignored.

## 9. Exclusions (not catalogued)

- LiDAR-only work: benchmark ATLAS (arXiv 2606.02924; its 32-frame alternating attack schedule is a transferable idea) and temporal consistency checks for LiDAR spoofing (arXiv 2106.07833).
- Elytra (arXiv 2506.00661): low-rank patching for classification, no temporal element.
- PAT (arXiv 2109.05695): frame detector for video classification, digital; verified in the ledger, Low relevance.
- Murguia et al. (arXiv 1710.04407): generic CPS CUSUM versus chi-squared; verified in the ledger; covered by P532 and P534 for this purpose.
- SlowTrack (arXiv 2312.09520): digital latency attack; verified in the ledger; covered by P525.
- Revisiting adversarial perception attacks and defenses on a production ADS (arXiv 2505.11532): non-temporal defenses; verified in the ledger; Low.
- Road Obstacle Video Segmentation (arXiv 2509.13181) and ARMBench (static BDD100K images, digital attacks): no attack-in-video setting.
- A study of camera-based 3D detection robustness (arXiv 2301.10766) reports that multi-frame benign inputs help against attacks; BEV detectors, not catalogued.
- Demo version of the CCS hijacking paper (Crossref record in the ledger) and an unrelated dissertation hit from the same search.

## 10. Problem cards (house layout of state/DECK_DIGEST.md section 3, moved to attack detection)

Each card states a hypothesis, not a result. Laptop limits (deck section 4): one laptop, 32 GB RAM, several TB SSD, GPU and VRAM not known; CPU baselines and frozen features first; cache cue features on disk; split by recording, never neighbouring frames; record each licence before download or release.

### Card 1 - A two-frame check judges a vanishing object on one comparison
- Problem: ADAV decides from one comparison between the current detector output and the output 0.5 s earlier, with a tuned threshold and a reference assumed clean (P501).
- Contribution to test: a causal accumulator (CUSUM or e-process) over the same per-frame disagreement score, with a bounded window, gives higher recall or earlier warning than the single comparison at the same false-alarm rate. Prior work already covers the two-frame rule (P501), window voting (P504, P509) and accumulators outside attack detection (P530, P532, P533).
- Open-source starting point: YOLOv5-class detector, OpenCV, NumPy implementations of the CUSUM and e-process formulas given in P530, P532, P533; no ADAV code seen, so re-implement from the paper.
- Data and laptop fit: BDD100K 40 s clips at 30 fps; the ADAV evaluation size was 200 clips, 240000 frames (P501), a size to test with a fit run on CPU. Licence question: BDD100K data terms allow research and not-for-profit use; whether attacked derivative clips may be shared is not stated (P542).
- Experiment workflow: (1) re-implement the two-frame rule and a pasted-patch generator on BDD100K clips; (2) add each accumulator on the same score; (3) calibrate thresholds on a separate calibration split to a fixed false-alarm rate on benign clips; (4) report recall at matched false alarms, delay in frames, ms per frame, memory.
- Success measure: detection delay and recall at matched false alarms against the two-frame rule, on recordings not used for calibration.
- Sources: P501, P504, P509, P529, P530, P531, P532, P533.

### Card 2 - A vanished object may be attacked, occluded or leaving the view
- Problem: AdROD-II separates abrupt from gradual disappearance and waits 3 frames (P511); no record read measures how often benign abrupt losses occur on driving video or reports an abstain output for them.
- Contribution to test: a three-way output (alarm, no alarm, abstain) driven by track quality and occlusion cues; abstaining at a set risk level cuts false alarms on occlusion and edge exits at a small cost in recall. Prior work covers the watch set and failure warning (P511), the Warning state (P512) and abstention outside attack detection (P535, P536).
- Open-source starting point: OpenCV Kalman filter and a simple IoU tracker; the thresholding design of P536; the watch-set logic described in P511 (code withheld).
- Data and laptop fit: BDD100K tracking labels give track start and end events (benign disappearances); whether occlusion flags exist in the label format is to be checked; synthetic vanishing at known times from card 4. Licence: as card 1.
- Experiment workflow: (1) extract benign abrupt and gradual track losses from the labels; (2) inject vanishing events at known onsets; (3) fit the three-way rule on a calibration split; (4) report coverage, abstain rate, false alarms per hour, recall among decided cases and time to decision.
- Success measure: false alarms per hour of benign driving at a given recall, and the count of cases with no usable evidence.
- Sources: P511, P512, P535, P536, P529, P533, P517.

### Card 3 - Trajectory-plus-looks checks are compared at unequal false-alarm rates
- Problem: P514 sets its threshold for under 5 percent benign false positives but lists baselines at other rates (PercepGuard 0.236 against 0.041), with attacks inserted into clips of public sets.
- Contribution to test: a matched-false-alarm protocol on held-out recordings comparing cheap frame cues (optical flow, local light, appearance consistency) with a track-consistency baseline rebuilt from the descriptions of P510 and P514. Hypothesis: the cue accumulator is not worse than the track-only baseline at matched false alarms, and the combination helps unseen attacks. Prior work covers the track-based checks and adaptive-attack results (P510, P514) but not a matched comparison with cheap frame cues.
- Open-source starting point: OpenCV optical flow, scikit-learn; no code of P510 or P514 seen; PADetBench and CARLA-GeAR for attacked renders (P543, P544).
- Data and laptop fit: BDD100K plus injected clips; CARLA rendering needs GPU time not known on this laptop (fit test first). Licence questions: nuScenes and KITTI not read; CARLA-GeAR not read; PADetBench code is MIT.
- Experiment workflow: (1) fix attacked and benign recordings with a recording-level split; (2) implement the baselines and the cue scores; (3) set every method to one false-alarm rate on calibration recordings; (4) compare recall, delay and ms per frame on held-out recordings, then repeat with a check-aware attacker (P516).
- Success measure: recall gain at matched false alarms by recording, with the adaptive-attacker result reported beside it.
- Sources: P510, P514, P512, P516, P502, P503, P543, P544.

### Card 4 - Real attack video is scarce, so injected benchmarks need a protocol
- Problem: ADAV used pasted patches moved by a random walk on 100 clips (P501); the few real physical-attack video sets found are a backdoor set (P545), repository assets (P511) and sign images (P505).
- Contribution to test: a reproducible injection protocol (patch overlay with random walk and scale change, tracker-hijack style box shifts, onset labels with ambiguity intervals, benign hard negatives such as glare and occlusion) shared as scripts, not clips. Hypothesis: a detector tuned on injected clips keeps its ranking on a small set of real physical clips. Prior work covers the overlay recipe (P501), generators (P543, P544) and real clips (P545).
- Open-source starting point: P501 recipe, PADetBench and CARLA-GeAR pipelines, CVAT for onset labels (named on the deck).
- Data and laptop fit: BDD100K clips; label time grows with clip count, so start with 50 to 100 clips. Licence questions: BDD100K derivative sharing, Drive-By-Fly-By terms, AdROD asset licence and patent notice, CARLA-GeAR terms.
- Experiment workflow: (1) write the injector with a fixed seed and hash of inputs; (2) label onset frames with an ambiguity interval and a second reviewer on a sample; (3) split by recording; (4) check that rankings of two or three detectors agree between injected and real clips.
- Success measure: agreement of method ranking between injected and real clips, and label agreement on onset.
- Sources: P501, P542, P543, P544, P545, P505, P520, P524.

### Card 5 - Check latency and attacker compute budget are not reported together
- Problem: records report FPS (P501), ms per frame (P512, P514, P539) and voting delay (P509); no text extract read reports peak memory, and compute-time attacks change the timing of tracker-based pipelines (P525).
- Contribution to test: a stage-timed harness with p50 and p95 latency and peak memory; warning time scored against the world state at output time using the streaming-accuracy idea (P537); a test of whether phantom-box load breaks the p95 budget of a per-object tracker check while a bounded accumulator stays flat.
- Open-source starting point: StreamYOLO, LongShortNet and DAMO-StreamNet code for timing references (licences unread); ONNX Runtime; a replay harness as named on the deck.
- Data and laptop fit: BDD100K clips replayed at 30 fps; CPU timing first. No new data licence beyond card 1.
- Experiment workflow: (1) time decode, detector, tracker and check separately; (2) score alarms against the world state at output time; (3) add phantom boxes in the SlowPerception style at the detector output and re-time; (4) report p95 ms, peak RAM and warning time per recording.
- Success measure: p95 end-to-end latency and peak memory per recording, and warning-time gain at matched false alarms.
- Sources: P537, P538, P539, P540, P541, P525, P512, P501.
