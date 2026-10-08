# UrbanHeat — Orientation Requirements and Delivery Review
Date: 8 October 2026
Project: UrbanHeat AI: Al Khor area study — Team Al Zubarah, Qatar
Reviewed repository snapshot: 9fa71a86c9d44b4303c36eac9c1fc2f4b91e7596

## Main decision

Prepare a presentation of up to **10 minutes**, followed by **5 minutes of judge questions**, if shortlisted. The existing three-minute script is a useful compact version, but it is not the stated live-pitch limit. A two-to-three-minute screen recording is recommended, optional supporting material. These are different deliverables.

Keep the existing twelve-slide design unless the team's live submission guide imposes a different requirement. The supplied transcripts specify no fixed slide count; supplementary detail and annexes are explicitly allowed. Do not pad the pitch to fill ten minutes. A rehearsed eight-to-nine-minute presentation, including a short demonstration and transitions, is a proposed preparation target, not an organizer requirement.

## Sources and evidence scope

1. User-supplied file: Whole sessions.txt. It contains three labelled sections:
   - 1st Orientation Session, source lines 1–27.
   - 2nd Orientation Session, source lines 29–85.
   - Special Technical Orientation Session, source lines 90–193.
2. Official public website, inspected 8 October 2026: https://spaceacademy-hackathons.space.gov.ae/
3. Project source at the reviewed immutable commit, including README, Submission-Checklist.md, Team-Review.md, Submission-Draft.md and Three-Minute-Presentation.md.
4. The existing presentation's reviewed twelve-slide structure and prior artifact reports.

This is a review of the supplied transcription, not a claim to have watched or independently transcribed the recordings. Some Arabic speech, names and technical terms are visibly garbled. Repeated clear English statements provide strong evidence for 10+5 timing. Do not infer rules from corrupted phrases. The mapping from these section titles to the three YouTube IDs supplied in the email has not been independently established.

The live account's detailed submission guide was not inspected in this review. Use it and the actual invitation for any final file limits, presentation slot or updated instructions. No project files were edited, no analysis was rerun, and no submission or organizer contact was performed by this review.

## Requirements, recommendations and project implications

| Item | Organizer evidence | Classification | UrbanHeat status / action |
| --- | --- | --- | --- |
| Satellite data as a core source | First session line 6; second session line 33 | Required | Met by Landsat/Sentinel-2 and land-cover inputs. Field photos supplement satellite analysis. |
| Publicly accessible GitHub repository | First session line 22; second session line 33 | Required access in the sessions | Current repository is public. Later supplied direct correspondence also accepts private collaborator access; no visibility change is needed. |
| README and clear run instructions | First session line 22; second session line 33 | Required minimum | Present. Ensure the final landing page clearly links the executable notebook, PDF and offline demo. |
| Executable notebook, dependency file, sample input and output | First session line 22; second session lines 33 and 57 | Required minimum | Present with retained execution/hash evidence. A written report alone is insufficient. No redundant analysis run is needed for wording/layout changes. |
| Presentation slides in PDF | First session line 22; second session line 33 | Required | PDF present. Keep editable PPTX as a useful extra, not a substitute. |
| Problem, intended end user, data/licences/tools, results, method, assumptions and limitations | First session lines 11–12 | Expected submission content | Mostly present. Make the intended planning user and actual decision path more concrete in the pitch. |
| Live pitch: up to ten minutes, then five minutes Q&A | First session lines 16–19; second session line 33 | Stated shortlisted-pitch timing | Replace three-minute-only rehearsal instructions with a new live-pitch script and demo cues. Keep the compact script separately labelled. |
| Fixed number of slides | No fixed count stated; first session line 17 allows longer submitted decks/annexes | Not established | Twelve slides are a team design choice. Retain them while adding photos and improving narrative. |
| One presenter | First session lines 18–19; second session line 33 | Explicitly allowed | Mohammed may present for the team without a stated score penalty. Teammates may help during Q&A. No rehearsal is complete until confirmed. |
| Q&A contributes to score | First session line 17 | Stated judging practice | Prepare short, accurate answers about AI, temperature, zero detected greenery, selection, uncertainty and next validation. |
| Pitch only after shortlist | First session line 16; second session line 33 | Stated process | Top 40 invited; sessions describe pitch slots on 14–16 October. Do not record a confirmed invitation or slot before receipt. Monitor email/platform. |
| Attendance at booked pitch | Second session line 33 | Required if invited | At least one member must attend; stated no-show rule prevents advancement. |
| Two-to-three-minute screen recording | First session line 22 | Recommended, explicitly not mandatory | Optional demo video of the application. The received six-second field video is site evidence, not this screen recording. |
| Docker/container | First session line 22 | Recommended, not mandatory | Do not add Docker merely to satisfy a nonexistent minimum. |
| Licence file | First session line 22 calls it recommended | Recommended / data obligations remain | Already present. Preserve actual source credits and licences. |
| New/deep-learning architecture | First session lines 5 and 12; second session lines 33, 41 and 83 | Not required | Simple explainable baselines are endorsed. Clearly disclose external AI and deterministic ranking. No new training is needed. |
| Hyperspectral data | First session lines 6 and 12; second session line 33; official public website | Bonus/recommended, not mandatory | Do not add a new dataset solely for points immediately before delivery. Existing open satellite workflow is acceptable in principle. |
| Full product, hosted app or actual customer adoption | Second session line 33 | Beyond minimum; potential bonus | Working portable UI is useful evidence. Do not claim real planner adoption, paid pilots or measured benefit. |
| Biosecurity examples in special session | Third section lines 93–94 | Illustrative guidance | Apply problem → user → decision → data thinking. Do not switch UrbanHeat to disease prediction or claim biological risk outputs. |

## Judging priorities and remaining presentation gaps

The sessions emphasize meaningful satellite use, team capability, problem relevance and impact, innovation and feasibility. They do not provide numerical weights sufficient to calculate a score. The official public page also includes a concise business-feasibility dimension. Do not invent percentages or a probability of selection.

UrbanHeat already has a working notebook, indicators, QA, a portable map, original inputs/outputs, source attribution, sensitivity scenarios, site observations and received field media. Reproducibility and honest limits are strengths. Current independent scientific/member reviews remain incomplete; that status should stay explicit. Neither this report nor an assistant visual check certifies scientific accuracy or eligibility.

The remaining presentation work should focus on:

1. **Real planning user and action.** Explain a proposed municipal/urban-planning team using the map to shortlist site inspections, then checking use, shade, access, ownership and feasibility before choosing an intervention. These are proposed users and workflow, not confirmed customers.
2. **Actual media in the deck.** Place a representative field photo for each of V04-23, V28-17 and V18-26 within the existing example slides/panels. Identify photographer Abdulrahman Almohannadi and the shared 8 October 2026 13:00–14:00 Qatar (UTC+3) capture window confirmed by Nasser. Exact per-file time is Unknown. State field evidence is from October and satellite thermal dates are in September.
3. **Short, real demonstration.** Use the existing offline preview to select a case, switch an existing layer/date, show the local photo and explain what decision this supports. A 60–90-second segment is our suggested budget, not an organizer minimum. Keep screenshots ready as fallback.
4. **Specific value and development plan.** Describe the proposed value: organizing evidence and choosing where to inspect first. Do not invent measured time saved, heat reduction, health benefits or economic impact. A modest future municipal pilot / planning-service pathway may be presented as a hypothesis to validate, with stakeholder feedback and field assessment as next steps.
5. **Limited historical experiment.** Dynamic World stays secondary. Its primary 30.94% common coverage fails the unchanged 50% gate. It does not support a citywide change result and does not alter the original score. Do not spend a large share of the pitch explaining export logistics or failed coverage.

The latest compact spoken script at the reviewed commit contains **388**, not 386, whitespace-separated words. It still targets 180 seconds and places live interaction only in questions. Treat it as a compact overview. Create a separate live-pitch script with realistic timings rather than simply slowing down these 388 words or repeating technical details.

## Proposed live-pitch preparation budget

This is editorial guidance, not a mandated agenda.

| Segment | Suggested seconds |
| --- | ---: |
| Problem and proposed planning user | 55 |
| Three local cases with photos | 90 |
| Data, actual AI, QA and ranking | 100 |
| Short offline demonstration and outputs | 90 |
| Validation, uncertainty and bounded historical experiment | 80 |
| Proposed value, pilot plan, team and close | 85 |
| **Prepared total, including deliberate pauses/transitions** | **500 (8 minutes 20 seconds)** |

Rehearse with the actual slide transitions and demonstration. Adapt to the presenter; leave margin below ten minutes. Q&A is a separate five-minute period, not included in this budget. Do not mark Mohammed's timing or teammate acceptance complete without confirmation.

## Deadline discrepancy

- The second-session transcript, line 33, describes 11 October at midnight and says the date/time is fixed to UAE time.
- The live official public page inspected on 8 October states 11 October 2026, 11:59 PM in the team creator's timezone.
- These are materially different statements. The supplied direct organizer correspondence previously recorded only 11 October, without an hour/timezone.

Do not silently collapse these into a single confirmed cutoff or reinterpret ambiguous midnight language. Use **10 October as the team's internal target** and finish before the deadline date, so this discrepancy does not delay preparation. If late submission becomes necessary, inspect the actual account guide/countdown or obtain explicit clarification through Nasser; this review sends no message. Do not replace the organizer's date with the internal target.

## Minimum handoff to the existing Codex task

Read current branch heads and preserve newer work before editing.

- Incorporate these requirements into a dated English review/checklist and PROJECT_STATE.md. Clearly distinguish transcripts from the live guide and the deadline conflict.
- Retain the existing twelve-slide design. Add representative photos to the three example slides/panels and revise matching PDF/PPTX without clipping or unreadable text. Update photo/review wording that is now stale.
- Prepare an English live-pitch script targeting eight-to-nine minutes including a short demo, within the organizer's stated up-to-ten-minute pitch. Keep the existing compact script as an explicitly labelled optional short overview/demo reference.
- Update judge questions, delivery guide and team rehearsal instructions for ten minutes plus five minutes Q&A. Emphasize concrete end user, proposed value and a realistic future pilot; do not invent actual adoption, revenue, partnerships or cooling.
- Keep the historical experiment secondary and fully bounded. Preserve external-AI disclosure, 24/25 and 0/30 NDVI diagnostic meaning, 18 sites/four dates versus independent review, Unknown and original analysis/ranks.
- Preserve all original inputs, seven CSV outputs, notebook/model assumptions, raw exports/reference imagery, original media and both backup refs. Do not run new analysis, train a model, obtain new satellite imagery, or add Docker/hosting merely for this handoff.
- Render and inspect the changed presentation, verify corresponding PDF/PPTX text, links and package identity, rebuild the ZIP and checkpoint. Existing app/preview checks apply only when their exact bytes remain unchanged.
- Recheck live account submission requirements before the final form step. Use guarded non-force publication within the already authorized project scope.
- No team practice/review is complete until confirmed. No organizer contact, form upload or hackathon submission is authorized by this report; final submission needs Nasser's separate approval.

