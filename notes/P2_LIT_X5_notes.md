# P2_LIT_X5 notes - lightweight and embedded attack detection

Task LIT_X5 (brief briefs/LIT_X5.md). Writer's own work, not audited. Rows: work/LIT_X5/rows.jsonl; verification states come from scripts/rows_check.py and the ledger work/LIT_X5/verify_ledger.jsonl, never from this file. Read depth: abstracts or search snippets only; no full text was read. Where a number below comes from a full-text passage, that passage was seen inside a web search snippet and is labelled "snippet". Every row is a lead for the owner to read, not a finding. Claim families: X5-F1 lightweight attack detection on embedded hardware; X5-F2 compression and quantization effects on robustness and detection; X5-F3 latency and memory reporting practice in defense papers.

Counts at the end of the run (scripts/rows_check.py): 22 rows, 0 schema problems; VERIFIED 21, UNVERIFIED 1 (P2-P1425, arXiv id only, NEEDS_VERIFY); High 10, Medium 12; read level 13 abstract, 9 metadata-only; families X5-F1 9, X5-F2 9, X5-F3 4; 3 problem cards; 14 unconfirmed leads and 10 confirmed records not catalogued (section "Leads"). Leads are cited in the text as "lead N"; they are not rows. AdROD is cited as P2-P511, a row of LIT_A5.

## Uncomfortable findings first
1. The "cheap always-on check, expensive defense only on alarm" shape is already published for patch attacks on detectors, with real-time numbers: ARES (P2-P1401, mode switch plus schedulability analysis), AdROD (P2-P511, anomaly detector always on, ensemble on demand, measured on a Jetson AGX Xavier against a 100 ms deadline) and ADAV (P2-P1420, two-stage detection with clean and attacked FPS measured separately). The design slides' shared pipeline (frozen detector, cheap cue, decision) is therefore not new as a system shape. What none of the rows in this sample uses as evidence is a physical cue (shadow geometry, reflection, illumination, flicker): to our knowledge from this sample, the cue-consistency evidence remains the distinct element. A wider search is needed before any claim.
2. Attacks can target the time budget itself (P2-P1409: phantom boxes overload non-maximum suppression and cut a Jetson Orin NX from real time to 13 FPS). A lightweight checker that is only timed on clean frames can miss its deadline under attack.
3. The lightweight detector a vehicle can afford is the easier one to fool: smaller YOLO models were less robust to naturalistic patches than larger ones (P2-P1405). Quantization is no reliable shield: apparent robustness of low-bit models is gradient masking (P2-P1404), and patch attacks keep high success even at 2-bit precision (lead 22).
4. No row in this sample reports p95 or tail latency, peak memory, or latency of the defense while another network shares the GPU, for a physical-attack detector. Mean milliseconds per image or FPS on a single GPU is the norm (P2-P1410, P2-P1402, P2-P1420); where the GPU is named it is a server or desktop card (T4, GTX 1080 Ti), and Jetson results appear only for latency-attack and ensemble defenses (P2-P1409, P2-P511, lead 21). This is a reporting gap the owner can fill, not a method gap.

## Problem map (attack families, from the angle of compute)
| Attack family | Rows that define or use it here | Compute angle |
|---|---|---|
| Physical and naturalistic patch hiding attacks on person and vehicle detectors | P2-P1405, P2-P1402, P2-P1410 | Smaller edge detectors are easier targets (P2-P1405) |
| Hiding and appearing (fabricated object) patch attacks | P2-P1402, P2-P1410 | Defense time per image differs up to about 700 times between the fastest and slowest defense (P2-P1410, snippet) |
| Object-vanishing patches in driving video | P2-P1420 | Defense cost differs for clean and attacked frames |
| Latency (availability) attacks: phantom candidate boxes overload NMS | P2-P1409 | The attack target is the frame deadline itself |
| Compression-aware attacks: perturbations crafted against compressed models | P2-P1408, lead 22 | Deployment compression opens its own attack surface |
| Adversarial traffic signs checked by a large multimodal model | P2-P1413 | Verifier too heavy to run every frame; gated by distance |
| Digital L-p perturbations on quantized classifiers | P2-P1404, P2-P1406, P2-P1425 | Background for what bit-width does to robustness |

## Solution map (defense and detection families, with the cost each reports)
| Family | Rows | What is reported about cost |
|---|---|---|
| A. Cheap input-side patch detection or masking in front of an unchanged detector | P2-P1402, P2-P1415, P2-P1416, P2-P1407 | Added time 8 percent (P2-P1402, abstract), about 4 percent (P2-P1415, snippet), ms per image (P2-P1416), localization under 1 ms while inpainting takes about 55 ms (P2-P1407, snippet) |
| B. Internal-activation detection at about one inference | P2-P1403, P2-P1414, P2-P1417, P2-P1412 | Time cost versus other defenses (P2-P1403); single pass per frame (P2-P1414); energy on accelerators (P2-P1417, P2-P1412) |
| C. Detect, then escalate to a heavy defense | P2-P1401, P2-P511, P2-P1420, P2-P1413 | FPS and schedulability (P2-P1401); FPS on a Jetson AGX Xavier (P2-P511); clean versus attacked FPS on a T4 GPU (P2-P1420) |
| D. Scheduling and system co-design | P2-P1411, P2-P1401 | Speed gain when denoiser and protected model share an embedded GPU (P2-P1411) |
| E. Robust training or ensembles sized for the edge | P2-P1409, lead 21 | FPS on Jetson boards (P2-P1409); ensemble renewal time on a Jetson AGX Xavier (lead 21) |
| F. Quantization-aware robustness | P2-P1425, lead 22 | Robustness per bit-width, no detector-of-attack timing |

## Answers to the brief's questions
### Q1. Which attack detectors report latency, memory or energy, and on which hardware
| Row | What is timed | Measure | Hardware named | Where read |
|---|---|---|---|---|
| P2-P1401 ARES | Detection pipeline with mode switch | Overall FPS, schedulability | Not named in the abstract | Abstract |
| P2-P1402 NutNet | Patch detector in front of six detectors | Added inference time (8 percent), FPS on KITTI images | GPU not seen | Abstract; arXiv snippet |
| P2-P1403 LanCeX | Activation-inconsistency detection | Time per attack (521 ms versus more than 1813 ms) | Not identified | Abstract; full-text snippet |
| P2-P1407 SAR | Localization and inpainting | ms per component | Not seen | Snippet |
| P2-P1409 Underload defense | Detector plus NMS under latency attack | FPS and ms per frame | Jetson Xavier NX, Jetson Orin NX, RTX 4070 Ti Super, A100 | Abstract; snippet |
| P2-P1410 Benchmark of 11 defenses | Nine defenses | Mean ms per image | Not seen | Snippet |
| P2-P1411 eDenoizer | Denoiser plus protected classifier | Speed gain | Embedded GPU, board not named | Abstract |
| P2-P1412 RobustEdge | Reduced-precision detector at the edge | Energy | 45 nm CMOS accelerator; Raspberry Pi comparison | Abstract |
| P2-P1413 LMM verifier | GPT-4V check near signs | Activation distance; no latency seen | ZED Box with ZED X camera | Snippet |
| P2-P1414 ACAT | Multi-frame shallow-layer defense | Total inference time with and without defense | Not seen | Snippet |
| P2-P1415 UAV patch defense | Tiny patch model | Added time per image, parameter count | Not seen | Snippet |
| P2-P1416 Universal defensive frame | Input frame | ms per image | GTX 1080 Ti | Snippet |
| P2-P1417 Noise-sensitivity detector | Small detector after an early layer | MAC and memory-access energy; AUC versus bit precision | Precision-scalable hardware accelerator (energy analysis) | Snippet |
| P2-P511 AdROD (LIT_A5 row) | Anomaly detector plus on-demand ensemble | FPS (5.4 always-on ensemble; 68.7 attack-free; 13.9 average) | Jetson AGX Xavier | Snippet |
| P2-P1420 ADAV | Two-stage detection and masking | FPS clean 56, attacked 20; baselines LGS 35, JPEG 8 | T4 GPU | Snippet |
| Lead 21 Sardino (unconfirmed, no row) | Dynamic ensemble renewal | Validation time 7.2 s for a 100-DNN ensemble | Jetson AGX Xavier | Snippet |
Memory: no row reports peak RAM or VRAM of a defense. Parameter count is the only size figure seen (P2-P1415). Energy appears only in classifier-level hardware papers (P2-P1412, P2-P1417).

### Q2. What quantization or pruning does to robustness and to detector-of-attack accuracy
- Robustness of the protected model: low-bit quantization gives no robust protection; apparent gains are gradient masking, and examples transfer poorly across bit-widths (P2-P1404). Quantized models were found more vulnerable under FGSM than full-precision ones (P2-P1425), while a later benchmark found quantized models more robust to attacks but weaker under natural corruption and processing noise (P2-P1406). The two results disagree; the gradient-masking explanation of P2-P1404 is one way to reconcile them. Patch attacks keep high success across bit-widths (lead 22), so pixel-level transfer failure does not carry over to patches. Compressed detectors can be targeted through the gap to their dense reference (P2-P1408). Review of the evidence: naive pruning and quantization can reduce robustness; past a critical compression ratio robustness falls first (P2-P1418).
- Detector-of-attack accuracy: evidence exists only for classifiers. A small detector's AUC was tracked across weight and activation bit precision (P2-P1417; direction of the effect not seen); 16-bit and 12-bit edge detectors kept AUC above 0.9 against gradient-based attacks and above 0.7 against score-based attacks (P2-P1412). For backdoor defenses, INT8 quantization lowered the aggregate detection rate of five defenses from 20 to 0 percent while backdoors stayed active (lead 23). No row reports what INT8 does to a physical-attack detector for an object detector: open question.
- Benign side: quantized classifiers were more vulnerable to natural corruption and processing noise than float ones (P2-P1406). For YOLO detectors, static INT8 gave speedups, and calibrating with degraded images did not consistently improve robustness, except possibly against noise in larger models (P2-P1423). Pruned detectors on driving data lost robustness unevenly across distortion types and classes (P2-P1419). Whether INT8 raises false alarms of a consistency checker at night is untested.

### Q3. Which reporting practice exists
- Mean time per image or FPS on one GPU: P2-P1410, P2-P1402, P2-P1416, P2-P1420, P2-P1409.
- Separate clean and attacked latency: P2-P1420 (FPS), P2-P511 (attack-free versus average FPS with on-demand ensemble).
- Deadline and schedulability: P2-P1401, P2-P511 (100 ms perception deadline), P2-P1411.
- Energy: P2-P1412, P2-P1417.
- p95 or tail latency, peak memory: not seen in any row. The only p95 figure seen in this run was in a public repository on INT8 YOLO under degradation, not in a paper (Leads, item 14).

## Closest prior work to the owner's design slides (ranked)
1. P2-P511 (LIT_A5 row) AdROD - always-on anomaly detector, on-demand heavy defense, Jetson AGX Xavier timing against a 100 ms deadline. Threatens the system-level framing of contribution 5 and slide 05 (bounded evidence with measured latency). Differs: the trigger is not a physical cue, and no explanation output is described in the snippet. Preprint, not peer reviewed.
2. P2-P1401 ARES - detection-triggered switch to a certifiably robust detector with schedulability guarantees. Threatens any claim that gating heavy defenses by a cheap detector is new. Differs: trigger quality is not evaluated in the abstract.
3. P2-P1414 ACAT - one inference pass per frame, attack trace carried across frames by shallow-layer channel attention. Closest to slide 05 "bounded frame memory at low cost"; segmentation rather than detection. Also catalogued by LIT_A5 (P2-P508).
4. P2-P1420 ADAV - named on slide 05 already; adds measured clean versus attacked FPS that the owner's comparison must match. LIT_A5 covers it as a video paper (P2-P501); duplicate on purpose for the timing angle.
5. P2-P1402 NutNet - the overhead bar (8 percent) for slide 01 and the best defense in the P2-P1410 benchmark.
6. P2-P1403 LanCeX - embedded-oriented activation-inconsistency detector including object detection; precursor of the "one inference cost" claim.

## Gaps and what is left to test
1. Timing under the vehicle's conditions: p50 and p95 per-frame latency including decode and queueing, peak memory, with the detector running concurrently, on clean and on attacked clips, for the checker and two or three baselines. Not seen in any row.
2. Precision sweep for the attack detector: FP32, FP16 and INT8 detector with the checker on top; attacks crafted on each precision and transferred. Not seen for physical attacks on object detectors (Q2).
3. Escalation trigger quality: if the cue checker is the trigger of a detect-then-escalate pipeline, its miss rate bounds safety and its false alarms bound throughput. ARES and AdROD time the pipeline but the trigger's matched-false-alarm performance is not visible in what was read.
4. Latency attacks against the checker itself: does a crafted input inflate the checker's own cost (as P2-P1409 does for NMS)?
5. Benign degradations after compression: whether INT8 raises false alarms of a consistency check at night (P2-P1406 suggests the risk for classifiers; P2-P1423 found the calibration choice changes little for YOLO).

## Problem cards (hypotheses, not results)

### Card X5-1. The attack detector is never timed the way the vehicle runs it
- Problem: defense papers report mean ms per image or FPS on one GPU for clean inputs; tail latency, peak memory, attacked-frame latency and GPU sharing are missing, so "lightweight" cannot be compared.
- Contribution to test: a timing protocol for the owner's cue checker and two or three baselines (NutNet, LGS, SAC as in P2-P1410): p50 and p95 end-to-end latency, peak RAM and VRAM, clean versus attacked clips, detector and checker sharing the GPU. Prior work already reports mean time per image (P2-P1410) and clean versus attacked FPS (P2-P1420); the contribution is the tail, memory and concurrency part.
- Open-source starting point: a YOLO nano detector exported to ONNX Runtime (deck card 10); baseline code from the P2-P1410 benchmark if released (not seen); NutNet demos (UNVERIFIED code).
- Data and laptop fit: 10-core CPU, 32 GB RAM, laptop GPU with 6 GB; nano or small detectors at 640 px fit; subsample the 94,000-image patch set of P2-P1410 and a few BDD100K clips with synthetic patches (as P2-P1420). Licence questions: the P2-P1410 dataset licence is unknown; BDD100K and INRIA terms must be recorded before use.
- Experiment workflow: (1) freeze the detector and export it; (2) wrap checker and baselines in a timestamped replay harness that includes decode and queueing; (3) run clean and attacked clips with detector and checker on the same GPU, logging per-frame latency and peak memory; (4) report p50, p95, peak memory and FPS under attack at matched false-alarm points.
- Success measure: hypothesis that the checker's added p95 latency stays a small fraction of the detector's p95 at the same false-alarm rate, and that its attacked-frame latency does not exceed its clean latency by more than a stated bound.
- Sources: P2-P1410, P2-P1402, P2-P1420, P2-P1409, P2-P511, P2-P1411.

### Card X5-2. INT8 deployment may silently change both the attack and the attack detector
- Problem: compression shifts robustness (gradient masking, patch transfer across bit-widths) and may shift the ROC of a detector-of-attack; for physical attacks on object detectors no measurement was seen.
- Contribution to test: TPR at a fixed false-alarm rate of the cue checker and of an activation-based baseline for FP32, FP16 and INT8 detectors, with patches crafted on FP32 and on INT8 (transfer and adaptive), plus benign degradations as hard negatives. Classifier-level evidence exists (P2-P1417, P2-P1412, lead 23); the detection-level, physical-attack part is untested in what was read.
- Open-source starting point: YOLO nano with ONNX Runtime static quantization (deck card 10); calibration recipes from P2-P1423 (code location seen in search, UNVERIFIED); patch generator code of P2-P1405 (UNVERIFIED).
- Data and laptop fit: INRIA Person for patches, a traffic-sign set for sign attacks (licence to record), COCO-style degradations; all INT8 and FP16 inference fits the 6 GB GPU or the CPU. Licence question: Ultralytics code licence and each dataset's terms.
- Experiment workflow: (1) quantize the detector (static INT8, clean and mixed calibration); (2) craft patches on each precision and test transfer both ways; (3) run checker and baseline on every precision; (4) compare TPR at matched FPR and false alarms under noise, blur and low light.
- Success measure: hypothesis that a physical-cue checker's TPR at fixed FPR changes less across precisions than an activation-based detector's, with no rise in benign false alarms.
- Sources: P2-P1404, P2-P1417, P2-P1412, P2-P1406, P2-P1423, P2-P1419, P2-P1405, P2-P1408, P2-P1425 (UNVERIFIED, NEEDS_VERIFY), P2-P1418. Unconfirmed leads behind the card: lead 22 (patches across bit-widths) and lead 23 (defenses failing after INT8).

### Card X5-3. A cheap always-on trigger for an on-demand heavy defense: is the trigger good enough
- Problem: ARES, AdROD and ADAV gate a heavy defense with a trigger; a missed trigger leaves the attack undefended and a false trigger costs throughput. The owner's cue checker could be such a trigger, with an explanation attached.
- Contribution to test: use the cue checker as the trigger and measure missed-attack windows, escalation delay and average FPS under realistic attack frequencies. Prior work already covers the gating and scheduling (P2-P1401, P2-P511, P2-P1420); only the cue-based trigger and its explanation would be new, to our knowledge from this sample.
- Open-source starting point: YOLO nano as the fast path; NutNet or SAC as the heavy path if code is available (not confirmed); a simple mode switch in the replay harness of card X5-1.
- Data and laptop fit: BDD100K clips with synthetic object-vanishing patches as in P2-P1420, plus benign clips as hard negatives; fits the laptop at reduced resolution. Licence question: BDD100K terms; patch generator licence.
- Experiment workflow: (1) run the fast path with the cue checker on clean and attacked clips; (2) switch to the heavy path on an alarm and back after a hold time; (3) log per-frame mode, latency and detection outcome; (4) report attack frames left undefended, mean and p95 escalation delay, and average FPS at matched false-alarm rates against an always-heavy and a never-heavy pipeline.
- Success measure: hypothesis that the cue trigger leaves fewer undefended attack frames than a patch-statistics trigger at the same false-alarm rate, while average FPS stays close to the fast path.
- Sources: P2-P1401, P2-P511, P2-P1420, P2-P1413, P2-P1411, P2-P1402.

## Datasets, benchmarks and code seen
- Patch defense benchmark dataset: 94 patch types, 94,000 images (P2-P1410 abstract). Licence not seen.
- INRIA Person, MPII Human Pose (P2-P1405); INRIA and KITTI (P2-P1402); VisDrone (P2-P1415); PASCAL VOC and BDD100K (P2-P1409); BDD100K videos with synthetic patches (P2-P1420); COCO val2017 with synthetic degradations (P2-P1423); GTSRB and CIFAR-10 (lead 23); CIFAR-10, CIFAR-100, TinyImageNet, SVHN, ImageNet (classifier studies P2-P1404, P2-P1406, P2-P1412, P2-P1417).
- Code named in records or snippets, all UNVERIFIED: github.com/Hill-Wu-1998/underload (P2-P1409); sites.google.com/view/nutnet (P2-P1402); a QRID repository for P2-P1423; a benchmark repository for lead 23; github.com/pralab/AdversarialPruningBenchmark (survey not catalogued, Leads item 6); github.com/RICE-EIC/Double-Win-Quant (Leads item 7).
- Hardware seen in records: Jetson Xavier NX, Jetson Orin NX, Jetson AGX Xavier, T4, GTX 1080 Ti, RTX 4070 Ti Super, A100, 45 nm CMOS accelerator model, Raspberry Pi, ZED Box.

## Leads not confirmed (or confirmed but not catalogued)
1. LanCe (arXiv 1910.08536), precursor of P2-P1403: arXiv page seen in search; not catalogued as a separate row.
2. DNNGuard (ASPLOS 2020, DOI 10.1145/3373376.3378532), an accelerator that runs a model and an adversarial detector together, named inside the P2-P1411 text snippet: Crossref record found, no abstract. Its successor sDNNGuard (ACM Transactions on Embedded Computing Systems 2024, DOI 10.1145/3677318): Crossref abstract read; it runs the target network and a detection network in parallel on one heterogeneous accelerator with dense and sparse support and reports an average 1.42 times speedup over compared accelerators. Not catalogued: accelerator design for classifier-level detectors, far from the laptop setting. Hardware answer to Q1 if the owner wants one.
2a. Region-aware adversarial distillation for deployment-efficient lightweight object detection (The Visual Computer 2026, DOI 10.1007/s00371-026-04758-7): Crossref record, no abstract; possibly relevant to X5-F2 (robust compact detectors). Not catalogued.
3. Defending Physical Adversarial Attack on Object Detection via Adversarial Patch-Feature Energy (ACM MM 2022, DOI 10.1145/3503161.3548362): Crossref record found, no abstract; not catalogued.
4. On the Effect of Pruning on Adversarial Robustness (ICCVW 2021, DOI 10.1109/iccvw54120.2021.00007): Crossref record, no abstract; not catalogued.
5. Robustness in Compressed Neural Networks for Object Detection (IJCNN 2021): catalogued as P2-P1419 (metadata-only).
6. Adversarial pruning: A survey and benchmark of pruning methods for adversarial robustness (Pattern Recognition 2025, DOI 10.1016/j.patcog.2025.111788): Crossref record and abstract; not catalogued (classifier pruning; covered in summary by P2-P1418).
7. Double-Win Quant (ICML 2021, PMLR page seen in search): no id checked; not catalogued.
8. HYDRA, ATMC, HARP, MAD (adversarially robust pruning): seen in search results; not checked.
9. QUANOS (arXiv 2004.11233) and LeQC-At (DSD 2024): seen; not checked.
10. Investigating the impact of quantization on adversarial robustness (arXiv 2404.05639): seen as a reference inside another paper; not checked.
11. EdgeShield (arXiv 2408.04181, shallow-layer attention detector at the edge): seen; not catalogued.
12. DisPatch (arXiv 2509.04597, diffusion-based patch removal; 0.32 s per image on an A100 in a snippet): seen; not catalogued.
13. Information Distribution Based Defense Against Physical Attacks on Object Detection (ICMEW 2020, DOI 10.1109/icmew46912.2020.9105983): Crossref record and abstract; training-free image processing, no cost figures; not catalogued (object-appearance angle of LIT_A1).
14. A public repository on INT8 YOLOv8n under degradation reported mean and P95 CPU latency and model size: the only P95 figure seen; it is not a paper and was not checked.
15. A web search result that pointed to an IEEE Xplore page (texture-feature and local-denoising patch defense on KITTI, detection time reported as reduced): title not seen; not pursued, because IEEE Xplore is dropped as a source (COORDINATOR UPDATE 3); an open copy would be needed.
16. PAD (CVPR 2024, DOI 10.1109/cvpr52733.2024.02310): Crossref record; slowest defense in the P2-P1410 table; object-appearance angle of LIT_A1.
17. FPGA, Edge TPU or microcontroller implementations of physical-attack detectors: two websearch queries and two rephrasings returned nothing; Crossref fallback returned no relevant record. Not found, which is not evidence of absence.
18. An IV 2024 paper by the first author of P2-P1413 (DOI 10.1109/iv55156.2024.10588595): Crossref record only.
19. Defenses Against Adversarial Attacks on Object Detection: Methods and Future Directions (Information 2025, DOI 10.3390/info16111003): Crossref abstract read; the survey excludes patch and physical attacks, so it is outside this angle; not catalogued.
20. Physical Invariant Based Attack Detection for Autonomous Vehicles: Survey, Vision, and Challenges (MetroCAD 2021, DOI 10.1109/metrocad51599.2021.00014): Crossref record only; the title matches the physics-consistency idea of the design slides; passed to the coordinator for the runtime-monitoring or consistency tasks; not read.
21. Sardino: Ultra-Fast Dynamic Ensemble for Secure Visual Sensing at Mobile Edge (arXiv 2204.08189, id from a search result address). Full-text snippet: validating a renewed 100-DNN ensemble with 4,410 samples takes about 7.2 s on a Jetson AGX Xavier, so per-frame renewal is not possible; a traffic sign recognition application is included. First author and venue not seen; no Crossref record found; arXiv not callable in this run (shared stop). NEEDS_VERIFY. Cited above as lead 21.
22. Breaking the Limits of Quantization-Aware Defenses: QADT-R for Robustness Against Patch-Based Adversarial Attacks in QNNs (arXiv 2503.07058, id from a search result address). Snippet: adversarial patches keep attack success above 70 percent even at 2-bit precision; patch-based adversarial training generalizes poorly to unseen bit-widths. Classification. First author and venue not seen; Crossref search found nothing; arXiv not callable in this run. NEEDS_VERIFY. Cited above as lead 22.
23. Quantization Blindspots: How Model Compression Breaks Backdoor Defenses (arXiv 2512.06243, id from a search result address). Snippet: INT8 quantization lowered the aggregate detection rate of five backdoor defenses from 20 to 0 percent while backdoor attack success stayed above 99 percent (BadNet trigger; GTSRB and CIFAR-10). Backdoors are a training-time threat, so this is an analogy for detectors of attack, not a physical-attack result. First author not seen; Crossref search found nothing; arXiv not callable in this run. NEEDS_VERIFY. Cited above as lead 23.
24. Overload latency attack on object detection for edge devices (title from memory, the attack family behind P2-P1409): one websearch returned nothing; not confirmed.

## Exclusions (outside the subject or the angle)
- Bit-flip and fault attacks on accelerators with performance-counter monitors (BARE-AI, SAMURAI, VERA): hardware fault or microarchitectural threats, not camera-facing attacks.
- Power side-channel detection of adversarial examples on microcontrollers (AdvScan): MCU classifiers, not camera perception.
- Compression versus robustness for EEG decoders, code language models and BERT: other modalities.
- Lightweight traffic-sign detectors with embedded timing but no attack detection (YOLOv8-CE on Jetson Nano, HAS-DETR, TurboCBAM, a Raspberry Pi 5 with Edge TPU study): detector efficiency only; useful only as timing references.
- Side-channel attacks on embedded neural networks survey: model-extraction threats.

## Run notes
- Websearch returned results for 10 queries, then returned nothing from about 23:44Z for every query; Crossref search was used as the fallback.
- arXiv: a shared stop for export.arxiv.org was in force for the whole run; arXiv was never called and, per the launch rule, was treated as ended for this run. Consequences: leads 21 to 23 have no first author and stay leads; P2-P1425 is UNVERIFIED; rows P2-P1414 to P2-P1420 and P2-P1425 stay metadata-only (their arXiv abstracts were not read).
- Budget used: websearch 18 of 40 (10 with results, 8 empty); lit_verify 29 of 50 (28 answered by Crossref, 1 STOP_HOST).
- Crossref: after 29 lit_verify calls the shared Crossref stop (set by another agent after a 429) answered STOP_HOST; Crossref was not called again. All Crossref records used by the rows were already in the ledger.
- No instruction-like text was found in search results or API answers.
- Cross-task duplicates (for the coordinator): AdROD is catalogued by LIT_A5 as P2-P511 and is cited here under that id without a row of its own; P2-P1420 (ADAV) = P2-P501 of LIT_A5; P2-P1414 (ACAT) = P2-P508 of LIT_A5; P2-P1410 (patch defense benchmark) = P2-P1025 of LIT_X1. The rows here add the timing angle only. AdROD figures quoted in this file come from search snippets of the arXiv HTML read by this agent; LIT_A5 read it in more depth.
