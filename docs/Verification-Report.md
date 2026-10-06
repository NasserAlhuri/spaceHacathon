# Al Khor verification report

Verified 6 October 2026. Public review package; nothing submitted.

## Expanded clean GitHub execution: passed

[Verified run](https://github.com/NasserAlhuri/spaceHacathon/actions/runs/37505530323), source commit `5e7c540afdd9954363f73b9cde588d237291c388`, job 112413109720. GitHub-hosted Linux, Python 3.12.14. The workflow removed `results` and `app/assets` before executing the notebook through an ordinary Jupyter kernel.

- Five code cells executed, zero errors, all 35 packaged input SHA256 hashes verified. Kernel runtime: 7.2 seconds, excluding dependency installation and checkout.
- Numerical checks passed: 104,931 common samples, 373 urban candidates and 115 source checks. The portable map includes 1,111 observed cells.
- All seven original CSV result tables reproduced byte for byte against the preserved SHA256 baseline.
- The separate V04-23 greenery audit, evidence-figure rendering and map-control tests passed in the same workflow.
- Map controls were checked with a Node VM/DOM adapter. Full browser visual and touch-device review remain team tasks.
- Artifact 11431542823 was downloaded. ZIP SHA256: `5e7dfbf69d1661adf339c7ad861020ceaebacecc28dcf16ed8a25b05f5df1f93`. The actual notebook, reports and generated result files were inspected and saved. Notebook cell sources are unchanged; every code cell has an execution count and no error output. All seven artifact CSV files also match the packaged originals.

The source revision includes the improved map, local-review metadata, greenery audit, twelve-slide deck and expanded workflow. Notebook cell sources, original analysis scripts, original input data and the seven original result tables remain unchanged. This test establishes reproducibility; independent scientific accuracy, thermal calibration and intervention benefits remain unvalidated.

`results/expanded-workflow-verification.json` contains current evidence. `results/notebook-verification.json` is the actual report from this run. `results/original-results-comparison.json` records the seven table checks. Earlier run 37269889977 (including attempt 2) remains historical evidence for the original analysis and is superseded for the full improved revision by this expanded run.

## Publication and backups

The approved package was published to `pilot/al-khor` and promoted to `main` by non-force fast-forward. The evidence refresh changes documentation and executed/generated outputs, with no change to tested code, dependencies, input data, ranking or original CSV tables.

- Pearl backup `backup/pearl-2026-10-05` remains `f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343`.
- Al Khor baseline backup `backup/al-khor-tested-2026-10-06` remains `2b46fd0b470ce586b110f117f96f8b9f4c98cfee`.
- Repository visibility is public. Every published file is checked against its local Git blob SHA.

## Remaining review and submission gates

Nasser confirms site visits and unchanged physical conditions relative to September 2026; exact visit dates are unspecified. Detailed shade/use/access and ownership checks, independent scientific validation and other teammates' reviews remain pending. The editable PowerPoint and matching PDF retain the prepared twelve slides.

The organizer message supplied by Nasser confirms that a public repository satisfies technical-team access and names 11 October as the deadline, without an hour or timezone. The team plans to finish before that date. See `Organizer-Access-and-Deadline.md`.

Final PDF/ZIP attachments, truthful platform declarations and final user approval remain required. No hackathon submission, organizer message or external demo deployment was performed. The portable Al Khor map remains the demonstration; the older hosted Pearl demo is not used as Al Khor evidence.

## Evidence reconciliation, 6 October 2026

Live branch heads and the successful expanded run were checked again. The artifact ZIP digest matches GitHub, and all 23 retrieved files match the local package. The 35 original input hashes and seven original result-table hashes pass again. The current checkpoint is PROJECT_STATE.md. Presentation and delivery review are recorded in Delivery-Review.md. A local real-browser attempt could not run because Chromium is unavailable; browser/device and teammate review remain pending.
