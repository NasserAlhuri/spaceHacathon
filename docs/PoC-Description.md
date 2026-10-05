# UrbanHeat AI: implemented PoC

UrbanHeat AI provides an explainable starting point for urban-planning site visits across the Al Khor area, Qatar. The broad analyst-defined window includes surrounding desert and coast and is not an official city boundary.

We combine two quality-screened September 2026 morning Landsat surface-temperature observations, Sentinel-2 green-pixel indicators, contributed OSM building footprints and historical WorldCover land cover. Conservative coastal and wetland exclusions and a common observation footprint support comparison. The map separates temperature, greenery, mapped buildings, relative investigation priority and uncertainty.

The analysis reports 373 screened urban candidate cells with 31.82 km² of retained sample footprint; 1111 observed cells remain inspectable. Thirteen alternative settings show that the leading candidates are sensitive to thresholds and weights. Contributed-reference checks have mixed results and human confirmation is pending. No overall accuracy or thermal calibration is claimed.

This is a first-stage open-data implementation of the submitted idea. WorldCover provides an upstream ML-derived product. We do not run our own VHR segmentation, separate paved surfaces, quantify shade or estimate human heat-health risk, cooling benefits or long-term urban expansion. Those features require additional data and validation.

The package includes hashed source crops, exact metadata, a notebook, pinned dependencies, portable interactive map, results and presentation. Normal separate Jupyter-kernel execution passed on GitHub: five cells, zero errors and 35 input hashes. All five members are signed in and review responsibilities have been assigned. Member reviews, evaluator access and final approval remain pending.
