# P2_LIT_X3 notes - open code, small models and Hugging Face Hub inventory

Task LIT_X3 (wave 2, continuation agent). Brief: briefs/LIT_X3.md. Rows: work/LIT_X3/rows.jsonl, 16 rows, paper_id P2-P1201 to P2-P1216 (rows_check: 0 problems, VERIFIED 11, ARXIV_API_VERIFIED 5). NOT AUDITED: written by this agent; fresh-agent audit required.

Reading rules used here:
- websearch returned nothing for this agent (7 of 7 queries empty, see progress/LIT_X3.log). No GitHub page, LICENSE file or project page was opened (no webfetch, no browser). Code locations come from (a) arXiv abstracts read through scripts/lit_verify.py, (b) Hugging Face Hub cards read with the read-only Hub tools, (c) the code_or_data fields of other tasks' rows (their reading, not re-checked here).
- After 3 successful arXiv calls, shared stops on export.arxiv.org and api.crossref.org were in force for the rest of this run; the leads left over are listed under "Leads not confirmed".
- A licence tag or licence sentence on a Hub card is the uploader's statement, not a verified licence. "Licence as seen" means exactly that. Download counts are the Hub listing values at read time.
- Items already catalogued by other tasks were not written again as rows: YOLOX P2-P2421, SAHI P2-P2423, MobileNetV3 P2-P2425 and Depth Anything V2 P2-P2426 (DECK_SRC); TOG P2-P2011 (LIT_X11); the person-detector patch attack of Thys et al. P2-P2309 (LIT_X14); multivariate detector calibration P2-P1516 (LIT_X6). The Hub and timing facts this task found for them are in sections B and C.

## Uncomfortable findings first
1. The attack-detection side has nothing to download from the Hugging Face Hub: 26 searches found detector and backbone weights but no model, dataset or Space from the physical-attack or attack-detection papers (section C3). Code for those papers sits in GitHub repositories whose licences nobody in this project has read: in table A a licence is recorded for 2 of 32 entries, both second-hand.
2. Reusable multi-attack harnesses already exist: PADetBench (P2-P543, LIT_A5) states 20 physical attack methods against 48 detectors in CARLA, and APDE (P2-P143, LIT_A1) states 11 patch defenses, 13 attacks and 11 detectors in one benchmark, both with code locations recorded. An own harness is not a contribution; reusing one saves time.
3. Transfer attacks threaten the cheapest independent cue: T-SEA (P2-P1210) states that one patch optimised on a single detector transfers to several black-box detectors, so a "second small detector" cue may be fooled together with the first.
4. Licence trap for a quick start: the popular community traffic-sign detectors on the Hub are ultralytics models tagged mit or apache-2.0, while Ultralytics' own cards carry agpl-3.0 (section C2).
5. No record read gives a timing on hardware like the owner's laptop (10-core CPU, 6 GB laptop GPU); the timings found are for server GPUs, phone CPUs, NPUs or an unnamed CPU (section B).
6. Several attack families have no code location at all: the abstracts of the shadow attack P2-P201, the infrared reflection attack P2-P309, GhostImage P2-P409, the two rolling-shutter attacks P2-P403 and P2-P404, and ShapeShifter P2-P108 state none (arXiv abstracts read by this task); the shadow, infrared and rolling-shutter families may need re-implementation.

## Problem map (attack families, from the reuse angle)
- Patch and sticker attacks with code locations recorded by LIT_A1 (some UNVERIFIED): RP2 P2-P101, Adversarial Patch P2-P103, naturalistic patches P2-P104 and P2-P105, camouflage P2-P106. This task adds T-SEA P2-P1210 (code named in the abstract) and DPatch P2-P1211 (no code location in the abstract). TOG P2-P2011 and the person-patch attack P2-P2309 are catalogued by other tasks; no code location was seen for either.
- Shadow attacks: P2-P201 (LIT_A2); its arXiv abstract states no code location.
- Reflected, laser and infrared light (LIT_A3): RFLA P2-P301, laser beam P2-P302, laser spot P2-P304 and near-infrared P2-P320 have code locations recorded; the infrared reflection attack P2-P309 states none.
- Projected and flickering light (LIT_A4): SLAP P2-P401, phantom objects P2-P402 and CausalAttack P2-P434 have code locations; GhostImage P2-P409 and the rolling-shutter attacks P2-P403 and P2-P404 state none.
- Digital attack libraries to stress a frozen detector or a sign classifier: ART P2-P1212 (MIT licence stated in its abstract), Torchattacks P2-P1213, Foolbox Native P2-P1214 (metadata only). CleverHans is a lead only (see "Leads not confirmed"); LIT_A1 records the cleverhans repository as the code location of P2-P103.

## Solution map (defense and detection families with reusable code)
- Patch localization and removal on detectors (LIT_A1, code locations recorded): PatchZero P2-P109, Segment and Complete P2-P110, NAPGuard P2-P114, Jedi P2-P115, PAD P2-P116, spectral defense P2-P129.
- Certifiable defenses: PatchCleanser P2-P113 with code; DetectorGuard P2-P111 and ObjectSeeker P2-P112 state no code location in their abstracts (read by this task).
- Training-free input-transformation checks: Feature Squeezing P2-P1215 (prediction consistency under squeezing) and Local Gradients Smoothing P2-P1216 (high-frequency patch localization); neither abstract states a code location.
- Physics-based detection inside attack papers: the infrared reflection attack P2-P309 states a detector based on physical properties of the reflections that catches 96% of those attacks; the rolling-shutter paper P2-P403 states a light backbone enhancement that recognizes rolling-shutter attacks (both abstracts read by this task; no code location).
- Multi-cue committee: phantom-object committee over light, context, surface and depth (P2-P402, code location recorded).
- Temporal consistency: ADAV P2-P501 (no code seen); streaming detectors with code P2-P538 to P2-P540; trackers SORT P2-P1207 and ByteTrack P2-P1208 (ByteTrack code named in its abstract); DIS optical flow P2-P1209.
- Calibration: multivariate detector calibration P2-P1516 (LIT_X6).
- Small detectors and backbones for the frozen detector and the crop classifier: PP-PicoDet P2-P1201, EfficientDet P2-P1202, MobileNetV2 with SSDLite P2-P1203, ShuffleNet V2 P2-P1204, RT-DETR P2-P1205, MMDetection P2-P1206, plus YOLOX P2-P2421, SAHI P2-P2423, MobileNetV3 P2-P2425 and Depth Anything V2 P2-P2426 (DECK_SRC).
- Toolkits and benchmarks: ART P2-P1212, APDE P2-P143, PADetBench P2-P543, REAP P2-P141.

## Closest prior work to the owner's design slides (code angle, ranked)
1. Phantom-object committee (P2-P402, LIT_A4): light camera-only models check light, context, surface and depth of each detected object; code location recorded. Closest in shape to the five slides (frozen detector, independent cues, consistency decision), for projected and displayed objects.
2. APDE (P2-P143) and PADetBench (P2-P543): ready comparison harnesses for slide 01 and for cross-attack evaluation; both state public code.
3. ADAV (P2-P501): prior-frame output consistency with T4 timings, the slide 05 baseline; no code seen, so a re-implementation must be validated against its reported numbers.
4. PatchZero (P2-P109) and Segment and Complete (P2-P110): the patch-detection baselines named on slide 01, with code locations.
5. Feature Squeezing (P2-P1215): prediction consistency under cheap input transforms, the simplest training-free consistency baseline; no code location seen.
6. X-Detect (P2-P134): explainable multi-check patch detection, closest in the explanation element; only a demo is mentioned, no code location.

## Gaps and what is left to test
- Licences: 30 of 32 code entries in table A have no licence read; the RP2 and PADetBench licences are second-hand. NEEDS_BROWSER: open each repository LICENSE file before any reuse or release.
- No downloadable attack-detection model or baseline exists on the Hub (section C3); every baseline must come from GitHub code or a re-implementation (ADAV, X-Detect have no code location).
- No laptop timing for any component (section B): measuring the full pipeline on the owner's laptop is still open (card X3-3).
- Whether a detector-disagreement cue survives transfer attacks such as T-SEA is untested in the rows read (card X3-1).
- Whether published attack code still works against the small frozen detector the design assumes is untested (card X3-2); shadow, infrared and rolling-shutter attacks have no code location.
- Family X3-F4 has 0 rows: no Hub model, Space or dataset on adversarial patches, shadows or light attacks for traffic signs links a paper, except the PADetBench dataset already catalogued as P2-P543.

## Problem cards (hypotheses, not results; card layout of state/DECK_DIGEST.md section 3)
Order and criteria: fit to the red-marked focus (lightweight, explainable, the five cues), laptop feasibility, measurability, novelty margin. X3-2 first: it is cheap, measurable and a prerequisite of every evaluation, but adds little novelty. X3-3 second: it fixes the compute budget of all slides and is fully feasible. X3-1 third: the highest novelty margin, with the largest risk from transfer attacks and from X-Detect.

### Card X3-1. A second, different small model as the independent cue
- Problem: the cheapest independent cue on a laptop is a second small model (a crop classifier or a detector of another architecture), but attacks optimised to transfer across detectors may fool both models at once.
- Contribution to test: disagreement between a one-stage CNN detector, a transformer detector and a crop classifier flags patch, shadow and light attacks at a fixed false-alarm rate, and keeps most of that recall under transfer-oriented attacks; the hypothesis fails if transfer attacks remove the gain. Prior work covers part of it: X-Detect (P2-P134) already combines several detectors with explanations, so the open part is the transfer stress test within a laptop budget.
- Open-source starting point: YOLOX (P2-P2421; apache-2.0 tags on Hub exports), RT-DETR R18 in HF transformers (P2-P1205; apache-2.0 tag), MobileNetV3-Small timm weights (P2-P2425; apache-2.0 tag), T-SEA attack code (P2-P1210), ART (P2-P1212), APDE harness (P2-P143).
- Data and laptop fit: inference of two small detectors plus one classifier, and a classifier head trained on sign crops, should fit 32 GB RAM and a 6 GB GPU; to be measured, not assumed; CPU-first for the classifier head. Licence questions: GTSRB, LISA and any Hub re-upload (LIT_X2); agpl-3.0 if an ultralytics model is used.
- Experiment workflow: (1) freeze two detectors and train only a crop-classifier head; (2) generate single-model attacks and transfer-oriented attacks from public code (table A, P2-P1210); (3) score per-object disagreement in class, box and confidence and calibrate a threshold on benign clips; (4) report recall at matched false alarms per attack family, with and without transfer attacks.
- Success measure: recall at a fixed false-alarm rate per hour of benign driving; drop of that recall under transfer attacks; added ms per frame.
- Sources: this task P2-P1205, P2-P1210, P2-P1212; other tasks P2-P2421, P2-P2425, P2-P134, P2-P143.

### Card X3-2. Do reported attack success rates hold on the small frozen detector the design uses?
- Problem: most public attack code targets large or older detectors (Faster R-CNN, YOLO and SSD in the 2018 to 2020 abstracts read); the slides assume a small frozen detector, and an attack that does not transfer to it changes which cue families matter.
- Contribution to test: a reproduction table in which each public attack generator of table A is run against the chosen small detector and a small sign classifier, with attack success compared with the paper's own number; families with no working public code are listed as gaps. The hypothesis fails if the reproduced rates match the papers for all families.
- Open-source starting point: PADetBench (P2-P543, MIT per its README as read by LIT_A5), APDE (P2-P143), REAP (P2-P141), RFLA (P2-P301), laser beam (P2-P302), SLAP (P2-P401), phantom committee (P2-P402), T-SEA (P2-P1210), ART (P2-P1212), Torchattacks (P2-P1213); DPatch (P2-P1211) and TOG (P2-P2011) without a code location seen.
- Data and laptop fit: digital overlays and REAP-style rendering run on CPU; CARLA-based PADetBench needs a GPU and its fit on 6 GB is unknown; every repository licence is unread (NEEDS_BROWSER); REAP builds on Mapillary Vistas, whose terms are a LIT_X2 question.
- Experiment workflow: (1) read each repository README and licence; (2) run each generator on one fixed sign set with the paper's settings; (3) evaluate on YOLOX-Nano or YOLOX-S and on MobileNetV3-Small; (4) publish the reproduced success rate next to the paper's rate, and the list of families without working code.
- Success measure: share of the five cue families with working, licensed code; absolute difference between reproduced and reported success; for the later detector, recall at matched false alarms on the reproduced attacks.
- Sources: this task P2-P1210, P2-P1211, P2-P1212, P2-P1213; other tasks P2-P2011, P2-P2421, P2-P2425, P2-P141, P2-P143, P2-P301, P2-P302, P2-P401, P2-P402, P2-P543.

### Card X3-3. Latency budget of the full consistency pipeline on the owner's laptop
- Problem: published timings for the candidate components are for server GPUs, phone CPUs, NPUs or an unnamed CPU (section B); none covers a 10-core laptop CPU with a 6 GB GPU or the cost of the added checks.
- Contribution to test: a per-stage latency profile (decode, detector, tracker, flow or cue extraction, decision) with p50 and p95, in CPU-only and GPU modes, that fixes the compute budget all five slides must respect; the hypothesis that the checks add under a stated share of frame time can fail.
- Open-source starting point: YOLOX ONNX and OpenVINO exports (P2-P2421, section C1), NanoDet in the OpenCV Zoo (no paper), PP-PicoDet (P2-P1201), SORT (P2-P1207), ByteTrack (P2-P1208), DIS optical flow (P2-P1209), SAHI for small distant signs (P2-P2423), ShuffleNet V2 guidance to time on the target device (P2-P1204).
- Data and laptop fit: inference only, on BDD100K clips (P2-P542, LIT_A5; licence page read by LIT_A5); fits by construction; licence question: BDD100K terms for any released derived data.
- Experiment workflow: (1) export the detectors to ONNX and fix input sizes; (2) replay timestamped clips at their native frame rate; (3) time every stage with each cue switched on and off; (4) report p50, p95, peak RAM and VRAM and dropped frames.
- Success measure: p95 end-to-end ms per frame and the share taken by the checks, at unchanged detector AP on clean clips and at the matched false-alarm operating point of the checks.
- Sources: this task P2-P1201, P2-P1204, P2-P1207, P2-P1208, P2-P1209; other tasks P2-P2421, P2-P2423, P2-P501, P2-P538, P2-P542.

## Datasets, benchmarks and code seen

### A. Official code of the main attack and defense papers of the five cue families (question 1)
Source column: "row" = code_or_data field of another task's row; "abstract" = arXiv abstract. Licence column: what the source states; "not read" when no licence statement was seen by anyone.

| Cue family (slide) | Paper (paper_id, task) | Code or project location as recorded | Source | Licence as seen |
|---|---|---|---|---|
| Object appearance (01) | RP2 sign stickers (P2-P101, LIT_A1) | github.com/evtimovi/robust_physical_perturbations | row (search result) | MIT per a search result seen by LIT_A1; UNVERIFIED |
| Object appearance (01) | Adversarial Patch (P2-P103, LIT_A1) | cleverhans repository, examples/adversarial_patch | row (abstract) | not read |
| Object appearance (01) | Naturalistic patch (P2-P104, LIT_A1) | github.com/aiiu-lab/Naturalistic-Adversarial-Patch | row (search result) | not read |
| Object appearance (01) | Patch of Invisibility (P2-P105, LIT_A1) | github.com/razla/Patch-of-Invisibility | row (search result) | not read |
| Object appearance (01) | FCA vehicle camouflage (P2-P106, LIT_A1) | project page idrl-lab.github.io/Full-coverage-camouflage-adversarial-attack | row (abstract) | not read |
| Object appearance (01) | PatchZero (P2-P109, LIT_A1) | github.com/Elysia200207/PatchZero | row (search result) | not read |
| Object appearance (01) | Segment and Complete (P2-P110, LIT_A1) | github.com/joellliu/SegmentAndComplete | row (abstract) | not read |
| Object appearance (01) | PatchCleanser (P2-P113, LIT_A1) | github.com/inspire-group/PatchCleanser | row (search result) | not read |
| Object appearance (01) | NAPGuard (P2-P114, LIT_A1) | github.com/wsynuiag/NAPGaurd (spelling as recorded) | row (search result) | not read |
| Object appearance (01) | Jedi (P2-P115, LIT_A1) | github.com/ihsenLab/jedi-CVPR2023 | row (search result) | not read |
| Object appearance (01) | PAD (P2-P116, LIT_A1) | github.com/Lihua-Jing/PAD | row (abstract) | not read |
| Object appearance (01) | Spectral patch and texture defense (P2-P129, LIT_A1) | github.com/weiz0823/adv-spectral-defense | row (abstract) | not read |
| Object appearance (01) | X-Detect (P2-P134, LIT_A1) | a demo is mentioned; location not seen | row | not read |
| Object appearance (01) | REAP benchmark (P2-P141, LIT_A1) | github.com/wagner-group/reap-benchmark | row (abstract) | not read |
| Object appearance (01) | APRICOT dataset (P2-P142, LIT_A1) | apricot.mitre.org | row (search result) | terms not read |
| Object appearance (01) | APDE patch-defense benchmark (P2-P143, LIT_A1) | github.com/Gandolfczjh/APDE | row (abstract) | not read |
| Shadows (02) | Shadow defense (P2-P208, LIT_A2) | code link stated in the abstract; location not seen | row | not read |
| Shadows (02) | Video shadow detectors STICT (P2-P213), Detect-AnyShadow (P2-P216), DTTNet (P2-P218), FastInstShadow (P2-P220), SynShadow (P2-P239) | github.com/yihong-97/STICT; github.com/harrytea/Detect-AnyShadow; github.com/city-cheng/DTTNet; github.com/wlotkr/FastInstShadow; github.com/naoto0804/SynShadow | row (abstract) | not read |
| Reflections (03) | RFLA reflected light (P2-P301, LIT_A3) | github.com/winterwindwang/RFLA | row (search result) | not read |
| Reflections (03) | Adversarial Laser Beam (P2-P302 LIT_A3, P2-P412 LIT_A4) | github.com/RjDuan/Advlight | row (search result) | not read |
| Reflections (03) | Adversarial Laser Spot (P2-P304, LIT_A3) | github.com/ChengYinHu/AdvLS | row (search result) | not read |
| Reflections (03) | AdvNIR near-infrared attack (P2-P320, LIT_A3) | github.com/MyNiuuu/AdvNIR | row (abstract) | not read |
| Reflections (03) | Glare detection review (P2-P333, LIT_A3) | github.com/maesfahani/glaredetection | row (abstract) | not read |
| Lighting (04) | SLAP projected light (P2-P401, LIT_A4) | github.com/ssloxford/short-lived-adversarial-perturbations | row (search result) | not read |
| Lighting (04) | Phantom of the ADAS / GhostBusters (P2-P402, LIT_A4) | github.com/ymirsky/GhostBusters | row (search result) | not read |
| Lighting (04) | CausalAttack (P2-P434, LIT_A4) | github.com/zxm2020/Causal | row (abstract) | not read |
| Video frames (05) | Real-time defense against object vanishing, ADAV (P2-P501, LIT_A5) | no code seen | row | - |
| Video frames (05) | AdROD (P2-P511, LIT_A5) | github.com/yutingwu-ntuiot/AdROD: patches and recorded sequences; implementation withheld with a patent notice | row | terms not read |
| Video frames (05) | Dual-FoV sign defense (P2-P509, LIT_A5) | said to be public; location not confirmed | row | - |
| Video frames (05) | StreamYOLO (P2-P538), LongShortNet (P2-P539), DAMO-StreamNet (P2-P540) | github.com/yancie-yjr/StreamYOLO; github.com/LiChenyang-Github/LongShortNet; github.com/zhiqic/DAMO-StreamNet | row (search result) | not read |
| Video frames (05) | PADetBench (P2-P543, LIT_A5) | github.com/JiaweiLian/PADetBench; datasets named on the Hub as Jiawei-Lian/PADetBench | row | MIT per the README as read by LIT_A5; Hub dataset licence left to LIT_X2 |
| Video frames (05) | CARLA-GeAR (P2-P544, LIT_A5) | github.com/retis-ai/CARLA-GeAR | row (project site) | not read |

Abstracts read by this task that state no code location: ShapeShifter P2-P108, shadow attack P2-P201, infrared reflection attack P2-P309, GhostImage P2-P409, rolling-shutter attacks P2-P403 and P2-P404, DetectorGuard P2-P111 (abstract cut at 1,800 characters), ObjectSeeker P2-P112.

A2. Code stated in the records of this task's rows: PP-PicoDet github.com/PaddlePaddle/PaddleDetection; EfficientDet github.com/google/automl/tree/master/efficientdet; RT-DETR project page zhao-yian.github.io/RTDETR (Hub card: github.com/lyuwenyu/RT-DETR); MMDetection github.com/open-mmlab/mmdetection; ByteTrack github.com/ifzhang/ByteTrack; T-SEA github.com/VDIGPKU/T-SEA; ART github.com/IBM/adversarial-robustness-toolbox with MIT licence as of release 1.0.0; Torchattacks github.com/Harry24k/adversarial-attacks-pytorch. None opened; licences not read except the ART statement in its abstract. Also from DECK_SRC rows' sources read here: YOLOX github.com/Megvii-BaseDetection/YOLOX and SAHI github.com/obss/sahi (both named in their arXiv abstracts).

### B. Published CPU or small-GPU timings (question 2)
| Component | Timing as stated | Hardware | Record |
|---|---|---|---|
| PP-PicoDet-S (P2-P1201) | 123 FPS, 150 FPS with Paddle Lite, input 320; 55% lower mobile CPU latency than YOLOX-Nano | mobile ARM CPU | arXiv abstract |
| MobileNetV3-Small (P2-P2425) | 5% lower latency than MobileNetV2 at 4.6% higher ImageNet accuracy; tuned to phone CPUs | mobile phone CPU | arXiv abstract read by this task |
| timm mobilenetv3_small_100 | 2.5 M parameters, 0.1 GMACs (not a timing) | - | Hub card |
| YOLOX Nano model (P2-P2421; written YOLO-Nano in the abstract) | 0.91M parameters, 1.08G FLOPs; only YOLOX-L is timed (68.9 FPS) | Tesla V100 (server GPU) | arXiv abstract |
| YOLOX-Nano, LiteRT FP16 export | 24.0 ms through the TFLite GPU delegate; the XNNPACK CPU path declined the graph, so no CPU number | GPU (OpenCL), device not in the lines read | Hub card litert-community/yolox-nano-litert |
| YOLOX (Qualcomm export, 640x640) | for example 13.311 ms on Snapdragon X Elite | NPU | Hub card qualcomm/Yolo-X |
| YOLO11n (no paper; agpl-3.0) | 56.1 ms CPU ONNX and 1.5 ms T4 TensorRT at 640 px; 2.6M parameters; mAP 39.5 | CPU model not in the lines read; T4 GPU | Hub card Ultralytics/YOLO11 |
| RT-DETR-R50 and R101 (P2-P1205) | 108 and 74 FPS | T4 GPU | arXiv abstract |
| ByteTrack (P2-P1208) | 30 FPS for the full tracker on MOT17 | one V100 GPU | arXiv abstract |
| SORT (P2-P1207) | tracker update at 260 Hz | hardware not in the abstract | arXiv abstract |
| DIS optical flow (P2-P1209) | 300 Hz up to 600 Hz | single CPU core | arXiv abstract |
| ADAV (P2-P501, LIT_A5) | 56 FPS clean, 20 FPS under attack, 63 FPS undefended | T4 GPU | LIT_A5 row (arXiv text) |
| NanoDet-m-0.5x int8 (no paper) | 364 KB model at 320x320; no timing in the lines read | i.MX NPUs | Hub card nxp/nanodet-m-imx |
Answer: no record read gives a timing on a laptop-class x86 CPU or a 6 GB laptop GPU. ShuffleNet V2 (P2-P1204) argues that speed must be measured on the target device, which supports card X3-3.

### C. Hugging Face Hub inventory (question 3)
Read-only Hub tools: 26 repository searches, 12 card reads plus 1 repository detail, 11 distinct paper pages. Licence = card tag or card sentence (uploader's statement).

C1. Detector and backbone weights relevant to a laptop pipeline

| Hub item | Owner | What it is (card) | Licence as seen | Downloads listed | Paper link on the card | Catalog |
|---|---|---|---|---|---|---|
| timm/mobilenetv3_small_100.lamb_in1k | timm | MobileNetV3-Small ImageNet-1k classifier; 2.5 M parameters, 0.1 GMACs | apache-2.0 | 7.7M | arXiv 1905.02244 | P2-P2425 (DECK_SRC) |
| AutowareFoundation/tensorrt_yolox | Autoware Foundation | YOLOX-s based ONNX models at 960x960 for the autoware_tensorrt_yolox camera node (detection; one model adds 16-class segmentation) | apache-2.0 | 534 | arXiv 2107.08430 | P2-P2421 (DECK_SRC) |
| litert-community/yolox-nano-litert | LiteRT community | YOLOX-Nano for LiteRT, FP16, 2.2 MB, 416x416; no CPU number (see B) | apache-2.0 | 2.5K | none in tags | P2-P2421 |
| qualcomm/Yolo-X | Qualcomm | YOLOX exported for Snapdragon devices; NPU timings (see B) | apache-2.0 | 524 | none in tags | P2-P2421 |
| OpenVINO/yolox_tiny-fp16-ov, yolox_s and yolox_x variants | OpenVINO | YOLOX in OpenVINO IR, FP16 and INT8 | apache-2.0 | 148 to 173 | none in tags | P2-P2421 |
| opencv/object_detection_yolox | OpenCV Zoo | YOLOX ONNX for the OpenCV DNN module; card links the YOLOX paper and repository | Apache 2.0 (card sentence for the directory) | not listed | arXiv 2107.08430 (card text) | P2-P2421 |
| opencv/object_detection_nanodet | OpenCV Zoo | NanoDet-m-plus-1.5x at 416 px, ONNX and int8 block-quantized; COCO 2017 val AP 0.304 | Apache 2.0 (card sentence) | 0 | none | no paper: table only |
| nxp/nanodet-m-imx | NXP | NanoDet-m-0.5x, full int8 (364 KB), 320x320, compiled for i.MX NPUs | mit tag; card also says original licence Apache-2.0 | 68 | none | no paper: table only |
| PekingU/rtdetr_r18vd | PekingU | RT-DETR with ResNet-18 backbone in HF transformers; repository github.com/lyuwenyu/RT-DETR | apache-2.0 | 21.0K | arXiv 2304.08069 | P2-P1205 |
| PekingU/rtdetr_v2_r18vd | PekingU | RT-DETRv2 R18 in HF transformers | apache-2.0 | 175.1K | arXiv 2407.17140 | not catalogued (lead) |
| depth-anything/Depth-Anything-V2-Small-hf | Depth Anything | small monocular depth model in HF transformers | apache-2.0 | 1.3M | arXiv 2406.09414 | P2-P2426 (DECK_SRC) |
| onnx-community/depth-anything-v2-small | ONNX community | ONNX export of the small depth model for transformers.js | apache-2.0 | 147.0K | none in tags | P2-P2426 |
| Ultralytics/YOLOv8, Ultralytics/YOLOv5 | Ultralytics | detector weights for the ultralytics library | agpl-3.0 | 58.5K and 2.4K | none | no paper: table only |
| Ultralytics/YOLO11 | Ultralytics | YOLO11 weights; timings in B; card offers an enterprise licence for commercial use | agpl-3.0 (card front matter) | 34.2K | none | no paper: table only |

C2. Traffic-sign models from the community (none links a paper; data and training UNVERIFIED)

| Hub item | What it is (card tags) | Licence as seen | Downloads listed |
|---|---|---|---|
| cvtechniques/TrafficSignDetection | ultralytics detector; dataset tag lisa-traffic-sign-dataset | mit | 285 |
| yahyagul/traffic-sign-yolov8 | ultralytics YOLOv8 detector; dataset tag roboflow | mit | 225 |
| star092304/traffic-sign-detection-vietnam-yolo | ultralytics detector, Vietnamese signs | apache-2.0 | 218 |
| kelvinandreas/vit-traffic-sign-GTSRB | ViT classifier on GTSRB | mit | 213 |
| ankitjha07/Traffic-Sign-Detection-YOLOv8 | ultralytics YOLOv8 detector | mit | 168 |
| bazyl/gtsrb-model | transformers image classifier, GTSRB | apache-2.0 | 156 |
| sergiopaniego/detr-resnet-50-hardhat-german-traffic-sign-detection-finetuned | DETR fine-tune | no tag shown | 85 |
| FraunhoferIOSB/convnextv2-atto-1k-224-finetuned-gtsrb | ConvNeXt V2 atto classifier, GTSRB | cc-by-4.0 | 70 |
| neitpm/traffic-sign-yolo11-benchmark | ultralytics YOLO11 detector | mit | 51 |
| tanganke/clip-vit-base-patch32_gtsrb | CLIP ViT-B/32 vision encoder fine-tuned on GTSRB | no tag shown | 3.2K |
| jack-perlo/MobileNetV2-Gtsrb | keras MobileNetV2 classifier, GTSRB | no tag shown | 28 |

Licence question for the owner (finding, not legal advice): community sign detectors built with the ultralytics library carry mit or apache-2.0 tags, while Ultralytics' own cards for YOLOv8, YOLOv5 and YOLO11 carry agpl-3.0 and offer an enterprise licence for commercial use. A tag on a fine-tuned model is the uploader's statement and may not reflect the terms of the base weights and library. Prefer Apache-2.0 detectors with a paper (YOLOX, RT-DETR) or resolve the question before any release.

C3. Spaces and attack or defense items
- Itanutiwari527/Adversarial_attack_on_traffic_signs: Streamlit demo, card text "a demonstration of adversarial attacks on traffic signs"; no licence tag, no paper.
- awacke1/AdversarialAIToolbox: Streamlit Space titled "System Defense Strategy"; mit tag; generic, no paper.
- elliotalderson000/Adversarial-Patch-Segmentation: Gradio Space created 22 May 2026; card not read.
- Traffic-sign recognition demo Spaces (Gradio, 2022 to 2023): ErenYeager01/Traffic_sign_recognition, Aristo/trafficsign, yadav/traffic_sign_recognizer, ShivrajBhor/traffic-sign-dect, ErtugrulDemir/TrafficSignRecognation, Yvan/Traffic_Sign_Detection, Dhanushlevi/DETECTRON_TRAFFIC_SIGN_DETECTION and 5 more; none read.
- Searches for "physical adversarial", "patch attack", "adversarial yolo", "adversarial robustness toolbox" and "robust traffic sign" returned no model or Space.
- Hub paper pages: YOLOX, MobileNetV3, RT-DETR and SAHI link many models and Spaces (SAHI: models and Spaces under the account fcakyon). The pages of REAP (2212.05680), APRICOT (1912.08166), RFLA (2307.07653) and PP-PicoDet (2111.00902) link no model, dataset or Space. The shadow attack (2203.03818), ART (1807.01069) and PADetBench (2408.09181) have no Hub paper page.
- Reading: to our knowledge from these searches, the Hub carries the detectors and backbones but almost none of the physical-attack or attack-detection artifacts; attack code has to come from GitHub (table A), and the attack-detection side has no Hub baseline to download.

C4. Datasets seen on the Hub (names only; licences and access terms are task LIT_X2)
emb-ai/traffic-sign-bench; KeenForgeAI/TrafficSigns_YOLO-corrected; keremberke/german-traffic-sign-detection; star092304/Traffic-sign-detection-VietNam; ThankGod/mapillary_traffic_sign_dataset; thanhhiepvos/vietnam_traffic_sign; PastaEvangelists/UK_Traffic_Sign_Inspection_Dataset; kannanwisen/Indian-Traffic-Sign-Classification; kuchidareo/chinese_trafficsign_dataset; afyfbadreddine77/moroccan-traffic-sign-dataset; Sayali9141/traffic_signal_images; tungitachi/vietnamese-traffic-sign-vqa-dedup-1k; tanganke/gtsrb; bazyl/GTSRB (named in card tags); dronefreak/LISA-Traffic-Lights; tanishqsharma2022/adversarial-patch-mask; Jiawei-Lian/PADetBench (named by P2-P543, not looked up here). Re-uploads of datasets with their own terms (for example Mapillary, GTSRB, LISA) need the original terms, not the uploader's tag.

## Leads not confirmed
- CleverHans technical report: the arXiv lookup was blocked by the shared arXiv stop; not catalogued. LIT_A1 records the cleverhans repository as the code of P2-P103.
- PatchGuard (patch defense for classifiers): arXiv lookup blocked; not catalogued. PatchGuard-Freq is catalogued by LIT_X12 (P2-P2113).
- DIFFender (diffusion-based patch defense) and Adversarial Pixel Masking (patch defense for pre-trained detectors): one search each was tried on arXiv and then on Crossref; both hosts answered STOP_HOST (shared stop); not catalogued.
- Implementations of DPatch and other detector attacks inside ART, and code locations for TOG, the person-patch attack and feature squeezing: known to this agent only from memory; no record read confirms them, so no location is written here.
- NanoDet: no paper found; the Hub cards point to github.com/RangiLyu/nanodet. Kept in table C1, not a row.
- ONNX Runtime, OpenVINO, TensorRT, LiteRT and timm: software without a paper read here; not catalogued. Hub cards show ONNX, OpenVINO, TensorRT and LiteRT exports of YOLOX exist.
- RT-DETRv2 (arXiv 2407.17140, linked from a Hub card): not looked up.
- GitHub licences of every repository in table A: not read (no websearch results, no browser).

## Exclusions
- davidgaofc/ShadowAttackF: a DistilBERT text classifier (repository details), unrelated to image shadows.
- Hub search noise: repositories named after the fruit apricot (robotics and language models); lens-ai/adversarial-clip-vit-base-patch32_pcam_finetuned (medical imaging); jiekeshi CodeBERT adversarial models (source code); TrustSafeAI/Defensive-Prompt-Patch-Jailbreak-Defense (language-model jailbreaks); ebnezr-isaac/qwen3-0.6b-traffic-signal-ft0-stock (language model). Outside the subject.
- Crossref search noise: 10.5220/0006511301100120 (R-FCN ensemble), 10.1109/iaw.2006.1652084 (intrusion detection), 10.47191/etj/v11i05.62 (shoulder surfing), 10.1117/12.3110508 and 10.23919/iccas66577.2025.11301171 (applications of a depth model). 10.2139/ssrn.7015398 ("Adversarial Attacks on Object Detection Systems", SSRN 2026) was returned by a search but not examined: left for LIT_A1 or the coordinator.
- Verified but not written as rows because other tasks hold them: YOLOX, SAHI, MobileNetV3, Depth Anything V2, TOG, the person-patch attack of Thys et al., multivariate detector calibration (paper_ids at the top of this file).
