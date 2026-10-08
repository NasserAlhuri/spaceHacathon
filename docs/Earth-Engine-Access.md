# Earth Engine execution and reference access — 8 October 2026

Nasser completed authorized Code Editor setup, corrected the masked-fallback runtime error, ran the September 2021/2026 workflow and exported eight files on 7 October. The supplied [external export review](Dynamic-World-External-Export-Review.md) records that successful execution history. A stale hard-coded local failure message was not evidence of Code Editor failure. Do not ask Nasser to repeat account setup or send secrets in chat.

All eight exact original files are now locally verified: the five CSVs and transition TIFF were received through Drive; the two annual TIFFs were reconstructed from six uploaded parts on 8 October. Every part and both output hashes match REASSEMBLY.json and the already recorded export identities. Complete actual raster checks passed. The earlier 32 MiB transfer problem has been resolved by parts. The original external ZIP's archive hash was not independently checked. See [current technical/scientific report](Dynamic-World-Reassembly-and-Scientific-Review.md).

The managed runtime still has no Google API identity/project bindings. Through its preserved configured proxy, Earth Search and Earth Engine requests returned CONNECT 403. The web tool could read the public catalog root but not requested dated 2021 item endpoints. No proxy/TLS/network policy was bypassed. Code Editor success and managed runtime API access are separate facts; the runtime limitation now blocks missing reference retrieval, not the completed DW transfer/checks.

The specific remaining evidence is suitably dated 2021 RGB with source identity and visibility/cloud evidence at the recorded changed/stable and coastal/vegetation targets. `src/export_dynamic_world_2021_reference_rgb.js` is prepared and syntax-checked for the existing authorized Code Editor: 1 and 26 September 2021 source IDs from the original provenance, two small RGB/QA60 exports and a provenance CSV. Expected combined uncompressed image size is about 19 MB; verify actual files. It defaults to no export creation and has not run here. This is a specific reference-data need, not another DW analysis or a new model. Metadata and dated pixels must be checked when supplied; cloud/ambiguity stays Unknown.

The unchanged plan uses the same analyst-defined rectangle, September 1 inclusive to October 1 exclusive, fixed EPSG:32639 10 m grid, mean probabilities, minimum 3 observations and confidence 0.60 with 0.50/0.70 sensitivity. The 50% common-window gate remains failed at primary 30.9385%. No general historical-change result is adopted. 2023, SamGeo and other models remain deferred.

Reproduce read-only checks in a scientific environment with numpy/rasterio/pyproj:

```bash
python src/validate_dynamic_world.py --exports data/dynamic_world/raw/2026-10-07 --output results/dynamic-world-table-verification.json
python src/validate_dynamic_world_rasters.py --exports data/dynamic_world/raw/2026-10-07 --manifest metadata/dynamic-world-export-manifest.json --output results/dynamic-world-raster-verification.json
```

Original source identifiers remain unchanged; canonical paths derived from declared dataset/index remain explicitly not independently fetched. The saved future export mask/provenance correction has not generated new server exports. Reading the original exports, complete numeric/raster integrity, reassembly and 18-location/36-view 2026 diagnostics do not establish historical classification accuracy. Paired 2021/2026 review and independent scientific/member acceptance remain pending. No submission or organizer contact is authorized or performed.

The [7 October access record](history/Earth-Engine-Access-2026-10-07.md) is preserved with its then-incomplete transfer status; it is superseded by this checkpoint.
