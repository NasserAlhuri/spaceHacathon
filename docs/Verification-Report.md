# Al Khor verification report

## Fresh notebook verification, 6 October 2026

[GitHub run attempt 2](https://github.com/NasserAlhuri/spaceHacathon/actions/runs/37269889977/attempts/2) passed on Python 3.12.14: five code cells, zero errors, 35 input hashes verified and 4.3 seconds of kernel runtime. Generated outputs were removed before execution. Artifact 11428558809 was downloaded and its ZIP SHA256 verified (`cca350ef0a16d570ac9390b75484dac0f70d3768de77131a44959fe39e4f6ec4`). All seven regenerated CSV tables match the preserved baseline byte for byte. Notebook cell sources are unchanged; the packaged notebook and notebook report now contain the actual fresh artifact outputs.

This reran source commit `9781b95a46d86eb858ae9714ee53198ad22cfb6c`. Its original analysis scripts, inputs, metadata and dependencies match current main and this package. The improved local-review interface and added audit/figure scripts were outside that earlier workflow. The supplied audit/figure evidence is retained; the current map-control checks were independently rerun successfully using the Node DOM adapter. Full browser/device and scientific validation remain separate.

The package adds `metadata/original-results-sha256.json`, `src/verify_reproduction.py` and a workflow step to check the seven tables on future clean runs. This expanded workflow is prepared locally and has not yet run on GitHub.

Full GitHub publication is pending: automatic approval review rejected `app/local-review.json` because the public upload includes precise site coordinates and local observations attributed to named individuals. No branch was updated. Current main and pilot remain `2b46fd0b470ce586b110f117f96f8b9f4c98cfee`; Pearl backup remains `f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343`. Some Git blobs were prepared before publication stopped; the package is not present on main. Explicit approval of the complete public payload is needed to finish publishing it. Nothing has been submitted to the hackathon; final submission approval remains required.

Machine-readable fresh evidence: `results/fresh-run-evidence.json`. Table comparison: `results/original-results-comparison.json`.

## Historical verification record


Verified 5 October 2026. Review package only. Nothing submitted.

## Ordinary Jupyter-kernel execution: passed

Run: https://github.com/NasserAlhuri/spaceHacathon/actions/runs/37269889977

Tested source commit: `9781b95a46d86eb858ae9714ee53198ad22cfb6c` on private branch `pilot/al-khor`.

- GitHub-hosted Linux runner, Python 3.12.14.
- Five code cells executed through an ordinary Jupyter kernel, zero errors.
- All 35 packaged input SHA256 hashes verified.
- Kernel runtime: 4.7 seconds. This excludes dependency installation and checkout.
- Workflow removed `results` and `app/assets` before notebook execution, requiring regeneration from packaged inputs.
- Workflow had `contents: read`. It did not push commits or change repository visibility.
- Retrieved artifact `verified-notebook`, ID 11328001190, ZIP SHA256 `fe209d0ba54780e03fe2eb515044542ae375eecf4d97919c82b2af6c6417e5e7`.
- Inspected the report and notebook: all five cells have execution counts, no error outputs, and the cell sources match the uploaded source exactly.
- All seven GitHub-regenerated CSV tables match the packaged baseline byte for byte.
- Replaced the packaged notebook and result files with the actual GitHub artifact outputs.

The machine-readable report is `results/notebook-verification.json`. The earlier in-process fallback record remains for provenance and is superseded by this ordinary-kernel pass.

## Other completed checks

- Initial upload: 105 files, zero remote Git-blob hash mismatches.
- Clean local regeneration and `src/verify.py` passed: 104,931 common samples, 373 urban candidates and 115 source checks. Interface has 1,111 observed context cells.
- English ten-slide Al Khor pitch PDF and editable PowerPoint include data attribution, scope limitations and the completed kernel test.
- ZIP contents and per-file SHA256 manifest checked. Pitch PDF is below 50 MB; optional ZIP is below 200 MB.

## GitHub and backup

Repository: https://github.com/NasserAlhuri/spaceHacathon

The user explicitly approved uploading to the private Al Khor branch and running the read-only test. That upload and test completed. Notebook outputs and verification documents are saved to that same branch in a follow-up evidence commit. The test evidence points to the exact source commit above. Analysis source and inputs are unchanged in the evidence update.

| Branch | Status |
| --- | --- |
| `pilot/al-khor` | Al Khor package, ordinary-kernel verification and executed outputs. |
| `backup/pearl-2026-10-05` | Pearl backup retained at `f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343`, unchanged. |
| `main` | Same existing Pearl commit, unchanged. |

Repository remains private. No backup, default-branch or visibility change was made.

## Remaining submission gates

- Evaluator access to the private repository and any demo.
- Actual teammate roles/contributions and completed registrations.
- Human review of boundary, reference labels and shortlisted sites.
- Live deadline confirmation. Prior sources conflict and were not rechecked here.
- Verify the hosted map shows Al Khor and arrange access. This task did not change the live deployment.
- Final user approval before submitting the platform form or contacting organizers.

Use the packaged portable Al Khor map until the hosted deployment is separately verified. Reproducibility does not establish independent scientific accuracy, thermal calibration or intervention benefit.


## Review preparation update, 5 October 2026

All five members showed Signed in on the live platform. Assigned review responsibilities are documented in README section 9 and Team-Review.md. Abdulrahman supplied local observations for three cells on this revision; Nasser confirms site visits and unchanged physical conditions relative to September 2026, with exact visit dates unspecified; detailed assessment and other reviews remain pending. The 12-slide deck adds the official theme, problem and affected users, native editable workflow, explicit non-use of hyperspectral/813/VHR imagery, potential impact and incubation next steps. The form title, summary and repository URL are drafted. Organizer-access declaration and Submit remain untouched. Historical access note: repository was private at that check; visibility is now public, verified 6 October 2026. Deadline displays conflict: Cockpit 10 October 2026, 22:59 (timezone unstated), versus guide 11 October, 23:59 creator-local time. Work toward the earlier deadline. Optional hosted application is not a submission prerequisite; use the packaged portable Al Khor map. Nothing has been submitted or sent to organizers.

Al Khor was promoted to main by non-force fast-forward on 5 October 2026. Pearl backup was rechecked at f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343. The final document/slide refresh leaves tested notebook, source code, workflow, dependencies and input data unchanged; the normal-kernel evidence remains the run of source commit 9781b95a46d86eb858ae9714ee53198ad22cfb6c, not a new test of presentation changes.

Team wording corrected on 5 October 2026 to Nasser’s selected responsibilities: Nasser coordinates and submits; Abdulrahman checks Al Khor locations against local knowledge; Mohammed tests the map and documents issues; Majed reviews slides and explains limitations; Ali demonstrates the project and prepares judge questions. Member checks remain pending. Dataset credits, licences, scientific limitations and the final-approval gate are retained.


## Local-review revision, 6 October 2026

This revision adds observations, an interface and separate audit/figure scripts. Original analysis scripts, pilot notebook and 35 input files remain unchanged. The existing normal-kernel notebook evidence remains applicable to that unchanged analysis; it does not validate human-use observations. Original seven CSV result tables remain unchanged. The separate V04-23 audit reproduces the original green-share values on matched support and locates the March 2023 Street View camera inside the cell. Nasser confirms site visits and unchanged physical conditions relative to September 2026; exact visit dates were not supplied. No pedestrian measurement, thermal calibration or intervention validation was added. See Improvement-Change-Log.md for revision checks and outstanding work.

## Publication consent, 6 October 2026

Nasser explicitly approved public publication of the complete reviewed package, including coordinates, local observations, visit confirmation, named attribution, team responsibilities, documentation, figures and the deck. Publication and expanded verification are in progress. Final hackathon submission approval remains outstanding.
