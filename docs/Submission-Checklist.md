# Submission checklist and handoff

Updated 4 October 2026. This is a review draft. Nothing has been submitted to the organizers.

## Prepared

- Root README covering the required use case, data, method, run instructions, results, limitations, licences and team status.
- Executable analysis notebook with visible outputs, generated from the packaged inputs.
- Pinned direct requirements and full tested environment lock.
- Small sample crops, exact scene metadata, source query, reference snapshot and hashes.
- Results under `results/`, with actual figures embedded in the README.
- Land-cover context, contributed building footprints, 16-cell investigation shortlist and 11 sensitivity settings.
- Reference checks and numerical/data-support tests with their limitations recorded.
- Required PDF pitch and editable PowerPoint, subject to team review.
- Updated optional interactive map. Its audience remains owner-private.

## Must complete before submission

1. Names are confirmed: Nasser Alhuri, Abdulrahman Almohannadi, Mohammed Almarri, Majed Alkuwari and Ali Alkubaisi. Roles have not been assigned. Confirm their actual contributions and full platform registration. The saved 3 October dashboard showed three invitations pending. Current status could not be checked because the sign-in session expired. A pending invitation is not proof of registration.
2. Complete the GitHub Actions notebook check in a separate clean environment, or run `python src/check_notebook.py` on another machine or Colab. The clean Python-cell execution passed here, but a normal kernel could not start under this workspace's networking restrictions. Do not tick the platform's notebook confirmation until the standard check passes.
3. Upload this project to the connected private repository `NasserAlhuri/spaceHacathon` and verify the automated check. Arrange evaluator access before submission. Replace the README's review-draft/member status after confirming it. Open the repository logged out, or grant the specific evaluation account access. The private Site does not satisfy repository access.
4. Review the PDF and approve the final submission. The platform form requires the GitHub URL and attached PDF, and confirms repository content and organizer access. The supporting archive is optional.
5. Verify the current deadline. Archived sources disagree: the Cockpit tooltip displayed 10 October 2026 at 22:59, with timezone unclear; the guide said 11 October at 23:59 in the team creator's local time. The guide gives the official website precedence. Plan to finish before the earlier displayed date while resolving this.

## Scientific work still pending

- Human confirmation of contributed reference samples and useful vegetation-reference coverage.
- Independent temperature validation and assessment of emissivity/mixed-pixel limitations.
- Suitable VHR imagery for current building/paving segmentation if extending toward the full original idea.

These limits are disclosed in the README, notebook and deck. Do not claim calibrated heat-health risk, true cooling benefits, air-temperature measurements, UHI intensity against a rural reference, or long-term change.

## Quick normal-kernel check

After installation and environment activation:

```sh
python src/check_notebook.py
```

A success regenerates outputs, updates the notebook's visible outputs and writes `results/notebook-verification.json`. Commit that executed notebook and result before the deadline.

For Colab, upload the source ZIP, unzip it, install `requirements.txt`, change to the project root and run the command above. Because the pinned package wheels require Python 3.12, check Colab's Python version first. If it differs, use a local Python 3.12 environment rather than changing dependencies without another verification run.

## Team review questions

- Are the shortlist locations sensible places for a planning site visit?
- What is each member's actual contribution?
- Does the team accept the clearly disclosed first-stage scope?
- Which accessible GitHub repository should receive the prepared project?
