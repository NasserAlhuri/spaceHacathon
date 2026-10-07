# Al Khor local review and bus-stop example

Recorded 6 October 2026 from the supplied teammate notes and Nasser's Street View link. Local observer: Abdulrahman Almohannadi. On 6 October, Nasser Alhuri reports that he visited the sites and confirms the described physical situation is the same as in September 2026. Exact visit dates were not supplied. Detailed shade, use and access measurements and independent scientific validation remain pending. The reports do not change the satellite score.

## Three different investigation needs

| Cell | Centre latitude, longitude | Local observation | Required next check |
|---|---|---|---|
| V04-23 | 25.717995, 51.515221 | Road near Al Khor Hospital linking Al Khor and Al Thakira; roadside trees, bus stop without a visible shelter, short sidewalk and reported limited route continuity | Current shade at waiting times, passenger use, exact stop location, walking access, ownership and feasibility |
| V28-17 | 25.653042, 51.497008 | Al Bayt Stadium parking, reported mainly busy on match days | Event timing, pedestrian routes, existing shade and use outside events |
| V04-24 | 25.717984, 51.518211 | Empty hospital-associated land; possible expansion is unconfirmed | Ownership, planned use and present or future pedestrian use |

Pins are centres of 300 m cells, not exact coordinates of every feature. V04-23 and V04-24 share a boundary and are not independent neighbourhood examples. A nearby seasonal farmers' market is not assigned to either cell; inclusion has not been demonstrated.

## V04-23: evidence for a site assessment

1. **Satellite evidence:** cell-median surface temperature was 51.35 °C on 14 September 2026 and 49.42 °C on 30 September. Mean of date medians: 50.39 °C. Green-pixel share at NDVI >=0.30 was 0% for the paired optical dates, 15 and 30 September. Mapped-building share: 2.33%. Scenario ranks: 1–14. All 100 delivered 30 m samples are retained; they are spatially dependent and the native thermal detail is about 100 m. These values describe the cell, not a measurement at the sign or waiting area.
2. **Local review:** Abdulrahman reports roadside trees, a stop without a shelter and limited continuous walking access. A shelter or safer route could be considered after inspection; planting is not an automatic prescription.
3. **Historical reference:** [Google Street View](https://maps.app.goo.gl/gPEzxW3NFqErPWNP8), panorama McFzT23rIzQ4UJTSgSHFCQ, capture March 2023. The linked camera is at 25.7175476, 51.5145504, inside V04-23 and approximately 84 m from its centre. This is a camera coordinate, not a surveyed stop coordinate. The supplied view shows a bus-stop sign, trees, a short paved sidewalk and no shelter in view. Some tree shadow is visible. The March 2023 image is historical. Separately, Nasser confirms the described physical situation is the same as in September 2026 based on his site visits; exact visit dates were not supplied. Neither source establishes all-day shade or measured walking safety. Retain the live link; Google imagery is not redistributed in this package.
4. **Unknowns:** passenger counts, waiting times, shade through the day, precise sign coordinates, current condition, ownership, cost, maintenance and feasibility.
5. **Planner's next action:** follow up at the stop and walking route at relevant use times, record dated evidence, confirm ownership and assess feasible shade or access improvements. No measured cooling or health benefit is claimed.

## Greenery audit

The separate audit uses the packaged scaling, scene classifications, grid, full polygon and matched thermal support. It reproduces the original 0% values; they are not a rounding artifact. The highest clear-land pixel-centre NDVI inside the cell is 0.26262 on 15 September and 0.24985 on 30 September, both below 0.30.

| Optical date | Clear-land pixel centres inside polygon | Pixels at NDVI >=0.30 | Matched-support green share at 0.20 | Matched-support green share at 0.30 |
|---|---:|---:|---:|---:|
| 15 September 2026 | 897 | 0 | 2.7222% | 0% |
| 30 September 2026 | 897 | 0 | 0.3889% | 0% |

Pixel-centre counts and the area-weighted matched-support percentages use different boundary conventions; the main pipeline's area-weighted method is preserved. There are 25 and 4 pixel centres passing 0.20, respectively. These thresholds detect vegetation signals, not individual trees. Narrow tree rows, mixed pixels, spectral conditions and differing dates may contribute; no single explanation is proven. Nasser confirms the described roadside trees and physical situation remain the same as in September 2026 based on his site visits. This is a firsthand qualitative report, not an NDVI or vegetation-health measurement; exact visit dates were not supplied. Keep the tested 0.30 threshold and ranking; do not adjust them to match the screenshot.

Reproduce after generating the original outputs:

```sh
python src/audit_local_greenery.py
```

See `results/local-greenery-audit.json` and the unchanged original analysis. The new audit is separate from the previously executed five-cell notebook and does not constitute independent vegetation or temperature calibration.

## Current site-check form

Record observer, date, time, coordinates and evidence type. Photograph the stop, waiting area and route without unnecessary identifiable people. Record shelter visibility and shade at the observation time; do not generalise one photograph to the whole day. Passenger observations should identify duration and avoid extrapolating an unrepresentative interval. Leave unknowns unknown. Confirm ownership, permissions, available space, water/maintenance needs and relevant development plans before choosing an intervention.

## Added attributed reports — 7 October 2026

V18-26 and V24-07 reports are recorded in app/local-review.json and explained in [Site-Evidence-Guide.md](Site-Evidence-Guide.md). V18-26 is the presentation's third case instead of hospital land. Its supplied point is geometrically inside the cell; the full route and nearby features remain unverified. V24-07's reported absence of pedestrians at an unspecified time does not establish no use at other times. All new photos, capture dates/times and detailed measurements remain pending. Original visit confirmations are not extended to these added locations. All satellite ranks and the original top three are unchanged.
