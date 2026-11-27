# P2_EMBED_1 notes - vehicle compute platforms, runtimes and latency budgets for the attack detector

Task EMBED_1 (brief briefs/EMBED_1.md). Writer's own work, not audited. Rows: work/EMBED_1/rows.jsonl (P2-P2501 to P2-P2527). Verification states come from scripts/rows_check.py and the ledger work/EMBED_1/verify_ledger.jsonl, never from this file. Read depth: Crossref abstracts, plus abstract or full-text passages seen in web search snippets during the first minutes of the run; otherwise title only. No full paper, vendor page or standard was opened: webfetch is banned for worker agents, websearch returned nothing after its fifth query, and the arXiv API was under a shared stop for the whole run. Every number below names the record it comes from. "Lead N" points to the list under "Leads not confirmed"; leads are not rows.

Counts (scripts/rows_check.py): 27 rows, 0 schema problems, VERIFIED 27 (Crossref); High 9, Medium 18; read level 16 abstract (several only partly read), 11 metadata-only; families E-F1 8, E-F2 6, E-F3 5, E-F4 4, E-F5 4. The count is 2 above the brief's target of 25 because the brief names TI and NXP platforms and P2-P2526 and P2-P2527 are the only records found for them. 4 problem cards; 25 leads.

## Uncomfortable findings first
1. The vehicle latency budget rests on a thin chain. The only primary statement of a numeric budget read in this run is the 2018 architecture paper P2-P2501: process within 100 ms, at least once every 100 ms, judged by tail latency. Its authors derive this from human reaction times and from Mobileye and Udacity statements that were not read here. Other records call 100 ms a "commonly used" reference (P2-P2514) or use it as a deadline (AdROD, P2-P511, via the LIT_X5 notes). No record read in this run states a production camera frame rate. A sentence such as "fits the vehicle budget" must cite P2-P2501 as an authors' design constraint and say so.
2. Sharing the board with the detector, not model size, decides whether a checker fits. On a Jetson Orin Nano a single YOLO pipeline had a mean latency of 83.91 ms and a p99 of 105.15 ms; a second concurrent stream moved the mean to 101.13 ms, the p99 to 137.88 ms and the share of frames over 100 ms from 1.50% to 43.75% (P2-P2514, abstract). An attack checker is a second workload on the same board, so Colab timings of the checker alone do not answer the vehicle question.
3. Peak vendor ratings do not predict per-network speed. On one Jetson board, a TensorRT framework that allocates layers across the GPU and the neural processing unit and tunes threading, pipelining and network duplication gained 101% to 680% in performance over GPU-only inference on nine benchmarks (P2-P2517). An excluded agricultural benchmark (lead 13) found the smaller Orin Nano Super faster than the AGX Orin at a matched 15 W for one INT8 detector. Scaling Colab or laptop numbers to a vehicle board by TOPS ratios would be extrapolation; the benchmark plan below rules it out.
4. Embedded cost of attack checks is already reported at strong levels, so "lightweight" alone is not a contribution. A binarised sign classifier with an attack-detector head and shape and content checks ran at over 9,000 fps at about 2.8 W on FPGA boards (P2-P2109 of LIT_X12, the same paper as P2-P123 of LIT_A1). An interpretable laser-artefact detector ran near real time on a Jetson Orin Nano (P2-P341 of LIT_A3, UNVERIFIED there). AdROD timed an anomaly-triggered ensemble on a Jetson AGX Xavier (P2-P511). What no record read here reports for a physical-attack checker: tail latency while sharing the board with the detector, frames over a stated budget, and accuracy at a matched false-alarm rate measured on the same configuration.
5. Precision results from Colab will not transfer. MODEL_1 plans ONNX Runtime dynamic INT8 on CPU, while the embedded records use vendor runtimes with FP16 or calibrated INT8 (TensorRT INT8 in P2-P2510, snippet; TensorRT FP16 on AGX Orin in P2-P2015; static INT8 with calibration through ONNX Runtime and TensorRT in P2-P1423 of LIT_X5). Accuracy and speed after INT8 in Colab describe that configuration only.
6. 11 of 27 rows are title level only. The production-chip paper (P2-P2503), Pylot (P2-P2513), CyberDet (P2-P2524), DNNGuard (P2-P2522), the TDA4VM paper (P2-P2526) and the integer-only quantization paper (P2-P2508) must be read before any claim rests on them. CyberDet is the one most likely to be close prior work.

## Q1. Platforms in published automated-driving and attack-defence work
| Platform | Class | Where it appears in records read | Compute figures stated, with source | Status |
|---|---|---|---|---|
| NVIDIA Jetson AGX Xavier | embedded GPU module | AdROD timing (P2-P511); GPU and NPU split with TensorRT (P2-P2517); framework comparison (P2-P2509); 3D detector benchmark (P2-P2507) | P2-P2517 abstract: NPUs beside a multi-core CPU and a GPU; no TOPS figure read | paper facts |
| NVIDIA Jetson Xavier NX, Orin NX | embedded GPU modules | latency-attack defence (P2-P1409: real time restored from 13 to 43 FPS on Orin NX, abstract); YOLOv8 on Orin NX (P2-P2511: TensorRT 17.7% faster than PyTorch at batch 2) | lead 1: Orin NX 16 GB at most 25 W | review figure, UNVERIFIED |
| NVIDIA Jetson Orin Nano | small embedded GPU module | concurrency study (P2-P2514); laser-artefact detector (P2-P341); PatchBlock test platform (P2-P146) | none from a paper; a blog in a search result quoted a peak INT8 rating (not a source) | UNVERIFIED |
| NVIDIA Jetson AGX Orin | embedded GPU module | TrackFlood with TensorRT FP16 (P2-P2015, LIT_X11) | lead 1: 200 TOPS (32 GB) and up to 275 TOPS (64 GB), 40 W for the 32 GB module in its table, two second-generation DLAs and a PVA; lead 14: power configurable from 15 to 60 W, 1792-core Ampere GPU with 56 Tensor Cores, two DLAs that support a subset of TensorRT layers | secondary, UNVERIFIED |
| NVIDIA DRIVE AGX Orin SoC | automotive SoC | Volvo Cars named as a deployment in lead 1 | lead 1: 254 TOPS and 200 W for the developer kit; 12 Arm Cortex-A78 cores, Ampere GPU, two DLAs, PVA and optical flow accelerator | secondary, UNVERIFIED |
| Tesla FSD computer | custom automotive SoC | P2-P2503 (title only); Tesla Model X with HW 2.5 and HW 3 attacked in P2-P402 (LIT_A4) | lead 1, citing that paper: two FSD chips, each with 12 CPUs, a GPU, two neural network accelerators and an ISP; 72 TOPS per chip below 40 W | secondary, UNVERIFIED |
| Mobileye EyeQ6 High | automotive vision SoC | Mobileye units attacked in P2-P402 (Mobileye 630) and P2-P2002 (LIT_X11); P2-P2501 cites Mobileye for its budget | lead 1: 8-core CPU cluster, ISP, GPU, two general-compute accelerator clusters and two DLA clusters; 34 TOPS at 33 W; Geely named as a deployment | secondary, UNVERIFIED |
| Industrial PC with desktop GPU (Neousys Nuvo-6108GC, Apollo reference computer) | x86 plus GPU | lead 1 | lead 1: Xeon or Core CPU with an RTX 3070; 162.6 TOPS in its table and 20.31 TFLOPS in its text (two different measures); 220 W | secondary, UNVERIFIED |
| Texas Instruments TDA4VM | automotive vision SoC | driver monitoring on TDA4VM (P2-P2526, title only); radiation test reports (excluded) | none read | not read |
| NXP i.MX 8M Plus | embedded SoC with NPU | P2-P2527: NPU offload of licence-plate detection cut overall CPU use 10x; end rate 1 Hz, limited by a second stage | no rating read | paper facts |
| Qualcomm Snapdragon Ride | automotive SoC | no record found (Crossref search returned unrelated items, websearch empty) | none | not read |
| Raspberry Pi class | single-board computer | energy comparison in RobustEdge (P2-P1412, LIT_X5); a Raspberry Pi 5 with Edge TPU sign-detector study excluded by LIT_X5 | none read | - |
| Edge TPU | accelerator | adversarial detectors timed on CPU, GPU and edge TPU (P2-P2525, preprint) | no number in the part of the abstract read | paper fact |
| FPGA boards (Zedboard, Ultra96) | FPGA SoC | sign defence (P2-P2109); 2018 driving pipeline (P2-P2501) | P2-P2109: over 9,000 fps at about 2.8 W; P2-P2501 passage: FPGA mean latency 369.6 ms for detection and 536.0 ms for tracking, above the 100 ms constraint (2018 networks) | paper facts |
| Custom defensive accelerators | ASIC designs | DNNGuard (P2-P2522), sDNNGuard (P2-P2523) | P2-P2523: 1.42x average speedup over compared accelerators while target and detector run together | paper fact |

Research vehicles and stacks: Autoware on embedded systems (P2-P2504, title only); lead 1 states that Apollo supports Jetson AGX Orin (32 GB, 64 GB) and Orin NX 16 GB; the 2018 system study ran on an Intel server with a Chevy Bolt power model (P2-P2501).

## Q2. Runtimes and precisions
| Runtime | Precisions or modes seen | Source and status |
|---|---|---|
| TensorRT (NVIDIA) | FP32, TF32, FP16, INT8; layers on GPU or DLA | P2-P2510 snippet (both tools cut inference time, TensorRT faster, INT8 faster again); P2-P2509 abstract (TensorRT and TF-TRT with Tensor Cores most efficient on AGX Xavier); P2-P2517 abstract (TensorRT assumes one processing element per inference); P2-P2511 snippet (FP16 on Orin NX, TensorRT 8.5); P2-P2015 (FP16 on AGX Orin). Lead 14 poster, RT-DETR R50 on AGX Orin, mean of 1,000 runs after 50 warm-up: 105.84 ms PyTorch FP32, 44.63 ms TensorRT FP32, 34.17 ms FP32 with TF32, 20.38 ms FP16, 19.94 ms FP16 with DLA; AP 53.1 to 53.0. Vendor documentation not read (UNVERIFIED) |
| ONNX Runtime (Microsoft) | FP32, FP16, dynamic UINT8, static INT8 | P2-P1423 (LIT_X5): YOLO12 scales converted with TensorRT and ONNX Runtime on an RTX 2070; static INT8 gave significant speedups. Documentation not read |
| TensorFlow Lite (Google) | integer-only inference | P2-P2508 (title); worst performer on the Jetson GPU in P2-P2509. Documentation not read |
| PyTorch eager | FP32 | baseline in P2-P2511 and lead 14 |
| Paddle Lite | mobile ARM CPU | PP-PicoDet (P2-P1201, LIT_X3): 150 FPS with Paddle Lite at input 320 (abstract) |
| NPU delegate in a GStreamer pipeline | NXP NPU | P2-P2527 |
| Deploy targets of the deck's detector | ONNX, TensorRT, NCNN, OpenVINO | YOLOX abstract (P2-P2421, DECK_SRC) |
| TI, Qualcomm, Mobileye tool chains | not read | - |

Accuracy retention for INT8: the MLCommons mobile benchmark page (search result, not opened) lists object-detection quality targets of about 95% of FP32 for MobileDETs and 93% for SSD-MobileNetV2. A retention threshold of this kind, fixed in the analysis plan before the run, is a defensible acceptance rule for an INT8 checker; read the MLCommons page before citing the numbers.

## Q3. Frame rates and latency budgets
| Figure | Value | Source | Status |
|---|---|---|---|
| End-to-end processing deadline | within 100 ms | P2-P2501, full-text passage | authors' design constraint; the Mobileye and Udacity statements it cites were not read |
| Update rate | at least once every 100 ms (10 Hz) | P2-P2501 | same |
| Latency metric | tail latency (99th, 99.99th percentile), not mean | P2-P2501 | recommendation; CPU-based configurations met 100 ms on mean but not on tail |
| Human reaction reference | 600 ms when expecting an interruption, 850 ms otherwise, fastest action 100 to 150 ms | P2-P2501, citing other work | secondary |
| Minimum frame rate of a driving stack | 10 FPS | lead 1 | UNVERIFIED |
| Real-time reference | 100 ms, called commonly used | P2-P2514 abstract | reference, not a standard |
| Perception deadline used in a defence | 100 ms | AdROD, P2-P511 (LIT_X5 notes) | used as a deadline |
| Multi-camera query interval | example of 50 ms | P2-P2512 (MLPerf multistream) | example in a benchmark, not a requirement |
| Tail percentile in an industry benchmark configuration | 90 for single-stream, 99 for multistream, 99.9 for single-stream runs of a model named pointpainting | mlcommons/inference load generator configuration seen in a search result | not opened, UNVERIFIED |
| Synthetic driving video rate | 60 fps | P2-P541 (LIT_A5) | dataset fact |
| Production camera frame rates | not found | - | gap |

Arithmetic, not a source: a per-frame pipeline fed at R frames per second must finish frames within 1000/R ms on average or it queues; at 10 Hz this is 100 ms. Any other R must come from the record of the camera or dataset actually used.

## Q4. Measured costs of attack detectors on embedded hardware
| Row | What is timed | Hardware | Figure | Where read |
|---|---|---|---|---|
| P2-P2109 = P2-P123 | binarised sign classifier with attack-detector head, shape and content classifiers | Zedboard and Ultra96 FPGA | over 9,000 fps at about 2.8 W | abstract, via LIT_X12 |
| P2-P511 AdROD | anomaly trigger plus on-demand ensemble | Jetson AGX Xavier | 5.4 FPS for the always-on ensemble, 68.7 attack-free, 13.9 on average; about 1.03 times baseline cost before an attack | LIT_X5 snippets and LIT_A5 extracts; preprint |
| P2-P1409 | detectors trained against latency attacks | Jetson Xavier NX, Orin NX | real time restored from 13 to 43 FPS on Orin NX; 13, 17 and 23 ms for three YOLO generations | abstract and arXiv text, via LIT_X5 |
| P2-P341 Blinded by the Beam | interpretable laser-artefact detector | Jetson Orin Nano | over 90% detection accuracy, near real time, no ms figure | abstract, via LIT_A3 (row UNVERIFIED) |
| P2-P146 PatchBlock | patch detection and neutralisation | Jetson Orin Nano and a laptop | cost not read | snippet, via LIT_A1 |
| P2-P2015 TrackFlood | trackers under phantom-detection floods, admission-cap defence | Jetson AGX Orin, TensorRT FP16 | detector latency flat, tracker latency rises; no deadline misses at the standard budget for association-dominated trackers, severe slowdowns at a higher budget | abstract, via LIT_X11; preprint |
| P2-P1420 ADAV | two-stage detection and masking | T4 GPU (not embedded) | 56 FPS clean, 20 attacked; LGS 35, JPEG 8 | snippet, via LIT_X5 |
| P2-P1305 ViLAS | small vision-language sign check | not stated in the row | 4.4 ms versus 9.3 ms for an off-the-shelf VLM and CLIP | abstract, via LIT_X4 |
| P2-P1412 RobustEdge | reduced-precision detector | 45 nm accelerator model; Raspberry Pi comparison | 25 times lower detection energy | abstract, via LIT_X5 |
| P2-P1411 eDenoizer | denoiser beside the protected model | embedded GPU, board not named | speed with defence up to 51.72% better | abstract, via LIT_X5 |
| P2-P1401 ARES | detector-triggered mode switch | not named | up to 8.9 times higher overall FPS | abstract, via LIT_X5 |
| P2-P2523 sDNNGuard | detection network beside the target network | custom accelerator | 1.42x average speedup over compared accelerators | abstract (this task) |
| P2-P2525 | statistical, ensemble and transformer detectors | CPU, GPU, edge TPU | no number in the part read; claims complex detectors cannot meet sub-100 ms windows | abstract (this task); preprint |
| P2-P2524 CyberDet | real-time adversarial attack detection (title) | not read | not read | title only (this task) |
| P2-P2113 PatchGuard-Freq | frequency-domain patch detector | none | embedded latency not measured (abstract) | via LIT_X12 |
| P2-P1413 LMM verifier | GPT-4V check near signs | ZED Box | latency not seen | via LIT_X5 |

Pattern: only P2-P2109 states a throughput and power pair for a sign-level attack check on embedded hardware; only P2-P511 and P2-P2015 time a defence inside a detection pipeline on a Jetson; none reports p95 or p99 or frames over a deadline while the detector shares the board.

## Q5. Proposed benchmark table for MODEL_1 (Colab) and how to state the gap
Configurations (batch 1, fixed input size, one JSON run log each, as MODEL_1 already plans):

| ID | Device | Runtime and provider | Precision | Threads | Workload |
|---|---|---|---|---|---|
| B1 | Colab CPU | ONNX Runtime CPU | FP32 | 1 | checker alone |
| B2 | Colab CPU | ONNX Runtime CPU | FP32 | 4 | checker alone |
| B3 | Colab CPU | ONNX Runtime CPU | INT8 dynamic | 1 | checker alone |
| B4 | Colab CPU | ONNX Runtime CPU | INT8 dynamic | 4 | checker alone |
| B5 | Colab T4 | ONNX Runtime CUDA | FP32 | - | checker alone |
| B6 | Colab T4 | ONNX Runtime CUDA | FP32 | - | frozen detector alone |
| B7 | Colab T4 and CPU | detector on CUDA, checker on CPU | FP32 detector, FP32 and INT8 checker | 4 | concurrent, frames fed at a fixed rate (card E-3) |
| B8 | Colab T4 | detector then checker on CUDA | FP32 | - | sequential pipeline (card E-1) |
| B9 (optional) | Colab CPU | ONNX Runtime CPU, static INT8 with a calibration set | INT8 static | 1 and 4 | checker alone; closer to calibrated INT8 on vehicle runtimes (P2-P1423 used both modes) |

Record for every configuration:
1. Environment: CPU model string and core count, GPU name, driver, CUDA and ONNX Runtime versions, Colab runtime type, seeds, sha256 of each ONNX file, input size.
2. Timing boundary, named: (a) inference call only; (b) end to end per frame: frame decode, pre-processing, inference, post-processing (non-maximum suppression for the detector), checker decision. Report both. P2-P2514 found pipeline latency grew faster than inference latency under load, and lead 13 shows why the boundary must be stated.
3. Run length: warm-up runs discarded and counted; at least 1,024 timed frames and at least 60 s per configuration, the single-stream minimums described in P2-P2512 (later MLCommons inference rules use 600 s for most scenarios, while the mobile page seen still lists 1,024 queries and 60 s for single-stream). The 500 runs planned by MODEL_1 fall short of both.
4. Statistics: p50, p95, p99, maximum and mean; a distribution-free confidence interval for p95 from order statistics; share of frames over 100 ms (the P2-P2501 constraint) and over 1000/R ms for the frame rate R stated in the dataset record, if one is stated.
5. Memory and size: peak resident memory of the process, peak GPU memory, ONNX file size.
6. Clean versus attacked inputs timed separately in every configuration, because latency attacks target the deadline (P2-P1409, P2-P2014, P2-P2015).
7. Accuracy on the same configuration: TPR at a fixed benign FPR and abstain rate (attack-eval-protocol skill); FP32 versus INT8 with the retention ratio judged against a threshold fixed in the analysis plan before the run.

Rules for stating the gap to vehicle hardware (no extrapolated numbers):
1. Name the device next to every number ("Colab T4", "Colab CPU, 4 threads"). Never convert to Jetson, DRIVE, TDA4 or EyeQ numbers by TOPS, clock or core ratios: the vendor figures in Q1 are secondary, and per-network speed depended on processor allocation and pipelining (P2-P2517), concurrency (P2-P2514) and power mode (lead 13).
2. Report the checker's cost in absolute time and as a ratio to the frozen detector on the same device and boundary; say that the ratio may change on other processors (P2-P2517).
3. Put published target-hardware measurements in a separate context column with citations, labelled as other models and other boundaries: for example YOLO-family detection at 13 to 23 ms per frame on a Jetson Orin NX (P2-P1409) and a single-stream YOLO pipeline at 83.91 ms mean and 105.15 ms p99 on a Jetson Orin Nano (P2-P2514).
4. State plainly in the paper: not measured on vehicle hardware; INT8 here is ONNX Runtime quantization on CPU, not calibrated INT8 in a vehicle runtime.
5. A run on a Jetson-class board is a separate study; buying or borrowing a board is the owner's decision (AGENTS.md 3.2, Ask first).

## Vendor pages and standards (no DOI, or not catalogued)
| Name | Publisher | What it states, as seen | Status |
|---|---|---|---|
| Jetson AGX Orin, Orin NX, Orin Nano module data | NVIDIA | figures in Q1, from lead 1 and lead 14 | UNVERIFIED: vendor page not read |
| DRIVE AGX Orin | NVIDIA | figures in Q1, from lead 1 | UNVERIFIED |
| EyeQ6 High | Mobileye | figures in Q1, from lead 1 | UNVERIFIED |
| FSD computer | Tesla | figures in Q1, from lead 1 citing P2-P2503 | UNVERIFIED |
| TDA4VM | Texas Instruments | nothing read | not read |
| i.MX 8M Plus NPU | NXP | nothing from NXP read; behaviour from P2-P2527 | not read |
| Snapdragon Ride | Qualcomm | nothing found | not read |
| TensorRT developer documentation | NVIDIA | precisions as used in papers (Q2); DLA supports a subset of TensorRT layers per lead 14 | UNVERIFIED |
| ONNX Runtime quantization documentation | Microsoft | not read | UNVERIFIED |
| TensorFlow Lite documentation | Google | not read | UNVERIFIED |
| MLPerf Inference rules and load generator | MLCommons | scenario table, tail percentiles and run lengths from MLCommons pages and the mlcommons/inference repository configuration seen in search results | seen in search results, not opened; UNVERIFIED |
| RF-DETR INT8 product page | Embedl | AGX Orin with TensorRT 10.16: median GPU time 5.951 ms INT8 versus 6.909 ms FP16; mAP 52.44% versus 53.30%; peak memory 631 versus 621 MiB | vendor marketing page seen in a search result; not for citation |
| ISO 26262, functional safety | ISO | Crossref holds a title-only BSI record "Road vehicles. Functional safety" (DOI 10.3403/30205385; standard number not in the record); scope per P2-P2519: risk from malfunctions of electrical and electronic components | standard not read |
| ISO 21448, safety of the intended functionality | ISO | title-only BSI records "Road vehicles - Safety of the intended functionality" (DOI 10.3403/30342655 and others); scope per P2-P2519: functional insufficiencies and performance limitations | not read |
| ISO/SAE 21434, cybersecurity engineering | ISO and SAE | concept-phase co-analysis with ISO 26262 in P2-P2521; called a standard for cybersecurity engineering in a chapter title (lead 15) | not read |
| ISO/PAS 8800, safety and artificial intelligence | ISO | a title-only BSI record "Road vehicles. Safety and artificial intelligence" (DOI 10.3403/30444595; the number is not in the record, so the match to the PAS is NEEDS_VERIFY); P2-P2218 (LIT_X13) says the safety-concern concept informed ISO PAS 8800 | not read |

Use in the paper: functional safety (ISO 26262) frames faults of the checker itself, SOTIF (ISO 21448) frames benign look-alikes as performance limitations, ISO/SAE 21434 frames the attacker, and the AI-specific PAS sits beside them. None of the four was read, so the paper may cite them only by title and by the scope stated in catalogued papers until someone reads them.

## Problem map (attack families from the compute angle)
| Attack family | Rows that define or use it | Compute angle |
|---|---|---|
| Latency (availability) attacks that flood NMS or trackers with phantom boxes | P2-P1409 (LIT_X5); P2-P2014 Phantom Sponges and P2-P2015 TrackFlood (LIT_X11) | the deadline is the target; a checker whose cost grows with box count is exposed |
| Physical patches, shadows, reflections and light, the slides' families | catalogued by LIT_A1 to LIT_A5 | they set what the checker must detect; this task asks only whether it can do so inside the budget |
| Phantom objects shown to commercial driver-assistance units | P2-P402 (LIT_A4), P2-P2002 (LIT_X11) | the attacked units are the vehicle-class platforms of Q1, with closed internals |
| Compression-aware attacks | P2-P1408 and lead 22 of LIT_X5 | the deployment precision opens its own attack surface (INT8 path of MODEL_1) |
| Resource contention (a failure mode, not an attack) | P2-P2514 | tail latency rose past 100 ms with one more concurrent stream |

## Solution map (defence and detection families with the compute they report)
| Family | Rows | Compute reported |
|---|---|---|
| Hardware co-design: detector of attack beside the target network | P2-P2522, P2-P2523 | 1.42x speedup (P2-P2523) |
| FPGA binarised checks for signs | P2-P2109 | over 9,000 fps at about 2.8 W |
| Interpretable image-statistics detector on a Jetson | P2-P341 | near real time on an Orin Nano |
| Cheap trigger plus on-demand heavy defence | P2-P511, P2-P1401 | FPS on an AGX Xavier; up to 8.9x FPS (platform not named) |
| Robust training sized to the board | P2-P1409 | FPS and ms on an Orin NX |
| Admission caps for trackers | P2-P2015 | latency restored at a cost in admitted detections |
| Allocation of a network across processors, with pipelining | P2-P2517 | 101% to 680% over GPU-only (nine benchmarks) |
| Safety architecture: monitor and actuator pair | P2-P2520 | no compute figure; asks for a simple monitor |
| Latency as a design constraint for detectors of attack | P2-P2525 | latency and robustness frontier across CPU, GPU and edge TPU (no numbers read) |

## Closest prior work to the owner's design slides (ranked, from the deployment angle)
1. P2-P2109 = P2-P123, FPGA hybrid defence (LIT_X12, LIT_A1): embedded throughput and power for a sign-level attack check that uses shape and content, the cue family of slide 01. Differs: it classifies crops rather than checking detector boxes, and its alarm is a learned head rather than a physical consistency residual.
2. P2-P511 AdROD (LIT_A5): always-on cheap trigger, on-demand ensemble, Jetson AGX Xavier timing against 100 ms; threatens the system-level framing of slide 05. Differs: the trigger is a tracking anomaly, not a physical cue. Preprint.
3. P2-P341 Blinded by the Beam (LIT_A3): interpretable laser detector on a Jetson Orin Nano, slide 03 family. Differs: no false-alarm rate or ms figure in the abstract; row UNVERIFIED in LIT_A3.
4. P2-P2524 CyberDet (this task): real-time attack detection for self-driving cars by its title; rank provisional until the abstract is read.
5. P2-P2525 (this task): latency as a design constraint for detectors of attack across CPU, GPU and edge TPU; digital attacks; preprint.
6. P2-P2523 sDNNGuard (this task): co-running the target network and a detector of attack; custom accelerator that the project cannot use.
7. P2-P1409 (LIT_X5): the time budget itself is attackable on Jetson boards.

## Gaps and what is left to test
1. Interference timing: checker and detector on one device, p95 and p99 end to end, frames over a stated budget, clean and attacked inputs; not seen in any record read (card E-1).
2. Budget derivation: no record read ties a camera rate, an end-to-end deadline and the warning time of slide 05 together for an attack checker (card E-2).
3. Placement: checker on CPU, GPU, DLA or NPU beside the detector; records cover allocation of a single network (P2-P2517) and NPU offload in a parking pipeline (P2-P2527) only (card E-3).
4. A safety requirement chain for an attack checker as a monitor; the standards themselves were not read (card E-4).
5. Calibrated INT8 for a physical-cue checker on a vehicle runtime; the Colab path covers dynamic INT8 on CPU only (the robustness side is card X5-2 of LIT_X5).
6. Vendor facts: every platform figure in this file is secondary; vendor pages must be read before a figure enters the paper.

## Problem cards (hypotheses, not results)

### Card E-1. The checker is timed alone, but the vehicle runs it beside the detector
- Problem: catalogued defences are timed alone or as one model per GPU, while on a vehicle board the frozen detector, the checker and the rest of the pipeline share processors; one more concurrent stream moved a Jetson Orin Nano detector pipeline from 1.50% to 43.75% of frames over 100 ms (P2-P2514).
- Contribution to test: interference-aware timing of the cue checker: p50, p95 and p99 end-to-end latency and frames over budget for the detector alone, detector then checker, and detector and checker concurrently, on clean and attacked clips, with TPR at matched FPR measured in the same runs. Prior work covers parts of this: card X5-1 of LIT_X5 proposes tail latency and GPU sharing for defences; P2-P2514 measures concurrency for detectors only; P2-P2523 co-runs a detector of attack in custom hardware. The joint latency and matched-FPR report for a physical-cue checker is the part not seen, to our knowledge from this sample.
- Open-source starting point: YOLOX-Nano (P2-P2421; Apache-2.0 as reported in COORDINATOR UPDATE 4, licence not read by this task) or a torchvision detector (BSD-3-Clause as reported there), exported to ONNX; ONNX Runtime; the MLPerf load generator (P2-P2512; repository UNVERIFIED) or a timestamped replay loop.
- Data and laptop fit: Colab T4 and its CPU; an optional local check on the 6 GB laptop GPU. Clips: MODEL_1 synthetic attack clips plus benign driving video. Licence question: BDD100K research-only terms (colab-experiments skill) must be recorded before any download; synthetic clips inherit the licence of their source images.
- Experiment workflow: (1) export detector and checker to ONNX and fix the input size; (2) build a replay harness that time-stamps decode, pre-processing, inference, post-processing and decision for every frame; (3) run configurations B6 to B8 on clean and attacked clips, at least 1,024 frames and 60 s each; (4) report p50, p95, p99, frames over budget, peak memory and TPR at fixed FPR per configuration.
- Success measure: hypothesis that the checker's added p95 under concurrency stays below a bound fixed in advance as a share of the detector's p95, that its attacked-clip p95 stays within a stated bound of its clean p95, and that its TPR at the fixed FPR does not drop between the alone and concurrent runs.
- Sources: P2-P2514, P2-P2501, P2-P2512, P2-P2523, P2-P2522, P2-P2517; from other tasks P2-P1409, P2-P2015, P2-P511.

### Card E-2. The frame budget is assumed, not derived
- Problem: "real time" in the catalog points to a 100 ms figure that traces to one derived design constraint (P2-P2501) or to a "commonly used" reference (P2-P2514); camera rate, pipeline stages and the warning time promised on slide 05 are not tied together.
- Contribution to test: a budget sheet that derives the checker's per-frame allowance from the frame rate stated in the dataset record and the cited end-to-end deadline, and reports how each added millisecond changes frames over budget and warning time. Prior work: streaming perception scores output against the world state at output time (P2-P537, LIT_A5); Pylot studies latency and accuracy trade-offs in a full stack (P2-P2513, title only). Only the budget accounting for an attack checker would be new.
- Open-source starting point: the replay harness of card E-1; the streaming evaluation code of P2-P537 (not checked).
- Data and laptop fit: clips whose frame rate is stated in their dataset record (record it, never assume it); Colab CPU or the laptop suffice for the accounting. Licence question: each video set's terms (BDD100K research-only; Argoverse-HD terms not read).
- Experiment workflow: (1) record the frame rate R from the dataset documentation and the deadline D from P2-P2501; (2) take stage times from the card E-1 runs; (3) compute the allowance, frames over budget and warning-time change per added millisecond; (4) set the latency cost against the detection gain at matched FPR.
- Success measure: hypothesis that, at the recorded R and D, the checker keeps frames over budget under a share fixed in advance, and that the warning time it gains on attacked clips exceeds the delay it adds.
- Sources: P2-P2501, P2-P2514, P2-P2512, P2-P2513, P2-P2515, P2-P2516; from other tasks P2-P537, P2-P511.

### Card E-3. Where the checker runs: placement beside the detector on heterogeneous processors
- Problem: vehicle and embedded SoCs pair CPUs with GPUs and NPUs or DLAs (P2-P2517, P2-P2527, P2-P2503), and runtimes place a network on one processing element; whether a checker fits may depend on its placement and priority more than on its operation count.
- Contribution to test: on available hardware as a proxy, compare the checker on CPU threads beside a GPU detector with both on the GPU, measuring interference on the detector and the checker's own p95. Prior work: P2-P2517 splits one network across GPU and NPU; P2-P2527 shows NPU offload frees the CPU; P2-P2523 co-runs in custom hardware; P2-P2516 sets task priorities for end-to-end deadlines (title only). The proxy cannot reproduce a DLA or NPU, and any result must say so.
- Open-source starting point: ONNX Runtime CPU and CUDA execution providers; Python processes with fixed thread counts.
- Data and laptop fit: Colab T4 and its CPU; the laptop's 10-core CPU and 6 GB GPU (free RAM can fall under 1 GB while Chrome is open, per the colab-experiments skill). Licence questions as in card E-1.
- Experiment workflow: (1) pin the detector to the GPU and the checker to 1, 2 or 4 CPU threads; (2) feed frames at the recorded rate; (3) log per-frame latency of both and CPU and GPU utilisation; (4) compare with both-on-GPU and sequential runs (configurations B7 and B8).
- Success measure: hypothesis that a CPU-placed checker with at most 4 threads adds less to the detector's p95 than a GPU-placed checker, at equal TPR at fixed FPR.
- Sources: P2-P2517, P2-P2527, P2-P2526, P2-P2523, P2-P2516, P2-P2514.

### Card E-4. The attack checker as the monitor of a monitor and actuator pair
- Problem: safety architecture separates a complex function from a simpler monitor that existing software-safety methods can assure (P2-P2520); the abstracts on adapting ISO 26262 to ML (P2-P2518) and on the SOTIF and functional-safety split (P2-P2519) do not name malicious inputs, and security is the subject of ISO/SAE 21434 (P2-P2521). The slides' checker has no stated place in that frame.
- Contribution to test: a requirement chain, built with the co-analysis steps of P2-P2521, from hazards to measurable checker properties: p99 latency and its variance, false alarms per hour on benign look-alikes, independence from detector internals, and the vehicle reaction to each output (attack suspected, clear, insufficient evidence). Prior work: safety monitors for ML perception are surveyed (P2-P2219, LIT_X13) and fault monitors over diagnostic graphs exist (P2-P2206, LIT_X13); the attack-specific requirement chain is what remains, to our knowledge from this sample. This is framing for the paper's discussion, not a hardware experiment.
- Open-source starting point: none needed; the STPA steps described in P2-P2521.
- Data and laptop fit: no new data; reuses the card E-1 latency logs and the long benign clips required by the attack-eval-protocol skill. Licence question: none beyond card E-1.
- Experiment workflow: (1) map the three outputs to vehicle reactions; (2) derive latency and false-alarm requirements with the co-analysis steps; (3) measure them with the card E-1 runs and long benign clips; (4) state which requirements hold and which do not.
- Success measure: hypothesis that the cue checker meets a stated p99 bound with low variance and a stated false-alarm-per-hour target while using no detector-internal features.
- Sources: P2-P2520, P2-P2518, P2-P2519, P2-P2521; from other tasks P2-P2219, P2-P2206, P2-P2218.

## Datasets, benchmarks and code seen
- Data named in records read: KITTI (P2-P2501); COCO and PASCAL VOC (P2-P2509); one prerecorded dashcam video (P2-P2514); point-cloud 3D detection workloads (P2-P2507); licence-plate images (P2-P2527); nine unnamed benchmarks (P2-P2517). No dataset licence was read in this task.
- Benchmarks: MLPerf Inference scenarios and query counts (P2-P2512); streaming perception metrics (P2-P537, LIT_A5).
- Code: github.com/mlcommons/inference (load generator and configuration; seen in search results, not opened, licence not read) UNVERIFIED. No other code location was named in the records read.

## Leads not confirmed (or confirmed but not catalogued)
1. Moving Forward: A Review of Autonomous Driving Software and Hardware Systems (arXiv 2411.10291): arXiv HTML seen in a search result; source of the vendor figures in Q1 and of a 10 FPS minimum. First author not seen; Crossref title search found no record; arXiv API under shared stop. NEEDS_VERIFY.
2. Sardino (arXiv 2204.08189; LIT_X5 lead 21): Crossref title search found no record; arXiv stopped.
3. EdgeShield (arXiv 2408.04181; LIT_X5 lead 11): Crossref search found nothing relevant; arXiv stopped.
4. D3 (EuroSys 2022, DOI 10.1145/3492321.3519576, Gog): the Crossref record holds only the title D3; the longer title used in the search came from memory; content not read; not catalogued.
5. Automotive safety and machine learning (SEFAIAS 2018, DOI 10.1145/3194085.3194090, Henriksson): Crossref record, no abstract; not catalogued.
6. Lightweight Deep Learning Framework for Real-Time Traffic Sign Detection on In-Vehicle Embedded Computing Platforms (IEEE T-ITS, record year 2026, DOI 10.1109/tits.2025.3640926, Yang): Crossref record, no abstract; read first if sign-detector timing on in-vehicle boards is needed; not catalogued to stay near the row target.
7. Connected Vehicle Perception Monitoring: A Runtime Verification Approach for Enhanced Autonomous Driving Safety (VEHITS 2024, DOI 10.5220/0012696400003702, Castelino): record, no abstract.
8. Real-Time Embedded Traffic Sign Recognition Using Efficient Convolutional Neural Network (IEEE Access 2019, DOI 10.1109/access.2019.2912311, Bangquan): record, no abstract.
9. YOLOv6+: simple and optimized object detection model for INT8 quantized inference on mobile devices (Signal, Image and Video Processing 2025, DOI 10.1007/s11760-025-04234-0, Moon): record, no abstract; relevant to an INT8-friendly frozen detector.
10. FALCONS (Array 2026, DOI 10.1016/j.array.2026.100829, Patil): record, no abstract; the title names a lightweight classifier with adversarial shielding for sign recognition.
11. Quantization white papers and an NVIDIA integer-quantization study (arXiv only; ids from memory): not checked because arXiv was stopped; nothing cited.
12. CAAD: Computer Architecture for Autonomous Driving (arXiv 1702.01894, seen in search results): not checked.
13. AgriJetsonBench (arXiv 2608.00927, preprint; arXiv HTML seen in a search result): agricultural models, excluded from rows. Points used here: name the timing boundary (pure engine versus end to end); at a matched 15 W the Orin Nano Super ran YOLO11s INT8 at 145.82 FPS with a p95 of 7.018 ms versus 80.90 FPS and 11.895 ms on the AGX Orin.
14. Poster on TensorRT optimisation of RT-DETR on a Jetson AGX Orin (Brookhaven National Laboratory, SC24 poster PDF seen in a search result; no DOI; not peer-reviewed as a paper): numbers in Q2.
15. ISO/SAE 21434 records from one Crossref search, not read: Goal and Threat Modelling for Driving Automotive Cybersecurity Risk Analysis Conforming to ISO/SAE 21434 (SECRYPT 2021, DOI 10.5220/0010603008330838, Ponsard); How to Prepare Automotive for Future Challenges - ISO 21434 - A Standard for Cybersecurity Engineering (VDI 2017, DOI 10.51202/9783181023105-29, Tschersich); Delivering Threat Analysis and Risk Assessment Based on ISO 21434 (SAE International Journal of Transportation Cybersecurity and Privacy 2021, DOI 10.4271/11-03-02-0008, Svancara).
16. On the Development of ISO/PAS 21448 Design Process and the Image Recognition System for the Safety of Intended Functionality by Autonomous Vehicle (SAE posted content 2022, DOI 10.47953/sae-pp-00223, Park): record, not read.
17. Challenges and Approaches to Realizing Autonomous Vehicle Safety (RAND 2017, DOI 10.7249/ct463, Kalra): record, not read.
18. Book chapters likely to hold platform tables, records only: Hardware Platforms (in Computing Systems for Autonomous Driving, Springer 2021, DOI 10.1007/978-3-030-81564-6_7, Shi); Hardware Platform for Autonomous Driving (Autonomous Driving Handbook 2026, DOI 10.1007/978-981-95-3725-9_3, Huang).
19. Benchmark Analysis of Deep Learning-based 3D Object Detectors on NVIDIA Jetson Platforms (ICTC 2021, DOI 10.1109/ictc52510.2021.9621072, Choe): conference precursor of P2-P2507; not catalogued.
20. Comprehensive Power and Performance Characterization of Deep Neural Networks on Jetson Orin Nano with PyTorch and TensorRT (Academic Journal of Computing and Information Science 2026, DOI 10.25236/ajcis.2026.090702): record without an author field; not read.
21. Texas Instruments TDA4VM, NXP and Qualcomm Snapdragon Ride vendor statements: websearch empty, Crossref searches gave unrelated items; not read.
22. CyberDet abstract: three websearch attempts empty; the Crossref record has no abstract.
23. Efficient and lightweight figures from vendor and blog pages (Embedl RF-DETR page; a blog on YOLOv8 INT8 on an Orin Nano): seen in a search result; not sources.
24. Platform figures for Tesla FSD and Mobileye EyeQ6 High: secondary through lead 1 only.
25. UL 4600 and other AV safety standards beyond the four in the table: not searched in this run; names from memory are not used.

## Exclusions
- AgriJetsonBench (lead 13): agricultural vision models; only its method points are used.
- A Lightweight Traffic Sign Detection Model Based on Improved YOLOv8s for Edge Deployment in Autonomous Driving Systems Under Complex Environments (World Electric Vehicle Journal 2025, DOI 10.3390/wevj16080478): abstract read; it reports parameters, GFLOPs and mAP but no device timing, so it answers none of the questions.
- GPU-accelerated chest X-ray classification on a Jetson Orin Nano (DOI 10.52783/dxjb.v37.363): medical imaging.
- Radiation and single-event-effect tests of the TDA4VM (two records): space qualification, not perception.
- FPGA MLP accelerator for destination prediction (ICACT 2026), similarity-based IoT malware detection (EDGE 2023), deepfake detection (Discover Computing 2026), edge-cloud inference frameworks: outside the subject.
- BSI standard records: standards are listed in the vendor and standards table, not as rows.
- Timing papers built on Ultralytics code are kept only as timing references (P2-P2511); no code reuse (COORDINATOR UPDATE 4).

## Run notes
- websearch: 14 queries, 4 with results (the first three and the fifth), 10 empty; treated as down from the sixth query onward, with Crossref search as the fallback.
- lit_verify: 35 of 50 calls: 7 Crossref lookups covering 35 DOIs, 27 Crossref searches, 1 arXiv call that returned STOP_HOST (shared stop already in force). arXiv was not called again. Crossref answered every call; no 4xx.
- No instruction-like text addressed to the agent was found in search results or API answers.
- Cross-task notes for the coordinator: (a) PatchGuard-Freq, P2-P2113 of LIT_X12, is UNVERIFIED there; this task's ledger holds a Crossref search record for DOI 10.3390/computers15090631 (Luan, 2026) with the same title. (b) P2-P2109 (LIT_X12) and P2-P123 (LIT_A1) are the same paper. (c) Localization and Elimination, P2-P705 of LIT_IEEE, came up again in a search; nothing new. (d) None of the 27 DOIs of this task appears in another catalog or staging file.
