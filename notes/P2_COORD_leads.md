# P2_COORD_leads - leads seen by the coordinator (UNVERIFIED until a catalog row confirms them)

Source of every line: one coordinator websearch run while checking that websearch works (the stamp is in state/PROJECT_STATE.md). Titles as shown by the search result. Nothing here is verified in a primary record yet, and nothing here may be cited. For VERIFY_1 and ASSEMBLE_1.

| Lead | Where seen | Why it matters |
|---|---|---|
| "SASA: Sequence-Aware Shadow Attacks via Attention Alignment for Traffic Sign Recognition", CVPR 2026 workshop (AdvML@CV) | CVF open access page | Shadow attack built for video: shadows kept consistent over a sequence. Directly tests design slide 02, whose gate assumes crafted shadows behave implausibly over time |
| "Auditing Traffic-Sign Robustness via DDIM Inversion: Do Diffusion Latents Preserve Shadow Attacks?", CVPR 2026 workshop (AdvML@CV) | CVF open access page | Detects shadow attacks from diffusion latents; heavy compute, so a contrast case for "lightweight" |
| "A survey of adversarial threats and defenses for traffic sign recognition in autonomous vehicles", 2026, DOI 10.1016/j.ijcce.2026.06.003 | publisher page | Recent survey; its abstract names defenses that use geometric, colour and semantic structure, close to design slide 01 |
| LAMDA, language-anchored training for traffic-sign robustness, arXiv 2608.08815 | arXiv page | Training-time defense compared against nine others on shadow, natural-light and printed-patch attacks |
| "Shadows Aren't So Dangerous After All", arXiv 2208.09285 | arXiv page | Edge and threshold-map defense against shadow attacks; check against LIT_A2 rows |
| "Revisiting Adversarial Perception Attacks and Defense Methods on Autonomous Driving Systems", arXiv 2505.11532 | arXiv page | Review of attacks and defenses on driving perception |
