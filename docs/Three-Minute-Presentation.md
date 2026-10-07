# Three-minute presentation script

Team Al Zubarah — UrbanHeat AI, Al Khor. Use the revised twelve-slide PDF or PowerPoint. Target: 180 seconds. Timing is a rehearsal target, not a completed team rehearsal. Speak the script below; headings and timing cues are not spoken. Avoid live map interaction within the three-minute slot; keep the offline preview ready for questions.

## Slide 1 — 0:00–0:10

We are Team Al Zubarah from Qatar. UrbanHeat AI uses satellite evidence and local observations to help investigate heat-protection opportunities in Al Khor.

## Slide 2 — 0:10–0:25

Our planning question is simple: where should a team investigate first? Hot surfaces alone do not tell us who is exposed. We screen locations, then ask about use, shade and access.

## Slide 3 — 0:25–0:45

At the bus-stop cell, the mean of the two date-level temperature medians is 50.4 degrees Celsius. Local observations describe roadside trees and no shelter. Nasser confirms site visits. User counts, use times and detailed shade assessment have not been measured.

## Slide 4 — 0:45–1:05

We combine Sentinel-2 greenery, Landsat surface temperature, historical WorldCover land cover and OpenStreetMap buildings. Two September thermal dates pass our checks; September sixth does not. Surface temperature is not air temperature or a health-risk score. Thermal detail is about 100 metres.

## Slide 5 — 1:05–1:25

We remove unsuitable or uncertain pixels, compare common inland support, then summarize 300-metre cells. Our relative ranking combines heat, low green signal and mapped buildings. We test thirteen settings. Our pipeline is deterministic; WorldCover provides upstream machine-learning-derived land cover.

## Slide 6 — 1:25–1:35

Our three presentation cases illustrate different uses. All 1,111 observed cells and 373 screened urban candidates remain; the satellite top three are unchanged.

## Slide 7 — 1:35–1:45

The accepted dates share about 94.4 square kilometres of inland thermal support. Comparing the same footprints reduces changes caused by missing coverage.

## Slide 8 — 1:45–2:10

Our third case is the reported jogging route, V18-26: a 47.47-degree cell summary, 72-percent coverage and rank 275. Abdulrahman reports nearby mangroves do not shade the path; dated photos are pending. This is a use example, not a top-three rank. Hospital land stays in the results. Zero detected greenery does not mean no trees.

## Slide 9 — 2:10–2:30

The package preserves thirty-five hashed inputs and seven original result tables. The expanded notebook test passed with five successful code cells and no errors. Reference checks have mixed results; they do not establish overall accuracy. The map and offline preview also passed technical Chromium checks.

## Slide 10 — 2:30–2:45

Next, measure use and shade and check access. We prepared a September 2021/2026 Dynamic World workflow, but access and validation are blocked. No historical-change result, health risk or causal cooling is claimed.

## Slide 11 — 2:45–2:55

Abdulrahman reviews the project and collects photographs. Mohammed practises the presentation. These tasks and other members' reviews remain pending until individually confirmed.

## Slide 12 — 2:55–3:00

Our public package includes sources, licences and reproducible evidence. Thank you.

## Rehearsal and demonstration cues

- Rehearse aloud with a timer. Shorten transitions if needed; do not drop the visits-versus-measurements or temperature limitations.
- For questions, open `preview/UrbanHeat-AlKhor-Preview.html` in a browser. Select V04-23, V28-17 and V18-26 for presentation cases; V04-24 remains available. Compare all five reviewed sites and show the two dates. Review CSV export has ten rows: five sites × two dates.
- Treat quoted temperatures as cell summaries, not surveyed point measurements. Keep Unknown values visible and distinguish reported conditions from quantitative measurements.
- This script is prepared material. It does not certify Ali's rehearsal, Abdulrahman's project review/photo collection, Majed's slide review, Mohammed's presentation practice or final submission approval.
