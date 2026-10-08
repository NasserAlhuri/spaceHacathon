# Exact annual reassembly and scientific review — 8 October 2026

## Completed transfer and technical verification

The six uploaded `DW-2021-part-01/02/03.zip` and `DW-2026-part-01/02/03.zip` archives were extracted into one separate staging directory. All ZIP CRC checks passed, and the copies of `REASSEMBLY.json`, `reassemble.py` and the transfer README were byte-identical across archives. The supplied 994-byte script was inspected and executed unchanged. It only reads local parts, verifies their sizes/SHA256 and writes the two output files in its own directory. Every part and assembled original matched `REASSEMBLY.json` and the already recorded original export hashes:

| Exact original | Bytes | SHA256 |
|---|---:|---|
| AlKhor_DynamicWorld_September_2021.tif | 70,946,103 | `dbd607e338d1feeafabace35b74d62836253412d85f270eacc8fde0aebbe3617` |
| AlKhor_DynamicWorld_September_2026.tif | 71,045,484 | `7fe54821078d813fcb9b00baaea005eda8249260616901b40701457e8ce4fdf4` |

All eight original exports are now locally available and independently checksum-verified under `data/dynamic_world/raw/2026-10-07/`. The raw CSVs/rasters remain immutable. Uploaded ZIPs and extracted parts remain in their separate workspace staging locations; the project/package contains the eight original exports and preserved transfer helpers/manifest, rather than duplicating six large parts. Individual-member verification does not establish the SHA256 of the original 137 MB Drive-download ZIP, which was not downloaded. Evidence is `results/dynamic-world-reassembly-verification.json`; exact supplied helpers are retained under `metadata/dynamic-world-transfer/`.

`src/validate_dynamic_world_rasters.py` completed actual checks on all three GeoTIFFs: EPSG:32639, 1108 × 1057 dimensions, fixed 10 m transform/origin 544635/2845905, exact band names/order, Float32 annual encoding/no-data -9999, UInt8 transition encoding/no-data 255, all nine probability ranges/sums, observation counts, confidence/max and class/argmax consistency. Both annual rasters have 1,163,270 finite exported samples and 7,886 nonfinite border samples. Counts range 4–6 in 2021 and 7–8 in 2026. Maximum probability-sum deviations are approximately 0.0000601113 and 0.0000579190; sums are numerically close to one, not exactly equal. The unchanged numerical tolerance 0.0001 is separate from confidence 0.60 and coverage 50%.

The raw transition file matches the computed primary class pair on all finite original clipped support. Its 7,886 nonfinite annual-border locations incorrectly contain raw zero; they are explicitly excluded, never displayed as water→water. Centre-in-study-rectangle checking additionally excludes finite clipped edge pixels whose centres lie outside the rectangle: finite centre-in-rectangle support is 1,161,343, and the combined outside/nonfinite diagnostic is 9,813 pixels. This explains why a centre-only border count differs from the raw annual NaN count. Both support definitions are recorded explicitly; no original export or CSV is repaired/replaced.

The checker now fails if named band order or positive transition categories disagree, rather than emitting a successful integrity status with a hidden false flag. Actual positive categories match the original CSVs at all three thresholds. On the finite original clipped support:

| Threshold | Matched raster pixels | Changed pixels | Relation to unchanged scientific rule |
|---|---:|---:|---|
| 0.50, sensitivity | 846,930 | 351 | Sensitivity only; not adopted |
| 0.60, primary | 360,063 | 0 | Common EE area is only 30.9385% of the window; **50% gate fails** |
| 0.70, sensitivity | 56,929 | 0 | Coverage gate fails |

At 0.50 the 351 differing pixels comprise 301 water→bare and 50 bare→built classifications. They are not validated historical changes. Primary selected-support stability is not citywide stability. Displayed scientific coverage/areas use the untouched Earth Engine pixelArea CSV sums. Full exported pixel counts ×100 m² exceed those EE areas by approximately 0.1254%, 0.1430% and 0.3384%. Centre-only counts are a separate conservative diagnostic. These differences are area conventions/boundary support, not accuracy estimates. No threshold, study boundary or baseline result was adjusted to make the result pass.

## Expanded dated-image diagnostic — still incomplete scientific validation

`src/review_dynamic_world_exports.py` prepared 18 actual target locations from changed/stable, built/bare, water/coastal, low-confidence vegetation and Unknown strata. Small strata use 8-connected components; larger strata use separated row quantiles. Within-stratum targets are separated by at least 300 m when possible and kept inside the image context margin. Only one suitably separated bare→built target was available under this selection rule; do not pretend three independent construction examples were checked. The convenience sample is biased and not designed to estimate citywide accuracy. Coordinates, confidence, raw labels, accepted 0.50 labels and primary 0.60 Unknown status are explicit in `metadata/dynamic-world-scientific-samples.csv`.

All 36 context views, from the preserved and source-dated **5 and 15 September 2026** Sentinel-2 L2A inputs, were visually inspected. Four context pages and per-sample observations are in `results/dynamic-world-scientific-context/` and `results/dynamic-world-scientific-review.json`. Source RGB has a 5 m grid-origin offset from the DW grid, so sampling uses each source's own geotransform. Each page shows 410 m context and an approximately 10 m target with a fixed display stretch; display brightness is not reflectance analysis.

- The selected bare→built target has a small block-like/paved structure next to water in 2026. That makes an after-built classification plausible, but does not establish bare land in 2021 or actual construction.
- Water→bare targets have bright bare-looking 2026 context; the 2021 water classification cannot be checked here. Their primary after labels remain Unknown.
- Stable built targets have mixed road/roof/bare material at 10 m; stable bare/water contexts appear plausible in 2026 only. No 2021 agreement was established.
- Coastal flooded-vegetation targets mix dark water/green shoreline context. Some SCL screening flags differ between dates or from a DW class name. SCL is a screening aid with a different taxonomy, not reference truth; these are ambiguity flags, not confirmed class errors.
- Green/dark coastal targets rejected at 0.60 demonstrate why **Unknown is not evidence of absent vegetation**. No species, shade or canopy total is inferred. Unknown urban targets also remain Unknown.

**No dated 2021 RGB was supplied or obtained, and no paired historical label or transition has been validated.** Reading the Earth Search catalog root worked through the web tool, but attempted dated item endpoints were inaccessible. Both Earth Search and Earth Engine runtime requests through the preserved configured proxy returned CONNECT 403; no Google runtime identity/project is configured. These are reference-access limitations, not a failure of Nasser's already successful Code Editor exports. No network restriction or TLS setting was bypassed. Existing WorldCover labels, scene metadata, current photos and the model's own labels cannot substitute for suitably dated reference interpretation.

The source Sentinel views themselves are not independent ground truth. No overall accuracy, error rate, surveyed growth or vegetation-change total is estimated. The paired manual-review CSV remains empty; Abdulrahman's review/photos, Mohammed's presentation practice and other teammate tasks are pending until independently confirmed.

## Exact remaining evidence and prepared helper

The specific missing reference is 2021 RGB with source/date and cloud/visibility evidence at the recorded changed/stable and vegetation/coastal targets. `src/export_dynamic_world_2021_reference_rgb.js` is a prepared, syntax-checked helper for Nasser's **already authorized** Code Editor. It uses the original provenance-linked source IDs:

1. `COPERNICUS/S2_HARMONIZED/20210901T070619_20210901T071620_T39RWJ`
2. `COPERNICUS/S2_HARMONIZED/20210926T070641_20210926T072035_T39RWJ`

The helper prints actual acquisition/cloud metadata and offers two whole-window RGB/QA60 GeoTIFF tasks plus a provenance CSV. Four UInt16 bands at this grid should total approximately 19 MB uncompressed across both images; actual output sizes must be checked. RGB is explicitly a fixed visualization, and QA60 retains native 60 m cloud/cirrus information. Its export switch defaults off; no helper execution/new source metadata or exports are claimed here. This is a narrowly identified reference need, **not another Dynamic World export, account setup, analysis rerun or new model**. If either date is cloudy/ambiguous at targets, record Unknown and obtain another actual suitably dated source with documented identity rather than inventing a label.

After receiving/retrieving these references: verify source dates, grid/masks/cloud visibility; inspect paired targets and record reference labels, disagreements and ambiguity; retain convenience-sample and same-source limits; complete independent scientific review. The unchanged failed primary coverage gate remains a separate blocker even if imagery review succeeds. Continue to show the limited real-coverage/Unknown experiment; do not adopt a general Al Khor urban-growth, vegetation-change or stability conclusion. 2023, SamGeo and additional models remain deferred. No organizer contact or hackathon submission is authorized or performed.
