# P2_LIT_OPT2_notes - light and optic attacks: peer-reviewed side, defenses and benign look-alikes

Written by the LIT_OPT2 worker agent. Not audited. Rows: work/LIT_OPT2/rows.jsonl (P2-P2701 to P2-P2748), catalog/P2_LIT_OPT2_catalog.csv (built by rows_check), IEEE subset: work/LIT_OPT2/ieee_leads.tsv.

## Uncomfortable findings first
1. Lightweight detectors of light attacks already exist in the catalog. Laser Guard (P2-P442, IEEE Access 2025) is a plug-and-play statistics-based detector of laser-spot and laser-beam examples; its abstract (read in a search result this run) reports about 70 to 75 percent of laser sign examples filtered, 80 percent for other objects, and about 24 ms (spots) and 57 ms (beams) detection time. The infrared-laser paper P2-P309 (NDSS 2024) includes a physics-based speckle colour-frequency detector with 96 percent TPR and 2.7 percent FPR by day, 92 percent and 6.7 percent by night, on 75 benign plus 75 attack samples per set (paper text in a search result). A guard cannot claim "lightweight light-attack detection" as such; to our knowledge the open part is one guard over several light families (laser, projector, LED flicker, flare) with benign look-alikes measured as false alarms per hour and a measured latency.
2. Attacks are built to look benign. Adversarial lens flare from a flashlight (P2-P2701, IEEE IoT J 2025) reaches above 90 percent average success by day and night; fakeWeather (P2-P2722) imitates raindrops and snow on the lens. Any rule that excuses flare-shaped or weather-shaped artefacts becomes an attack channel.
3. LED flicker attacks survive defenses and are localised. LIMA (P2-P2719, Neural Networks 2026) reports 69.67 percent success against defense models; the attention-superpixel LED attack (P2-P2720, ESWA 2025) confines stripes to small regions (physical success 90 percent day, 100 percent night). A global-flicker cue alone misses them.
4. Benign flicker is everywhere. PWM LED lights above about 90 Hz look steady to people but appear off or banded to cameras (P2-P2712); IEEE P2020 metrics show equal average detectability can hide 0.5 s outages (P2-P2713); simulated rolling-shutter banding can hide a motorcycle (P2-P2714). A flicker detector without a model of legitimate PWM lighting will raise false alarms on traffic lights, signs, brake lights and streetlights.

## What was added
- 48 rows, all pass rows_check: VERIFIED 44 (Crossref), ARXIV_API_VERIFIED 4. Peer-reviewed 44, preprints 4 (P2-P2709, P2-P2710, P2-P2723, P2-P2740; preprint, not peer reviewed).
- By publisher group: IEEE 20; ACM 4; NDSS and ISOC workshops 3; Elsevier 4; MDPI 4; IS&T Electronic Imaging 3; Springer 2; Springer Nature (Nature Communications) 1; SPIE 2; PLOS 1; arXiv only 4.
- By role: ATTACK 14, METHOD 12, DEFENSE 6, DETECTION 5, DATASET 5, BENCHMARK 5, SURVEY 1. Rows on defenses, detectors or benign look-alikes: 34 (brief minimum 12).
- By relevance: High 13, Medium 35.
- By read level: abstract 17, full-text (text shown in search results or open-access pages) 11, metadata-only 20. The metadata-only rows are title-level; they carry no numbers and should be read before citing.
- New category O-F7 Benign look-alikes and false alarms (22 rows). Attack rows reuse O-F1 to O-F4; defense rows O-F5 and O-F6.

## Closest prior work to a lightweight light-attack guard
1. Laser Guard (P2-P442, catalogued earlier; abstract read this run). Does: lightweight statistics on approximated laser regions, plug-and-play, latency reported. Does not (per abstract): projector, LED-flicker or flare attacks; temporal evidence; benign glare or flare false-alarm rates.
2. Infrared laser reflection detector inside P2-P309. Does: physics cues (false colour plus high spatial frequency of speckle), day and night TPR and FPR. Does not: visible light, flicker or projectors; only a 150-image proof of concept per condition; no latency.
3. Morphological real-time defense (P2-P2729, ICMV 2025). Does: detector-agnostic, real-time frame-to-frame morphological change analysis with a re-check, fewer false positives (abstract, no numbers). Does not: light attacks (tested on printed patches on people); no flicker, flare or exposure benign cases.
- Also close: AD^2 (P2-P2626, coordinator note) for spatial-temporal consistency in CARLA with non-light attacks; Hadamard-coded outputs (P2-P2709) flag attacks and natural disturbances in one pass but do not separate them; MirrorGuard (P2-P2710, LiDAR) is the best reporting template: physics cues, multi-frame evidence, 96.31 percent phantom removal at 98.30 percent precision, 99.99 percent of other returns untouched, 59 ms per scan on a CPU (abstract); Laser Shield (P2-P2703) is a hardware polariser, 100 percent defense success and 100 percent benign preservation on its 300-image LAPA set (paper text), laser only.
- The adaptive CUSUM detector of P2-P2706 (RTAS 2021) gives the sequential template for N5: detection delay 0.3 to 4.63 s across drift settings on CAN data, trading delay against false alarms with a deadline (paper text). Not camera data.

## Benign look-alike evidence and reported false-alarm or latency numbers
| Benign case | Paper | Number | Record that states it |
|---|---|---|---|
| LED PWM flicker | P2-P2712 | 60 Hz light appeared off (index below 0.1), 150 Hz stayed on (0.75); 11.111 ms exposure needed for 90 Hz | IS&T paper text |
| Flicker outages | P2-P2713 | detection index 0.53, 0.4, 0.5 at 121, 129, 135 Hz with very different outage lengths | IS&T paper text |
| Flicker simulation | P2-P2714 | 200 scenes; synchronised 105 Hz LEDs hid a motorcycle | IS&T paper text |
| Auto-exposure jumps, sun glare | P2-P2707 | methods completed 47 percent of trajectories; sun-glare subset failed for all | arXiv 2506.18844 text |
| Tunnel exit saturation | P2-P2715 | pedestrian found about 460 ms earlier with fast exposure control; real tunnel mAP 73.37 versus 42.45 and 49.79 | Nature Communications article text |
| Tunnel transitions | P2-P2717 | mAP 0.278 inside, 0.319 entrance and exit, 0.425 outside on original images | MDPI article text |
| Own headlamp beam | P2-P2708 | recognisable coverage 18.95 to 53.48 percent across 16 headlamps | Crossref abstract |
| High-contrast scenes | P2-P2734 | HDR-trained detectors 10 to 12 percent more accurate on real high-contrast set | IEEE Access abstract |
| Oncoming headlight flare | P2-P2739 | training with modelled flare raised mAP50 up to 8 percent on real flare images | accepted manuscript text |
| Emergency lights | P2-P2740 | blue-light detector accuracy 94.7 percent, recall 94.1 percent, up to 70 m | arXiv abstract |
| Emergency lights break detectors | P2-P2636 (catalogued earlier) | confidence fluctuates below 0.4; mitigation runs 30 to 50 FPS | arXiv text in a search result |
| Low light (signs) | P2-P2741 | plus 11.0 points mAP@50 from in-network enhancement | Crossref abstract |
| Detector false alarms | P2-P510 (catalogued earlier, PercepGuard) | FPR 5 percent, TPR 99 percent against adaptive attacks; 96 percent of displayed and projected patch attacks detected | paper text in a search result |
No record in this batch reports false alarms per hour of driving for a light-attack detector. To our knowledge that number is still missing in the literature read so far.

## Gaps still open
1. No paper read measures a light-attack detector against the benign set in one protocol (flicker, flare, headlights, tunnel exits, emergency lights, auto-exposure jumps) with false alarms per hour.
2. No detector read covers more than one light family (laser, projector, LED flicker, flare) at once.
3. Benign data exists mostly as simulators (P2-P2714, P2-P2739) or small HDR and tunnel sets (P2-P2717, P2-P2734, P2-P2736); licences were not read.
4. Order of pipeline stages is unaddressed: flicker removal (P2-P2737), low-light enhancement (P2-P2741, P2-P2747) and weather restoration (P2-P2742) can erase the evidence a guard reads.
5. Cross-sensor agreement is not proof of reality (P2-P2721, digital emulation only).

## Problem cards (hypotheses, not results)
1. Problem: a flicker cue raises false alarms on legitimate PWM lighting. Contribution to test: row-banding frequency and duty estimates compared with expected PWM bands separate LIMA-style modulation from traffic-light flicker. Open-source starting point: ISET-LFM simulator and data (P2-P2714; licence UNVERIFIED). Data and laptop fit: synthetic frames, CPU feature extraction fits the 10-core laptop; licence question open. Workflow: (1) generate benign PWM scenes; (2) inject attacker modulation following P2-P2719 and P2-P2702 descriptions; (3) compute row-wise FFT features; (4) score with a logistic model. Success measure: false alarms per hour on benign sequences and detection rate on injected sequences, with latency per frame. Prior work: P2-P2746 (rolling shutter as frequency sensor) and P2-P2712 cover the physics; the attack-versus-benign test is not covered in what was read. Sources: P2-P2702, P2-P2712, P2-P2713, P2-P2714, P2-P2719, P2-P2720, P2-P2746.
2. Problem: flare and glare are both benign and weaponised. Contribution to test: flare geometry consistency (flare axis through the light source and image centre, change with ego motion) separates natural headlight flare from a flashlight flare aimed at a sign. Open-source starting point: headlight flare model (P2-P2739) for benign flare, digital flare attack described in P2-P2701. Data and laptop fit: image-space injection on public frames in Colab; licences of flare data open. Workflow: (1) synthesise benign flare; (2) synthesise adversarial flare; (3) compute geometry and saturation-map features; (4) evaluate on held-out scenes. Success measure: AUROC and false alarms per hour on benign night sequences. Prior work: Laser Guard (P2-P442) covers laser only. Sources: P2-P2701, P2-P2722, P2-P2738, P2-P2739.
3. Problem: tunnel exits and auto-exposure jumps look like light attacks. Contribution to test: a global-versus-local illumination residual with an exposure-transition state (insufficient evidence) suppresses alarms during benign transitions. Open-source starting point: BorealHDR emulator (P2-P2707; code location seen, licence not read). Data and laptop fit: bracketed sequences in Colab; CPU scoring. Workflow: (1) emulate exposure policies; (2) add local light attacks; (3) score residuals with CUSUM as in P2-P2706; (4) report delay and false alarms. Success measure: false alarms per transition and detection delay. Sources: P2-P2706, P2-P2707, P2-P2715, P2-P2717.

## Datasets, benchmarks and code seen
- ISET-LFM code and data (P2-P2714): GitHub and Stanford Digital Repository links named in the paper; licence not read.
- BorealHDR and TFR24 code (P2-P2707): GitHub link seen; licence not read.
- LAPA laser dataset (P2-P2703), AUTOFIRE flare set (P2-P2739), POLAR-GLV tunnel set (P2-P2717), native HDR test set (P2-P2734), HDRDCL (P2-P2736), ABLDataset (P2-P2740): named only; locations and licences UNVERIFIED.
- HadamardPerturbationDetection code (P2-P2709): GitHub link named in the abstract.

## Leads not confirmed
- 10.1109/icmlt69916.2026.11688387 "Adversarial Zoom Lens: A Camera-Based Physical Attack to DNNs" (ICMLT 2026): Crossref first author Yang, while the preprint P2-P2723 with almost the same title is by Hu and Shi; relation not confirmed, not catalogued. Possible duplicate publication; flag for the coordinator.
- Published versions of rows already catalogued, matched only by title in the Crossref harvest (DOIs not verified in this run): P2-P2625 to 10.1109/icassp49660.2025.10889447; P2-P211 and P2-P509 to 10.3390/s26051737; P2-P2613 to 10.5244/c.35.387; P2-P305 and P2-P440 to 10.1016/j.cviu.2023.103877; P2-P410 (arXiv 2108.06247) to 10.1109/iccvw54120.2021.00016; P2-P2605 to 10.1109/icme59968.2025.11209575; P2-P525 to 10.1145/3830454.3832618.
- AdvLIM conference version (PRCV 2023, 10.1007/978-981-99-8435-0_38), LIMA SSRN preprint (10.2139/ssrn.5153899), Beyond the Glow (USENIX VehicleSec 2025, luminescent lane markers; no DOI found), illumination normalization comparison including tunnel transitions (ACM, 10.1145/3795154.3795256), PEOD event-RGB benchmark (arXiv 2511.08140), SIREN-Bench (arXiv 2608.24094): seen in search results, not verified.
- Numbers for already-catalogued rows (Laser Guard P2-P442, P2-P309, PercepGuard P2-P510) were read this run but those rows belong to other tasks; the coordinator may add them.

## Exclusions
- Verified but not catalogued: 10.1007/s11036-023-02284-7 (GNSS and IMU time-series spoofing, not camera); 10.1142/s0219843626400256 (non-visual sensors); 10.3390/s24185912 (tunnel surveillance cameras, Low); 10.15282/ijame.20.3.2023.08.0822 (Raspberry Pi detection under day and night, Low); arXiv 2610.21034 (thermal side-channel survey, Low); 10.1109/tdsc.2026.3757020, 10.1109/spw53761.2021.00042, 10.1016/j.cose.2023.103460, 10.1109/access.2023.3307133, 10.1145/3570361.3613278, 10.1109/cvci56766.2022.9964980, 10.1587/transfun.2021wbi0002 (light relevance not confirmable from title or snippet, or phone cameras).
- Duplicates of existing rows found during verification: 10.1109/tifs.2024.3422920 (P2-P715), 10.5220/0012309900003660 (P2-P438), 10.1007/s10514-022-10072-7 (P2-P2405).
- From the unread OPTIC arXiv list (170 titles with score 4 or more not in a catalog): 2 rows kept (P2-P2709, P2-P2710); the rest excluded by title: infrared and thermal-only attacks (about 30), face recognition, shadow detection and removal, remote sensing and SAR, LiDAR-only, wireless and network security, language models, unrelated matches.
- From OPTIC2 (667 Crossref records not in a catalog): all 214 titles with score 3 or 4 and a keyword-filtered list of score 1 to 2 titles were read; the many lightweight-detector, optical-design, optical camera communication, medical and remote-sensing records were excluded as outside the subject.

## Method
- Inputs: work/OPTIC2/candidates.tsv (717 records), work/OPTIC/candidates.tsv (338 records). Selection by title and venue; the keyword score was a screening aid only.
- Dedup: DOI, arXiv id and normalised title against every catalog/P2_*_catalog.csv before verification; 7 OPTIC2 records were published versions of existing rows (listed above).
- Verification: scripts/lit_verify.py, 19 calls (Crossref by DOI in batches, Crossref and arXiv searches, arXiv by id). Crossref returned abstracts only for MDPI, PLOS, Springer Nature and a few others; IEEE and ACM abstracts were read from search results where available, otherwise rows are metadata-only.
- Websearch: 20 queries, each logged as a Q: line in progress/LIT_OPT2.log.
- No STOP_HOST or RETRY_LATER occurred. No WebFetch, browser, download or install was used.
