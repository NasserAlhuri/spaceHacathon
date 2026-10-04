# UrbanHeat AI: The Pearl planning pilot

Team **Al Zubarah (الزبارة)**, Qatar. Theme: **Urban Expansion, Land Use Change & Heat Risk**. This PoC combines satellite surface temperature, a greenery signal, contributed building footprints and historical land cover to shortlist places for urban-planning investigation in a small part of The Pearl.

**Status:** review draft. Source repository: [NasserAlhuri/spaceHacathon](https://github.com/NasserAlhuri/spaceHacathon). Member contributions, a normal Jupyter run in a separate environment, reviewer access and platform submission remain to be completed. The live optional map is owner-private and cannot substitute for an accessible GitHub repository.

## 1. Business use case

The intended user is an urban planner deciding where to arrange site visits before proposing shade or planting improvements. The pilot provides a small, explainable shortlist with observation coverage and sensitivity. Site visits must confirm pedestrian activity, shade, ownership and feasibility. We have not interviewed an end user or measured time/cost savings. Existing imagery and site inspection remain part of the decision.

## 2. Problem and scope

Building and paved surfaces, sparse vegetation and shade can affect urban thermal conditions. Satellite data provide repeatable spatial context, while field inspection provides local detail. Our analyst-defined window is 51.538–51.556°E, 25.360–25.379°N, around Porto Arabia and nearby areas. It is approximately 3.84 km² including water and is not an official Zone 66 boundary or a study of all Doha.

The original proposal described VHR pretrained AI segmentation of buildings, paving, vegetation and open land. This first-stage PoC uses available open data: contributed building geometry, a precomputed ML-derived land-cover product, optical indices and an existing thermal retrieval. **We do not run our own AI segmentation, separately measure paved area, or claim individual-building thermal detail.** VHR segmentation and additional indicators remain extensions.

## 3. Data

| Dataset | Dates / version | Processing and source | Licence |
|---|---|---|---|
| Copernicus Sentinel-2 L2A | 5, 15, 30 September 2026 | BOA reflectance, 10 m red/NIR/visible and 20 m SWIR/SCL; Element 84 Earth Search | Copernicus Sentinel terms; acknowledge modified data |
| USGS Landsat 8/9 Collection 2 L2 | 6, 14, 30 September 2026 | ST_B10, QA_PIXEL, QA_RADSAT, ST_QA and cloud distance; Microsoft Planetary Computer | Unrestricted USGS use, citation included |
| ESA WorldCover | 2021, v200 | Historical CatBoost-derived 10 m land cover from Sentinel-1/2 and auxiliary inputs; Planetary Computer | CC BY 4.0 |
| OpenStreetMap | Downloaded 4 October 2026, feature edit dates vary | Filtered contributed building, grass, water and coastline geometry; official OSM API | ODbL 1.0 |

Exact scene IDs, unsigned source URLs, dates and scale/offset metadata are in `scene.json`, `landsat-scene.json` and `metadata/`. Source crop hashes are in `data/sample_input/SHA256.json`. Reference provenance is in `metadata/reference-provenance.json`. The OSM excerpt removes contributor identifiers, contact tags and unrelated features. It is not a complete building inventory. Historical WorldCover is context, not evidence of 2026 land cover or change since 2021. No commercial, VHR, 813 or hyperspectral imagery is used.

## 4. Technical approach

1. Align optical crops on a 10 m UTM 39N grid. Honor Earth Search's already-applied BOA offset flag. Use nearest-neighbour SCL and bilinear SWIR resampling. Calculate NDVI and MNDWI.
2. Screen land using SCL 4/5. Combine SCL water, Landsat QA water and the illustrative spectral rule MNDWI >0.20 with NDVI <0.10. Require persistent clear land across all three optical dates.
3. Exclude a 60 m water buffer and the outer 60 m crop halo. The crop-border exclusion prevents treating unseen water beyond the crop as absent.
4. Convert Landsat ST_B10 with `DN × 0.00341802 + 149 − 273.15`. Reject QA bits 0–5, water bit 7, radiometric flags, missing values, ST_QA >2 K, cloud distance <1 km or <90% inland optical support. Thermal detail is approximately 100 m on a delivered 30 m grid. No downscaling is used.
5. Compare the same retained thermal footprints on 14 and 30 September. The 6 September scene fails the combined filters. Its exclusion is a screening choice, not a claim that the source scene is unusable.
6. Rasterise closed OSM building ways onto the optical grid, and reproject historical WorldCover with nearest neighbours. Class 50 combines buildings, roads and structures. OSM relations and unmapped buildings may be missed.
7. Aggregate matched-support cell medians and green-pixel share (`NDVI ≥0.30`) in 300 m cells with at least 25 delivered samples. Report the observed proportion of each cell. Green-pixel share is not subpixel fractional vegetation cover or a shade/tree inventory.
8. Calculate an exploratory score: `100 × (0.50 × heat percentile + 0.30 × inverse green-signal percentile + 0.20 × mapped-building percentile)`. Percentile midranks handle ties. The score compares only this pilot and provides a site-investigation shortlist. It is not calibrated heat-health risk. The historical WorldCover layer is context and does not enter the score.
9. Check contributed-reference points and 11 sensitivity scenarios. Change NDVI thresholds (0.2/0.3/0.4), coastal buffers (30/60/100 m), ST_QA limits (2/2.5/3 K), minimum cell counts (25/50) and weights, including a heat-only baseline.

The pipeline is deterministic. Reference sampling uses seed `20261004`. No model training, GPU, API key or live API is required for the packaged analysis.

## 5. Installation

Requires Python 3.12. After cloning your accessible GitHub repository or extracting this package, change into its root:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

All direct dependencies, including notebook execution and map asset generation, are pinned. `requirements-lock.txt` records the full tested environment. A normal laptop should need no GPU.

## 6. Run

```sh
jupyter lab pilot.ipynb
```

Restart the kernel and run all cells. The notebook regenerates maps, tables, reference checks and map assets from the included crops. It uses paths relative to this repository. A command-line equivalent is:

```sh
python src/export_map.py
python src/verify.py
```

The included inputs run offline. Optional `python src/fetch_sample.py` retrieves the exact satellite crops if missing. Preserve the packaged OSM snapshot for exact reproduction because the live database changes. Results appear under `results/`; map assets under `app/assets/`. Expect roughly a minute on a standard laptop, depending on hardware. See `results/notebook-verification.json` for the actual execution status and runtime rather than assuming notebook validation passed.

## 7. Example input and output

Source examples include `data/sample_input/red.tif`, `data/sample_input/landsat/lwir11.tif`, `data/sample_input/reference/worldcover2021.tif` and `data/sample_input/reference/osm-map.osm`.

![Actual land-cover context and investigation score](results/planning-map.png)

![Actual accepted surface-temperature comparison](results/multidate-temperature.png)

`results/planning-cells.csv` and `.geojson` contain values, ranks, sensitivity ranges and retained cell coverage. `reference-samples.csv` exposes source labels and pending human confirmations. `planning-sensitivity.csv` provides all tested settings. `app/assets/data.json` and PNGs reproduce the optional hosted map's numerical layers. The hosted interface is maintained separately through Sites and is a supplement to the notebook.

## 8. Results, validation and limits

The corrected main comparison retains **1.1502 km²**, **1,278 delivered thermal samples** and **16 reported cells**. Delivered samples are spatially dependent. The top shortlist is V02-05, V04-04 and V04-03. The first stays rank 1 across all 11 scenarios, the second ranges 2–3 and the third 2–6. This stability applies only to the selected data and tested settings; it does not certify true planning priority.

Contributed-reference checks use 100 m sample spacing where feasible. All 30 offshore reference points agree with the water screen. Three sampled interiors of small mapped water features are missed. Of 30 sampled mapped-building interiors, one passes the greenery threshold and 25 overlap historical WorldCover built-up. No OSM grass interior survives the 10 m erosion, so these data do not independently validate vegetation. Reference data are contributed, vary in age and await human confirmation. Positive-only, limited-coverage checks are not overall accuracy estimates. WorldCover uses some OSM auxiliary inputs, so OSM-building agreement is not independent WorldCover validation.

QA and numerical checks verify raw temperature conversion, grid alignment, source exclusions, support/counts and score bounds. A fresh-environment notebook check is documented separately. The GitHub Actions workflow executes the notebook through a normal Jupyter kernel in a clean, separate environment and retains the executed notebook and verification report. Its current outcome must be checked before declaring reproducibility passed; a separate environment is not independent scientific validation.

There is no independent temperature calibration. ST_QA is product-reported per-pixel uncertainty, not a confidence interval for a cell median or proof of accuracy. Historical ASTER emissivity inputs, known Landsat vegetation-adjustment issues, small-target blockiness, water mixing, shadows, reference ages and threshold choices may affect results. Surface temperature is distinct from air temperature and human exposure. We have not estimated UHI intensity against a rural reference, long-term urban expansion, warming trends, population vulnerability, cooling effects or health outcomes. Two September morning observations cannot support those claims.

## 9. Team, licence and attribution

Team: Al Zubarah (الزبارة), Qatar. Members confirmed by the team on 4 October 2026:

- Nasser Alhuri — registered team leader.
- Abdulrahman Almohannadi
- Mohammed Almarri
- Majed Alkuwari
- Ali Alkubaisi

**Roles are not assigned yet, and each member's actual project contribution remains to be confirmed.** The submission guide asks for members and roles. The team can divide the remaining map review, demo testing and presentation work, then document completed contributions. No contribution or role is invented. The code and writing were developed with AI assistance and require team ownership/review.

Original project code: MIT (`LICENSE`). Sentinel, Landsat, WorldCover and OpenStreetMap data retain their own terms. The filtered OSM database and adapted OSM geometry remain ODbL (`DATA-LICENSES.md`). Do not imply that the MIT licence relicenses upstream data.

Sources:

- [USGS surface-temperature method and caveats](https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-temperature)
- [USGS known issues](https://www.usgs.gov/landsat-missions/landsat-collection-2-known-issues)
- [NASA Landsat-9 thermal resolution](https://science.nasa.gov/mission/landsat-9/)
- [Element 84 Earth Search processing](https://github.com/Element84/earth-search/blob/main/README.md)
- [Copernicus Sentinel terms](https://dataspace.copernicus.eu/terms-and-conditions)
- [ESA WorldCover 2021 v200 dataset](https://doi.org/10.5281/zenodo.7254220)
- [WorldCover product manual and CatBoost method](https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/docs/WorldCover_PUM_V2.0.pdf)
- [WorldCover licensing](https://esa-worldcover.org/en/data-access)
- [OpenStreetMap copyright and licence](https://www.openstreetmap.org/copyright)
- [OSM coastline direction convention](https://wiki.openstreetmap.org/wiki/Tag:natural%3Dcoastline)

Contains modified Copernicus Sentinel data (2026). Landsat Collection 2 Level-2 imagery courtesy of the U.S. Geological Survey. EROS Center (2020), Landsat 8–9 OLI/TIRS L2, C2, https://doi.org/10.5066/P9OGBGM6. ESA WorldCover 2021 v200, Zanaga et al. (2022), https://doi.org/10.5281/zenodo.7254220. © OpenStreetMap contributors.
