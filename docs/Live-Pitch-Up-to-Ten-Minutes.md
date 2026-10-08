# Live pitch preparation — up to ten minutes, then five-minute Q&A

Prepared 9 October 2026 for Team Al Zubarah, Qatar. Use the existing twelve-slide PDF/PPTX. **Prepared target: 8:20, including a 75-second offline demonstration and transitions.** The up-to-ten-minute pitch followed by five-minute questions is reported in the supplied orientation review; 8:20 and the demo budget are team preparation choices. This is for a possible shortlisted invitation; no invitation, booked slot, attendance, rehearsal or submission is confirmed. The account's actual invitation/guide must govern any final slot.

Mohammed may present the prepared material; teammates may help during questions. Role assignment does not certify practice. Speak only the **Say** paragraphs and the separately labelled demo speech. Timing cues, actions and source notes are not spoken. See Five-Minute-Judge-QA.md for the separate questions period. The compact Three-Minute-Presentation.md remains an optional overview; it is not the live-pitch time limit. Do not stretch or repeat that script to fill ten minutes.

## Slide 1 — 0:00–0:20

**Say**

We are Team Al Zubarah from Qatar. UrbanHeat AI combines satellite evidence and local observations to help investigate heat-protection opportunities in Al Khor. We built an inspectable screening prototype, with a working map, reproducible notebook and documented limitations.

**Cue:** Introduce the title; move directly to the planning user. Do not claim an official citywide boundary or a completed municipal deployment.

## Slide 2 — 0:20–1:05

**Say**

Our proposed user is a municipal or urban-planning team deciding where to inspect first. A hot satellite cell cannot tell that team how many people use a place, when they arrive, or whether shade is adequate. Our proposed decision path is to shortlist locations, inspect use, shade and access, then check ownership and feasibility before choosing an intervention. The value hypothesis is better-organised evidence and clearer inspection decisions. We have not confirmed a customer, partnership, adoption or measured benefit. Trees, shelters and safer routes are options to assess, not approved recommendations.

**Cue:** Point to proposed user → inspection → feasibility. This workflow, rather than the hottest value alone, is the decision being supported.

## Slide 3 — 1:05–1:50

**Say**

At the bus-stop example, V04-23, the summary is 50.4 degrees Celsius: the mean of two date-level surface-temperature medians for a 300-metre cell. This is not air temperature, a bus-stop measurement or personal exposure. Abdulrahman's observations describe roadside trees, no shelter and limited walking access; Nasser confirms visits. The field photograph helps us ask where passengers actually wait and whether the walking route is safe. Passenger counts, use times and detailed shade have not been measured. The next step is a documented site assessment, not estimating exposure from this cell.

**Cue:** Keep the cell-versus-point distinction explicit; the representative photo is on slide 6.

## Slide 4 — 1:50–2:45

**Say**

We combine Sentinel-2 green-pixel indicators, Landsat surface temperature, historical WorldCover land cover and contributed OpenStreetMap building footprints. The accepted thermal dates are September fourteenth and thirtieth, twenty twenty-six. September sixth fails our coverage checks and is excluded. Native thermal detail is about 100 metres, even though the delivered grid is 30 metres; we report 300-metre cells. WorldCover is historical, and mapped buildings can be incomplete. The field photographs were taken on October eighth, after the September observations, so they provide later context rather than simultaneous measurements. No hyperspectral or proprietary very-high-resolution source is used. Source credits remain in the package.

**Cue:** The October/September distinction is visible on this slide and in slide 3's footer. Avoid implying that photographs validate temperature or historical classes.

## Slide 5 — 2:45–3:25

**Say**

The workflow starts with packaged satellite inputs and mapped context, screens cloud, coast and shared spatial support, then computes cell indicators. Our relative ranking combines heat, low green signal and mapped buildings, with eligibility rules and thirteen sensitivity settings. These choices are not a validated optimum. External AI land-cover inputs differ: WorldCover supports heat screening; Dynamic World is a separate historical experiment. Quality checks and ranking are rule based. We trained no new model, and Dynamic World does not feed the original score.

**Cue:** Follow the editable arrows. Keep export logistics and additional models out of the pitch.

## Slide 6 — 3:25–4:10

**Say**

These actual photographs show our three presentation cases: the bus-stop road, stadium parking and jogging route. Abdulrahman Almohannadi took them on October eighth, twenty twenty-six. Nasser confirms a shared one-to-two p.m. Qatar-time capture window; this is user confirmation, not EXIF, and exact per-file times remain Unknown. The stadium raises an event-use question, while the route raises a path-shade question. A visible tree or shadow does not measure all-day shade. All 1,111 observed cells and 373 screened candidates remain; these team-selected use examples do not replace the satellite top three.

**Cue:** Point to each photograph, not a claimed camera coordinate. Retain the visible common date/window and source attribution.

## Slide 7 — 4:10–4:35

**Say**

The two accepted thermal dates share about 94.4 square kilometres of inland sample footprints. Comparing the same retained support reduces apparent differences caused by missing coverage. These are two screened snapshots, not evidence of seasonal change, a warming trend or causal cooling.

**Cue:** Point to the existing output; no new result or recalculation is introduced.

## Slide 8 — 4:35–6:15

**Say**

V18-26 has a 47.47-degree cell summary, 72-percent retained coverage and rank 275. It is a use example; hospital land stays in the full results. Let's compare satellite evidence with the local photograph and remaining Unknowns.

**Cue:** Allocate 4:55–6:10 to the following 75-second demonstration, including its speech. Return to slide 8 by 6:10; transition to slide 9 by 6:15. Open the exact standalone preview beforehand. Detailed actions and fallback are in Live-Demo-Runbook.md. Do not depend on an external Street View page.

**Demo speech**

Here is the bus-stop cell. I switch the accepted September date and the existing layer, then show its October photograph. The satellite value describes the cell; the photograph supplies later local context. These Unknown fields show what still needs field assessment. I compare the stadium and jogging examples without changing their ranks. A planner can use this evidence to organise a site visit, then verify use, shade, access and feasibility before proposing an intervention.

**Demo actions:** Select V04-23; switch the two accepted dates and an existing layer; open its local photo; show Unknown fields; compare V28-17 and V18-26; return to the deck. Stop by the budget. If interaction is blocked, use the prepared slide 6 photograph and slide 8 result table plus docs/Demo-Fallback-Screenshots.pdf; describe the intended controls without claiming live success.

## Slide 9 — 6:15–7:00

**Say**

Our package preserves 35 hashed inputs and seven original analytical tables. A previous clean GitHub notebook run completed five code cells without errors and reproduced the tables byte for byte. We have not rerun analysis for these presentation changes. The NDVI threshold is met at twenty-four of twenty-five grass references and zero of thirty building references. That is a vegetation diagnostic, not building-detection accuracy. Contributed labels can conflict, and independent validation remains pending. Recorded Chromium checks support the unchanged map and offline preview on desktop and mobile emulation; physical-device and teammate acceptance are still pending.

**Cue:** Distinguish reproducibility, reference diagnostics and independent accuracy; none substitutes for the other.

## Slide 10 — 7:00–7:45

**Say**

The separate Dynamic World experiment stays secondary. Its 30.94-percent common coverage fails our unchanged fifty-percent gate, so we claim no citywide historical change. Assistant review of eighteen sites across four dates is complete; independent scientific validation is pending. Our proposed pilot would seek planner feedback, document use, shade, access and ownership, and test whether the shortlist is useful and feasible. A future planning-support service is a hypothesis to validate, not an existing business. We have measured no time saved, cooling, health benefit or revenue. Further dates and models remain deferred.

**Cue:** Spend only the first two sentences on Dynamic World; focus the remaining time on practical validation and the proposed pilot. Confidence 0.60 and Unknown/excluded 69.06% remain in the full evidence and judge answers.

## Slide 11 — 7:45–8:05

**Say**

Nasser coordinates the team and confirms visits. Abdulrahman's supplied photo collection is complete, but his project review remains pending. Mohammed rehearses the pitch, Majed reviews limitations, and Ali prepares the demonstration and questions. These assignments do not certify completed reviews or practice.

**Cue:** One presenter is allowed according to the supplied review; actual teammate availability and acceptance are unconfirmed.

## Slide 12 — 8:05–8:20

**Say**

Our public package includes the notebook, inputs, outputs, licences and offline demonstration. We propose choosing where to inspect first, then validating decisions in the field. Thank you.

**Cue:** End the pitch. The separate five-minute judge period follows only if invited. Do not start new analysis or spend pitch time opening external credits.

## Timing, readiness and provenance

The prepared spoken text contains **895 whitespace-separated words**: 821 outside the demo and 74 within it. At 135 words/minute, non-demo speech is estimated at 364.89 seconds. The 75-second demo includes its narration; it is not added twice. Approximately 60.11 seconds remain for pauses/transitions within 500 seconds. These are estimates, not measured speaking time. See metadata/live-pitch-timing-2026-10-09.json.

Actual rehearsal is **pending**. Mohammed must record a timed run including opening the demo, transitions and a fallback run; adjust concise delivery rather than inventing results. If reaching 9:00 unexpectedly, shorten commentary and use the prepared fallback rather than beginning a long interaction. Stop within the actual allotted maximum. The optional three-minute overview and optional two-to-three-minute screen recording are distinct; no screen recording has been produced or certified. The received six-second field video is site evidence, not an application recording.

The unchanged original analysis, ranking, confidence threshold, failed coverage gate and Unknowns are preserved. All media provenance follows Nasser's explicit confirmation. Organizer timing/process statements are attributed to the supplied 8 October orientation review; its underlying Whole sessions.txt, recordings, YouTube-section mapping and live account guide were not independently reviewed in this task. See Orientation-Requirements-and-Handoff.md. No submission or organizer contact is authorized by this prepared script.
