# P2 LIT_A3 notes - reflections (design slide 03: view-conditioned light consistency)

Status: written by the LIT_A3 worker agent. Not audited. Every row is in work/LIT_A3/rows.jsonl and, after the final build, in catalog/P2_LIT_A3_catalog.csv. Paper names from the brief were treated as leads and checked in records. Read depth is "abstract" for most rows, with body extracts seen through search results; three rows are metadata-only (P2-P323, P2-P324, P2-P336).

## 0. Counts and run facts
- Rows: 45, High 14, Medium 31, no schema problems. Verification (computed by scripts/rows_check.py): VERIFIED 22 (Crossref), ARXIV_API_VERIFIED 20, UNVERIFIED 3 (P2-P341, P2-P344, P2-P345, all NEEDS_VERIFY).
- By family: A3-F1 12, A3-F2 8, A3-F3 4, A3-F4 17, A3-F5 4.
- By role: ATTACK 22, DETECTION 7, METHOD 8, SURVEY 4, BENCHMARK 2, DATASET 2.
- Budget used: 29 of 60 websearch calls, 32 of 80 lit_verify calls. OpenAlex not called (Crossref citation counts are already in the ledger).
- STOP_HOST: api.crossref.org answered HTTP 429 in a chained batch of nine lit_verify calls (seven Crossref searches and two arXiv searches in one shell command). The second, third and fourth calls returned 429; the fifth, sixth and seventh then returned records. I chained the calls, so five Crossref calls were sent after the first 429 (my error). No Crossref call was made after that batch. Effects: the DOI of Yang 2010, the physics-aware defence of 2026 and several other candidates could not be checked (section 8); three rows are UNVERIFIED.
- Deviation to report: the five Crossref calls sent after the first 429.

## 1. Answers to the four questions of the brief

### Q1. Which reflection or laser attacks were shown physically, on which sensors, by day or night
| Attack (row) | Light and mechanism | Sensor and target | Physical test | Time of day |
|---|---|---|---|---|
| RFLA (P2-P301) | Sunlight or flashlight reflected by a mirror through coloured sheets and a cut-out | ImageNet and sign classifiers; camera model not read | Six printed images, 2 m, 48 photos per source; 81.25% (sunlight) and 87.5% (flashlight) | Daylight and flashlight; fog and rain named as limits |
| AdvCL (P2-P303) | Catoptric (reflected) light from coloured lamps | iPhone 6s, ResNet50 | Indoor 30 samples, outdoor street sign 103 samples, 83.5% outdoors | Authors list weaker effect in daylight |
| AdvLB (P2-P302) | Laser pointers 450, 532, 680 nm | Pixel 4 phone, ResNet50 | Indoor banana, conch, stop sign; outdoor stop sign 77.43% | Outdoor time not stated in extracts; static scenes only |
| AdvLS (P2-P304) | Small laser spots | Classifiers | Outdoor stop sign 80.56%, 77.78%, 41.67% at 0, 30, 45 degrees | Daytime (authors claim first daytime light attack) |
| AdvNB, AdvCP (P2-P305, P2-P306) | Neon beam, projector colour | Classifiers | Abstract only: 81.82% physical; 100% indoor and 82.14% outdoor | Not read |
| Natural-light patterns (P2-P345, UNVERIFIED) | Simulated sunlight, headlight and flashlight patterns found by black-box search | GTSRB and LISA models | Real-world signs per the abstract; details not read | Natural-like conditions per the abstract |
| SLAP (P2-P307) | Projector on a stop sign | Mask R-CNN, YOLOv3, sign CNNs | Indoor and outdoor, approach video 18 m to about 7 m | "Non-bright" ambient light; up to 99% |
| LaserGuider (P2-P308) | Laser spot as backdoor trigger | iPhone 12 mini; sign classifiers | 676 real laser-stamped sign photos, 5-30 m | Urban streets; 90.5-95.3% (backdoor setting) |
| Rolling Colors (P2-P321) | Laser exploiting rolling shutter | 5 cameras, 2 traffic-light recognisers | Moving vehicle over 40 m; 30% and 86.25% | Not read |
| ICSL (P2-P311) | Infrared light aimed at the camera | Tesla Model 3 camera, enterprise AD platform | Production-vehicle tests | Not read |
| WIP and ILR (P2-P310, P2-P309) | Infrared laser spot on the sign | Four IR-sensitive cameras, single- and two-stage sign models | Indoor 100%; outdoor moving vehicle at 5, 8, 13 km/h from 12 m, at least 80.5% | Day and night; authors say nearly 100% outdoors, particularly at night |
| POV display (P2-P312) | Rotating near-infrared LED display | Sony IMX708 module without IR filter, 12 models | Up to 20 m, varying illumination | Dawn or night use case |
| Near-infrared flashlight (P2-P313) | IR flashlight through a transparent film | Traffic-sign models, moving vehicle | Static and moving tests; up to 99.4% targeted | Bright lighting per abstract |
| GhostStripe (P2-P314) | LED modulated against the rolling shutter | Moving victim vehicle | Up to 94% of frames | Not read |
| Fluorescent ink (P2-P315) | UV-triggered fluorescence | Sign models | 98.31% in low light | Low light |
| ARP and WIP (P2-P318, P2-P317) | Retroreflective patch lit by the victim headlights | FLIR Blackfly S; YOLOv5, Faster R-CNN, CNNs; two 2024 production systems | 5-25 km/h, 15-50 m; 60% and 75% on production systems; STOP attack only works below about 900 lux | Dusk and night |
| Reflective pedestrian patches (P2-P319) | Retroreflective sheeting on clothes | Pedestrian detectors | Night tests with passing vehicles | Night |
| NIR surveillance tapes (P2-P320) | Retro-reflective and insulating tape under NIR illumination | NIR surveillance camera, YOLO | 3-5 m; average 87.93% | Night mode (IR-cut filter off) |

### Q2. Which are invisible to an RGB camera with an infrared-cut filter, and what the papers say
- Visible-light attacks (RFLA, AdvCL, AdvLB, AdvLS, SLAP, retroreflective patches under headlights) do not depend on infrared and are not removed by an IR-cut filter.
- Infrared attacks need an IR-sensitive sensor. P2-P309 says its attack targets cameras without the filter, names the Tesla Model 3 as lacking it to the authors' knowledge, notes that cameras often drop the filter for night vision, and recommends IR filters or detection. P2-P312 measured that a near-infrared cut-off filter on the same sensor removes the display from the image (all filtered images classified correctly, mean confidence about 93%) and warns the filter can conflict with low-light perception. P2-P320 shows a case where the filter is switched off at night. The arXiv v1 text of the ultraviolet-ink paper (seen in a search result, P2-P315) says, citing reports and manufacturers, that most commercial cameras carry IR-cut filters, which limits infrared attacks.
- Invisible to people but visible to a filtered camera: GhostStripe (P2-P314, visible-band LED), ultraviolet fluorescence (P2-P315).
- Consequence for slide 03: the "IR limit" is a sensor assumption to state, not a property of the detector; the filter state of the test camera must be recorded.

### Q3. Detection methods found and the signal they use
| Method (row) | Signal | Reported result | Limits |
|---|---|---|---|
| Colour range plus spatial frequency (P2-P309) | Spectral and spatial, one frame, sign crop | 96% TPR and 2.7% FPR day, 92% and 6.7% night, 75 benign plus 75 attack images per time | Camera-specific colour ranges; small set; no abstain |
| Saturated region with red and blue above green (P2-P312) | Spectral, one frame | True-negative 99.97-100%, true-positive 55.45-98.89% on over 180k images | Sensor-specific; needs per-camera calibration |
| Segment Anything shape count (P2-P313) | Spatial (edges, shapes) | F1 up to 99% static, 85% moving | Large ViT-L model; latency not read |
| HSV contours, sharpening and Laplacian filters, geometry cues (P2-P341, UNVERIFIED) | Spatial and geometric | Over 90% accuracy on a Jetson Orin Nano | Accuracy only in the abstract; subtle AdvLS needs geometry-aware methods |
| Ghost-object overlap plus two moving-camera frames (P2-P338) | Physical model plus temporal | Worst-case EER 5% | Needs lens model and light-source detector; no abstain |
| Three-sensor disparity error (P2-P316) | Multi-sensor | Effective per abstract; works above about 20% contaminated area in the text | Needs LiDAR or several cameras |
| Software module in ICSL (P2-P311) | Infrared features (details not read) | Not read | Abstract only |
| Patch detector SentiNet (P2-P340) | Saliency of a localised region | Bypassed in over 95% of frames by SLAP (P2-P307) | Assumes a localised patch |
| Hardware: IR-cut filter (P2-P312), polarised headlight with crossed camera filter (P2-P318), random rolling-shutter order (P2-P321) | Optical or sensor change | DPR Shield: STOP-sign success 100% to 0% in its tests | Needs hardware change |
Temporal consistency is not a safe signal alone: P2-P313 argues it has limited effect when a targeted attack is consistent over most frames (163-frame clip, 0.6% flicker), while P2-P338 uses it to reject natural light sources.

### Q4. Reflection-separation or highlight-detection methods light enough to be a cue, and the data they were tested on
- HSV thresholds with a brightness-based Value threshold, contrast reduction under saturation and a gradient test: 0.0371 s per image against 0.0584 s for an older method, tested on a 100-image database (P2-P344, UNVERIFIED). Closest to a laptop-CPU cue; image size and hardware not stated.
- U-Net segmentation of specular pixels (P2-P329): trained on public specular sets; outdoor results qualitative (the paper says no outdoor ground truth exists). Detection branch of P2-P328: a plain four-level U-Net on 200 x 200 crops of shiny materials (SHIQ).
- Frozen vision-transformer encoder with a light localisation head (P2-P331), trained on rendered synthetic highlights; evaluated on natural and surgical images.
- Compute figures seen (P2-P330, 256 x 256 input): 4.53 M to 116.99 M parameters and 18.03 to 250.84 GFLOPs across six removal networks. No laptop CPU timing in any record read.
- Classical bilateral-filter removal (200 times faster than an older method on CPU, per the text) and a lightweight reflection-removal network (3.01% of parameters of a reference network) are leads only (section 8).
- Data used by these methods: SIR2 and SIR2+ (objects behind glass, P2-P324, P2-P325), SHIQ (about 16K real images of shiny materials, P2-P327, P2-P328), WoodScape sun-glare images (P2-P332), a multi-camera glare set (P2-P333), night road glare (P2-P337). None evaluates a highlight mask as an attack-detection cue.

## 2. Problem map (attack families and the papers that define them)
- A3-F1 Reflected-light and laser attacks: reflected sunlight or flashlight (P2-P301), catoptric light (P2-P303), laser beam (P2-P302), laser spot (P2-P304), neon beam (P2-P305), projected colour (P2-P306, P2-P307), laser backdoor trigger (P2-P308), rolling-shutter laser interference (P2-P321), light-spot attack (P2-P323, not read), natural sunlight, headlight and flashlight patterns on signs (P2-P345, UNVERIFIED), family survey (P2-P322). Almost all tests are static images and classifiers; moving-video object-detector tests are the exception (P2-P307, P2-P321).
- A3-F2 Infrared and invisible-light attacks: infrared into the camera (P2-P311), infrared laser reflection from a sign (P2-P310, P2-P309), infrared persistence-of-vision display (P2-P312), infrared flashlight with film (P2-P313), visible-band LED stripes (P2-P314), ultraviolet fluorescence (P2-P315), and a detection framework for optical attacks (P2-P316).
- A3-F3 Retroreflective attacks at night: patches on signs (P2-P317, P2-P318), patches on clothing for pedestrian detectors (P2-P319), tapes in near-infrared night mode (P2-P320).
- Benign look-alikes that the slide must not flag: sun, headlight and wet-road glare (P2-P332, P2-P333, P2-P334, P2-P337), and normal sign retroreflection (P2-P335).
- System context: commercial recognition systems memorise detections spatially and temporally, which lowers measured attack success (P2-P339, P2-P318).

## 3. Solution map (defence and detection families)
- Training-time: random laser-beam augmentation cut the laser-beam success on ResNet50 from 95.1% to 77.2% with no clean-accuracy loss (P2-P302); adversarial training lowered but did not remove neon-beam and projector attacks (P2-P305, P2-P306).
- Patch-oriented defences: SentiNet is bypassed by projected light (P2-P340, P2-P307); PatchCleanser mis-certifies at least 33.5% of infrared-reflection cases and lowers benign accuracy by at least 12% in that paper (P2-P309); test-time defences and adversarial training only reduce the near-infrared attack to about 62-68% (P2-P313).
- Hardware and sensor: IR-cut filter (P2-P312), polarised headlight plus crossed camera filter (P2-P318), random rolling-shutter row order (P2-P321), polarimetric sensors for specular separation (P2-P342, P2-P343; not tested against attacks).
- Spectral and spatial software detectors: P2-P309, P2-P312, P2-P313, P2-P341 (UNVERIFIED), P2-P311.
- Physical-model plus temporal consistency: P2-P338.
- Multi-sensor cross-check: P2-P316.
- Benign branch tools: glare and highlight detection (P2-P329, P2-P332, P2-P333, P2-P344), removal (P2-P327, P2-P328, P2-P330, P2-P331), glare reduction for perception (P2-P334, P2-P337), retroreflection physics (P2-P335).

## 4. Closest prior work to the design slide (ranked)
Slide 03 proposes a view-conditioned reflection residual with confidence or abstain. To our knowledge, within the 44 rows and the extracts read, no work combines (a) an expectation of reflection that depends on viewpoint and illumination for a sign, (b) a residual against it and (c) an abstain state. Nearest work, in order:
1. P2-P338 (Man, ACM TCPS): predicts lens-flare ghost positions from the lens model and a detected light source, alarms when a ghost overlaps a detected object, then needs two frames from a moving camera to reject natural lights. Worst-case EER 5%. It already is a physics-conditioned check with benign look-alike rejection. Differences: lens-flare ghosts, not reflections on a sign; needs lens knowledge; no abstain.
2. P2-P309 (Sato, NDSS 2024), the detector the slide names: colour range plus spatial frequency in the sign crop. Differences: single frame, no view or illumination model, no benign-glare set, no abstain; 150 images per time of day.
3. P2-P341 (Solanki, IEEE Access 2026, UNVERIFIED): lightweight HSV, Laplacian and geometry detector for the laser beam and laser spot on a Jetson Orin Nano. Differences: accuracy only in the abstract; no view conditioning or benign-glare test described.
4. P2-P312 (infrared POV paper, preprint): saturation plus red-and-blue-above-green check; sensor-specific.
5. P2-P313 (NDSS 2026): brightness-agnostic shape count; states limits of frame-consistency defences.
6. P2-P318: the only defence found for retroreflective patches is hardware (polarisers).
7. Component work for the cue itself: P2-P329 and P2-P344 (specular masks), P2-P335 (sign retroreflection physics).
Closest attacks the residual must face: RFLA (P2-P301), catoptric light (P2-P303) and natural-light patterns (P2-P345, UNVERIFIED) look like benign glare; the retroreflective patch (P2-P318) uses normal sign behaviour.

## 5. Gaps and what is left to test
- No public video set of reflected-light, laser or retroreflective attacks on signs was found. LaserMark (P2-P308) is 676 laser-stamped photos plus 158 clean photos for a backdoor setting. The slide's "controlled reflected-light videos" must be recorded by the owner.
- Reflected-light and laser attacks are mostly shown on classifiers with static images (P2-P301, P2-P302, P2-P303, P2-P304). Detector-level moving-video tests exist for infrared reflection and retroreflective patches (P2-P309, P2-P318).
- Detection papers report TPR and FPR on small image sets (for example 150 images per time of day in P2-P309). None reports false alarms per hour on ordinary driving, which the owner deck asks for.
- Benign glare appears as something to detect or remove (P2-P332, P2-P333, P2-P337) but not as a hard-negative class for attack detectors.
- Test to run: does a view- and exposure-conditioned residual beat brightness-only and texture-only checks at matched false alarms on held-out recordings, with the camera's IR-cut state recorded?
- Test to run: does the abstain state remove false alarms from sun, wet-road and headlight glare at a small cost in recall?
- Test to run: does a cue calibrated on one camera transfer to another (the infrared cues in P2-P309 and P2-P312 are camera-specific)?
- Test to run: system-level success with the memorisation of a tracker (P2-P339) rather than single-frame scores.
- Claim wording: "to our knowledge"; never "first". Papers claiming "first" (P2-P304 daytime light attack, P2-P310 invisible attack) are the authors' claims.

## 6. Datasets, benchmarks and code seen
Licences were not checked for any item. Each needs a licence check before download or release (rule in state/DECK_DIGEST.md section 4).
| Item | What | Row | Licence question |
|---|---|---|---|
| LaserMark | 676 laser-stamped sign photos, 158 clean, 32 classes | P2-P308 | Release location and licence not seen |
| GTSRB, LISA, ARTS, ImageNet-compatible set | Sign and image sets used by attack papers | P2-P301, P2-P309, P2-P318 | Terms of each set; derived overlays |
| RFLA code | github winterwindwang/RFLA | P2-P301 | Seen in a search result, not opened |
| Advlight code | github RjDuan/Advlight | P2-P302 | Same |
| AdvLS code | github ChengYinHu/AdvLS | P2-P304 | Same |
| AdvNIR code | github MyNiuuu/AdvNIR | P2-P320 | Stated in the arXiv abstract, not opened |
| Infrared perturbations project page and detector code | rub-infsec.github.io/infrared_perturbations | P2-P313 | Code location seen on a project page; not opened |
| SIR2, SIR2+ | Reflection-removal benchmarks, objects behind glass | P2-P325 | Project page seen; licence not checked |
| SHIQ | About 16K real highlight images with masks | P2-P327, P2-P328 | Licence not checked |
| WoodScape sun-glare set | About 1,115 training and 294 test fisheye images | P2-P332 | Release announced; status not confirmed |
| Glare detection set | Multi-camera images, github maesfahani/glaredetection | P2-P333 | Not opened |
| NRGD, Flare7K++ | Night road glare and flare sets | P2-P337 | Not opened |
| RGB-polarimetric dataset | RGB, polarimetric, lidar, GNSS/IMU, free space | P2-P343 | Not opened |
| PolarLITIS | RGB and polarimetric images in fog; named in a survey text seen in a search result | none | Not read |
| BDD100K, ACDC | Benign day and night driving sets named on the owner deck | none | Terms to record before download |

## 7. Problem cards (hypotheses, not results)

### Card 1. Reflected light and glare look alike in one frame
Problem: reflected-light and laser attacks on signs resemble sun, wet-road and headlight glare, so a brightness or highlight check alone either flags glare or misses an attack shaped like glare.
Contribution to test: a viewpoint-conditioned highlight residual inside the tracked sign box (saturated and low-saturation area, contrast against the neighbouring sign surface, exposure drift) separates attack reflections from natural highlights better than brightness-only or texture-only checks at the same false-alarm rate, and abstains when tracking or exposure is unreliable.
Open-source starting point: OpenCV and scikit-learn; a frozen small detector as in the deck (YOLOX-Nano); optional mask sources P2-P344 (UNVERIFIED), P2-P329, P2-P328; attack generators with public code seen in search results (P2-P301, P2-P302, P2-P304; locations UNVERIFIED).
Data and laptop fit: attack side = digital overlays of reflected-light shapes on GTSRB and LISA sign tracks plus the owner's controlled clips; benign side = BDD100K and ACDC clips plus glare images (P2-P332, P2-P333). Licence question: record the licence of every set, including terms for derived overlays, before download; the LaserMark and WoodScape release terms are unverified. Laptop: deck route A (OpenCV cues cached on disk, logistic regression or boosting); no GPU assumed; a mask network only after a measured fit test. Split by recording, never by neighbouring frames.
Experiment workflow:
1. Build attack and benign tracks: overlay or record reflected-light patterns on sign tracks; collect glare, wet-road and headlight clips; split by recording.
2. Extract per-frame cues in the tracked sign box and cache them on disk.
3. Fit the expected cue change with box scale and image-plane motion on benign tracks; score the residual; set the abstain gate from tracking and exposure quality; calibrate on a separate set.
4. Compare detector-only, brightness-only, texture-only, an ILR-style colour-frequency check (P2-P309) and the residual at matched false alarms on held-out recordings.
Success measure: attack recall at a fixed false-alarm rate; false alarms per hour on benign glare clips; share of abstentions; p50 and p95 ms per frame; peak memory.
Prior work already covering part of it: P2-P338 pairs a light-source physics check with two-frame moving-camera consistency to reject natural lights; P2-P341 (UNVERIFIED) detects laser artefacts with HSV and Laplacian features on a Jetson. Neither is described as conditioning on viewing angle for reflections on a sign or as having an abstain state. The contribution is an increment.
Sources: P2-P301, P2-P302, P2-P303, P2-P304, P2-P329, P2-P338 (also P2-P341, P2-P344 and P2-P345, UNVERIFIED).

### Card 2. Infrared traces exist only for cameras without an infrared-cut filter
Problem: infrared attacks are invisible to people and visible to the detector only when the camera passes near-infrared light; the cue and the claim both depend on a sensor assumption.
Contribution to test: a per-camera false-colour check inside saturated regions (red and blue above green; colour range plus spatial frequency), calibrated on one camera and tested on a second, with a "not applicable" state when the camera has an IR-cut filter.
Open-source starting point: OpenCV; algorithm outlines in P2-P312 and P2-P309; no code located for either (UNVERIFIED).
Data and laptop fit: no public infrared-attack sign set was found. It needs the owner's recordings with an infrared-sensitive camera module and a low-power infrared source; buying hardware is an owner decision (NEEDS_OWNER). Licence question: own recordings have none; overlay tracks carry the GTSRB and LISA terms. Laptop: CPU only.
Experiment workflow:
1. Record signs with the infrared source on and off on a filterless camera, and again with a cut-off filter fitted.
2. Measure the false-colour cast and saturation statistics per camera.
3. Set cue and threshold on camera A.
4. Test on camera B, on visible reflections and on red or magenta benign objects.
Success measure: true-positive rate at a fixed false-alarm rate on the unseen camera; false alarms on colour look-alikes; ms per frame.
Prior work already covering part of it: P2-P309 (96% and 2.7% by day, 92% and 6.7% at night, 150 images per time) and P2-P312 (true-negative 99.97-100%) give such cues at proof-of-concept level; P2-P313 says speckle detection does not apply to incoherent infrared light. Open: transfer to an unseen camera and an honest abstain state.
Sources: P2-P309, P2-P310, P2-P311, P2-P312, P2-P313, P2-P320.

### Card 3. A retroreflective patch is hard to tell from normal sign sheeting at night
Problem: retroreflective patches in the sign colour are quiet by day and return headlight light at night, the same behaviour as normal sign sheeting.
Contribution to test: an angle-conditioned expectation of the sign's retroreflective response (headlight, sign, camera geometry from box scale and tracking) with a residual that flags excess return in patch-shaped regions, abstaining when ambient light or geometry leaves the calibrated range.
Open-source starting point: OpenCV; the retroreflection model of P2-P318 (entrance and viewing angle, roughness, IoR, specular tint) and the photometric relation in P2-P335.
Data and laptop fit: benign signs from BDD100K and ACDC night clips; attack clips would be the owner's tape-on-sign recordings (permission and safety are owner decisions). No public retroreflective-attack video set was found. Licence question: BDD100K and ACDC terms. Laptop: CPU features, no large model.
Experiment workflow:
1. Collect benign night sign tracks at several distances and angles with exposure data.
2. Fit expected region brightness against geometry per sign class and colour region.
3. Score the residual in patch-shaped regions; abstain by ambient light and tracking quality.
4. Test against own tape-on-sign clips and against a brightness-only baseline.
Success measure: attack recall at fixed false-alarm rate by distance and angle bin; false alarms per hour of night driving; abstain share; ms per frame.
Prior work already covering part of it: the defence found is hardware, a polarised headlight with a crossed camera filter (P2-P318). No software detector for retroreflective patches was found. The only earlier sign-level physical study found is small (P2-P317). Production systems' temporal memory lowers measured success (P2-P318, P2-P339), so system-level evaluation matters.
Sources: P2-P317, P2-P318, P2-P319, P2-P335, P2-P339.

### Card 4. Highlight networks are built for photo quality, not for a laptop cue
Problem: reflection and highlight removal networks are trained for image quality on glass or shiny-object scenes; their cost and fit to sign boxes are unknown.
Contribution to test: compare three mask sources for the sign-box specular region (HSV thresholds with a gradient test, a small U-Net, a frozen-encoder head), judged by how much each improves the Card 1 residual and not by removal quality.
Open-source starting point: P2-P344 (UNVERIFIED), P2-P329, P2-P328, P2-P331; compute table in P2-P330; surveys P2-P324, P2-P326.
Data and laptop fit: SHIQ (P2-P327), SIR2+ (P2-P325), WoodScape glare images (P2-P332), glare set (P2-P333). Licence question: all four unverified. Laptop: measure CPU latency and peak memory first; the only compute table seen lists 4.53 M to 116.99 M parameters for removal networks and no laptop timing (P2-P330).
Experiment workflow:
1. Time the three mask sources on laptop CPU at the sign-box crop size.
2. Score masks against weak labels on glare sets and sign crops.
3. Plug each mask into the Card 1 residual.
4. Ablate against a saturation-only region.
Success measure: p50 and p95 ms and peak memory; attack recall gain at matched false alarms over the saturation-only region; abstain rate.
Prior work already covering part of it: highlight detection and removal are well covered (P2-P327, P2-P328, P2-P329, P2-P331); no record read tests a highlight mask as a cue for attack detection.
Sources: P2-P324, P2-P326, P2-P327, P2-P328, P2-P329, P2-P330, P2-P331.

## 8. Leads not confirmed
From the brief: all seven leads were confirmed in records (RFLA 2307.07653 and ICCV DOI; NDSS 2024 infrared-laser paper; Adversarial Laser Beam; retroreflective patches; mirror and catoptric light; reflection removal; highlight detection).
Found during the run, not confirmed by lit_verify (NEEDS_VERIFY, most because Crossref was stopped):
1. LightRR, a lightweight reflection-removal network (CVPR 2026 open-access PDF seen; abstract says 3.01% of the parameters and 5.22% of the FLOPs of a reference network). Tried: arXiv search, no hit.
2. Physics-aware spatiotemporal consistency defence for driving perception (PubMed Central page dated 2026-01-27; trajectory-appearance energy; tested against RP2, CAPatch and SLAP; nuScenes figures 86.5% to 92.1% correction accuracy and 42 ms to 19 ms). Probably the "physics-aware defense (2026)" named on slide 05. Authors and journal not read. Tried: arXiv search, no hit.
3. Bilateral-filter specular highlight removal, UIUC-hosted PDF named eccv-10 (text says about 200 times faster than an older method on a CPU, video rate on a GPU). Tried: Crossref search, 429.
4. Motion and appearance of specularities in image sequences (Microsoft Research PDF named criminisi_eccv2002; covers how highlights move as the camera translates). Not checked.
5. Specular highlight enhancement from video sequences (PDF named icip_2013_cr on a university page; temporal specularity map using optical flow). Not checked.
6. Self-supervised sun glare detection CNN (ML4AD workshop PDF; BiSeNet-v2 on a MobileNet-v2 backbone, 6k real glare images, 95.5% accuracy for its best setting). Authors not read. Tried: arXiv search, no hit.
7. Survey of navigational perception sensors' security (IEEE Access 2025, DOI seen on a university page). Crossref stopped.
8. Passive polarised vision for autonomous vehicles, a review (Sensors 2024). Crossref stopped.
9. A dual field-of-view defence that treats glare among natural perturbations (Sensors 2026). Crossref stopped.
10. An image-processing-pipeline security SoK that mentions HDR against laser blinding. Crossref stopped.
11. A Japanese-language journal version of the retroreflective-patch work (CiNii record dated 2025-10-20). Not checked.
12. "Fight light with light: a review of physical adversarial attack within light transmission pipeline" (Neurocomputing 2026, DOI seen in a search result). A recent review of light-based physical attacks and a likely cross-check for this catalog. Authors and abstract not read. Crossref stopped.
Also unverified: an ACSAC 2026 acceptance notice for P2-P318 on a university lab page (venue claim, not a separate work).
Unconfirmed lead count: 12 works (items 1-12) plus 1 venue claim. Separately, 3 UNVERIFIED rows (P2-P341, P2-P344, P2-P345) need an official-page check.

## 9. Exclusions
- LiDAR reflective-surface attacks (an SVM detector for foil on LiDAR returns, seen in a search result): sensor outside the camera scope.
- Electromagnetic signal injection into image sensors (arXiv 2609.06973, seen in two results): not optical.
- Long-wave thermal-infrared detector attacks: not searched; different sensor.
- Shadow attacks (Zhong et al., CVPR 2022, seen): belongs to LIT_A2.
- Patch attacks and patch defences without light (PatchCleanser, naturalistic patches arXiv 2603.00217, PBCAT, transferable patches arXiv 2604.23105, AD-squared arXiv 2602.10160): other tasks; AD-squared not read.
- Seen, verified in the ledger but outside this cue family (the coordinator may route them to LIT_A4 or LIT_A5): EvilEye (arXiv 2307.13131, transparent display at the camera lens; the abstract says it bypasses state-of-the-art physical-attack detectors), VisionGuard-star (arXiv 2304.13919, majority-vote video detector with a brightness-transformation consistency test, built for patch attacks), and a TIFS 2024 projector-video attack that exploits high-speed shutters (not verified).
- Endoscopy and other medical highlight-detection papers seen in results: medical domain.
- A patent on a light backdoor method: not a paper.
- Camera-blinding experiments described in a secondary analysis page (it cites Qayyum et al., 2020): secondary source only, not catalogued.
- ImageNet-only or face-recognition light attacks beyond those listed: not searched.
