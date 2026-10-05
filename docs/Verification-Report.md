# Al Khor verification report

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

All five members showed Signed in on the live platform. Assigned future review responsibilities are documented in README section 9 and Team-Review.md; no prior contribution or completed human review is claimed. The 12-slide deck adds the official theme, problem and affected users, native editable workflow, explicit non-use of hyperspectral/813/VHR imagery, potential impact and incubation next steps. The form title, summary and repository URL are drafted. Organizer-access declaration and Submit remain untouched. Private repository evaluator access still needs an explicit decision. Deadline displays conflict: Cockpit 10 October 2026, 22:59 (timezone unstated), versus guide 11 October, 23:59 creator-local time. Work toward the earlier deadline. Optional hosted application is not a submission prerequisite; use the packaged portable Al Khor map. Nothing has been submitted or sent to organizers.

Al Khor was promoted to main by non-force fast-forward on 5 October 2026. Pearl backup was rechecked at f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343. The final document/slide refresh leaves tested notebook, source code, workflow, dependencies and input data unchanged; the normal-kernel evidence remains the run of source commit 9781b95a46d86eb858ae9714ee53198ad22cfb6c, not a new test of presentation changes.
