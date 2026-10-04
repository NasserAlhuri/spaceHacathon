# UrbanHeat AI: implemented PoC scope

UrbanHeat AI helps an urban planner identify places that deserve a closer site inspection before proposing heat-mitigation work. Our first pilot covers a small part of The Pearl, Qatar.

We combine two accepted September 2026 morning Landsat surface-temperature observations with Sentinel-2 green-pixel indicators, contributed building footprints from OpenStreetMap, and historical ESA WorldCover land cover. The workflow excludes coastal and uncertain observations, compares the same retained footprints, and produces an explainable planning shortlist with observation coverage and sensitivity to alternative settings.

The corrected comparison retains 1.15 km² and reports 16 cells. The leading candidate remains first across all eleven tested settings. We use limited contributed-reference checks and publish their failures as well as agreements. These checks do not establish overall land-cover accuracy or thermal calibration.

This is a first-stage open-data implementation of the submitted idea. ESA WorldCover provides a precomputed machine-learning-derived product. Our PoC does not run its own VHR AI segmentation, separate buildings from paved surfaces automatically, or estimate air temperature, human heat-health risk or intervention cooling benefits. Suitable VHR segmentation, shade/paving indicators, independent validation and broader temporal coverage are planned extensions.

The repository includes source crops, exact metadata, a notebook, pinned dependencies, example figures and tables. The interactive map is a supplementary demonstration. Normal Jupyter execution on another machine and final team/repository details must be confirmed before submission.
