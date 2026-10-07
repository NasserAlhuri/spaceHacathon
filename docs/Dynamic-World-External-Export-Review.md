# UrbanHeat: review of actual Dynamic World exports

Reviewed 7 October 2026. This is a review handoff, not a publication or hackathon submission approval.

## Conclusion

Earth Engine access and actual server exports succeeded in Nasser's authorized Code Editor. The eight exported files are readable and their table arithmetic reconciles. However, this comparison is NOT ready for a headline claim about Al Khor's urban expansion or vegetation change. The prespecified primary threshold of 0.60 retains only 30.94% common support, below the provisional 50% coverage gate, and independent dated-imagery review remains pending. Keep original thermal/NDVI inputs, results, rankings and backup branches unchanged.

## Source and identity

- Uploaded archive: `drive-download-20261007T201055Z-1-001.zip`.
- ZIP size: 137120705 bytes; SHA256: `b67a6eca5208f9ddc4dc03bd5b0b8e5fb338622a2e50d439dd7f86e136a700c6`.
- Eight files; ZIP integrity check passed: two 12-band annual-window composites, one transition raster and five CSV tables.
- The prepared script was taken from commit `14bd1e1e626cf71f667db4062fbbd4aea271e573`.
- A runtime error occurred when a fully masked fallback image was merged with real probability images (MaskOnly vs Float). Nasser replaced `var safe = ee.ImageCollection([empty]).merge(clean);` with:

```javascript
var safe = ee.ImageCollection(ee.Algorithms.If(
  collection.size().gt(0), clean, ee.ImageCollection([empty])
));
```

- Exports were subsequently enabled. The script's stale `Blocked locally` print is a hard-coded message, not evidence of current Code Editor failure. The original managed Codex environment's network restriction is a separate issue.
- Actual observations: 6 scene records in September 2021 and 8 in September 2026. These are scenes intersecting the study window, not six/eight guaranteed cloud-free observations per pixel.
- Provenance records contain model version 3.5 and QA version 1 for both years; the date windows are September 1 inclusive to October 1 exclusive.

## Coverage and sensitivity

Study-window area from the exported tables: 116.213995 km².

| Threshold | Matched support (km²) | Window coverage | Provisional 50% gate |
|---|---:|---:|---|
| 0.5 | 84.586895 | 72.785% | Pass |
| 0.6 | 35.954878 | 30.939% | Fail |
| 0.7 | 5.673699 | 4.882% | Fail |

At 0.60, accepted whole-year coverage is 35.31% for 2021 and 37.51% for 2026. These are accepted-support fractions, not classification accuracy. Do not lower the threshold merely to obtain an attractive coverage/result. A threshold change requires a documented justification, sensitivity results and independent review.

At 0.60 and 0.70, the accepted common-support classifications show no pixel transitions. This is a selected subset and DOES NOT establish that Al Khor was unchanged. At 0.50 there are 351 changed raster pixels, and the matched-support built-class net change is about 0.005004 km². This is unvalidated, threshold-sensitive classified change; it is not a surveyed construction total or a citywide growth estimate. Do not promote it as a finding. Classes failing acceptance, including vegetation, must not be interpreted as absent from the city.

## Checks actually performed

- Eight archive members decoded; CSV rows: provenance 14, coverage 6, whole-window areas 60, matched changes 27, transitions 243.
- 105 numerical consistency checks passed: accepted + Unknown area, accepted fractions, whole-window class totals, before/after change arithmetic, transition row and column margins, transition totals and net-area conservation.
- Three GeoTIFFs inspected: each is 1108 × 1057 pixels, CRS EPSG:32639, 10 m grid with origin 544635, 2845905. Both annual-window files have 12 Float32 bands; transition codes use UInt8. Declared no-data values are -9999 and 255 respectively.
- Raster samples decoded through libtiff. Both annual-window rasters contain 1,163,270 finite in-window pixels. Valid-observation counts are 4–6 in 2021 and 7–8 in 2026.
- Nine probabilities remain in [0,1]; maximum deviation of their sums from one is approximately 0.0000601 in 2021 and 0.0000579 in 2026. Report this numerical precision rather than pretending exact equality.
- Exported confidence equals the maximum of the nine probability bands, and exported class equals their argmax at all finite pixels.
- The transition raster exactly matches the primary-threshold class-pair calculation inside the finite study support. Positive transition categories agree with the CSVs for all thresholds.
- Outside the clipped study support, the decoded annual rasters have 7,886 NaN border pixels, while the transition raster has value 0 at those locations despite its declared no-data value. Explicitly mask outside-region and nonfinite pixels; do not display border 0 as water→water. Do not rely solely on `value != -9999` as the valid-data test.
- Simple projected pixel-count × 100 m² differs from exported Earth Engine areas by roughly 0.13–0.34% on common support. These are different area calculations; the CSV arithmetic was checked separately. Use one documented area convention consistently. Exact independent per-pixel reproduction of Earth Engine area totals was not performed.

## Documentation/validator issues

The exported `asset_id` values are image indexes such as `20210901T070619_20210901T071620_T39RWJ`, rather than full `GOOGLE/DYNAMICWORLD/V1/...` paths. The current validator requires the full prefix and will reject these real exports at its first provenance check. Preserve the originals. Document an explicit derived canonical identifier using the declared dataset plus image index, check it against the actual source metadata/imagery, and fix future export provenance. Do not silently rewrite original CSVs or claim that a reconstructed identifier was independently fetched.

The validator also raises an exception when any sensitivity threshold fails the coverage gate. Separate arithmetic integrity, provenance/grid checks, coverage suitability and publication readiness. A failed scientific coverage gate must remain recorded as failed; do not remove it or weaken it to obtain a green report. Missing manual validation remains a separate blocker.

## Next work for Nasser's Codex task

1. Read the current live repository checkpoint and branch heads; reconcile newer work. Preserve both recorded backups and original analysis outputs.
2. Ingest the exact uploaded archive as actual external exports, with checksums/provenance and the above execution history. Update the checkpoint so authorized Code Editor export success is distinct from the managed runtime's blocked network. Save the verified fallback correction and update the stale status message.
3. Fix provenance handling and validity masks transparently, and run integrity checks on actual exports. Keep raw files immutable. Correct the validator's reporting structure without changing its coverage criteria. Check DataSet attribution and all public file/package sizes before any publication.
4. Inspect representative changed and stable locations against suitably dated Sentinel-2 imagery or other licensed historical evidence. Pay attention to built/bare confusion, vegetation and coastal areas. Current site photos cannot validate 2021 labels. Record samples, dates, disagreements and uncertainty; do not claim overall accuracy from a small convenient sample.
5. Assess whether the existing monthly comparison supports a useful limited result. If it does not, retain an honest experimental-layer/coverage demonstration and document why a general change result was not adopted. Do not add 2023, new models, or arbitrary threshold adjustments merely to obtain a result.
6. Only integrate a clearly labelled historical/experimental display after actual checks. Show Unknown, coverage and limits, and keep thermal ranks independent. Update the preview, presentation and tests only to match what was actually established.
7. Nasser's photographs and teammate reviews remain pending unless separately supplied/confirmed. No hackathon submission or organizer contact is authorized.

Nasser has completed the current account setup and export step. These files suffice for the next analysis; request another export only for a specific identified data need.

## Export checksums

| File | Bytes | SHA256 |
|---|---:|---|
| AlKhor_DW_coverage.csv | 1284 | `1456a415ccc98867125e2112b21bc7d7218409746f43228f887a77e42610cf11` |
| AlKhor_DW_matched_changes.csv | 5816 | `a6bc0d94401e0b2c26009b81735352bcedaded36af23990dd02e6a8c3467f8ba` |
| AlKhor_DW_provenance.csv | 3952 | `71bdf717c21460c033838c07159c0b4b64da180a15cdd81577dcf2a49d55de79` |
| AlKhor_DW_transition_2021_2026.tif | 44826 | `2e71882ebb2d950f3c0d5f0a2479b2e026be8b4d7674984bd139667625d8aa4d` |
| AlKhor_DW_transitions.csv | 22381 | `9815e94fe7e361331d931257139b7ad0874016419f1c76490369c52232e7d4f6` |
| AlKhor_DW_whole_window_areas.csv | 6207 | `e82fb6f84b544e327abaa6378e2c7cc4c46f4bc83baa0de712abcb31709cf68c` |
| AlKhor_DynamicWorld_September_2021.tif | 70946103 | `dbd607e338d1feeafabace35b74d62836253412d85f270eacc8fde0aebbe3617` |
| AlKhor_DynamicWorld_September_2026.tif | 71045484 | `7fe54821078d813fcb9b00baaea005eda8249260616901b40701457e8ce4fdf4` |
