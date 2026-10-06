# Local-review improvements, 6 October 2026

## Completed

- Preserved the 108-file baseline before edits; Pearl backup is separate and must remain unchanged. Clean rebuilds found incomplete local TIFF copies (5 and 15 September green, and 30 September SWIR). Restored them from the intact earlier test copy, verified against the unchanged 35-input hash manifest and GitHub blob hashes. This restores the tested data; it does not introduce new imagery or change the analysis.
- Added Abdulrahman's supplied local observations for the bus-stop road, stadium parking and hospital-associated empty land. Nasser subsequently confirms visiting the sites and that the described physical situation is the same as in September 2026. Exact observation and visit dates were not supplied; the recording date is not a visit date.
- Located the March 2023 Street View camera inside V04-23, about 84 m from the cell centre. Its coordinate is not the bus-stop sign coordinate.
- Added an independently runnable pixel audit that reproduces the baseline 0% green shares on matched support. Lower-threshold diagnostics are explanatory; the tested threshold and ranking are unchanged.
- Added named map examples, selected-cell local evidence, date/source distinctions, study-boundary outline, three-location comparison, focus control and downloadable review CSV. All observed cells remain accessible.
- Added review figures from packaged satellite assets and two accepted thermal maps, with an explicit rejected-date explanation.
- Updated the twelve-slide deck, PoC description, README, submission summary, source resources and team-review record.

## Verification

Local verification completed: clean regeneration passed; all seven original CSV tables match byte for byte; numerical checks passed (104,931 common samples, 373 candidates, 115 source checks); the separate greenery audit and map-control tests passed. All 35 input hashes match. All 12 slide renders were inspected, the editable table and workflow are retained, and the PDF matches the rendered deck. Full browser/touch-device review remains a team task; the control tests use a DOM adapter. The ordinary five-cell notebook was previously verified on GitHub; its source, original analysis scripts and inputs are unchanged. This revision does not claim a newly calibrated scientific model.

## Unresolved

Detailed follow-up site assessment; exact bus-stop sign coordinates; passenger use/times; shade through the day; route safety; ownership and hospital expansion plans; independent thermal/vegetation validation; other team reviews; final submission attachments and approval. Deadline displays still conflict; no current authenticated deadline confirmation was performed in this revision. Use the earlier recorded cutoff until resolved.

## Future work

A third suitable thermal date, comparable imagery from different years, validated segmentation, shade/paving indicators and reliable human-use data. None is represented as implemented. No new heatwave feature, human-use score or measured cooling/health benefit is claimed. No external demo was deployed and nothing was submitted.

## Fresh notebook verification, 6 October 2026

[GitHub run attempt 2](https://github.com/NasserAlhuri/spaceHacathon/actions/runs/37269889977/attempts/2) passed on Python 3.12.14: five code cells, zero errors, 35 input hashes verified and 4.3 seconds of kernel runtime. Generated outputs were removed before execution. Artifact 11428558809 was downloaded and its ZIP SHA256 verified (`cca350ef0a16d570ac9390b75484dac0f70d3768de77131a44959fe39e4f6ec4`). All seven regenerated CSV tables match the preserved baseline byte for byte. Notebook cell sources are unchanged; the packaged notebook and notebook report now contain the actual fresh artifact outputs.

This reran source commit `9781b95a46d86eb858ae9714ee53198ad22cfb6c`. Its original analysis scripts, inputs, metadata and dependencies match current main and this package. The improved local-review interface and added audit/figure scripts were outside that earlier workflow. The supplied audit/figure evidence is retained; the current map-control checks were independently rerun successfully using the Node DOM adapter. Full browser/device and scientific validation remain separate.

The package adds `metadata/original-results-sha256.json`, `src/verify_reproduction.py` and a workflow step to check the seven tables on future clean runs. This expanded workflow is prepared locally and has not yet run on GitHub.

Full GitHub publication is pending: automatic approval review rejected `app/local-review.json` because the public upload includes precise site coordinates and local observations attributed to named individuals. No branch was updated. Current main and pilot remain `2b46fd0b470ce586b110f117f96f8b9f4c98cfee`; Pearl backup remains `f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343`. Some Git blobs were prepared before publication stopped; the package is not present on main. Explicit approval of the complete public payload is needed to finish publishing it. Nothing has been submitted to the hackathon; final submission approval remains required.

Machine-readable fresh evidence: `results/fresh-run-evidence.json`. Table comparison: `results/original-results-comparison.json`.

## Publication consent, 6 October 2026

Nasser explicitly approved public publication of the complete reviewed package, including coordinates, local observations, visit confirmation, named attribution, team responsibilities, documentation, figures and the deck. Publication and expanded verification are in progress. Final hackathon submission approval remains outstanding.
