# Earth Engine access and historical comparison

## Actual access result — 7 October 2026

The managed environment is running, with current readiness observations. It has no configured Google outbound identity, secret binding or project variable. The Python Earth Engine SDK and standard Earth Engine/Google default credential files are absent. The enforced restricted network policy does not allow `earthengine.googleapis.com`; the inherited-proxy HEAD request failed with `URLError: Operation not permitted`. No authenticated collection query was made. This is an environment setup blocker, not a finding that Google has no Al Khor imagery.

The [official Dynamic World catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1) was accessible through the web research tool. It describes a global 10 m upstream AI land-cover product, nine classes and probabilities, scene cloud/shadow masking, and warnings about bright arid surfaces. The global archive includes the requested years. This establishes dataset documentation, **not local September coverage, confidence or valid change results**. Actual scene counts for September 2021 and 2026 remain null. 2023 is deferred.

## Nasser's setup step

1. Use a Google Cloud project registered for Earth Engine, with its API enabled and the appropriate IAM permissions. Follow [Google's access guide](https://developers.google.com/earth-engine/guides/access). Do not create commitments or choose a use classification on another person's behalf.
2. Bind the authorized Google identity and project through the environment's secure configuration. Allow the Earth Engine API and authentication endpoints required by that binding, including `earthengine.googleapis.com` and, as applicable, `oauth2.googleapis.com` and `sts.googleapis.com`. Keep the configured proxy and TLS verification. Do not send passwords, tokens or service-account JSON in chat.
3. After setup, recheck current environment readiness and actual collection access. Install the Python SDK only in a separate optional environment if using Python; do not modify the original pinned analysis dependencies.

Alternative: use your authorized [Earth Engine Code Editor](https://code.earthengine.google.com/), select the registered Cloud project, and run `src/dynamic_world_earthengine.js`. Share the exported scientific files and provenance rather than credentials. The script is prepared and syntax-checked locally; **its server execution and exports have not been verified**.

## Prespecified comparison protocol

The plan in `metadata/dynamic-world-plan.json` uses the existing study window and an explicit EPSG:32639 10 m grid aligned to the thermal-grid origin. Each year uses September 1 inclusive to October 1 exclusive. The method averages the nine valid scene probabilities, takes their maximum-probability class, requires at least three observations and a composite top probability ≥0.60, and checks thresholds 0.50 and 0.70. These are provisional screening choices, not calibrated accuracy. Missing or rejected pixels remain Unknown.

Exports preserve all nine classes and probabilities, observation counts, confidence, source image IDs, model/QA versions and grid settings. Whole-window coverage and Unknown area are separate from change estimates, which use only the intersection of accepted support in both years. A provisional 50% common-window coverage gate is an initial check, not sufficient approval to publish changes. The export switch is off until actual diagnostics are inspected. The code does not update the original NDVI, WorldCover eligibility, temperature or scores.

No historical map, area estimate or change percentage is displayed in the app yet. A status panel states that retrieval and validation are pending. Prepared comparison code is not an implemented, validated historical result. September is a monthly window, not an annual map or a warming trend.

## Before displaying results

Check actual scene dates/counts and version consistency; inspect cloud/edge/mangrove/arid-surface behaviour. Validate grid/provenance, area totals, Unknown area, class transitions and arithmetic with `src/validate_dynamic_world.py`. Compare spatially separated changed and stable examples against dated source imagery. Fill `metadata/dynamic-world-manual-review.csv` with real observations; historical labels cannot be validated by current photographs alone. Do not repeatedly tune thresholds to the same checks and call them independent validation.

If the 2021/2026 result is suitable, add 2023 using the same method and repeat checks for each pair. Report limited manual-review counts and ambiguity without claiming citywide accuracy. Dynamic World classifications cannot calibrate thermal measurements or establish causal urban warming.
