# UrbanHeat Al Khor delivery bundle

Prepared 7 October 2026 for Team Al Zubarah. This is a review-ready bundle. Nothing has been submitted to the hackathon and no organizer has been contacted.

## Files to use

| File | Purpose |
|---|---|
| [UrbanHeat-AlKhor-Pitch.pdf](UrbanHeat-AlKhor-Pitch.pdf) | Twelve-page presentation; 2,917,430 bytes (2.92 MB). |
| [UrbanHeat-AlKhor-Pitch.pptx](UrbanHeat-AlKhor-Pitch.pptx) | Matching editable twelve-slide presentation; 1,574,000 bytes (1.57 MB). |
| UrbanHeat-AlKhor-Project.zip | Downloadable full project snapshot, including presentations, inputs, notebook, original results, complete app, standalone preview and English preparation notes. |
| [UrbanHeat-AlKhor-Preview.html](../preview/UrbanHeat-AlKhor-Preview.html) | Standalone map with embedded CSS, JavaScript, data and twelve images; 2,218,848 bytes (2.22 MB). |
| [Three-Minute-Presentation.md](Three-Minute-Presentation.md) | Timed English narration for all twelve slides, 377 spoken words; rehearsal still required. |
| [Judge-Questions.md](Judge-Questions.md) | Suggested answers grounded in the actual results and limitations. |
| [PROJECT_STATE.md](../PROJECT_STATE.md) | Continuity checkpoint, pending reviews and submission approval gate. |

The final downloadable delivery folder also includes `DELIVERY-VERIFICATION.json` and `SHA256SUMS.json`. They identify the exact published source commit, archive size, checksums and link-verification limits. `UrbanHeat-AlKhor/SOURCE-COMMIT.txt` inside the ZIP identifies its source commit. The ZIP and its checksum report are generated outside the repository to avoid an archive containing itself or its own checksum.

## Open the map

Extract the project ZIP and open `UrbanHeat-AlKhor/preview/UrbanHeat-AlKhor-Preview.html` with Chrome or Edge. A separate copy is also supplied beside the ZIP. It should immediately show the styled map rather than Loading satellite layers. The map needs no internet; Street View and external source links do. Do not open just the multi-file app's `index.html`. For browser policy restrictions and the local-server fallback, see [Preview-Guide.md](Preview-Guide.md).

The exact standalone content was tested in real Chromium, offline, at desktop 1440 × 900 and simulated mobile 390 × 844. The complete HTTP app passed 24 check groups per profile. Dates, layers, all three sites, comparison, CSV download, zoom/reset and page errors were checked. Managed Chromium blocks `file://`, so the standalone check used Playwright `set_content`. ChatGPT's embedded preview, physical phones, other browsers and member acceptance are not verified.

## What the field evidence means

Nasser confirms site visits; exact visit dates are unspecified. Abdulrahman's attributed reports add qualitative site context. **User counts, use times and detailed shade assessment have not been measured.** The map states this in the overview, each reviewed site's details and the comparison panel. Unknown values and the original local-review JSON remain unchanged. Visits do not verify temperature, ownership, hospital expansion plans or intervention effectiveness.

## Verification and limits

- The PDF pages were rendered and visually reviewed, and matching PowerPoint slide text was checked. Both presentation binaries are unchanged from the published baseline.
- All 35 input hashes and seven original CSV hashes remain unchanged. The existing successful expanded analysis run is retained; no new analysis was run.
- The packaging script checks every file against `PACKAGE-SHA256.json`, tests ZIP integrity and verifies the zipped snapshot against those same hashes. It excludes Git metadata, caches, credentials and unrelated workspace files by using the explicit manifest.
- The supplied checklist limits are PDF ≤50 MB and optional ZIP ≤200 MB; the final verification report records the actual sizes. MB means decimal bytes here.
- GitHub repository and delivery-file references are checked through the public GitHub API against the published tree. Relative documentation links are checked locally. Third-party source/Street View availability, organizer-form attachment acceptance and a live hosted map are not certified by these checks.

## Still pending before submission

Mohammed's assigned map review, Majed's slide/limitations review and Ali's demo rehearsal require their own confirmations. Abdulrahman's detailed boundary/site assessment and ownership/access checks remain pending. Nasser's final approval to submit is a separate gate. Prepared scripts and automated checks do not complete these reviews. See [Team-Review.md](Team-Review.md).

Do not upload to the hackathon form, contact organizers or click Submit until separately authorized by Nasser. GitHub publication permission does not authorize submission.

## Rebuild only the delivery package

The optional packager uses Python with PyMuPDF and python-pptx for presentation checks. These are packaging tools, not changes to the pinned analysis environment. Opening the standalone map needs no Python packages.

After obtaining an exact published checkout and checking the live branch heads:

```sh
python src/build_delivery.py --source-commit <verified-published-commit> --output /tmp/UrbanHeat-AlKhor-Delivery
```

This command packages existing files and checks hashes. It does not fetch or analyze data, execute notebooks, change original CSVs or modify backup branches. It does not prove that the supplied commit was published; remote tree verification is a separate step recorded in the final report.
