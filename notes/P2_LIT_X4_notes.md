# P2_LIT_X4 notes - explainability for attack detection (X4-F1, X4-F2, X4-F3)

Written by LIT_X4 (continuation run). Not audited: a fresh-agent audit is required. Rows: work/LIT_X4/rows.jsonl (25 rows: VERIFIED 15, ARXIV_API_VERIFIED 9, UNVERIFIED 1; High 10, Medium 15). Read depth is abstract-level or less unless a row says otherwise. Paper ids P2-P13xx are rows of this task; other ids belong to the named tasks.

## Findings first (uncomfortable ones first)
1. Prior work already flags patch attacks on object detectors with explanations attached: X-Detect (P2-P1301) raises real-time alerts with explanations and reports a 0% false positive rate on its retail data (abstract). PhySense (P2-P1302) already cross-checks detector labels against independent physical evidence on nuScenes, KITTI, CARLA and 8.6 hours of real driving (project page). "Explainable consistency check" as such is not new; novelty has to come from the specific cheap cues (shadow, reflection, light), the abstain state, matched-FPR evaluation and laptop cost.
2. The most common explanation form, the heat map, did not add user understanding of an object detector beyond showing the detector output (P2-P1314), and subjective, objective and mathematical evaluations of saliency maps disagree (P2-P1320). An explanation module judged only by heat-map metrics would not support contribution 6.
3. Heat-map evidence can be hidden by the attacker: patches can be optimized so Grad-CAM no longer points at them (P2-P1318), and the SoK on explainable ML in adversarial environments states current explanation methods are not robust to manipulation (P2-P1319). Any explanation that feeds the alarm must be tested under explanation-aware attacks.
4. Cost: ODExAI (P2-P1321, arXiv text) reports about 98.67 s per image for D-RISE and 70.12 s for D-CLOSE, against 0.43 s for G-CAME; Grad-CAM for YOLO takes about half a second per explanation (P2-P1312, paper text). Post-hoc detector explanations do not fit a per-frame loop; only amortized explainers (P2-P1313) or explanations that fall out of the consistency check itself are candidates.
5. To our knowledge, from the records read, no attack detector names shadow, reflection or lighting as the cause of an alarm. The nearest are the IR-laser speckle detector catalogued by LIT_A3 (P2-P309), PhySense object-property reasons (P2-P1302) and sign-rule reasons (P2-P1304, P2-P1317). This family was searched with only 2 queries before it stopped yielding new records, so the gap is provisional.
6. Operator evidence for explained attack alerts comes from a video study with designed alerts across infrastructure, perception and execution attacks, not from a working camera-attack detector: with false alarms, a bare alert did worse than no display while alert plus explanation helped (P2-P1325).

## 1. Problem map (attack families with the papers that define them, seen from the explanation angle)
| Family | What goes wrong for explanation | Rows |
|---|---|---|
| Localized patches on classifiers and detectors | Region evidence (the disputed region) exists but needs many extra forward passes | P2-P1303, P2-P1306, P2-P1301 |
| Physically realizable patch and projection attacks on AV perception | Detector label conflicts with physical object evidence; explanation is a violated property | P2-P1302 |
| Digital L-p and physical sticker attacks on sign recognition | Class conflicts with sign shape, colour or content rules | P2-P1304, P2-P1317, P2-P1305 |
| Digital perturbations on classifiers | Attribution statistics shift; the output is a score, not a reason | P2-P1315, P2-P1316 |
| Explanation-aware attacks | The attacker fools the prediction and the explanation together | P2-P1318, P2-P1319 |
| Operator-facing failure | Heat maps add no understanding; bare alarms under false alarms do harm | P2-P1314, P2-P1320, P2-P1325 |

## 2. Solution map (defence and detection families)
- Saliency region plus consistency test: SentiNet overlays salient regions on held-out images (P2-P1303); Jujutsu moves them into the least-salient area of hold-out images, then inpaints (P2-P1306).
- Explainable-by-design multi-check ensemble for detectors: X-Detect (P2-P1301).
- Physical-consistency reasoning on AV perception: PhySense CRF over a spatial-temporal object graph (P2-P1302). Related rows of other tasks: PercepGuard (LIT_A5 P2-P510), physics-aware spatiotemporal consistency (LIT_A5 P2-P514), IR speckle detector (LIT_A3 P2-P309).
- Knowledge or rule monitors for signs: KEMLP factor graph with permissive and preventive rules (P2-P1304); NeuroShield symbolic attribute heads and logic losses (P2-P1317).
- Attribution as detector features: ML-LOO (P2-P1315), SHAP signatures (P2-P1316).
- Language-based checks: ViLAS pairs image and class-label text in a small VLM, outputs a score (P2-P1305); an LLM explains whether a scenario anomaly is benign or adversarial from symbolic scene data (P2-P1324, NEEDS_VERIFY).
- Post-hoc detector explanation methods: D-RISE (P2-P1307), ODAM (P2-P1308), G-CAME (P2-P1311), Grad-CAM for YOLO (P2-P1312), amortized Shapley (P2-P1313), BSED (P2-P1322).
- Evaluation: sanity checks (P2-P1309), DExT metrics and user study (P2-P1310), ODExAI framework (P2-P1321), human-attention plausibility (P2-P1323), user studies (P2-P1314, P2-P1320, P2-P1325), explanation robustness (P2-P1318, P2-P1319).

## 3. Closest prior work to the owner's design slides, ranked
Design element in question: the decision node shared by slides 01 to 05, "flag with an explanation" (contribution 6), and slide 01's "show the disputed ROI and the mismatched cues".
1. X-Detect (P2-P1301): patch alarms for object detectors with explanations by design, named on slide 01. Retail scenes; the abstract does not say what the defender sees or how explanations were judged.
2. PhySense (P2-P1302): frozen-perception output checked against independent physical evidence, with real-vehicle tests and about 0.037 s per frame (VehicleSec 2025 poster). Reasons are object size, texture, behaviour and interactions, not illumination; needs 3D lifting and tracking.
3. KEMLP (P2-P1304): sign class checked against shape, colour and content detectors; each violated rule is a readable reason. Classification only, label correction instead of a calibrated alarm.
4. SentiNet and Jujutsu (P2-P1303, P2-P1306): the disputed region plus a label-consistency test. Classifier setting, extra forward passes, and exposed to explanation-aware patches (P2-P1318).
5. LLM scenario explanation (P2-P1324): text reason separating benign sensor errors from manipulation. Symbolic inputs, LLM cost, work in progress.

## 4. Gaps and what is left to test
- Cause-labelled alarms (patch, shadow, reflection, light, unknown) built from cheap cue residuals, scored for cause accuracy and not only detection: not found in the records read.
- Direct evaluation of the explanation of an attack alarm: the attack detectors read evaluate detection or correction; X-Detect calls its explanations actionable without a stated test in the abstract. Among the rows, only P2-P1325 tests explanations of attack alerts with people, using videos; a VehicleSec 2025 poster (not catalogued) reports preliminary simulator results.
- Robustness of cue-based reasons to explanation-aware attacks: shown for Grad-CAM (P2-P1318), untested for contour, shadow or light cues.
- Explanation cost on laptop hardware at video rate: only GPU timings on COCO-type images were read (P2-P1321, P2-P1312).
- Abstain or insufficient-evidence output paired with an explanation: not seen in any row.

## 5. Datasets, benchmarks and code seen (licences not read; record each before any download)
- COCO and the authors' Superstore set (P2-P1301); nuScenes, KITTI, custom CARLA set (P2-P1302); GTSRB 12-class subset and LISA (P2-P1304), GTSRB (P2-P1317); ImageNette, ImageNet, CelebA, Place365 (P2-P1306, code README); MS COCO and PASCAL VOC (P2-P1307, P2-P1321, P2-P1322); BDD-100K (P2-P1323); AutoSec-X, 40 scenarios (P2-P1324).
- Code: github.com/DependableSystemsLab/Jujutsu (P2-P1306); github.com/UMBCvision/fooling_network_interpretation (P2-P1318); github.com/GitVirTer/HAG-XAI (P2-P1323); PhySense project page sites.google.com/view/physense, code said to be released (UNVERIFIED); github.com/tigerseclab/VehicleSec25_LLM_Reasoning (stated in P2-P1324, UNVERIFIED); xaitk-saliency library with a third-party D-RISE implementation (seen in search results, not opened).
- Licence questions for the owner: BDD100K, nuScenes, KITTI, GTSRB, LISA, COCO and any attack clips from LIT_A1 to LIT_A5 need their terms recorded before download or release; a user study (card X4-2) needs the owner's and advisor's decision on ethics approval.

## 6. Leads not confirmed (what was tried)
- VX-CODE (named CVPR 2026 by the earlier run): no record opened in this run; not confirmed.
- XAI strategies survey for object detection, arXiv 2509.01991 (2025): text seen in search results; arXiv host stopped, no Crossref check; UNVERIFIED.
- PASA (EuroS&P 2024), Interpretable Deep Learning under Fire (USENIX Security 2020), Disguising attacks with explanation-aware backdoors (IEEE S&P 2023), Interpretations Cannot Be Trusted (arXiv 2211.15926), a saliency-map detection defense: named in earlier Q lines; not checked in this run.
- Fuzzy interpretable perception monitor, arXiv 2505.14407 (explains perception unreliability by brightness, contrast, blur, weather and time of day on BDD100K): no Crossref hit; arXiv host stopped; UNVERIFIED. Relevant to the benign side of question 3.
- Hudson, LLM driving agent that detects perception attacks, arXiv 2409.14488: seen only; UNVERIFIED.
- LMM sign verification WIP (VehicleSec 2024, DOI printed in the PDF, not checked): seen only.
- VehicleSec 2025 poster on explanations, situation awareness and takeover under attacks (Li et al.): poster abstract read; preliminary; not catalogued.
- CogSci 2024 paper by the authors of P2-P1314: eScholarship page seen; covered by the journal row.
- ODAM journal extension (IEEE TPAMI 2024): IEEE CSDL page seen; DOI not checked.
- Verified in the ledger but not catalogued (row target reached, lower relevance): AmI attribute-steered detection (arXiv 1810.11580, face recognition), ExAD (arXiv 2103.11526), concept-based explanations for OOD detectors (arXiv 2203.02586), human drivers' situation awareness under physical-world attacks (VehicleSec 2023, 10.14722/vehiclesec.2023.23002).

## 7. Exclusions (not catalogued, with reasons)
- Generic adversarial-ML taxonomies (NIST AI 100-2 and similar): not about explaining detection.
- Glare degradation and mitigation (arXiv 2404.10992; ESREL 2026 synthetic glare): natural degradation, no attack alarm; belongs to the lighting cue task if anywhere.
- SHAP-based detection for text, IoT traffic and a 2026 DeepSHAP summary method: other modalities or classifier-only, outside camera-based detection.
- Neuro-symbolic safety guard for end-to-end driving control (arXiv 2608.11451): control level, not perception attacks.
- Uncertainty and introspection monitors (UAI 2024 failure recognition, frame-level introspection, calibration papers): natural failures, no explanation of attacks.
- Attack papers met in searches (text-to-image sign appearance attack, fluorescent patch, reflectivity-difference night attack, modulated LED attack, natural light attack, CVPRW 2025 sign perturbations): attack families of LIT_A1 to LIT_A5.
- Already catalogued by other tasks and cited here by id: PercepGuard (LIT_A5 P2-P510), physics-aware spatiotemporal consistency (LIT_A5 P2-P514), Invisible Reflections (LIT_A3 P2-P309), shadow edge-map defense (LIT_A2 P2-P208).

## 8. Answers to the three questions of the brief
1. Form and run-time cost. Region: SentiNet and Jujutsu return the disputed region; both need extra forward passes (Jujutsu uses 2 hold-out images in its main evaluation, paper text). Cue: PhySense returns the violated physical property at about 0.037 s per frame (poster). Rule: KEMLP returns the violated sign rule from auxiliary detectors (19 submodels in its implementation, supplementary text); NeuroShield predicts sign attributes with the class at the cost of extra heads. Text: an LLM reasons over symbolic scene data (P2-P1324, cost not read); ViLAS uses label text but returns a score at 4.4 ms (abstract). Score only: ML-LOO and SHAP signatures. Post-hoc detector heat maps cost from about 0.43 s (G-CAME) to about 98.67 s (D-RISE) per image (P2-P1321).
2. Evaluation. Detector explanations are judged by insertion and deletion (P2-P1310, P2-P1322, P2-P1321), pointing games (P2-P1322, P2-P1321), model-randomization sanity checks (P2-P1309), agreement with human attention or gaze (P2-P1323, P2-P1308 extension), and user studies (P2-P1307 trust test, P2-P1310, P2-P1314, P2-P1320). Attack detectors in the rows evaluate detection or correction, not the explanation; among the rows, only P2-P1325 tests attack-alert explanations with people. Robustness of explanations: P2-P1318 doubles as a controlled test; P2-P1319 defines robustness notions.
3. Physical cause instead of a heat map. PhySense (object size, texture, behaviour, interactions), KEMLP and NeuroShield (sign shape, colour, content), and LIT_A3 P2-P309 (IR laser speckle colour and spatial frequency). None found that names shadow, reflection or lighting as the alarm cause (finding 5).

## 9. Problem cards (hypotheses, not results; laptop limits: 10-core CPU, 32 GB RAM, one 6 GB laptop GPU; CPU baselines and frozen features first, per the deck)

### Card X4-1. Alarms do not name the physical cause
- Problem: attack detectors return a region, a score or an object-property conflict, but none in the records read says "shadow", "reflection" or "light" as the cause.
- Contribution to test: a cause-labelled alarm (patch, shadow, reflection, light, insufficient evidence) taken directly from which slide cue residual fired, scored for cause accuracy as well as detection. Prior work covers object-property reasons (P2-P1302) and IR speckle (LIT_A3 P2-P309) only.
- Open-source starting point: frozen YOLOX-Nano as on the deck; OpenCV cue extractors from the cue tasks; KEMLP-style rule table (P2-P1304) as the reason vocabulary.
- Data and laptop fit: clips with each attack type from the LIT_A1 to LIT_A5 sources plus benign look-alikes (tree shadows, glare, wet roads); inference and cue features on CPU; licence of every clip set to be recorded first.
- Experiment workflow: (1) label each attack clip with its true cause and each benign clip with its look-alike cause; (2) run the frozen detector and the cue residuals; (3) map the strongest residual to a cause label, abstain below a calibrated threshold; (4) report cause confusion matrix and detection at matched FPR.
- Success measure: cause accuracy above a residual-free baseline (heat-map location only) at the same alarm rate, with abstentions counted.
- Sources: P2-P1302, P2-P1304, P2-P1317, P2-P1301, P2-P1303.

### Card X4-2. Heat maps do not help the person who receives the alarm
- Problem: saliency maps did not improve understanding of object detectors (P2-P1314), evaluation families disagree (P2-P1320), and bare alerts did worse than no display under false alarms (P2-P1325).
- Contribution to test: a short cue-level reason plus the disputed ROI improves human attack detection and benign-alarm rejection over a bare alert and over a heat map. Partly covered: P2-P1325 shows the effect for designed alerts in videos across infrastructure, perception and execution attacks, not for alerts produced by a camera-attack detector with cue reasons.
- Open-source starting point: Grad-CAM for YOLO approach (P2-P1312) or G-CAME (P2-P1311) for the heat-map arm; HAG-XAI code (P2-P1323) for human-attention comparison.
- Data and laptop fit: short alarm videos rendered offline on the laptop; an online study needs the owner's and advisor's ethics decision; dataset licences as in section 5.
- Experiment workflow: (1) build three displays per alarm: bare alert, heat map, cue reason with ROI; (2) mix attack and benign alarms at a fixed detector FPR; (3) run a small between-subjects video study; (4) analyse by attack type and compare with faithfulness metrics.
- Success measure: higher attack detection and benign rejection, and no slower response, for cue reasons than for both other displays.
- Sources: P2-P1314, P2-P1320, P2-P1325, P2-P1307, P2-P1310.

### Card X4-3. The explanation can be attacked along with the detector
- Problem: patches can suppress Grad-CAM at their own location (P2-P1318), and explanation methods are not robust to manipulation (P2-P1319); region-evidence detectors (P2-P1303, P2-P1306) rely on such maps.
- Contribution to test: whether physically grounded cue reasons (contour against class shape, shadow geometry) are harder to suppress than heat maps under an explanation-aware loss.
- Open-source starting point: fooling_network_interpretation code (P2-P1318); Jujutsu code (P2-P1306) as the region-evidence baseline.
- Data and laptop fit: digital sign crops (GTSRB, LISA; licences to record) and small patch optimizations; a fit test on the 6 GB GPU before any larger run.
- Experiment workflow: (1) reproduce the Grad-CAM-suppressing patch on a sign classifier; (2) add the same suppression term against the contour or shadow residual; (3) measure alarm recall and reason localization at fixed FPR, plain versus explanation-aware attack; (4) report the attacker's extra cost.
- Success measure: a smaller drop in alarm recall and reason localization for cue reasons than for heat maps.
- Sources: P2-P1318, P2-P1319, P2-P1303, P2-P1306, P2-P1304.

### Card X4-4. Post-hoc explanations cost more than the frame budget
- Problem: sampling explanations take tens of seconds per image and CAM-style ones about half a second (P2-P1321, P2-P1312); amortized explainers need training (P2-P1313).
- Contribution to test: an explanation that is a by-product of the consistency check (the cue residual map itself), compared on latency and faithfulness with G-CAME, Grad-CAM for YOLO and a reduced-mask D-RISE.
- Open-source starting point: xaitk-saliency D-RISE implementation (third party, not opened); Grad-CAM for YOLO approach (P2-P1312); metric definitions from P2-P1321 and P2-P1322.
- Data and laptop fit: a few hundred alarm frames from COCO-type and BDD100K images (licences to record); timing on the laptop CPU and 6 GB GPU, p50 and p95 as on the deck.
- Experiment workflow: (1) time each explanation method on the same alarms; (2) compute deletion, insertion and pointing game for each; (3) compute the same for cue residual maps; (4) plot latency against faithfulness.
- Success measure: cue-residual explanations inside the per-frame budget the project sets, with faithfulness not below G-CAME on the same alarms.
- Sources: P2-P1321, P2-P1311, P2-P1312, P2-P1313, P2-P1322, P2-P1307, P2-P1308.

## 10. Run facts
- Searches: 31 of 40 websearch calls in total for this label (10 by the earlier run, 21 in this run); 13 of 50 lit_verify calls. export.arxiv.org was under a shared stop for this whole run: no arXiv calls; arXiv-only candidates were not added or are listed as UNVERIFIED.
- Text met in search results that addressed a reader (a prompt template inside one paper, site marketing text) was treated as data and not followed.
