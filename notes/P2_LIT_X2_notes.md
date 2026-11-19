# P2_LIT_X2 notes - datasets and benchmarks with licences (X2-F1 to X2-F4)

Status: written by LIT_X2 (continuation of an agent stopped by a provider rate limit). NOT AUDITED: fresh-agent audit required. Rows: work/LIT_X2/rows.jsonl, 20 rows, P2-P1101 to P2-P1120, all with a matching Crossref record (VERIFIED per scripts/rows_check.py). Catalog: catalog/P2_LIT_X2_catalog.csv. Read depth: 19 rows metadata-only (Crossref record without abstract), 1 row abstract (P2-P1107). Row ids of other tasks are marked with the task label.

## Findings first (uncomfortable ones first)
1. No dataset licence was read from a primary source in this task. Websearch returned no results for all 10 queries, webfetch is banned for workers, and the arXiv API host was under a shared stop recorded earlier in the project (an earlier 4xx or bot check). Every licence below is UNVERIFIED except two secondary readings: BDD100K (official licence page read by LIT_A5 for P2-P542 through a search result; the same licence text is reproduced in the Hub card dronefreak/BDD100K) and ExDark (the Hub card dronefreak/ExDark cites the authors' LICENSE file as BSD 3-Clause and reports a separate request that commercial users contact the authors). Needed before any download: one read of each official terms page.
2. Hugging Face licence tags are not evidence of the original terms. bazyl/GTSRB is tagged gpl-3.0 while its own Licensing Information section reads "Needs More Information". Two TT100K copies disagree: finedet/tt100k is tagged cc-by-nc-4.0 and its card says the original is non-commercial (CC BY-NC); PrashantDixit0/TT-100K is tagged cc-by-2.0. dgural/bdd100k is tagged bsd, but the BSD-3-Clause licence covers only the BDD100K toolkit code (dronefreak/BDD100K card; P2-P542). A Waymo copy is tagged apache-2.0 with an empty card. ExDark copies carry bsd-3-clause and apache-2.0. One Mapillary traffic-sign copy is tagged mit.
3. Closest prior work for the evaluation the design slides ask for: no dataset seen in this task combines real physical attacks on traffic signs, video with original frame timing, and night or adverse conditions. Nearest pieces: Drive-By-Fly-By (P2-P545, LIT_A5: real road video with physical sticker triggers and clean counterparts, in a training-time backdoor setting), PADetBench (P2-P543, LIT_A5: 20 physical attacks in CARLA under controlled weather, views rather than sequences), CURE-TSD (P2-P1105: sign detection under challenging conditions, no attacks; content not read). Attack-injected or self-recorded clips remain necessary, and sharing them depends on base-set terms (finding 1).
4. All 13 leads of the brief now have a catalogued record with a DOI or arXiv id, in this task (Crossref-verified) or in wave 1 (GTSRB P2-P1101 and P2-P243, GTSDB P2-P1102, LISA P2-P244, MTSD P2-P1104, TT100K P2-P1103, BDD100K P2-P420 and P2-P542, nuScenes P2-P1111, ACDC P2-P416, CODA P2-P1113, Lost and Found P2-P1114, PVDN P2-P415, APRICOT P2-P1108, REAP P2-P1110). Content details (video, frame rate, conditions, size) for 19 of the 20 new rows are title-level only.
5. The slide-01 acronym "APDE patch attacks" was not identified: a Crossref search for it returned REAP (P2-P1110) as the only patch benchmark.

## 1. Problem map (attack data families with the records that define them)
| Attack data family | Records | What was read |
|---|---|---|
| Physical patch photographs for object detectors | APRICOT P2-P1108; APRICOT-Mask inside P2-P110 (LIT_A1) | Title; P2-P110 abstract read by LIT_A1 (pixel masks; physical patch photos) |
| Realistic patch benchmark | REAP P2-P1110 | Title only; capture mode and base imagery not read |
| Fixed digital patch set | ImageNet-Patch P2-P1109 | Title only |
| Simulated physical attacks with controlled physics | PADetBench P2-P543, CARLA-GeAR P2-P544 (LIT_A5) | Abstracts read by LIT_A5 |
| Real road video with physical triggers | Drive-By-Fly-By P2-P545 (LIT_A5) | Abstract and text extract read by LIT_A5; backdoor setting |
| Natural illusions in simulation (shadows, reflections) | LanEvil++ P2-P241 (LIT_A2) | Abstract read by LIT_A2; lane task |
| Released recordings of shadow, reflected-light or projected-light attacks | none found in this task | Attack papers of LIT_A2 to LIT_A4 may release data; not checked |

## 2. Solution map (what each defence or detection family needs from data)
| Need of the design slides | Candidate data | Terms status |
|---|---|---|
| Frozen sign detector and classifier baselines (slides 01, 02) | GTSRB P2-P1101, GTSDB P2-P1102, MTSD P2-P1104, TT100K P2-P1103, DFG P2-P1106, ATSD P2-P1107, LISA P2-P244 (LIT_A2) | UNVERIFIED for all |
| Patch localisation and mismatch evidence (slide 01) | APRICOT and APRICOT-Mask, REAP, ImageNet-Patch, PADetBench | UNVERIFIED; PADetBench Hub tag apache-2.0 (uploader statement) |
| Shadow cue training and compositing (slide 02) | ISTD P2-P1120; ViSha P2-P236 and the other LIT_A2 shadow sets | UNVERIFIED |
| Benign light, night and weather hard negatives (slides 03, 04; owner contributions 3, 4) | ACDC P2-P416, Foggy Cityscapes P2-P1117, Seeing Through Fog P2-P1116, Dark Zurich P2-P1118, NightCity P2-P1119, ATSD tunnels P2-P1107, SHIFT P2-P1115, CURE-TSD P2-P1105, PVDN P2-P415, ExDark P2-P417, Flare7K P2-P418 and P2-P419 | UNVERIFIED except ExDark (secondary) |
| Timestamped driving video for temporal and causal checks (slide 05) | BDD100K P2-P542, nuScenes P2-P1111, Waymo P2-P1112 | BDD100K read (secondary); others UNVERIFIED |
| Benign missed-object cases (slide 05) | CODA P2-P1113, Lost and Found P2-P1114 | UNVERIFIED |

## 3. Closest prior work to the design slides, ranked (data that already provides what the evaluation needs)
1. Drive-By-Fly-By (P2-P545, LIT_A5): the only real road video with physical triggers and clean counterparts seen, with object-disappearance scenarios. Limits: backdoor setting, not a test-time evasion attack; dataset licence UNVERIFIED.
2. PADetBench (P2-P543, LIT_A5): aligned clean and attacked samples for 20 physical attacks under controlled weather, view and distance; the Hub dataset Jiawei-Lian/PADetBench exists with an apache-2.0 tag (uploader statement; P2-P543 reports MIT for the code). Limits: simulated; views, not driving sequences.
3. CURE-TSD (P2-P1105): sign detection under challenging conditions; nearest match to the benign-condition needs of slides 02 and 04 if the dataset link holds. Limits: no attacks; content and terms not read.
4. REAP (P2-P1110): large realistic patch benchmark; candidate replacement for the unidentified "APDE patch attacks" of slide 01. Limits: capture mode and base imagery not read.
5. APRICOT (P2-P1108) with APRICOT-Mask (P2-P110): physical patch photographs with pixel masks. Limits: video, traffic signs and night not read.

## 4. Gaps and what is left to test
- No set seen pairs real physical sign attacks with timestamped video at night or in adverse weather, and none labels benign look-alikes (tree shadows, glare, wet roads, exposure jumps) inside the same recordings.
- Whether attack-injected derivative clips may be shared is open for every base set. For BDD100K the terms read (P2-P542) allow educational, research and not-for-profit use; derivative release was not addressed in what was read.
- Original frame timing: not read for GTSRB, LISA, CURE-TSD, nuScenes, Waymo, SHIFT and PVDN. BDD100K tracking labels are at 5 fps per P2-P542.
- Hub licence tags are unreliable (finding 2); a fresh agent with page access must read every official terms page (NEEDS_BROWSER).
- Cheap benign corruption negatives for a sign classifier exist on the Hub: tanganke/gtsrb holds GTSRB test splits named contrast, gaussian_noise, impulse_noise, jpeg_compression, motion_blur and pixelate (12.6K rows each, 38.5 MB to 118.5 MB of parquet each, per the Hub dataset viewer). They are digital corruptions, not physical conditions, and the copy carries no licence tag.

## 5. Datasets, benchmarks and code seen
Legend: "not read" = the records read do not state it. Licence "UNVERIFIED" = no primary statement read in this task. Hub = Hugging Face Hub card or tag, an uploader statement.

| Dataset | Content (as read) | Video | Conditions | Licence or terms | Licence source | Row id |
|---|---|---|---|---|---|---|
| GTSRB | 43 sign classes, cropped single images (Hub cards) | not read; single images per Hub cards | not read; Hub copy tanganke/gtsrb adds digital corruption splits | UNVERIFIED | Hub: bazyl/GTSRB tag gpl-3.0 with empty licence section; tanganke/gtsrb no tag | P2-P1101; P2-P243 (LIT_A2) |
| GTSDB | full-scene sign detection images (title) | not read | not read | UNVERIFIED | Hub: GlowBond/GTSDB, no tag, no licence text | P2-P1102 |
| LISA signs | US sign data (survey title; content not read) | not read | not read | UNVERIFIED | no Hub copy found | P2-P244 (LIT_A2) |
| MTSD (Mapillary) | global sign detection and classification (title) | not read | not read | UNVERIFIED | Hub: three ThankGod copies, one tagged mit | P2-P1104 |
| TT100K | 100,000 Street View panoramas, over 30,000 sign instances, 221 categories; 232 categories in the 2021 release (Hub cards) | no (panoramas, per Hub card) | illuminance and weather variation (Hub card) | UNVERIFIED; Hub statements conflict: CC BY-NC versus cc-by-2.0 | Hub: finedet/tt100k card and tag; PrashantDixit0/TT-100K tag | P2-P1103 |
| CURE-TSD | sign detection under challenging conditions (title; dataset link UNVERIFIED) | not read | challenging conditions (title) | UNVERIFIED | none found | P2-P1105 |
| DFG | 200 sign classes (title of a PeerJ figure record); paper link UNVERIFIED | not read | not read | UNVERIFIED | none found | P2-P1106 |
| ATSD (Austria) | almost 7,500 scene images, more than 28,000 annotations, more than 100 classes, 2014 (abstract) | not stated | urban to mountainous roads, many tunnel images (abstract) | "freely available online" (abstract), not a licence: UNVERIFIED | Crossref abstract | P2-P1107 |
| BDD100K | 100K videos of 40 s; tracking subset at 5 fps (P2-P542, LIT_A5) | yes (P2-P542) | weather and time-of-day variety (P2-P420, P2-P542) | data: UC Regents licence for educational, research and not-for-profit use without fee; toolkit code BSD-3-Clause | official page read by LIT_A5 via a search result; same text in Hub card dronefreak/BDD100K; dgural/bdd100k tag bsd mixes code and data | P2-P542 (LIT_A5), P2-P420 (LIT_A4) |
| nuScenes | multimodal autonomous-driving data (title) | not read | not read | UNVERIFIED | Hub copies without tags | P2-P1111 |
| Waymo Open | perception data (title) | not read | not read | UNVERIFIED | Hub: one copy tagged apache-2.0 with empty card | P2-P1112 |
| ACDC | 8,012 images; fog, night, rain, snow with same-scene normal images (P2-P416, LIT_A4) | not stated | fog, night, rain, snow | UNVERIFIED | no Hub copy found | P2-P416 (LIT_A4) |
| CODA | road corner cases for detection (title) | not read | not read | UNVERIFIED | no Hub copy found | P2-P1113 |
| Lost and Found | small road hazards (title) | not read | not read | UNVERIFIED | no Hub copy found | P2-P1114 |
| SHIFT | synthetic driving for continuous domain adaptation (title) | not read | not read | UNVERIFIED | no Hub copy found | P2-P1115 |
| Seeing Through Fog | multimodal fusion in unseen adverse weather (title) | not read | adverse weather (title) | UNVERIFIED; release not read | none | P2-P1116 |
| Foggy Cityscapes | synthetic fog data (title; dataset link UNVERIFIED) | not read | synthetic fog | UNVERIFIED; base-image terms would also apply | none | P2-P1117 |
| Dark Zurich | nighttime segmentation and uncertainty-aware evaluation (title; dataset link UNVERIFIED) | not read | night | UNVERIFIED | no Hub copy found | P2-P1118 |
| NightCity | large real night-time scene parsing set (title; name UNVERIFIED) | not read | night | UNVERIFIED | no Hub copy found | P2-P1119 |
| PVDN | 59,746 grayscale night frames, 346 rural scenes (P2-P415, LIT_A4) | not stated as video | night, rural, headlamp light | UNVERIFIED | no Hub copy found | P2-P415 (LIT_A4) |
| ExDark | ten low-light types (P2-P417, LIT_A4) | no (images) | low light | BSD 3-Clause plus a request that commercial users contact the authors (secondary) | Hub card dronefreak/ExDark citing the authors' LICENSE file (file not opened); fuhao7i/ExDark tag apache-2.0; the card says an intermediate export self-declares CC BY 4.0 | P2-P417 (LIT_A4) |
| ISTD | shadow detection and removal data (title; dataset link UNVERIFIED) | not read | shadows | UNVERIFIED | no Hub copy found | P2-P1120 |
| ViSha | 120 videos, 11,685 frames, pixel shadow masks (P2-P236, LIT_A2) | yes (P2-P236) | shadows, general scenes | UNVERIFIED | not searched on the Hub | P2-P236 (LIT_A2) |
| APRICOT | physical adversarial attacks on detection (title); photographs per P2-P110 | not read | not read | UNVERIFIED | no Hub copy found | P2-P1108 |
| APRICOT-Mask | pixel masks for APRICOT (P2-P110, LIT_A1) | no | as APRICOT | UNVERIFIED | none | P2-P110 (LIT_A1) |
| REAP | realistic adversarial patch benchmark (title) | not read | not read | UNVERIFIED | no Hub copy found | P2-P1110 |
| ImageNet-Patch | adversarial patch set around ImageNet (title) | no (ImageNet context) | none | UNVERIFIED | no Hub copy found | P2-P1109 |
| PADetBench | 20 physical attacks, 48 detectors, CARLA, controlled weather, view, distance (P2-P543, LIT_A5) | no (views, per P2-P543) | simulated weather | code MIT per README (LIT_A5); data on the Hub tagged apache-2.0 | Hub tag read in this task (uploader statement); README via LIT_A5 | P2-P543 (LIT_A5) |
| CARLA-GeAR | simulated patch datasets on billboards and truck backs (P2-P544, LIT_A5) | not stated | simulated | UNVERIFIED | none | P2-P544 (LIT_A5) |
| Drive-By-Fly-By | real scenarios with sticker triggers, sign videos at 3840x2160 (P2-P545, LIT_A5; its key_idea says 44 scenarios, its data field 8 clean plus 34 triggered: check) | yes (P2-P545) | not stated | dataset licence UNVERIFIED (the paper licence differs from the data licence) | LIT_A5 | P2-P545 (LIT_A5) |
| LanEvil++ | CARLA illusions incl. shadows and reflections, 1,596 video clips (P2-P241, LIT_A2) | yes, synthetic (P2-P241) | shadows, reflections | UNVERIFIED | none | P2-P241 (LIT_A2) |
| Flare7K, Flare7K++ | synthetic and 962 real night flare images (P2-P418, P2-P419, LIT_A4) | no | night flare | UNVERIFIED | none | P2-P418, P2-P419 (LIT_A4) |

Hub copies read in this task (uploader statements, not the original terms):
- bazyl/GTSRB: tag gpl-3.0; card licence section "Needs More Information".
- tanganke/gtsrb: no tag; cites the Neural Networks 2012 GTSRB paper (P2-P243); corruption test splits as in section 4.
- GlowBond/GTSDB: no tag, card without licence text.
- finedet/tt100k: tag cc-by-nc-4.0; card names the official TT100K 2021 archive and states the original is non-commercial; parquet 6.9 GB train (6.0K rows) plus 3.5 GB test (3.0K rows).
- PrashantDixit0/TT-100K: tag cc-by-2.0; card cites the CVPR 2016 paper (P2-P1103).
- ThankGod/mapillary_traffic_sign_dataset, _cleaned, _recommended: only _recommended is tagged (mit).
- dronefreak/BDD100K: tag other (bdd100k-data-license); unofficial redistribution of the 10-class detection labels; reproduces the UC Regents licence and says the BSD-3-Clause licence applies to code only.
- dgural/bdd100k: tag bsd; FiftyOne set of 10,000 samples.
- huangyuan123/waymo_open_dataset_v_1_4_2: tag apache-2.0; card of 4 lines. AnnaZhang/waymo_open_dataset_v_1_4_3: no tag.
- Xiaodong/Nuscenes-v1.0-trainval-CAM_FRONT, data-loader/nuScenes_raw_data: no tags. The CAM_FRONT parquet export is 7.2 MB for 34.1K rows, too small to hold the images; content not checked.
- dronefreak/ExDark: tag bsd-3-clause, card as in the table; parquet 2.2 MB (text format, so annotations rather than images).
- Jiawei-Lian/PADetBench: tag apache-2.0; dataset viewer could not list its configs.
- Not found by the Hub searches run (the query wording may miss copies under other names): LISA, CURE-TSD, CURE-TSR, DFG, ATSD, APRICOT, REAP, CODA, Lost and Found, Dark Zurich, SHIFT, ACDC, ISTD, NightCity, PVDN, Foggy Cityscapes, SID, LOL.

### Answers to the questions of the brief
1. Licence or access terms per dataset: table above. Read in this project, secondary: BDD100K (LIT_A5 page reading plus a Hub card reproduction) and ExDark (Hub card citing the authors' file). Everything else is UNVERIFIED, and the Hub tags for GTSRB, TT100K, BDD100K, Waymo, MTSD and ExDark conflict with each other or with the card text.
2. Video: confirmed only from other tasks' readings: BDD100K (P2-P542), ViSha (P2-P236), Drive-By-Fly-By (P2-P545), LanEvil++ (P2-P241, synthetic). Original frame timing: a rate is stated only for the BDD100K tracking labels (5 fps, P2-P542); for every other set it was not read. Night or adverse weather: ACDC, PVDN, ExDark, Flare7K (wave 1 abstracts); ATSD tunnels (abstract); Seeing Through Fog, Foggy Cityscapes, Dark Zurich, NightCity (titles only). Attack recordings: APRICOT (photographs, per P2-P110), Drive-By-Fly-By (real video, backdoor triggers), PADetBench and CARLA-GeAR (simulated); REAP and ImageNet-Patch content not read.
3. Laptop fit (32 GB RAM, 6 GB GPU, about 468 GB free on drive C per the coordinator's hardware audit): sizes in bytes were read only for Hub copies: TT100K about 10.4 GB of parquet, GTSRB corruption splits under 0.12 GB each. Counts read: ATSD almost 7,500 images, ACDC 8,012 images, PVDN 59,746 frames, ViSha 11,685 frames, PADetBench 7,200 samples per attack method (P2-P543). These image sets fit the disk and can be streamed for frozen-detector inference. BDD100K (100K videos of 40 s) and nuScenes and Waymo sizes were not read: check the size and the terms before any download, and work on a subset split by recording.

## 6. Leads not confirmed (6)
- LISA full version with video for every annotated sign: lead from memory; P2-P244 is metadata-only and no other record was read.
- CURE-TSR (classification counterpart of CURE-TSD): no Crossref record; arXiv host stopped.
- "APDE patch attacks" (slide 01): Crossref search returned no matching record.
- ARTS dataset named in the data field of P2-P318 (LIT_A3): Crossref search found nothing.
- DAWN vehicle detection in adverse weather: arXiv or data-repository record only; not checked.
- Benchmark of corruptions for driving detection ("winter is coming" paper): arXiv only; not checked.
Also UNVERIFIED inside rows: the paper-to-dataset links of P2-P1105 (CURE-TSD), P2-P1106 (DFG), P2-P1117 (Foggy Cityscapes), P2-P1118 (Dark Zurich), P2-P1119 (NightCity) and P2-P1120 (ISTD) come from memory; the titles fit, the content was not read.

## 7. Exclusions (not catalogued, with reasons)
- Learning to See in the Dark (Crossref 10.1109/cvpr.2018.00347, record found): raw low-light photography, not road data; relevance Low.
- The Bangladesh road traffic sign dataset (Crossref 10.1016/j.dib.2025.111523, record found, no abstract): content and terms not read; no link to attacks.
- CURE-OR (Crossref 10.1109/icmla.2018.00028): object recognition, not traffic scenes.
- MIST rural synthetic driving dataset (Crossref 10.1109/access.2026.3725755): content not read; outside the four families as far as the title shows.
- Lima real-world attack model (SSRN posted content 2025) and the NDSS 2025 commercial-systems study (already P2-P119, LIT_A1): attack papers, not datasets.

## 8. Problem cards (hypotheses, not results)

### Card X2-1. Ordinary condition changes are scored as attacks
- Problem: an attack detector tuned on clear daytime clips may alarm on fog, night, tunnels and slow light change, and no single labelled sign-video set covering these conditions was confirmed in this task.
- Contribution to test: a condition-stratified hard-negative suite assembled from existing condition-labelled sets, reporting false alarms per condition at a fixed attack recall. Hypothesis: false-alarm rates differ strongly by condition, so one global threshold fails, and per-condition calibration lowers false alarms at matched recall. Prior work: ACDC (P2-P416) already pairs adverse and normal images of the same scene; CURE-TSD (P2-P1105) may already label sign-detection challenges (not read).
- Open-source starting point: a frozen small detector as named on the deck (YOLOX-Nano); dataset toolkits not read in this task.
- Data and laptop fit: image subsets of ACDC, ATSD, Dark Zurich, NightCity, Foggy Cityscapes and SHIFT; byte sizes not read except Hub copies (TT100K about 10.4 GB). Frozen-detector inference on image subsets should fit 32 GB RAM and a 6 GB GPU; measure first. Licence question: all base sets UNVERIFIED; read each official terms page before download.
- Experiment workflow: (1) read terms and split by recording or route; (2) set the alarm threshold on clear-weather benign data at a target false-alarm rate; (3) run each benign condition subset and count alarms per condition; (4) inject the attack set (for example REAP-style patches) into held-out subsets per condition and report recall at the fixed threshold.
- Success measure: false alarms per 1,000 frames (per hour for video) by condition at matched recall; spread across conditions; count of abstentions.
- Sources: P2-P1105, P2-P1107, P2-P1115, P2-P1116, P2-P1117, P2-P1118, P2-P1119.

### Card X2-2. Real attack recordings with frame timing are scarce
- Problem: the attack data confirmed here are photographs (APRICOT, per P2-P110), a benchmark whose capture mode was not read (REAP), a digital patch set (ImageNet-Patch) and simulator renders (PADetBench, CARLA-GeAR); only Drive-By-Fly-By (P2-P545) holds real road video with physical triggers, in a backdoor setting.
- Contribution to test: a small controlled recording protocol: printed patches, cast shadows and projected light on a few real or mock signs, recorded as timestamped video with matched benign clips (same place, speed and time; natural shadows; headlights), split by recording. Hypothesis: cue scores measured on simulator renders differ in distribution from scores on real recordings of the same attack type.
- Open-source starting point: PADetBench and CARLA-GeAR generators (P2-P543, P2-P544) for the simulated counterpart; the Hub copy of PADetBench data.
- Data and laptop fit: own recordings avoid third-party terms, but faces and plates need blurring (Drive-By-Fly-By blurred them, per P2-P545); a few hours of video fits the free disk. Licence question: the owner chooses the licence of own recordings; privacy and ethics approval are owner decisions.
- Experiment workflow: (1) list attack and benign scenarios matched by location, speed and light; (2) record with fixed camera settings and keep timestamps; (3) label attack onset and offset intervals; (4) compare detector-only, temporal-only and the proposed cue at matched false-alarm rates on held-out recordings, and compare real against simulated score distributions.
- Success measure: recall at matched false alarms per hour on held-out recordings; warning time from attack onset; distance between real and simulated score distributions.
- Sources: P2-P1108, P2-P1109, P2-P1110.

### Card X2-3. Base-set terms may block release of attack-injected clips
- Problem: attack-injected clips are derivatives of base datasets; only the BDD100K terms were read in this project (educational, research, not-for-profit use, P2-P542), Hub tags for TT100K conflict, and the GTSRB tag is unsupported, so whether derived clips may be shared is open.
- Contribution to test: release only a manifest of source frame identifiers, overlay parameters and generation scripts with hashes, so others rebuild the attacked set from their own licensed copy. Hypothesis: metrics reproduce exactly when the set is rebuilt from an independent download.
- Open-source starting point: dataset toolkits (BDD100K toolkit BSD-3-Clause per P2-P542); an own build script.
- Data and laptop fit: overlays and manifests are small; base data stays with each user. Licence question: per-set terms and whether manifests of frame identifiers are allowed.
- Experiment workflow: (1) record each set's terms from its official page; (2) generate attacked clips from a manifest; (3) rebuild on a second machine from a fresh download and compare frame hashes and metrics; (4) publish only manifest, scripts and metrics.
- Success measure: share of attacked frames rebuilt bit-identically; identical metrics; zero third-party images redistributed.
- Sources: P2-P1101, P2-P1103, P2-P1104, P2-P1111, P2-P1112.

## 9. Tool and budget record
- Websearch: 10 queries, all returned no results (logged as Q lines in progress/LIT_X2.log).
- scripts/lit_verify.py: 19 calls (1 arXiv call refused by the shared stop on export.arxiv.org; 4 Crossref DOI calls; 14 Crossref searches). No Crossref error.
- Hugging Face (read-only exception of this task): repository searches, card overviews, README reads and dataset-viewer structure for the copies listed in section 5. Nothing created or changed.
- Not used: webfetch, browser, downloads, OpenAlex (Crossref records already carry citation counts in the ledger).
