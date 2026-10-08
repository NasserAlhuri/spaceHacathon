# Earth Engine access and historical comparison

## Successful authorized Code Editor execution — 7 October 2026

Nasser completed the current account setup, ran the workflow from commit `14bd1e1e626cf71f667db4062fbbd4aea271e573` in his authorized Code Editor, corrected its masked-fallback runtime error, enabled exports and obtained eight scientific files. The supplied [external export review](Dynamic-World-External-Export-Review.md) records this history and checksums. The original hard-coded `Blocked locally` print was not a current Code Editor access test. No passwords or secret keys are required in chat.

Actual provenance CSVs have 6 September 2021 scene rows and 8 September 2026 rows; both model version 3.5 and QA version 1. Five CSVs and the primary transition TIFF were transferred through connected Google Drive and independently match the review's byte sizes/SHA256. Raw originals are immutable under `data/dynamic_world/raw/2026-10-07/`. The 137 MB ZIP and two approximately 71 MB annual TIFFs exceed the 32 MiB executor attachment transfer limit. Their Drive references exist, but direct materialization returned inherited-proxy CONNECT 403 because the artifact host is not allowed. They are not independently checked here. Permit transfer of the existing files or provide byte-for-byte split parts no larger than 32 MiB; no repeat DW export/account setup is needed.

## Managed runtime access is a separate limitation

Current readiness still has no Google outbound identity/project or credential bindings, and the enforced network policy excludes Earth Engine and authentication endpoints. The earlier local HEAD failure/SDK observations are preserved in `results/earthengine-access-check.json` as dated evidence. Successful Code Editor operation does not imply an authenticated query from this runtime, and the runtime restriction does not imply Nasser's Code Editor failed. Configuring this runtime is optional for independent processing of complete exported files; never send credentials in chat or bypass the configured proxy/TLS.

## Preserved protocol and scientific decision

The unchanged plan uses September 1 inclusive to October 1 exclusive, the original analyst-defined study rectangle, EPSG:32639 and fixed 10 m origin 544635/2845905. Mean valid scene probabilities determine the argmax class. At least 3 observations and primary confidence 0.60 are required, with 0.50/0.70 sensitivity and explicit Unknown. Matched changes use accepted support in both years. The provisional common-window coverage gate stays 50%; it is not accuracy or publication approval.

Actual CSV common coverage is 72.7855%, **30.9385%**, and 4.8821% at 0.50/0.60/0.70. Primary coverage fails. No general change conclusion is adopted. The app displays a limited real-coverage experiment, pending dated-imagery validation and missing annual raster transfer, separate from original thermal results/ranks. 2023, SamGeo and extra models are deferred.

## Saved fixes and reproducible checks

`src/dynamic_world_earthengine.js` preserves the supplied successful conditional fallback correction, writes full asset paths plus image indexes in future provenance, fills explicit no-data after clipping and removes stale unconditional failure text. The new provenance/mask revision was syntax-checked locally but has not generated new server exports. Preserve the original eight exports rather than silently repairing them.

```bash
python src/validate_dynamic_world.py --exports data/dynamic_world/raw/2026-10-07 --output results/dynamic-world-table-verification.json
python src/validate_dynamic_world_rasters.py --exports data/dynamic_world/raw/2026-10-07 --manifest metadata/dynamic-world-export-manifest.json --output results/dynamic-world-raster-verification.json
```

The raster command requires optional numpy/rasterio/pyproj dependencies already retained in this workspace; portable users should use their scientific environment. Raw CSVs remain unchanged. Canonical IDs reconstructed from declared dataset/index are explicitly derived and not independently fetched. Table arithmetic success, grid/provenance consistency, raster completeness, failed coverage and scientific readiness have separate fields. Current raster checks are partial and explicitly list missing annual files. Finite in-region support is required even if declared no-data is -9999/255; border zero must never become water→water. Scientific displayed areas use original EE pixelArea sums; projected pixel counts remain separate diagnostics.

See [Dynamic-World-Assessment.md](Dynamic-World-Assessment.md) for checks, precision and area conventions. Eight 2026-only stable/Unknown locations were visually inspected against packaged 5/15 September 2026 RGB context; this does not validate 2021 or change. Paired manual review remains empty. `src/review_dynamic_world_imagery.js` prepares provenance-linked dated source layers/targets for the existing authorized Code Editor, without exports. Complete changed/stable, built/bare, vegetation and coastal checks with actual reference dates, disagreements and ambiguity before considering any general result. Current photographs cannot validate 2021 labels. Team reviews and photographs remain pending. No hackathon submission is authorized or performed.
