# UrbanHeat Al Khor reviewed delivery

Revised 8 October 2026 for Team Al Zubarah. The three final content corrections are applied; the twelve-slide design is preserved. Actual Code Editor exports and paired assistant review are complete, but primary coverage fails and independent scientific validation remains pending. Nothing has been submitted or sent to organizers.

## Files

- [Twelve-page PDF](UrbanHeat-AlKhor-Pitch.pdf) and [editable twelve-slide PowerPoint](UrbanHeat-AlKhor-Pitch.pptx): preserved examples/design, explicit external-AI roles, NDVI-reference interpretation and completed assistant versus pending independent review status.
- Full `UrbanHeat-AlKhor-Project.zip`: manifest-listed project, original inputs/tables/notebook, complete app, standalone preview, preparation notes, historical plan/prepared code and current technical evidence.
- [Standalone preview](../preview/UrbanHeat-AlKhor-Preview.html): embeds the complete map resources. Includes all 11 received photographs and one video, with Abdulrahman as photographer and a shared 8 October 2026 13:00–14:00 Qatar (UTC+3) window, confirmed by Nasser, not EXIF; exact individual times Unknown.
- [Three-minute script](Three-Minute-Presentation.md): 388 spoken words with a 180-second rehearsal target; actual Mohammed rehearsal is pending; [judge questions](Judge-Questions.md).
- [Earth Engine execution and runtime limitations](Earth-Engine-Access.md), [site evidence and photographs](Site-Evidence-Guide.md), [team status](Team-Review.md), [project checkpoint](../PROJECT_STATE.md).

Final sizes and hashes are recorded in the external `DELIVERY-VERIFICATION.json` and `SHA256SUMS.json`. The ZIP contains `UrbanHeat-AlKhor/SOURCE-COMMIT.txt`. The archive and checksum reports are generated outside the repository to avoid containing themselves.

## Open and demonstrate

Extract the ZIP and open `UrbanHeat-AlKhor/preview/UrbanHeat-AlKhor-Preview.html` with Chrome or Edge. A separately downloaded copy can also be opened directly. Do not open the multi-file app's index.html by itself. See [Preview-Guide.md](Preview-Guide.md) for browser-policy restrictions and a local-server fallback.

The satellite top three remain V04-23, V28-17 and V04-24. For the deck, show V04-23, V28-17 and V18-26 as team-selected use examples. The hospital cell remains available. Review comparison/export includes five sites and ten date/site rows. V04-23, V28-17 and V18-26 galleries show received media; V04-24 and V24-07 remain Evidence pending. Precise camera positions, bearings and exact per-file times remain Unknown; photographer and shared capture window are confirmed by Nasser. The historical panel displays real experimental coverage and Unknown, while general change results/year maps are withheld because primary coverage fails and scientific validation is pending.

The gallery update is verified in results/site-media-verification-2026-10-08.json, including real Chromium HTTP and offline desktop/mobile checks of all actual photographs and full video playback. The previous 29-group app/preview reports are historical. Capture metadata now records Nasser's shared-window confirmation; no project-review acceptance is inferred. Latest confirmation evidence is results/site-media-capture-verification-2026-10-08.json; original receipt/browser checks are historical. The preserved PDF/PPTX and earlier content corrections are checked in results/final-content-revision-verification.json; the updated 388-word spoken status and capture confirmation are checked in results/site-media-capture-verification-2026-10-08.json and [Final-Content-Revision.md](Final-Content-Revision.md). A temporary synthetic gallery fixture tested image embedding/decoding, missing metadata, escaped captions and unsafe-path rejection. It is not site evidence and is excluded from deliverables. Managed Chromium blocks file://, so standalone checks used set_content. ChatGPT's embedded preview, other browsers and physical phones were not verified.

## Scientific and team limits

Original temperature/NDVI/QA/eligibility/rankings, 35 inputs and seven analytical CSV tables are unchanged. New code and imagery are separate presentation/evidence preparation. Nasser executed/exported Dynamic World in Code Editor. All eight exact original exports are included; verified reassembly, real CSV integrity and complete actual TIFF checks passed. Ten table and four raster regression tests passed. Two unique 2021 reference TIFFs and their provenance are now included and verified; the exact duplicate was ignored. All 18 targets/72 dated 2021/2026 views were reviewed by the assistant: eight clear broad patterns, ten exact-class ambiguities and three overlapping potential disagreement flags. Independent scientific review remains pending. See Dynamic-World-Paired-Reference-Review.md. See Dynamic-World-Reassembly-and-Scientific-Review.md. See Dynamic-World-Assessment.md. This revision does not claim measured land change or overall accuracy. SamGeo and other models are deferred.

Nasser's visit confirmations apply to the original three reviewed sites. The added reports are attributed to Abdulrahman. Nasser now confirms his 8 October visit and media capture at V18-26 (and the other two photographed sites) within the shared 13:00–14:00 Qatar (UTC+3) window, not EXIF. Exact individual times, route geometry, user counts and detailed shade remain unknown or pending; V24-07 visit confirmation remains pending. Media are received for the jogging route; the unused-land and hospital-land galleries still lack media. Unknowns are preserved. Mohammed practises the presentation; Abdulrahman reviews the project and collects photos/observations. Collection of this supplied batch is complete by Nasser confirmation; project review and presentation practice are separate and remain pending.

PDF ≤50 MB and optional ZIP ≤200 MB are retained from the supplied checklist; current organizer limits/deadline were not newly verified. Final attachment acceptance and Nasser's separate submission approval remain pending. Do not upload to the form, contact organizers or Submit without authorization.

## Rebuild the package only

The optional packaging tools are PyMuPDF and python-pptx, separate from the pinned analysis environment:

```sh
python src/build_delivery.py --source-commit <verified-published-commit> --output /tmp/UrbanHeat-AlKhor-Delivery
```

The builder checks hashes and archive integrity; it does not analyze data or prove remote publication. Inspect live heads and verify the remote tree separately. Third-party link availability and organizer-form acceptance are not certified by packaging.
