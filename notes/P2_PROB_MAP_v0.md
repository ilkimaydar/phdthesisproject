# P2 problem map v0 (PROB_MAP)

Status: worker agent PROB_MAP; sources: state/PROJECT_BRIEF.md and state/DECK_DIGEST.md only. No literature search, no catalog rows, nothing run. Every statement, problem lines included, is a hypothesis; no novelty is claimed. Paper, method and dataset names are the owner's labels, UNVERIFIED until a catalog row confirms them. NOT AUDITED: written by this agent; fresh-agent audit required.

## 0. Conventions
- Slide pipeline: frozen detector plus independent cue -> consistency residual -> flag with explanation, or benign / abstain.
- Injected attack: a physical attack (patch, shadow, light spot, projected or flickering light, object hiding) rendered into public video; kept only if it changes the detector output (slide 05: "valid attack-injected").
- Measures: recall at a fixed FPR set on separate calibration recordings; FA/h = false alarms per hour of benign driving; time-to-alarm from attack onset; p50/p95 ms per frame with decode; abstain rate. Tests on held-out recordings, split by recording or route (deck rule).
- Laptop: 10-core CPU, 32 GB RAM, 6 GB GPU; CPU first, GPU only after a measured fit test (deck rule).
- Licence question for every dataset named: research use and release of attack-injected derivatives; record before download (not read here).
- B: depends on OWNER_INPUT item 5 (benign-or-abstain branch versus the sentence slide 45 marks dropped).

## 1. Deck cards 1-14 -> attack-detection analogue (all 14 mapped; card 3 in part)
| Deck | Deck problem | Analogue (hypothesis) | Card |
|---|---|---|---|
| 1 | Unlit obstacles recognised too late | attack evidence fades at night and in bad weather | P12 |
| 2 | Ordinary shadows trigger false alarms | benign shadows flood a shadow-attack check | P04 |
| 3 | A cue does not locate its source | the alarm does not name its cue and region; distance: no analogue | P13 |
| 4 | Confidence survives when visibility fails | the attack score stays confident when its cue is unreliable | P14 |
| 5 | The next camera changes the result | thresholds do not transfer across camera or view | P02 |
| 6 | The correct warning arrives too late | the alarm comes after the detector output was used | P15 |
| 7 | The prediction describes an old frame | detector and cue outputs come from different frames | P15 |
| 8 | Confirmation consumes the warning time | fixed persistence delays every attack alarm | P10 |
| 9 | Resizing deletes the earliest cue | downscaling erases distant patch and stripe evidence | P16 |
| 10 | Compression erases weak evidence | quantization and codec change attack evidence | P17 |
| 11 | Exposure changes masquerade as hazards | exposure jumps and headlights mimic optical attacks | P08 |
| 12 | Frame alignment fails in darkness | misalignment fakes temporal attack evidence | P14 |
| 13 | Compute is spent on the wrong regions | the cue budget skips objects an attacker can target | P16 |
| 14 | Sparse labels cannot measure cue onset | no labels say when an attack becomes visible and effective | P20 |

Card headings name the slide item (test = left to test; failure, limit = critical failure case). Owner contributions (numbers of state/PROJECT_BRIEF.md section 2): 1 P01-P11, P18; 2 P19; 3 P04, P06, P08, P12; 4 P12, P14; 5 P15-P17; 6 P13; 7 P11, P20, P21.

## 2. Cards (Sources on every card: to be linked to catalog rows by the coordinator)

### P01 Natural-looking patches pass texture checks (slide 01, test a)
- Problem: a patch in the sign's own colours can keep texture normal while the detector output is wrong.
- Contribution to test: H: a class-specific contour cue (outline versus the shape implied by the class, or outline without detection) adds recall beyond texture for shape-changing flips and hiding, not for same-shape pairs.
- Open-source starting point: OpenCV contours and HSV; YOLOX-Nano; scikit-learn.
- Data and laptop fit: benign sign clips (LISA, GTSRB named on slide 02) plus injected palette-limited patches; CPU only.
- Experiment workflow: (1) crop tracked sign ROIs; (2) inject patches that flip the detector; (3) fit texture, contour, both; (4) compare by pair type.
- Success measure: recall at fixed FPR per pair type; ms per ROI.

### P02 A small head may not hold across viewing angle and camera (slide 01, test b; deck 5)
- Problem: a head fitted on near-frontal views from one camera may read oblique or distant outlines as attacks.
- Contribution to test: H: normalising the ROI by estimated perspective, or conditioning on size and aspect bins, keeps FPR stable on unseen angles and an unseen camera.
- Open-source starting point: OpenCV perspective warp; frozen MobileNetV3-Small; scikit-learn.
- Data and laptop fit: two public sources split by camera; CPU, GPU features after a fit test.
- Experiment workflow: (1) bin ROIs by size and aspect as a viewpoint proxy; (2) set the threshold on seen bins and one camera; (3) apply it to the rest; (4) compare with and without normalisation.
- Success measure: FPR shift at the transferred threshold; recall at matched FPR.

### P03 Occlusion and artistic signs destroy geometric evidence (slide 01, failure; B)
- Problem: occluded, damaged, stickered or artistic signs break the outline without an attack.
- Contribution to test: H: a contour-quality score (share of the expected outline recovered) sends low-quality ROIs to abstain and holds FPR at a reported coverage.
- Open-source starting point: OpenCV contour fitting; synthetic occlusion masks; scikit-learn.
- Data and laptop fit: benign occluded signs in public data plus synthetic occlusion; CPU only.
- Experiment workflow: (1) grade or synthesise occlusion; (2) score contour quality; (3) sweep the abstain threshold; (4) plot FPR and recall against coverage.
- Success measure: FPR at fixed coverage; abstain rate and recall per occlusion level.

### P04 Benign shadows flood a shadow check with false alarms (slide 02, test a; deck 2; B)
- Problem: tree, pole and cloud shadows on signs change the shadow cue, sometimes the detector too, in ordinary sunny driving.
- Contribution to test: H: a physics gate (shadow edges move with ego-motion and agree with other scene shadows in direction and darkening) lowers FA/h at matched recall versus shadow-only and temporal-only scores.
- Open-source starting point: OpenCV shadow mask, edges, optical flow; scikit-learn.
- Data and laptop fit: BDD100K daytime clips with natural shadows plus injected shadows; CPU only.
- Experiment workflow: (1) mine shadowed sign tracks; (2) inject shadows that change the detector; (3) score shadow-only, temporal-only, gated; (4) compare at matched recall.
- Success measure: FA/h at matched recall; recall at fixed FPR; ms per frame.

### P05 Coherent, plausible shadow attacks evade the checks (slide 02, test b; failure)
- Problem: a crafted shadow held stable over frames gives temporal checks nothing, and a real occluder's shadow obeys the same physics as a tree's.
- Contribution to test: H1: a shadow-to-sign geometry residual keeps recall on coherent attacks where temporal-only scores fall. H2: separability falls as shadows approach natural ones; report that boundary and abstain beyond it.
- Open-source starting point: own shadow renderer on OpenCV; the P04 cues.
- Data and laptop fit: injected shadows on public clips, swept from crafted to natural-like; CPU only.
- Experiment workflow: (1) render re-placed and track-attached shadows, swept in softness, darkening and shape; (2) keep those that fool the detector; (3) score temporal-only, geometry, both; (4) plot by regime.
- Success measure: recall at fixed FPR per regime; AUROC against plausibility.

### P06 Natural highlights look like reflected-light attacks (slide 03, test; B)
- Problem: retroreflection under headlights, sun glints, wet roads and glare put bright saturated regions on signs at night and in rain.
- Contribution to test: H: a view-conditioned residual (highlight motion and scale on the sign during approach; whole-face retroreflection versus a local spot) rejects natural highlights better than brightness-only or texture-only checks.
- Open-source starting point: OpenCV saturation mask, region tracking, ECC alignment; scikit-learn.
- Data and laptop fit: BDD100K and ACDC night and rain data plus injected light spots; own recordings need an owner decision; CPU only.
- Experiment workflow: (1) mine highlight-on-sign events; (2) inject light spots that change the detector; (3) score the three checks; (4) evaluate per condition.
- Success measure: FA/h per condition at matched recall; recall at fixed FPR.

### P07 The sensor model decides what an RGB cue can see (slide 03, limit)
- Problem: an IR attack may reach a camera without IR filtering in a form no public RGB data shows, and an IR-filtered camera may never see it.
- Contribution to test: H: a threat-model table (attack family against the sensor property it needs: IR sensitivity, rolling shutter, auto-exposure) scopes every claim.
- Open-source starting point: none (documentation task).
- Data and laptop fit: no physical test without IR hardware; documentation only.
- Experiment workflow: (1) list attack families from catalog rows; (2) note the sensor property each needs; (3) note each dataset's camera documentation; (4) mark claims in or out of scope.
- Success measure: every claim names its sensor assumption; families out of scope counted.

### P08 Exposure jumps and headlights mimic optical attacks (slide 04, test; deck 11; B)
- Problem: exposure steps, headlight sweeps and LED lighting change global and local luminance as projected or flickering attacks do.
- Contribution to test: H: separating the global luminance trend from persistent local residuals, plus a gate that needs ROI flicker absent from the background, lowers FA/h versus local-only and temporal-only checks.
- Open-source starting point: OpenCV luminance statistics; NumPy FFT on ROI traces; scikit-learn.
- Data and laptop fit: BDD100K night clips plus injected projections and stripe flicker; CPU only.
- Experiment workflow: (1) extract global and ROI luminance traces; (2) inject attacks that change the detector; (3) score local-only, temporal-only, gated; (4) repeat on an unseen camera.
- Success measure: FA/h at matched recall; recall at fixed FPR; p95 ms.

### P09 Rolling shutter and frame rate hide or fake flicker (slide 04, limit)
- Problem: flicker near the frame rate shows as stripes, beats or nothing by exposure and readout, so attacks differ per camera and benign LEDs can alias into attack-like ones.
- Contribution to test: H: a sampling model (frame rate, exposure, row readout) predicts where flicker is observable; gating to that band and abstaining outside it keeps FPR stable across simulated sensors.
- Open-source starting point: own NumPy and OpenCV rolling-shutter simulator.
- Data and laptop fit: synthetic sequences; real cross-sensor recordings need hardware (owner decision); CPU only.
- Experiment workflow: (1) simulate modulated light through sensor models; (2) map observable and aliased regions; (3) run the P08 gate per region; (4) compare predicted and measured recall.
- Success measure: recall and FPR per simulated sensor.

### P10 Fixed persistence trades warning time for false alarms (slide 05, test; deck 8)
- Problem: requiring k suspicious frames suppresses false alarms but delays every alarm and ignores cue strength.
- Contribution to test: H: causal evidence accumulation weighted by cue reliability, with bounded memory and an insufficient-evidence state, alarms earlier than fixed persistence at the same FA/h, also on unseen families.
- Open-source starting point: own cumulative-score rule on scikit-learn cue scores; OpenCV Kalman tracker.
- Data and laptop fit: injected clips with known onset (P20) plus long benign clips; CPU only.
- Experiment workflow: (1) compute per-frame cue scores on tracks; (2) fit fixed-k and accumulation rules; (3) set both to the same FA/h on calibration recordings; (4) compare.
- Success measure: median and p95 time-to-alarm at matched FA/h; recall on held-out families.

### P11 Gains over prior consistency checks must survive controls (slide 05, limit; footer)
- Problem: the slide says prior work already uses temporal and physical consistency, so any gain is incremental and may vanish under other operating points or splits.
- Contribution to test: H: with matched FPR from a calibration set and recording-level bootstrap intervals, the multi-cue model keeps a recall gain over temporal-only and the slide comparators; a null result is reported as one.
- Open-source starting point: slide comparators PatchZero, X-Detect, ADAV, physics-aware defense 2026 (UNVERIFIED; code unknown); own temporal-only baseline.
- Data and laptop fit: P20 benchmark; reimplementation cost unknown; GPU (fit test first).
- Experiment workflow: (1) confirm comparators in catalog rows and look for code; (2) run all on one frozen detector; (3) fix operating points; (4) report gains with intervals and a per-cue ablation.
- Success measure: recall gain at matched FPR with its interval; per-cue ablation; p95 ms.

### P12 Attack evidence fades at night and in bad weather (deck 1; contributions 3, 4)
- Problem: noise, blur and low contrast weaken edges, outlines, shadow masks and texture, so cues lose signal and an attack hides behind ordinary degradation.
- Contribution to test: H: scoring each cue alone per condition shows which keeps signal at night; a condition-aware fusion narrows the day-night recall gap at the same FPR.
- Open-source starting point: frozen YOLOX-Nano and MobileNetV3-Small, small temporal head (deck card 1); OpenCV.
- Data and laptop fit: BDD100K night, ACDC, PVDN, a low-light set (deck) plus injected attacks; night rendering realism is open; GPU (fit test first).
- Experiment workflow: (1) inject matched attacks into day, night, rain and fog clips; (2) score each cue per condition; (3) fuse with and without condition input; (4) compare per condition.
- Success measure: recall at fixed FPR per condition and cue; cases with no usable evidence.

### P13 An alarm does not show which cue and region caused it (deck 3; contribution 6)
- Problem: a bare attack score gives nothing to verify, and post-hoc saliency may point at regions the score did not use.
- Contribution to test: H: with one residual per cue, an additive fusion names the top cue and its ROI per alarm; masking that evidence lowers the score (faithfulness); abstain when no cue localises.
- Open-source starting point: per-cue residuals; scikit-learn logistic regression terms; OpenCV masks.
- Data and laptop fit: injected attacks give the true region and family; CPU only.
- Experiment workflow: (1) log per-cue contributions per alarm; (2) compare named cue and ROI with the injected family and mask; (3) mask the named evidence and rescore; (4) count abstentions.
- Success measure: share of alarms naming the right cue; IoU with the attack mask; score drop after masking.

### P14 The attack score stays confident when its cue is unreliable (deck 4, 12; contribution 4; B)
- Problem: under glare, darkness or rain a score calibrated on clear days stays confident, and failed alignment in the dark creates attack-like residuals.
- Contribution to test: H: three outputs (attack, no attack, insufficient evidence) calibrated per condition on cue-quality features, alignment included, hold the stated error rate and lower night FA/h at a reported abstain rate.
- Open-source starting point: scikit-learn calibration; OpenCV ECC alignment and optical flow (deck cards 4, 12).
- Data and laptop fit: ACDC and BDD100K night with a separate calibration set per condition; CPU only.
- Experiment workflow: (1) compute cue quality (contrast, noise, ECC score, flow consistency); (2) relate residual size to it on benign clips; (3) calibrate with abstain thresholds; (4) report risk against coverage.
- Success measure: calibration error per condition; night FA/h at matched recall; abstain rate.

### P15 The alarm arrives late or compares stale frames (deck 6, 7; contribution 5)
- Problem: an alarm after the detector output was used changes nothing, and a cue slower than the detector pairs outputs of different frames.
- Contribution to test: H1: timing every stage (decode, detector, cues, fusion, queue) ranks cue sets differently than accuracy does. H2: pairing by timestamp (Kalman extrapolation) lowers false residuals versus latest-output pairing.
- Open-source starting point: ONNX Runtime, replay harness, OpenCV Kalman (deck cards 6, 7); StreamYOLO comparator (deck label).
- Data and laptop fit: public clips replayed at native frame rate; timing on the laptop itself.
- Experiment workflow: (1) build the replay harness with per-stage stamps; (2) run cue sets at real speed; (3) compare both pairings on fast-motion clips; (4) report timing and FPR.
- Success measure: p50 and p95 end-to-end ms; time-to-alarm at matched FA/h; FPR per pairing.

### P16 Downscaling erases distant evidence; checking every object costs too much (deck 9, 13; contribution 5)
- Problem: the downscaled detector input may erase a sticker or stripe on a distant sign, while full-resolution cues on every object exceed the frame budget.
- Contribution to test: H: a cheap overview picking a few full-resolution ROIs by uncertainty recovers distant-attack recall at fixed compute; an attack on an unpicked object is the failure to test.
- Open-source starting point: SAHI utilities, YOLOX-Nano, bounded scheduler (deck cards 9, 13).
- Data and laptop fit: native-resolution public video (resolution to be checked); GPU (fit test first).
- Experiment workflow: (1) measure cue signal against apparent size at two resolutions; (2) add ROI selection under fixed budgets; (3) compare random and uncertainty-ranked picks; (4) attack the lowest-ranked object.
- Success measure: recall at fixed FPR by apparent size and budget; ms per frame.

### P17 Quantization and video compression change attack evidence (deck 10; contribution 5)
- Problem: quantizing detector and cue head, and the codec of recorded video, can erase fine attack texture or add artefacts.
- Contribution to test: H: choosing quantization and codec settings by attack recall at fixed FPR selects a different setting than detector mAP does; codec artefacts raise texture-cue false alarms.
- Open-source starting point: YOLOX-Nano export, ONNX Runtime quantization (deck card 10); OpenCV re-encoding.
- Data and laptop fit: P20 benchmark re-encoded at several qualities; CPU only.
- Experiment workflow: (1) export float and quantized models; (2) re-encode clips; (3) run the pipeline per setting; (4) compare recall, FPR, mAP and latency.
- Success measure: recall at fixed FPR and mAP per setting; model size and ms.

### P18 The check fits the attacks it has seen (contribution 1; abstract: unfamiliar attacks)
- Problem: a check trained on one family (patches) may miss another (projected light) or a new variant.
- Contribution to test: H: benign-only residual thresholds, or leave-one-family-out training, keep held-out-family recall at the same FPR closer to in-family recall than a supervised attack classifier does.
- Open-source starting point: scikit-learn one-class and supervised models on the P01-P10 cue features.
- Data and laptop fit: P20 benchmark with the five families of section 0; CPU only.
- Experiment workflow: (1) label attacks by family; (2) train on four families and on benign data only; (3) test on the fifth; (4) rotate.
- Success measure: recall at fixed FPR on the held-out family; gap to in-family recall.

### P19 Which object was hidden, missed or misclassified (contribution 2)
- Problem: "attack in this frame" does not say which object is affected or how, which a safety decision needs.
- Contribution to test: H: track predictions plus cue evidence type the outcome per track: vanished (track and cue, no detection), misclassified (shape-class disagreement), phantom (detection without cue or motion support).
- Open-source starting point: OpenCV Kalman tracker; per-cue residuals.
- Data and laptop fit: injected attacks with known outcome type; CPU only.
- Experiment workflow: (1) log tracks and detections; (2) write typing rules; (3) inject each outcome type; (4) score typing and restored boxes.
- Success measure: precision and recall per outcome type; IoU of restored boxes of vanished objects.

### P20 The attack benchmark with onset labels must be built (contribution 7; deck 14)
- Problem: the slides need attack video with benign hard negatives and onset labels; public driving video gives only the benign side.
- Contribution to test: H: injecting the five families with matched perspective and lighting, logging visible-onset and effect-onset (first changed detector output) and keeping only valid injections gives a reproducible benchmark.
- Open-source starting point: OpenCV rendering (homography, blending, light model); CVAT for any real clips (deck card 14).
- Data and laptop fit: BDD100K, ACDC, LISA, GTSRB (deck and slides); CPU only; derived clips shared only if the licence allows.
- Experiment workflow: (1) select clips, split by recording; (2) render attacks with logged parameters, seeds and onsets; (3) keep valid ones; (4) write a manifest with hashes; double-label real clips if any.
- Success measure: valid clips per family and condition; attack success rate; identical hashes on rerun.

### P21 An attacker who knows the checks keeps the cues consistent (contribution 7; this agent's reading)
- Problem: each check is a fixed rule; an attack shaped to keep its cue consistent while the detector still fails would pass.
- Contribution to test: H: adding a cue-consistency penalty to the attack objective lowers check recall; the drop and the constrained attack's success on the detector measure robustness.
- Open-source starting point: the detector's training framework for gradients (install is an owner decision); differentiable cue proxies.
- Data and laptop fit: digital only; 6 GB GPU at reduced resolution after a fit test.
- Experiment workflow: (1) build differentiable contour, luminance and shadow proxies; (2) craft attacks with and without the penalty; (3) measure detector success and check recall; (4) plot the trade-off.
- Success measure: check recall at fixed FPR against penalty weight; attack success under the penalty.

## 3. Ranking
Scores are this agent's judgment. F (fit to the red focus of slide 45): 3 core of a red cue family or a direct test of lightweight or explainable; 2 supports them; 1 infrastructure. L (laptop): 3 CPU, OpenCV and scikit-learn on public clips plus injection; 2 GPU, harder rendering, reimplementation or an install; 1 hardware or data not available. M (measurement): 3 one number read from the run; 2 own protocol or proxy labels; 1 none with public data. Order: sum, F, design-slide origin, M, L, number.

| Rank | Card | F | L | M | Sum | B | Reason |
|---|---|---|---|---|---|---|---|
| 1 | P01 | 3 | 3 | 3 | 9 | | slide 01 test; CPU contour cue |
| 2 | P04 | 3 | 3 | 3 | 9 | B | slide 02 test; CPU shadow cues |
| 3 | P08 | 3 | 3 | 3 | 9 | B | slide 04 test; CPU luminance traces |
| 4 | P10 | 3 | 3 | 3 | 9 | | slide 05 test; CPU rule on cue scores |
| 5 | P13 | 3 | 3 | 3 | 9 | | explainable; injection gives the truth |
| 6 | P15 | 3 | 3 | 3 | 9 | | lightweight; timing on the laptop itself |
| 7 | P17 | 3 | 3 | 3 | 9 | | lightweight; ONNX Runtime on CPU |
| 8 | P05 | 3 | 2 | 3 | 8 | | slide 02; coherent rendering is harder |
| 9 | P06 | 3 | 2 | 3 | 8 | B | slide 03; light-spot realism uncertain |
| 10 | P11 | 3 | 2 | 3 | 8 | | slide 05 limit; comparator code unknown |
| 11 | P02 | 3 | 3 | 2 | 8 | | slide 01; viewpoint bins are a proxy |
| 12 | P03 | 3 | 3 | 2 | 8 | B | slide 01 failure; occlusion grading |
| 13 | P16 | 3 | 2 | 3 | 8 | | lightweight; native-resolution video, GPU |
| 14 | P14 | 2 | 3 | 3 | 8 | B | supports all cues at night |
| 15 | P18 | 2 | 3 | 3 | 8 | | contribution 1; needs all five families |
| 16 | P19 | 2 | 3 | 3 | 8 | | contribution 2; rules on tracks |
| 17 | P20 | 2 | 3 | 3 | 8 | | prerequisite; fit is indirect |
| 18 | P09 | 3 | 2 | 2 | 7 | | slide 04 limit; simulation only |
| 19 | P12 | 2 | 2 | 3 | 7 | | night not red-marked; rendering realism |
| 20 | P21 | 2 | 2 | 3 | 7 | | gradients need GPU and an install |
| 21 | P07 | 2 | 1 | 1 | 4 | | slide 03 limit; needs IR hardware |

## 4. Cross-cutting open points (hypotheses)
1. False-alarm definition: when a benign shadow or glare makes the detector wrong, an alarm flags a real detector error but is a false attack alarm. Fix one definition before any FA/h number; report both counts.
2. B cards (P03, P04, P06, P08, P14) rest on the branch OWNER_INPUT item 5 leaves open. If it is dropped, benign look-alikes are still needed as hard negatives for FA/h; only the abstain parts lapse.
3. Every card assumes a frozen sign-capable detector; whether a sign-trained YOLOX-Nano checkpoint exists, and under which licence, is open.
4. Which named datasets hold video rather than single frames is UNVERIFIED (LISA, GTSRB, ACDC, PVDN in particular).
5. P20 is a prerequisite of every card that injects attacks; schedule it first regardless of rank.

## 5. Not mapped or only partly mapped
- Deck card 3, distance interval: no analogue (an alarm needs an image region, not a hazard distance).
- Slide 03 IR limit: scope card only (P07). Slide 04 cross-sensor test: simulation only (P09).
- Slide 01 "APDE patch attacks": acronym not identified. Comparator labels (PatchZero, X-Detect, ADAV, physics-aware defense 2026, StreamYOLO): not searched by design; UNVERIFIED.
