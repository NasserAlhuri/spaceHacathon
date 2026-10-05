# Al Khor verification report

Checked 5 October 2026. Review package only. Nothing submitted.

## Completed locally

- Python 3.12.14. Required analysis and notebook packages match the direct version pins in `requirements.txt`.
- All 35 packaged input SHA256 hashes match.
- Deleted generated results and map assets in a fresh test copy, then regenerated them from packaged inputs without fetching new imagery or changing the OSM snapshot.
- `src/verify.py` passed: 104,931 common samples, 373 urban candidates and 115 source checks. The interface contains 1,111 observed context cells.
- All seven regenerated CSV tables match the uploaded baseline byte for byte.
- Executed all five unchanged notebook code cells in IPython in-process. Zero errors. Saved visible outputs in `pilot.ipynb` and an explicitly labelled report in `results/notebook-verification-inprocess.json`.
- Prepared an English ten-slide pitch PDF and editable PowerPoint for Al Khor. Data attribution and scientific limitations are included.

## Ordinary Jupyter-kernel gate remains open

The default kernel failed before cell execution because the workspace denies its local TCP sockets. Jupyter's supported IPC transport also failed with `Operation not permitted`. The in-process check above does **not** constitute a separate ordinary Jupyter-kernel pass. Do not describe it as a GitHub Actions pass.

After upload approval, run the packaged read-only GitHub Actions workflow on `pilot/al-khor`. It removes generated outputs, checks input hashes, executes `src/check_notebook.py`, and retains the executed notebook and results as an artifact. Inspect the run report, then retrieve the executed notebook into the final package.

## GitHub status verified

Repository: https://github.com/NasserAlhuri/spaceHacathon

Visibility: private. The three observed branches currently point to `f9514a479d0d7a9092c32c9e7a2dcbd1ecab6343`:

| Branch | Verified content/status |
| --- | --- |
| `backup/pearl-2026-10-05` | Pearl backup exists, with 79 files in its tree. Unchanged. |
| `main` | Same existing Pearl commit. Unchanged. |
| `pilot/al-khor` | Still the existing Pearl commit. Al Khor upload did not complete. |

Automatic approval review blocked the upload to this repository, requiring explicit authorization for that destination. No remote branch, visibility or backup changes were made. A proposed workflow with write access was rejected and removed. The packaged workflow only requests `contents: read` and cannot push commits.

## Submission gates

- Ordinary separate Jupyter-kernel execution and outputs from that run.
- Evaluator access to the private repository and any demo.
- Actual teammate contributions/roles and completed registrations.
- Human review of boundary, reference labels and shortlisted sites.
- Live deadline confirmation. Prior sources conflict and have not been rechecked here.
- Final user approval before sending the form or contacting organizers.

The hosted map was not changed or verified in this workspace. Use the packaged portable Al Khor map until its live deployment is separately checked.

Reproducibility does not establish independent scientific accuracy.
