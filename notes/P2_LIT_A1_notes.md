# P2_LIT_A1_notes - object appearance: patch, sticker, camouflage

Status: NOT AUDITED. Written by the LIT_A1 worker agent. A fresh-agent audit is required before anything here is used.
Scope: ASSUMPTION from briefs/00_COMMON.md (physical visual attacks on camera-based object and traffic-sign detection in autonomous vehicles; lightweight, explainable consistency checks). No banned phrases are defined.

Files: work/LIT_A1/rows.jsonl (48 rows, P2-P101 to P2-P148), catalog/P2_LIT_A1_catalog.csv, work/LIT_A1/verify_ledger.jsonl, work/LIT_A1/query_log.tsv, progress/LIT_A1.log.

Checker result (scripts/rows_check.py): 48 rows, 0 schema problems, 0 MISMATCH. VERIFIED 34 (Crossref record matches title, first author and year). ARXIV_API_VERIFIED 14 (preprint record; check the published version before citing). UNVERIFIED 0. Relevance High 24, Medium 24. Roles: ATTACK 13, DEFENSE 15, DETECTION 13, BENCHMARK 5, DATASET 1, SURVEY 1. Rows per family: F1 14, F2 14, F3 6, F4 9, F5 5.
The row count is 3 above the 45 target: P2-P146, P2-P147 and P2-P148 were added after OpenAlex and Crossref resolved three leads that the arXiv stop had left open.

Read depth: no full text was read. Abstract level for 46 rows (API abstract, publisher page text or search snippet). Metadata-only for P2-P147 and P2-P148. Rows built from partial snippets say so in their notes field: P2-P104, P2-P114, P2-P121, P2-P123, P2-P127, P2-P131, P2-P132 (abstract of a withdrawn earlier submission), P2-P133, P2-P137, P2-P138, P2-P146.

Budget used: websearch 45 of 60, lit_verify 36 of 80 (ledger: 40 arXiv records, 64 Crossref records, 34 OpenAlex records). STOP_HOST: export.arxiv.org answered HTTP 429 after 40 arXiv ids were found; the arXiv API was not called again. A search result then named a free search quota limit; the task paused and resumed under a ban on further searches.

## 0. Findings first

1. Prior work already covers the slide 01 pipeline shape (frozen detector, independent cue, consistency check, alert). DetectorGuard (P2-P111) predicts objectness with a robust classifier, checks that detector boxes explain it, and raises an attack alert when they do not. It covers patch hiding only, certifies instead of calibrating, and its cue is objectness, not contour.
2. Prior work already covers a low-cost shape-and-content check against stickers on signs. P2-P123 uses binarised networks on FPGA hardware, with a shape classifier (diamond, square, pentagon, octagon, reverse triangle) and a content check; the publisher page snippet states 93.82% on LISA and 76.50% on GTSRB under strong sticker attacks. It is a sign-classification defense, not a check on detector boxes; the snippets show no viewpoint conditioning and no calibrated uncertainty. P2-P124 covers the explainable side with symbolic shape, colour and text rules for stop signs.
3. To our knowledge, no verified row combines (a) a contour or shape cue compared with detector boxes, (b) viewpoint conditioning and (c) calibrated uncertainty with abstention. This is a statement about 45 searches and abstract-level reading, not a proof of absence.
4. "APDE" is best explained by the repository and dataset released with P2-P143 (Zheng et al., ICCV 2025; 94,000 images, 11 defenses, 13 attacks): the repository URL in its abstract contains APDE, and a repository snippet lists an "APDE Dataset". The letters are not expanded in anything read, and the slide was not re-read, so the identification with the slide phrase is UNVERIFIED. Its findings: the difficulty of naturalistic patches lies in the data distribution, not in high frequency; adaptive attacks substantially bypass existing defenses; attack strength falls with distance (search snippet).
5. Threats to a contour cue: patches placed along the sign outline (P2-P117), patches that are not on the object (screen patch P2-P118, lens patch P2-P120), advertising-style attack patterns (P2-P121; target objects not named in the snippet). A consistency check can itself be a target (P2-P127).
6. Slide wording: the Eykholt CVPR 2018 paper (P2-P101) attacks classifiers; the detector attack is the follow-up preprint P2-P102. X-Detect (P2-P134) was built and tested in retail. ADAV (P2-P136): an arXiv HTML table snippet gives accuracy 0.67 and recall 0.52 for patch scale below 0.8, against 0.88 and 0.95 above 0.8.
7. Threat realism: commercial traffic sign recognition systems use a spatial memorisation design that lowers system-level attack success (P2-P119). REAP (P2-P141) concludes that patch attacks may be a smaller threat than believed. Paper 2 should state its system and sensor assumptions.
8. No public benchmark was found that gives physical patch attacks on road signs together with benign driving clips. REAP is digital rendering on 14,000+ real sign images (Mapillary Vistas; CC BY-NC-SA per a dataset-page snippet). APRICOT has physical photos, but its listed categories contain no road sign.

Leads of the brief: 12 named papers or datasets were confirmed in a primary record (P2-P101, P2-P109 to P2-P116, P2-P134, P2-P141, P2-P142); the naturalistic-patch topic is covered by P2-P104, P2-P105 and P2-P117; APDE is only partly resolved (item 4). No lead of the brief was left without a candidate; the APDE identification and its letters remain unconfirmed.

## 1. Problem map (attack families and the papers that define them)

| Family | What changes in the scene | Rows | Facts read |
|---|---|---|---|
| Sticker or poster on a sign, classifier target | Black and white stickers on a stop sign; one universal printable patch | P2-P101, P2-P103 | P2-P101 abstract: targeted misclassification in 100% of lab images and 84.8% of video frames from a moving vehicle |
| Sticker or poster on a sign, detector target | Disappearance of a stop sign for the detector; mis-detection as another class | P2-P102, P2-P108 | P2-P102 abstract: YOLOv2 missed the sign in over 85% of lab frames; outdoors 72.5% (poster) and 63.5% (stickers). P2-P108: Faster R-CNN mis-detected perturbed stop signs |
| Natural-looking patches | Patch drawn from a GAN image manifold, black-box search, edge-aligned colour-matched patch, advertising-style sign | P2-P104, P2-P105, P2-P117, P2-P121 | P2-P117 abstract: over 90% attack success on sign classifiers under limited query budgets, masks follow the sign shape |
| Whole-surface camouflage | Texture over a full 3D vehicle surface | P2-P106, P2-P107 | P2-P107 abstract: tested on 15 detector models; P2-P106 abstract describes rendering and transfer into photorealistic scenes (physical details not read) |
| Patch not on the object | Screen patch on another moving vehicle; translucent patch on the camera lens | P2-P118, P2-P120 | P2-P120 abstract: 42.27% of stop sign instances undetected while nearly 80% of other classes stay detected |
| Reality checks on the threat | Commercial systems, realistic rendering, viewpoint and distance | P2-P119, P2-P141, P2-P143, P2-P145 | P2-P119 abstract: 100% success on one commercial functionality, much lower overall, 7 observations; P2-P145: effectiveness varies with viewpoint, distance and scene |
| Benign look-alikes (no attack) | Harmless alterations of signs: shape, colour, content, visibility, angle, background | P2-P144 | Abstract: notable drop in YOLOv7 detection and classification accuracy; no attack detector evaluated |
| Surveys | Overview of attacks on sign recognition | P2-P122 | abstract level only |

## 2. Solution map (defense and detection families)

| Family | How it works | Rows | Notes on cost and on what the user sees |
|---|---|---|---|
| Patch localisation and removal | Find patch pixels, mask or inpaint, rerun the detector | P2-P109, P2-P110, P2-P115, P2-P116, P2-P129, P2-P130, P2-P132, P2-P133, P2-P148 (title-level); P2-P114 detects naturalistic patches | Output is a patch mask or repaired image (where, not why). Run-time cost not read for any of them |
| Certified or provable | Masking with a proof; alert or recovery | P2-P111, P2-P112, P2-P113 | Extra robust classifier or many masked passes; cost not read. P2-P113 is a classifier defense |
| Output-consistency checks | Compare detector output between region and whole frame, between tasks, with scene context, or over frames | P2-P125, P2-P126, P2-P128, P2-P136, P2-P139; the attack on the idea is P2-P127 | Cheap when no extra model is needed; P2-P128 needs a second task model; P2-P136 and P2-P139 use frames |
| Shape and symbolic cues | Sign shape class, colour and text rules | P2-P123, P2-P124 | P2-P124 is explainable by construction (abstract); both classify signs rather than check detector boxes |
| Runtime anomaly detectors for sign or perception inputs | A learned model of clean signs or inputs flags and repairs altered ones | P2-P131, P2-P147 (title-level) | P2-P131 has a detector plus a clean-sign generator; cost not read |
| Explainable detection | Ensemble of explainable detectors, saliency, attention maps, attribution | P2-P134, P2-P135, P2-P138, P2-P124, P2-P136 | See section 4, question 4 |
| Lightweight or embedded | Binarised networks on FPGA, block autoencoder, edge-device framework | P2-P123, P2-P133, P2-P146, P2-P137 (title claim) | Latency figures not read; P2-P146 snippet lists a Jetson Orin Nano and a laptop as test platforms |
| Calibration and abstention | Evidential learning, Bayesian-uncertainty baseline | P2-P140, P2-P142 (baseline inside the dataset paper), P2-P111 (alert semantics) | No patch-specific calibrated abstention for road signs found. A conformal abstention paper (arXiv 2502.07255) is in the ledger and excluded as not attack-specific |

## 3. Closest prior work to the slide 01 design (ranked)

Slide 01 element: viewpoint-conditioned shape/detector mismatch plus calibrated uncertainty, with an abstain state, on a frozen detector.

1. P2-P111 DetectorGuard (CCS 2021). Same pipeline shape: frozen detector plus an independent cue plus an explaining check plus an alert. Differences: cue is objectness from a robust classifier; patch hiding only; certified, not calibrated; no viewpoint conditioning. Cost of the robust classifier over all locations not read.
2. P2-P123 FPGA hybrid defence (J Signal Process Syst 2026). Shape class plus content check against sticker attacks at low cost. Differences: classifies signs, does not compare detector boxes; no viewpoint conditioning or calibrated uncertainty seen in the snippets. Full text needed.
3. P2-P125 We Can Always Catch You (TDSC 2025; related earlier workshop paper in the ledger, DOI 10.1145/3475724.3483606). Detector output on a part of the input versus the whole input; the abstract says an adversarial object appears locally but disappears globally. Differences: not shape-based; abstract examples are surveillance cameras.
4. P2-P124 symbolic stop-sign rules (EPTCS 385). Shape, colour and text as an explainable cue robust to RP2 and AdvCam in the abstract. Differences: stop sign only; a classifier, not a check on a detector.
5. P2-P128 multi-task consistency (preprint 2026). Disagreement between detection and instance segmentation on BDD100K; ROC-AUC 99.9% against PGD within its attacker model (abstract). Differences: digital PGD only; needs a second task model.
6. P2-P136 ADAV (2024, slide 05 baseline). Temporal consistency of detector output plus gradient-based localisation; evaluated on BDD100K. Weak on small patches per the table snippet.
7. P2-P134 X-Detect (2024, named on the slide). Ensemble of explainable detectors, real time, 0% false positive rate on the authors' retail data (abstract). Differences: retail domain.
8. P2-P140 AEGIS (preprint 2026). Evidential learning gives calibrated uncertainty for adversarial detection. Differences: digital image classification on Tiny ImageNet.

How much of the slide 01 contribution already exists: the pipeline shape (1), a low-cost shape cue against stickers (2), detector-output consistency (3, 5, 6), explainability (4, 7) and calibrated uncertainty for attack detection in a digital setting (8). What was not found: contour or shape compared with detector boxes at frame level, viewpoint conditioning, and calibrated abstention on physical sign attacks.

## 4. Answers to the four questions of the brief

Question 1: which defenses compare an object's expected shape or contour with detector output, and at what cost?
- No verified row compares a contour with a detector box. Nearest: P2-P123 (shape class of the sign; classification level), P2-P124 (shape rules; classification level), P2-P111 (objectness versus boxes), P2-P128 (segmentation output versus detection), P2-P125 (region versus whole frame).
- Cost statements read: P2-P123 targets resource-constrained FPGA hardware with binarised networks (low-cost claim; no latency or power number read). P2-P125: the signature-based method runs in real time (abstract). P2-P136: both stages target low latency (abstract). P2-P128: the abstract calls the scheme efficient. P2-P133 and P2-P146 claim real-time or lightweight operation. No ms-per-frame number was read in any of them.

Question 2: which defenses stay effective against natural-looking patches, and which rely on high-frequency texture?
- Built for or tested on naturalistic patches: P2-P114 (feature modulation, built for them), P2-P115 (the abstract says entropy stays high even for naturalistic patches; about 90% of patches detected on average, up to 94% of successful attacks recovered), P2-P116 (tested on localized-noise, printable and naturalistic patches), P2-P132 (earlier-submission abstract: 8% higher mean average precision on the naturalistic patch).
- Texture or frequency cues: P2-P109 (abstract: patches tend to be highly textured), P2-P115 (entropy), P2-P130 (Error Level Analysis, Haralick texture), P2-P132 (high-frequency signature), P2-P129 (wavelet scales; AP 21.73% above earlier defenses under adaptive attacks, abstract).
- Masking-based defenses: ObjectSeeker (P2-P112) states that its masking works without knowing patch shape, size or location; DetectorGuard (P2-P111) and PatchCleanser (P2-P113) certify against any attacker within a threat model whose patch-size bound was not read.
- The benchmark P2-P143 reports that naturalistic patch difficulty lies in data distribution rather than high frequency, and that training on its dataset improved existing defenses by 15.09% AP@0.5 (abstract). The P2-P109 repository note that the released code handles PGD patches only is from a search snippet and is UNVERIFIED.

Question 3: which benchmarks give physical patch attacks on road signs with benign clips, and under which licence?
- None found with both. P2-P141 REAP: 14,000+ real sign images (Mapillary Vistas) with geometric and lighting transforms; patches are rendered digitally; images, not clips. Mapillary Vistas is CC BY-NC-SA per a dataset-page snippet; the REAP code licence was not read.
- P2-P142 APRICOT: 1,000+ photographs of printed patches in public places; a search snippet lists COCO categories without a road sign. Licence not read.
- P2-P143 APDE: 94 patch types, 94,000 images; sign content and licence not read.
- P2-P139 uses videos of clean and physically attacked signs; public release not seen. P2-P136 evaluates on BDD100K driving data (abstract); attack injection is the route to benign plus attacked clips (BDD100K licence not checked here).

Question 4: what does "explainable" mean in the existing defenses?
- P2-P134 X-Detect: the abstract says each alert comes with explanations and the detectors are explainable by design (object extraction, scene manipulation, feature transformation). The form of the explanation (what the defender sees) is not in the abstract.
- P2-P135 SentiNet: model-interpretability techniques (Grad-CAM per a paper-text snippet), that is, salient regions.
- P2-P138: attention-map inconsistency (NoiseCAM) is both the signal and the explanation; digital attacks on a small CNN.
- P2-P124: symbolic rules over shape, colour and text; the abstract calls it fully explainable and debuggable.
- P2-P136 ADAV: gradient-based attribution localises the pixels that break temporal consistency.
- P2-P109, P2-P110, P2-P115, P2-P116: a patch mask or repaired image (where the patch is, not why the alarm fired).
- P2-P111: the alert is tied to objectness that no detector box explains.
- Only the AEGIS abstract (P2-P140) names interpretability together with calibrated uncertainty, for digital image classification; no detector of physical attacks read here pairs an explanation with a calibrated confidence.

## 5. Gaps and what is left to test

1. Contour or shape cue compared with detector boxes, conditioned on viewpoint, with calibrated abstention: not found in any row (cards C1 and C5).
2. Slide 01 question "does class-specific contour consistency add signal against natural-looking patches, beyond texture": P2-P143 suggests the main difficulty is data distribution, so test the contour cue as an add-on to P2-P114, P2-P115 and P2-P116, not as a replacement (card C2).
3. Slide 01 question "can a tiny head generalise across viewing angles": hold out viewpoint bins; P2-P143 and P2-P145 show attack strength varies with distance and viewpoint (card C5).
4. Patch location: edge-aligned, off-object and lens patches (P2-P117, P2-P118, P2-P120) are not covered by any defense row (card C3).
5. Benign look-alikes: P2-P144 measures harmless sign alterations against YOLOv7 but evaluates no detector of attacks; P2-P121 shows advertising-style patterns as attacks. No row evaluates an attack detector on benign altered signs (card C4).
6. Adaptive attackers: P2-P127 targets consistency checks; P2-P143 reports adaptive attacks bypass defenses and that complex or stochastic defenses are relatively robust. Plan an adaptive-attack test of any mismatch score.
7. Compute: no ms-per-frame number was read for any shape or consistency check. Measure all stages on the laptop, including decode and queueing.
8. System realism: P2-P119 reports spatial memorisation in commercial systems. Include a temporal-smoothing baseline and report frame-level and event-level results.
9. Sensor assumption: every cue here is RGB-camera based.
10. Next reading to close the shape-cue question: the defense groups of the 2026 survey by Andleeb et al. (DOI 10.1016/j.ijcce.2026.06.003, in the ledger; its snippet lists structure-aware reasoning), and the full text of P2-P123 and P2-P111.

## 6. Problem cards (hypotheses, not results)

Laptop limits from state/DECK_DIGEST.md section 4: one laptop, 32 GB RAM, several terabytes of SSD, GPU and VRAM not known; start with CPU baselines and frozen features; record each licence before download; split by recording; never put neighbouring frames of one recording into both training and testing.

### Card C1 - A sticker changes the detector answer while the sign outline stays intact
- Problem: a sticker or patch can change the class a detector reports for a sign, or hide it, while the sign outline is still visible in the frame.
- Contribution to test: hypothesis that a class-specific contour score on the detector's region of interest disagrees with the detector's class more often under sticker attacks than under benign conditions, after conditioning on viewpoint, and that a calibrated head with an abstain state keeps false alarms low at a matched operating point.
- Prior work already covers: a shape-and-content check against stickers for sign classification (P2-P123), symbolic shape rules (P2-P124), and a detector-versus-independent-cue alert for patch hiding (P2-P111). Not found: contour versus detector box with viewpoint conditioning and calibrated abstention.
- Open-source starting point: a frozen small YOLO-family detector as on the deck, OpenCV contour and ellipse fitting, scikit-learn logistic regression with isotonic calibration; RP2 code (P2-P101; MIT licence per a search snippet, UNVERIFIED); REAP code (P2-P141; licence not read).
- Data and laptop fit: REAP sign images with geometric and lighting transforms (P2-P141); GTSRB and LISA (licences not checked); CPU only, features cached on disk. Licence question: REAP images come from Mapillary Vistas, CC BY-NC-SA per a dataset-page snippet (non-commercial, share-alike); read the terms before download and before releasing any derived crops, features or trained heads.
- Experiment workflow: (1) run the frozen detector on clean and patched sign images and store class, box and score; (2) compute contour shape class, polygon-fit residual, aspect ratio and skew per region with OpenCV; (3) fit logistic regression on mismatch features per viewpoint bin, calibrate on a separate calibration split by sign instance, define abstain when contour evidence is unreliable; (4) compare with detector-only, PatchZero (P2-P109) and an entropy baseline (P2-P115) at matched false-alarm rate, timing every stage.
- Success measure: true-positive rate at a fixed false-positive rate against the texture-only baseline; abstain rate; calibration error per viewpoint bin; p95 milliseconds per region on CPU.
- Sources: P2-P101, P2-P102, P2-P108, P2-P111, P2-P123, P2-P124, P2-P141.

### Card C2 - Natural-looking patches avoid texture-based patch detectors
- Problem: patch detectors that assume a busy texture or high entropy may miss patches that look like natural images.
- Contribution to test: hypothesis that a contour consistency cue adds detection power on natural-looking patches beyond texture and entropy cues only where the patch changes the outline or the class on a clean outline; the test is an add-on ablation, not a new patch detector.
- Prior work already covers: detection of naturalistic patches (P2-P114, P2-P115, P2-P116, P2-P132) and a benchmark of 11 defenses with naturalistic patches (P2-P143). The contribution here is only the added cue.
- Open-source starting point: the APDE repository (P2-P143), Jedi, PAD and NAPGuard code locations listed in their rows (not opened, UNVERIFIED), GAN patch generators (P2-P104, P2-P105).
- Data and laptop fit: a subset of APDE patch types (94,000 images in total; size on disk not read); REAP signs (P2-P141); use released patches instead of training generators; CPU timing of Jedi and PAD to be measured, not assumed. Licence question: APDE dataset and code terms not read; patch-generator repositories carry their own licences (not read); Mapillary terms as in C1.
- Experiment workflow: (1) pick naturalistic patch types and matched clean images; (2) run the available defenses and record average precision of the attacked object (P2-P143 reports it tracks defense performance); (3) add the contour mismatch feature and train a small head with held-out patch types; (4) ablate texture-only, contour-only and both.
- Success measure: gain in attacked-object average precision at matched false alarms on held-out patch types; abstain rate; added milliseconds.
- Sources: P2-P104, P2-P105, P2-P114, P2-P115, P2-P116, P2-P132, P2-P143.

### Card C3 - Patches off the object or on its outline break patch-on-object checks
- Problem: lens patches, screen patches and edge-aligned patches avoid or alter the object region that patch localisers inspect.
- Contribution to test: hypothesis that a detector-versus-shape mismatch score that does not need to locate the patch still fires for lens and screen patches, loses signal for edge-aligned patches, and that the abstain state captures the outline-altered cases.
- Prior work already covers: patch localisation on the object (P2-P109, P2-P110, P2-P115, P2-P116). Not found: any defense tested against edge-aligned patches or off-object patches. P2-P127 shows consistency checks can be targeted by adaptive attacks.
- Open-source starting point: simplified digital versions of the three attacks built with OpenCV and an instance-segmentation model (code of P2-P117 and P2-P118 not seen); translucent overlay to mimic P2-P120.
- Data and laptop fit: REAP signs plus synthetic overlays; simulation only, no physical test; CPU. Licence question: as in C1.
- Experiment workflow: (1) render the three attack types on sign images; (2) run the detector and the mismatch score; (3) report recall at a fixed false-positive rate per attack type and the count of cases flagged as evidence destroyed; (4) run a small-budget adaptive attack that optimises the edge patch against the score.
- Success measure: per-attack recall at fixed false-positive rate; share of abstentions; recall drop under the adaptive attack.
- Sources: P2-P117, P2-P118, P2-P120, P2-P127, P2-P143.

### Card C4 - Harmless sign alterations and look-alikes raise false alarms
- Problem: graffiti, bent or recoloured signs, stickers and advertising-style signs change shape, colour and content and also confuse detectors, so a mismatch alarm can fire on harmless cases.
- Contribution to test: hypothesis that calibrating the mismatch score on a benign-alteration set lowers false alarms per hour at the same true-positive rate compared with calibration on clean signs only, and that an abstain state covers severe occlusion.
- Prior work already covers: measurement of benign alteration effects on YOLOv7 without a detector of attacks (P2-P144); a 0% false positive rate on retail data only (P2-P134). No row evaluates an attack detector on benign altered signs.
- Open-source starting point: OpenCV alteration scripts (colour shift, partial occlusion, graffiti-like marks), the calibration code from C1, BDD100K road clips for long negative stretches.
- Data and laptop fit: BDD100K video and GTSRB or LISA signs; split by recording; false alarms per hour of ordinary driving need long clips, so decode time and disk use must be measured first. Licence question: BDD100K and GTSRB or LISA terms were not checked here; the deck rule is to record each licence before download; derived benign-alteration images inherit them.
- Experiment workflow: (1) build the benign alteration set from clean signs; (2) run the detector and the score; (3) calibrate with and without the benign set on a separate calibration recording set; (4) compare false alarms per hour at matched true-positive rate and report abstentions.
- Success measure: false alarms per hour at matched true-positive rate; abstain count; p95 latency including decode.
- Sources: P2-P144, P2-P121, P2-P134, P2-P119, P2-P141.

### Card C5 - Attack strength and shape visibility change with viewpoint
- Problem: the same patch is strong at some distances and angles and weak at others, and an outline is less visible at small scale or oblique angles, so one global threshold over-alarms or misses.
- Contribution to test: hypothesis that conditioning the mismatch score on viewpoint proxies (region size, aspect ratio, skew) and calibrating per bin gives better-calibrated alarms, and that a small head trained on some bins generalises to held-out bins.
- Prior work already covers: measurement of attack strength versus distance and viewpoint (P2-P143 snippet, P2-P145). Not found in two queries on viewpoint or 3D geometry: a defense that conditions on viewpoint. Coverage is limited.
- Open-source starting point: REAP geometric transforms (P2-P141) to build viewpoint bins; the AdvScene idea of a viewpoint sweep (P2-P145; code not seen); OpenCV homography and ellipse fits.
- Data and laptop fit: REAP images binned by transform parameters; CPU; small head (logistic regression or a tiny network). Licence question: as in C1.
- Experiment workflow: (1) bin REAP signs by transform parameters; (2) train on some bins and test on held-out bins; (3) compare global calibration with per-bin calibration; (4) log abstain when a bin offers too few reliable contour pixels.
- Success measure: calibration error per bin; true-positive rate at fixed false-positive rate on held-out bins; abstain rate; generalisation gap between seen and held-out bins.
- Sources: P2-P141, P2-P143, P2-P145, P2-P119.

## 7. Datasets, benchmarks and code seen

| Item | Row | What it offers | Licence or terms | Fit for slide 01 |
|---|---|---|---|---|
| REAP | P2-P141 | 14,000+ real sign images (Mapillary Vistas) with geometric and lighting transforms; digital patch rendering; code named in the abstract | Mapillary Vistas CC BY-NC-SA per a dataset-page snippet (non-commercial, share-alike; the snippet goes on to mention a login); REAP code licence not read | Images only, no clips |
| APRICOT | P2-P142 | 1,000+ photographs of printed patches in public places, three COCO detectors, defense baselines | Not read (project page seen in a search result) | No road sign class in the listed categories |
| APDE dataset and code (best candidate for the slide term) | P2-P143 | 94 patch types, 94,000 images, benchmark of 11 defenses | Not read | Patch types; sign content unknown |
| Videos of clean and attacked signs | P2-P139 | Used in the VisionGuard* paper | Not seen | Release not seen |
| Commercial system measurement | P2-P119 | Attack tests on commercial sign recognition | Not seen | Threat realism; no data seen |
| Superstore dataset | P2-P134 | Retail scenes for X-Detect | Not seen | Not a road setting |
| GTSRB, LISA | P2-P123 | Sign datasets used under strong sticker attacks | Not checked | Digital stickers |
| BDD100K | P2-P128, P2-P136 | Driving video used by two consistency checks | Not checked here | Benign clips; attack injection needed |

Code locations seen in rows (none opened, all UNVERIFIED unless the abstract names them): RP2 (P2-P101), PatchZero (P2-P109), SAC (P2-P110, named in the abstract), PatchCleanser (P2-P113), NAPGuard (P2-P114), Jedi (P2-P115), PAD (P2-P116, named in the abstract), naturalistic patch (P2-P104), black-box naturalistic patch (P2-P105), spectral defense (P2-P129, named in the abstract), REAP (P2-P141, named in the abstract), APDE (P2-P143, named in the abstract).

## 8. Leads not confirmed (12 items: 7 papers, 5 other items)

Papers seen but not verified in any record:
1. "Cloaking Signals with Signs: Traffic-Sign-Camouflaged Adversarial Patch": poster page of a 2026 vehicle security symposium, two search snippets; per the snippets it hides objects from a detector while the patch resembles a real traffic sign (a contour check might then see a plausible sign shape: inference). Tried: Crossref title search (no match); arXiv search not tried (API closed). Check on the venue page.
2. "Adversarial Patch Detection: Leveraging Depth Contrast for Enhanced Threat Visibility": a 2024 workshop paper title seen in a paper-list snippet; depth contrast would be a geometric cue (inference from the title). Tried: nothing beyond the snippet.
3. "NarAdv: Natural-Style Physical Adversarial Attack on Traffic Sign ...": a 2026 journal page snippet. Tried: snippet only.
4. PhyCamo (AAAI proceedings page; year not shown in the snippet): multi-view camouflage attack; title seen in one search. Not verified.
5. GRAC, "Gradient-Reweighted Adversarial Camouflage for Physical Object Detection Evasion" (ICCV 2025 open-access page snippet). Not verified.
6. "Dynamic Adversarial Patch for Evading Object Detection Models" (arXiv 2010.13070 per a snippet). Not verified.
7. "From Vulnerability to Robustness: A Survey of Patch Attacks and Defenses in Computer Vision" (2026, repository PDF snippet). Not verified.

Other items not confirmed:
8. Preprint ids not verified because the arXiv API stopped: 2406.10285 (arXiv HTML of the NutNet paper, P2-P133), 2601.00367 (PatchBlock, P2-P146), 2503.12567 (listing with a similar title to P2-P148), 2002.09792 (seen only as a URL with a snippet about an RP2 stop-sign evaluation; its title was not seen). The link between 2002.09792, the detector named VisionGuard in the abstract of P2-P139, and the ICCPS 2021 record P2-P147 is inferred from an OpenAlex answer and from memory: UNVERIFIED. The DOIs of P2-P133, P2-P146, P2-P147 and P2-P148 are verified in Crossref.
9. The P2-P109 repository note that the released PatchZero code handles PGD patches only (search snippet).
10. Licences: REAP code, APRICOT, APDE dataset and code, GTSRB, LISA, BDD100K; the Mapillary Vistas statement is from a snippet.
11. The expansion of the letters APDE, and whether the slide phrase "APDE patch attacks" refers to this dataset (the slide itself was not re-read).
12. Public availability of the VisionGuard* attack videos (P2-P139) and of the commercial-system measurement data (P2-P119).

## 9. Exclusions and verified records not catalogued

Out of the subject or not read enough (reason in brackets):
- Zhao et al., "Seeing isn't Believing" (CCS 2019; DOI 10.1145/3319535.3354259; arXiv 1812.10217; verified in the ledger): in scope; hiding and appearing attacks at 1 m to 25 m, up to 92.4% success in the abstract. Not catalogued because the row count was already above the 45 target; add it for a fuller attack list.
- Thys et al. (arXiv 1904.08653) and the diffusion patch of Lin et al. (arXiv 2307.08076): both verified in the ledger; person targets in surveillance and privacy settings, a gray zone against the road-sign focus. The diffusion paper is a naturalistic-patch generator and could be added to the F1 list.
- Khan et al. hybrid defense (arXiv 2205.01225; TechRxiv record in the ledger): digital attacks only (PGD, FGSM, MIM, C&W); OCR as a local feature mapper.
- Kumar et al. dual-threshold conformal abstention (arXiv 2502.07255): not attack-specific (CIFAR-100, ImageNet1K, ModelNet40). It is the nearest abstention pattern.
- Shua et al., "Redesigning Traffic Signs to Mitigate Machine-Learning Patch Attacks" (arXiv 2402.04660): environment-side redesign with adversarial training; not a detection method.
- Gu et al., Segment and Recover (DOI 10.3390/jimaging11090316), and Lee et al., SSIM-based autoencoder (DOI 10.3390/s24196461): snippet level only; the detect-and-remove family is covered by P2-P110 and P2-P115.
- Andleeb et al. survey (DOI 10.1016/j.ijcce.2026.06.003) and Dong et al. survey (DOI 10.1109/southeastcon56624.2025.10971663): snippet level only. The first lists structure-aware reasoning among its defense groups, the nearest survey category to a shape check.
- Li et al. global-local consistency workshop paper (DOI 10.1145/3475724.3483606): abstract seen in part; see P2-P125.
- Sarwatt et al., recovery methods for adversarial traffic signs (DOI 10.1049/itr2.70115): seven recovery methods on TSRD, BTSC and GTSRB per a snippet; digital attacks.
- Triggered, invisible-light, retroreflective and optical attacks (for example TPatch and a fluorescent-ink patch seen in search results; not verified) appear to fall under the sensor, lighting and reflection families of slides 03 and 04, not this one.
- Patch attacks on monocular depth estimation, LiDAR attacks and person-surveillance patches: outside the subject.

## 10. Limits of this file

- Rows rest on abstracts, publisher snippets or metadata; any statement tagged "inference" or "hypothesis" is the agent's reading, not a finding of the cited paper.
- Numbers quoted here come from the abstract or snippet of the cited row; the row notes say which.
- Third-party claims (for example "almost impossible" defense-aware attacks in P2-P125) are the authors' claims and were not tested here.
- The search was not exhaustive: 45 queries, arXiv API closed after 40 ids, no full text read.
