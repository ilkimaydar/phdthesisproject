# P2_LIT_A4 notes - lighting: projection, exposure, flicker (design slide 04)

Status: written by the LIT_A4 worker agent. NOT AUDITED: fresh-agent audit required. Reading depth is abstract level or metadata only; no full text was read. Rows: work/LIT_A4/rows.jsonl (42 rows; scripts/rows_check.py: VERIFIED 29, ARXIV_API_VERIFIED 13, MISMATCH 0, NOT_FOUND 0, schema problems 0; High 17, Medium 25). Read level by row: abstract 27, metadata-only 15 (Crossref carries no abstract for those; their text comes from the title and is marked as such in each row). Paper ids below are the paper_id values P2-P4xx written as P4xx.

Tool state during the run (limits the completeness of this note):
- websearch answered the first 11 queries and then returned "no results" for 14 consecutive queries (queries 12 to 25, any wording). Later discovery ran through scripts/lit_verify.py search-crossref and search-arxiv.
- export.arxiv.org returned HTTP 429 (STOP_HOST) on the 12th arXiv call; arXiv was not called again. Papers that exist only on arXiv could not be checked after that point.
- Crossref title search ranks short, exact titles well and descriptive phrases badly, so discovery of defence papers by topic was weak. Treat "no paper found" statements below as "none found with this search", not as proof of absence.

## Findings first (uncomfortable ones first)

1. Prior work already covers a large part of the slide 04 detection idea for lens-flare and auto-exposure projection attacks. P431 (ACM Transactions on Cyber-Physical Systems, 2024) adds a countermeasure to the GhostImage attack: it reduces detection to checking whether a ghost overlaps a detected object and uses spatiotemporal consistency to remove false positives; abstract reports a worst-case equal error rate of 5% on the authors' experimental data. The slide cites only the 2020 GhostImage attack (P409); this journal version is not on the slide.
2. Stripe and flicker detection has prior art too: P403 (ACSAC 2021) proposes a lightweight enhancement of the detector backbone that recognises rolling-shutter attacks and reports that common image-distortion metrics do not detect the attack; P406 (ACM Transactions on Sensor Networks, 2026) adds GhostBuster, a perturbation detector plus sign restorer, to the GhostStripe attack. A "temporal flicker gate" is therefore not new as a concept. Novelty would have to come from exposure normalisation, explicit false-alarm control on benign light, cross-sensor transfer and cost, none of which the abstracts report.
3. P402 (CCS 2020) already uses an explicit reflected-light expert (one of four lightweight CNNs on the detected object crop) against projected phantoms.
4. Patch-style defences do not transfer to projected light: the SLAP abstract (P401) says projections carry no patch-like behaviour and bypass the patch detector SentiNet.
5. No abstract read reports false-alarm rates on benign headlights, glare, rain or auto-exposure jumps. That is the open measurement the slide asks for.
6. No public data set found labels projected or flicker attack frames together with benign headlight, PWM flicker or auto-exposure events. Negatives exist (P415, P416, P420); attack positives must be simulated or recorded.

## 1. Problem map (attack families with the papers that define them)

A4-F1 Projector-based attacks (light placed on the object or scene)
| Id | Paper (year, venue class) | Mechanism and target | Reported in the record read |
|---|---|---|---|
| P401 | SLAP (2021, USENIX Security) | Optimised projection on a stop sign; detectors and sign classifiers | Up to 99% success in non-bright settings; evades SentiNet (abstract) |
| P402 | Phantom of the ADAS (2020, CCS) | Projected or billboard phantom objects shown for a split second; two commercial driver-assistance systems | 125 ms phantom in an advertisement video (ePrint text snippet); countermeasure in section 2 |
| P410 | OPAD (2021, ICCV workshop) | Projector-camera model inside the attack optimisation; classifiers; real 3D object | Works under background light (abstract); no numbers |
| P411 | Transient adversarial 3D projection (2024, preprint, not peer reviewed) | Projection on 3D curved surfaces such as vehicles; YOLOv3 and Mask R-CNN | Up to 100% in low ambient light, indoors (abstract); weakens as ambient light rises (text snippet) |
| P426 | Light projection vanishing attack against car detection (2023, ICASSP) | Projected light makes a detector miss a car; a review describes a drone-borne projector (secondary) | Abstract not read |
| P412, P440 | Adversarial laser beam (2021, CVPR); adversarial neon beam (2022, preprint) | Laser or neon beam as perturbation; classifiers | P440 abstract: 81.82% physical success; no driving detector |
| P432, P433, P434 | Adversarial color projection (2023); spot light (2023); CausalAttack (2026, SSRN preprint) | Projected colour, spot light, real-time light attack with brightness-aware transformation | P434 abstract claims about 2.14 times higher success than earlier light attacks (authors' claim) |

A4-F2 Camera-pipeline attacks (lens, exposure, rolling shutter, flicker)
| Id | Paper | Mechanism | Reported |
|---|---|---|---|
| P409 | GhostImage (2020, preprint record; venue RAID 2020 unconfirmed) | Projector aimed at the camera exploits lens flare and ghost effects and auto-exposure control | Up to 100% success depending on distance; 3 cameras (abstract) |
| P403 | They See Me Rollin' (2021, ACSAC) | Modulated light (cheap laser) injects stripes through the CMOS rolling shutter; 7 cameras | Hides up to 75% of objects seen by detectors (abstract) |
| P404 | Invisible Perturbations (2021, CVPR) | Modulated LED light, rolling-shutter stripes, ImageNet classifier | Targeted success up to 84% (abstract) |
| P413 | Over-the-air adversarial flickering (2021, CVPR) | Temporal flicker of illumination against video action classifiers; universal and synchronisation-free variants | No numbers in the abstract; not a detector or driving study |
| P414 | LED illumination modulation on face recognition (2023, preprint) | LED modulation plus rolling shutter against face detectors | 97.67%, 100%, 100% denial success on three face detectors (abstract); domain differs |
| P423, P436, P437 | AdvRain (2023); adversarial camera patch (2024); AdvLensPolluter (2025) | Lens-level stickers or contamination: raindrop look-alikes, transparent patch, lens contamination | Abstracts of P423 and P436 give no numbers; P437 title only |

A4-F3 Modulated-light attacks on traffic-light and sign recognition
| Id | Paper | Mechanism | Reported |
|---|---|---|---|
| P407 | Rolling Colors (2022, USENIX Security) | Laser stripe through the rolling shutter flips traffic-light colour | Maximum 30% (red to green) and 86.25% (green to red); effective over continuous frames from over 40 m against a moving vehicle (abstract) |
| P405 | GhostStripe, MobiSys 2024 | LED flicker timed to the camera and the vehicle position creates stripes on a sign | Wrong class held in up to 94% of frames while the vehicle passes (abstract) |
| P408 | L-HAWK (2025, NDSS) | A printed patch is activated by a long-distance laser that creates a colour strip in the camera image | Talk description only; no numbers read |
| P425 | MLIA (2022, TrustCom) | Modulated LED illumination against sign recognition | Title only |

Surveys that map these families: P441 (short-lived adversarial examples: flickering, motion, sensor, projection and gradient-based; Research Square preprint, not peer reviewed), P427 (physical attacks and defences, ACM Computing Surveys 2026), P435 (light transmission pipeline review, title only). Lens-level and contamination attacks are listed under A4-F2.

## 2. Solution map (defence and detection families)

| Family | Papers | What it does | Limits seen in the record |
|---|---|---|---|
| Authenticity experts on the detected object | P402 | Four lightweight CNNs judge object light, context, surface and depth on the crop; committee output | Authors report TPR about 0.99 at FPR 0 on their data; ePrint table snippet (column order assumed): light expert alone TPR 0.959 at FPR 0, and TPR 0.9968 with FPR 0.0652 at threshold 0.5. Sign crops, single frames, no flicker |
| Ghost-overlap test plus spatiotemporal consistency | P431 | Checks whether a lens-flare ghost overlaps a detected object; spatiotemporal consistency removes false positives | Worst-case EER 5% (authors' data). Aimed at ghost and auto-exposure projection; stripes not mentioned in the abstract |
| Stripe, laser or perturbation detectors | P403, P406, P442 | P403: lightweight backbone enhancement that recognises rolling-shutter attacks. P406: perturbation detector plus sign restorer (GhostBuster). P442: detector for laser-based physical attacks, title only | No false-alarm numbers on benign light in the abstracts; P442 abstract not read |
| Temporal prediction | P422 | Next-frame prediction by a convolutional encoder-decoder; flags camera blinding when predicted-versus-received frame similarity falls below a fixed threshold | Fixed threshold, no exposure normalisation stated; results not read (abstract cut at 1,800 characters) |
| Training-side defence | P401, P411 | SLAP abstract: an adaptive adversarial-learning defender lowered success by up to 80%. P411 names adversarial training as a candidate | Generic; not a light check |
| Sensor-level | P407, P405, P406, P428, P429 | Rolling-shutter redesign proposed by P407; P405 and P406 discuss camera-sensor countermeasures; flicker-mitigation sensors (P428, P429) | Hardware; titles only for P428 and P429 |
| Benign-light handling (the negative side) | P438, P418, P419, P430, P424, P439 | Flare-aware detector, flare data sets, LED traffic-light flicker removal, learned auto-exposure for detection, PWM headlight study with event cameras | Titles only except P418 and P419 |
| Reported failures | P401, P403 | SentiNet misses SLAP projections (P401); common image-distortion metrics do not flag rolling-shutter stripes (P403) | Abstract-level statements |

## 3. Closest prior work to design slide 04, ranked (exposure-aware local light anomaly score plus temporal flicker gate)

1. P431 (Man, ACM TCPS 2024). Reason: a detector-side light check for projected flare and auto-exposure attacks that already combines a local overlap test with spatiotemporal consistency and reports an EER. Difference to test: it targets ghost and flare patterns, not stripes or flicker; false alarms on benign headlight, rain and auto-exposure jumps are not in the abstract (UNVERIFIED).
2. P403 (Kohler, ACSAC 2021). Reason: an in-detector recogniser for the stripe half of the slide, built on a model of stripe size from camera datasheet values. Difference to test: false-alarm behaviour and cross-camera transfer of the recogniser are not in the abstract.
3. P406 (Guo, ACM TOSN 2026). Reason: perturbation detector plus restorer for stripes on signs, from the group that built the stripe attack. Difference to test: results and false alarms not in the abstract.
4. P402 (Nassi, CCS 2020). Reason: explicit reflected-light expert for projected content. Difference to test: learned, per-crop, no temporal gate, no flicker, no exposure test seen.
5. P422 (SAE paper 2020, authors' family name reads "D H" in Crossref). Reason: temporal frame-prediction detector for light-based blinding in driving video. Difference to test: fixed similarity threshold, no stated exposure normalisation.
6. P442 (Laser Guard, IEEE Access 2025): found late; only the title was read. Its title promises an efficient detector for laser-based physical attacks, so it may belong near the top of this list. Read it before ranking.
To our knowledge from these abstracts, no paper combines an explicit exposure-normalised local-versus-global residual with a flicker-frequency gate and reports false alarms per hour on benign headlight, rain and auto-exposure events. The search was incomplete (see tool state), so this is a gap candidate, not a verified gap.

Attack baselines to reproduce for slide 04 (positives): P401, P409, P405, P407, P403, P404.

## 4. Gaps and what is left to test

1. False alarms on benign light are not reported in any detection abstract read (P402, P403, P406, P422, P431). Needed: events and rates per hour for headlight glare, lens flare, rain, tunnel exits, PWM LED flicker, auto-exposure jumps.
2. Cross-sensor behaviour: P403 shows the effect depends on the camera readout (7 cameras; datasheet model), P407 used 5 cameras, P409 used 3. No detector abstract reports leave-one-camera-out results.
3. Rolling-shutter and frame-rate aliasing (the slide limitation): P413 builds a synchronisation-free variant; P405 adapts LED timing to the camera. No abstract reports where a detector's flicker cue vanishes or fakes a pattern.
4. Persistence: P405 keeps the wrong class stable across frames on purpose (demo text snippet says anomaly detectors could otherwise trigger a fail-safe). A gate that only looks for temporal inconsistency may not fire. P408 keeps a patch benign until a laser strip appears.
5. Adaptive attackers: P434 models brightness changes in its transformation; P401 tested an adaptive defender. No adaptive attack against an exposure-aware cue was found.
6. Moving-vehicle realism: only P405 and P407 (abstracts) and P401 (slides snippet) report moving-vehicle tests; the rest are static or lab set-ups.
7. Hardware: flicker-mitigation sensors (P428, P429) change the flicker signature at capture; the gate must be tested with and without such a sensor.
8. Data licences are not stated in the records read (P415, P416, P420, P421): record before download (deck rule).

## 5. Datasets, benchmarks and code seen

| Id | Name | What the record says | Hard-negative value | Licence or access |
|---|---|---|---|---|
| P415 | PVDN (also arXiv 2012.15376, in the ledger) | 59,746 annotated grayscale night images, 346 rural scenes; oncoming vehicles, headlamps, light reflections labelled | Headlamp light and reflections as benign light; grayscale only; no attack frames | Not stated in the abstract: check |
| P416 | ACDC | 8,012 driving images; 4,006 split over fog, night, rain, snow with same-scene normal-condition pairs; supports object detection | Night and rain with matched normal frames | Dataset page named in the abstract (not opened): check terms |
| P420 | BDD100K | Deck data; another paper describes 100,000 driving images with varied weather and lighting | Night and rain clips | Not stated: check |
| P421 | NightOwls | Pedestrians at night (title only) | Unknown glare content | Not stated: check |
| P417 | ExDark | Ten low-light image types including strong light, screen, window, shadow | Non-uniform benign illumination; images, not video | Repository named in the abstract (not opened): check |
| P418, P419 | Flare7K, Flare7K++ | 7,000 synthetic nighttime flares (5,000 scattering, 2,000 reflective; 25 and 10 types); 962 real flare captures; light-source annotations | Flare and glare around lights; overlay source for synthetic benign flare | Not stated: check |
| P439 | PWM headlight and event camera study | Title only | PWM headlight flicker reference; event cameras, not RGB | Unknown |
Code locations seen in search results and abstracts (none opened; all UNVERIFIED): SLAP artifacts repository (YOLOv3, Mask R-CNN, LISA-CNN, GTSRB-CNN, indoor and outdoor data), GhostBusters repository (P402), AdvLB code (P412), CausalAttack repository (P434), ExDark repository (P417), ACDC site (P416). No code was found for P403, P406, P431 or P422.
Open question for Q4 of the brief: no public set found with labelled auto-exposure jumps in driving video or labelled PWM flicker events (search limited; UNVERIFIED).

## 6. Leads not confirmed

Brief leads: all were matched to a verified record: SLAP (P401), Phantom of the ADAS (P402), GhostImage (P409; record found, published venue RAID 2020 not confirmed: only a curated list seen in search results names it, and it gives a slightly different title), ACSAC 2021 rolling-shutter paper (P403), CVPR 2021 rolling-shutter paper (P404), GhostStripe (P405, P406), Rolling Colors (P407), OPAD (P410), NDSS 2025 laser-triggered patch attack (P408, L-HAWK), LED flicker mitigation sensors (P428, P429 matched by title only), ACDC, ExDark, NightOwls (P416, P417, P421).
Unconfirmed leads (count 10; item 5 counts four titles and item 6 two titles):
1. GhostImage published venue and exact published title (arXiv record only; curated list says RAID 2020). Tried: websearch twice (no results), Crossref title search (found only the 2024 journal version P431).
2. Adversarial Camera Stickers (recalled by the agent, not a brief lead). Tried: Crossref title search (no match); arXiv stopped.
3. Adversarial Laser Spot (PMLR volume 189, seen in a search snippet). No DOI; arXiv stopped; not catalogued.
4. A later projector-phantom defence named PHANTOM in a search snippet that claims robustness across lighting. Title and venue not recovered; two follow-up searches returned nothing.
5. Titles seen without abstract and with unclear content, not catalogued: Detection of LiDAR and Camera Sensor Spoofing in Autonomous Vehicles (PICC 2025); Spatial-Temporal Anomaly Detection for Sensor Attacks in Autonomous Vehicles (SWC 2023); Physical Integrity Attack Detection of Surveillance Camera with Deep Learning based Video Frame Interpolation (IoTaIS 2019); Defense Against Physical Adversarial Attacks via Projection-Based Re-Attack (IEICE 2026).
6. Titles seen late, no abstract, mechanism unknown: AdvGLOW: Covert adversarial attacks against autonomous driving perception (ETS-Data 2026; may be a light-based attack, not known); Dynamic Adversarial Attacks on Autonomous Driving Systems (RSS 2024; may use emissive displays, not known).
Not read (details, not leads): the SAE paper P422 full author name and the results part of its abstract.

## 7. Exclusions (not catalogued, with reasons)

- Infrared laser reflection attacks, retroreflective patches and nighttime reflectivity masks (for example the RDPA preprint): reflection family, design slide 03 (LIT_A3 scope).
- Patch-only attacks and patch-only defences, including Revisiting Physical-World Adversarial Attack on Traffic Sign Recognition (NDSS 2025; patches against commercial systems): slide 01 and slide 05 scope; its spatial-memorization finding matters for temporal gating and is a pointer for LIT_A1 and LIT_A5.
- bAdvertisement (print phantoms), STOP! camera spoofing via the in-vehicle IP network (digital injection), LiDAR and radar spoofing: not optical attacks on the camera.
- Acoustic attacks on camera stabilisation (Poltergeist): not light.
- Face-recognition projector attacks other than P414: domain. P414 is kept because it uses the same LED plus rolling-shutter mechanism on a detector.
- PVDN follow-ups (saliency annotation, rain denoising on PVDN): low relevance to slide 04.
- Rolling-shutter correction and flicker-removal image-quality papers without an attack or driving link (Crossref hits): outside scope.

## 8. Answers to the four questions of the brief

1. Line of sight and equipment; moving vehicles. All optical attacks here need a line of sight to the camera or to the target. Projector attacks need a projector (P401 text snippet: long-throw projectors cost a few thousand dollars; P402 describes projection from a drone or a hacked billboard). Laser attacks need a laser aimed at the camera (P403, P407, P408). P405 needs LEDs near the sign plus vehicle tracking and a timing controller. Moving-vehicle results: P407 (over 40 m, continuous frames, abstract), P405 (real testbeds, up to 94% of frames, abstract), P401 (outdoor moving-vehicle settings, conference slides snippet only), P402 (commercial vehicles; projected phantom made a driver-assistance system react, authors' page). P411, P404, P403, P412 and P440 are indoor or lab only as read.
2. Dependence on camera sampling. P403 (stripe size predictable from datasheet; 7 cameras), P404 and P414 (LED modulation read through row exposure timing), P407 (5 cameras), P405 (timing adapted to the camera and vehicle), P408 (laser colour strip as trigger), P409 and P431 (auto-exposure control and lens flare; 3 cameras; success depends on distance), P413 (synchronisation-free variant). Sensors differ in line time, exposure and flicker mitigation (P428, P429), so results do not transfer by default.
3. Detection or defence for projected or flickering light. P431, P402, P406, P403, P422 (section 2). False-alarm behaviour on benign light changes: not reported in any abstract read. P431 says spatiotemporal consistency removes false positives (benign classes not named); P402 gives FPR on its own sign data only.
4. Public data with benign headlight, glare and auto-exposure changes. PVDN (headlamps and reflections, P415), ACDC (night and rain with matched normal frames, P416), BDD100K (P420), NightOwls (P421, contents not read), ExDark (P417), Flare7K and Flare7K++ (flare and glare, P418, P419). Labelled auto-exposure jumps or PWM flicker events: none found.

## 9. Problem cards (hypotheses, not results; all experiments stay inside the deck limits: one laptop, 32 GB RAM, CPU baselines first, GPU unknown)

Safety note for every card: no laser on any camera or person; recorded attacks use a low-power LED or projector indoors only.

### Card A4-1. Projected or flare light is accepted as a real object, and patch detectors do not see it
- Problem: a projector can place a phantom or an optimised pattern on a sign or into the lens; a frozen detector accepts it and patch detectors miss it (P401, P402, P409).
- Contribution to test: an exposure-normalised local light residual (object region versus its surround after removing the global exposure trend), added to detector confidence, separates projected content from real content with fewer false alarms than a brightness-only check at the same recall. Prior work covers part of this: P402 (learned light expert) and P431 (ghost-overlap test plus spatiotemporal consistency). The open point is whether a few hand-built features match them at far lower cost and whether exposure normalisation lowers false alarms on benign light.
- Open-source starting point: a frozen small detector (the deck names YOLOX-Nano), OpenCV and NumPy features, scikit-learn logistic regression or boosting; SLAP artifacts repository (models, indoor and outdoor data) and the GhostBusters repository as reference code (both UNVERIFIED, not opened).
- Data and laptop fit: positives are projections composited onto benign night frames with a simple additive-light and colour-mixing projector model (the models in P401 and P410), plus a small own indoor recording with a low-power projector. Negatives: PVDN (P415), ACDC night and rain (P416), BDD100K night clips (P420). CPU only; features cached on disk; frames streamed. Licence question: PVDN, ACDC and BDD100K terms for research use and for sharing derived frames are not in the records read; SLAP artifact licence unknown.
- Experiment workflow: (1) freeze the detector, run it on benign clips and on composited positives, split by recording; (2) compute the global exposure trend (median luminance per frame), then the object-minus-surround residual in luminance and chroma and the sharpness of the region boundary; cache; (3) fit the small head with recording-grouped cross-validation and set the threshold at a fixed false-alarm rate; (4) compare with detector-confidence only, brightness-only and, if it can be re-implemented, a GhostBusters-style light expert; report per-condition tables for headlight, rain and night.
- Success measure: TPR at a fixed FPR on held-out recordings; false alarms per hour on long benign night clips; p95 ms per frame on CPU; count of abstentions.
- Sources: P401, P402, P409, P410, P411, P431, P415, P416, P420.

### Card A4-2. Stripe and flicker attacks depend on the camera, so a flicker cue tuned on one sensor may fail on another
- Problem: modulated LED or laser light becomes stripes through the rolling shutter, and stripe period, contrast and persistence depend on line time, exposure and frame rate; flicker-mitigation sensors and benign PWM lights alter the same signal (P403, P404, P405, P407, P428).
- Contribution to test: a small row-profile flicker gate (detrend each frame, spectrum along image rows, persistence over a few frames, overlap with the detected object) calibrated per camera from its line time and exposure setting, with an explicit abstain state in aliasing regions. Prior work covers part of this: P403 (stripe recogniser inside the detector backbone) and P406 (perturbation detector plus restorer). The open point is cost, exposure-aware normalisation, the abstain state and transfer to an unseen sensor.
- Open-source starting point: NumPy FFT and OpenCV; stripe models from P403 and P404 as simulation guides. No public code for P403 or P406 was seen (UNVERIFIED).
- Data and laptop fit: fully synthetic stripes on benign frames using a rolling-shutter row model with several line times, exposures and LED frequencies (CPU); a small own recording with a low-power LED and one or two different cameras; negatives with LED headlights and LED signs from BDD100K (P420) and PVDN (P415, grayscale). Licence question: BDD100K and PVDN terms; own recordings carry no third-party licence.
- Experiment workflow: (1) build the stripe simulator with line time, exposure, LED frequency and duty cycle as parameters; (2) implement the gate and the exposure normalisation; (3) evaluate leaving one camera profile out, and sweep frame rate and exposure to list the aliasing cases where stripes vanish or are faked; (4) compare with temporal-only and local-intensity-only checks and report the abstain rate in aliasing zones.
- Success measure: recall at a fixed FPR on held-out sensor profiles; false alarms per hour on benign flicker (PWM headlights, LED signs); abstain rate in aliasing zones; p95 ms per frame.
- Sources: P403, P404, P405, P406, P407, P413, P428, P429, P430.

### Card A4-3. Benign light changes look like attacks and nobody reports the false-alarm rate
- Problem: headlight glare, lens flare, rain, tunnel exits and auto-exposure jumps change local and global brightness; none of the detection abstracts read reports false alarms on them (P402, P403, P406, P422, P431).
- Contribution to test: a hard-negative protocol (event taxonomy with automatic tagging) and a false-alarms-per-hour measurement for simple checks and for published-style detectors. Prior work covers: none found at abstract level; P431 says spatiotemporal consistency removes false positives but names no benign light classes.
- Open-source starting point: OpenCV luminance statistics (the deck card 11 starting point), scikit-learn; frozen detector.
- Data and laptop fit: PVDN (P415), ACDC (P416), BDD100K (P420), NightOwls (P421, contents not read), ExDark (P417, images), Flare7K and Flare7K++ (P418, P419) as overlay source for synthetic flare. Clips are streamed and only tags and features stored. Licence question as in card A4-1.
- Experiment workflow: (1) auto-tag events: global luminance step within k frames, saturated-blob growth (oncoming headlight), overlaid flare, rain; (2) run local-intensity, temporal-only and exposure-aware residual checks over the tagged clips; (3) count alarms per hour by tag at a recall matched on synthetic attack insertions; (4) have an independent reviewer inspect a sample of alarms.
- Success measure: false alarms per hour by event tag at matched recall; share of alarms explained by a tag; p95 ms per frame.
- Sources: P415, P416, P417, P418, P419, P420, P421, P424, P430, P438, P439.

### Card A4-4. Attacks built to stay stable over frames, or to wait for a trigger, can slip past a per-frame or purely temporal gate
- Problem: GhostStripe holds the wrong class over consecutive frames by timing the LED (P405); L-HAWK keeps a patch benign until a laser strip triggers it (P408); CausalAttack models brightness changes (P434).
- Contribution to test: an onset-coincidence rule: flag when a detector output change (class flip or disappearance) in a region follows, within a short window, a light-cue onset in the same region, with abstention when the light cue is unreliable. Prior work covers part of this: P431 (spatiotemporal consistency for ghost overlap) and P422 (frame prediction); neither is reported at abstract level for detector-change onset coincidence (UNVERIFIED).
- Open-source starting point: timestamped replay of per-frame detector outputs and simple causal event logic (the deck cards 6 to 8 starting points).
- Data and laptop fit: simulated insertions of stable-stripe sequences and trigger strips onto benign BDD100K or ACDC clips with recorded detector outputs; no public GhostStripe or L-HAWK data seen (UNVERIFIED). CPU only. Licence question as in card A4-1.
- Experiment workflow: (1) record per-frame detector outputs on benign clips; (2) insert stripe or strip sequences with controlled onset, duration and persistence; (3) compute the onset-coincidence score and compare with persistence-only and per-frame scores; (4) add an adaptive variant whose stripes follow the exposure and report the loss.
- Success measure: recall and warning delay (frames) at a fixed FPR; drop under the adaptive variant; abstain rate.
- Sources: P405, P407, P408, P431, P422, P434, P401.
