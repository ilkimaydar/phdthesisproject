# P2_LIT_OPT_notes - light and optic attacks: arXiv harvest (coordinator, no subagent)

Written by the coordinator session. Not audited. Machine-collected candidates, partly hand-selected.

## Method
- scripts/optic_harvest.py ran 18 arXiv API queries on light and optic attacks (laser, infrared, projector, flicker and rolling shutter, reflection, adversarial light and illumination, shadow, glare and headlight, exposure, phantom objects, camera-side injection, night, physical-world optical attacks, spotlight, traffic lights, defenses, thermal), 40 results per query at most, one request per 3.5 s through scripts/lit_verify.py.
- Result: 338 unique candidates (work/OPTIC/candidates.tsv); 297 are not yet in any catalog; 205 of those have a keyword score of 4 or more (score = optic keyword + attack word + driving or camera word + optic keyword in the title). The score is a screening aid only.
- From the 56 not-yet-catalogued records with an optic keyword in the title and an attack word, 16 were chosen by reading the title and the first 300 characters of the abstract. They are the rows P2-P2601 to P2-P2616 (work/LIT_OPT/rows.jsonl, catalog/P2_LIT_OPT_catalog.csv). All 16 match their arXiv API record (title, first author, year). Only the abstract opening was read, so summaries are cautious and every row has read_level abstract.
- Left out on purpose: face-recognition projection and relighting papers, shadow-detection image papers (not attacks), thermal-only papers beyond three representatives, and unrelated matches (for example a prompt-injection paper that matched "spotlight").

## What the 16 rows add
- Exposure and pulsed light (design 4): P2-P2601 shows that temporal HDR fusion, which merges frames of different exposure times, assumes stable light and can be attacked with pulsed light. This is the first record in the catalog that names HDR fusion as an attack surface, and it bears directly on N4 (local-versus-global illumination plus flicker).
- Camera-side optics: P2-P2602 and P2-P2603 (scratched lenses, dynamic optical perturbations) act on the camera path, not on the scene. A scene-based consistency check should state whether it can see such artifacts.
- Projected light: P2-P2604 to P2-P2606; the view-invariant projector attack P2-P2606 is a ready test for a view-conditioned check (N3).
- Defense: P2-P2612 is an image-inpainting defense aimed at light-patch attacks on traffic sign recognition (reported cost not read), a baseline for designs 3 and 4.
- Infrared (three records): attacks need a sensor assumption; the defense P2-P2616 is for thermal human detection.

## Gaps this pass confirms
- None of the 16 abstract openings mentions false alarms on headlights, glare, rain or auto-exposure; the benign look-alike class for light attacks is still unmeasured in the catalog.
- Public data: no new dataset of optic-attack recordings appeared.

## Next
- Read the abstracts of the 205 high-score candidates and add rows (an agent task, or the coordinator in small batches); then verify published versions.
- IEEE Xplore is paused (Error 418, see the state log); IEEE-indexed light and optic papers come later through the in-page loop scripts/pdf/ieee_search_loop.js.
