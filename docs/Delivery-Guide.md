# UrbanHeat Al Khor improvement delivery

Prepared 7 October 2026 for Team Al Zubarah. Review-ready independent improvements; historical comparison remains blocked. Nothing has been submitted or sent to organizers.

## Files

- [Twelve-page PDF](UrbanHeat-AlKhor-Pitch.pdf) and [editable twelve-slide PowerPoint](UrbanHeat-AlKhor-Pitch.pptx): revised presentation examples, corrected responsibilities and truthful historical-access status.
- Full `UrbanHeat-AlKhor-Project.zip`: manifest-listed project, original inputs/tables/notebook, complete app, standalone preview, preparation notes, historical plan/prepared code and current technical evidence.
- [Standalone preview](../preview/UrbanHeat-AlKhor-Preview.html): embeds the complete map resources. No actual site photographs have been received.
- [Three-minute script](Three-Minute-Presentation.md): 383 spoken words with a 180-second rehearsal target; [judge questions](Judge-Questions.md).
- [Earth Engine blocker and setup](Earth-Engine-Access.md), [site evidence and photographs](Site-Evidence-Guide.md), [team status](Team-Review.md), [project checkpoint](../PROJECT_STATE.md).

Final sizes and hashes are recorded in the external `DELIVERY-VERIFICATION.json` and `SHA256SUMS.json`. The ZIP contains `UrbanHeat-AlKhor/SOURCE-COMMIT.txt`. The archive and checksum reports are generated outside the repository to avoid containing themselves.

## Open and demonstrate

Extract the ZIP and open `UrbanHeat-AlKhor/preview/UrbanHeat-AlKhor-Preview.html` with Chrome or Edge. A separately downloaded copy can also be opened directly. Do not open the multi-file app's index.html by itself. See [Preview-Guide.md](Preview-Guide.md) for browser-policy restrictions and a local-server fallback.

The satellite top three remain V04-23, V28-17 and V04-24. For the deck, show V04-23, V28-17 and V18-26 as team-selected use examples. The hospital cell remains available. Review comparison/export includes five sites and ten date/site rows. Every photo gallery currently says Evidence pending. Historical land-change results are not displayed because access/retrieval/validation are blocked.

The exact current app passed 28 real Chromium HTTP groups per desktop/mobile profile; the standalone content passed offline tests. A temporary synthetic gallery fixture tested image embedding/decoding, missing metadata, escaped captions and unsafe-path rejection. It is not site evidence and is excluded from deliverables. Managed Chromium blocks file://, so standalone checks used set_content. ChatGPT's embedded preview, other browsers and physical phones were not verified.

## Scientific and team limits

Original temperature/NDVI/QA/eligibility/rankings, 35 inputs and seven analytical CSV tables are unchanged. New code and imagery are separate presentation/evidence preparation. Dynamic World code was syntax-checked; five synthetic validator tests passed. Earth Engine server execution, actual local scene availability, raster exports and manual historical validation were not performed. This revision does not claim measured land change or overall accuracy. SamGeo and other models are deferred.

Nasser's visit confirmations apply to the original three reviewed sites. The added reports are attributed to Abdulrahman; separate visit confirmation, photos, capture dates/times, route geometry, user counts and detailed shade remain pending. Unknowns are preserved. Mohammed practises the presentation; Abdulrahman reviews the project and collects photos/observations. Neither task is complete without the member's confirmation.

PDF ≤50 MB and optional ZIP ≤200 MB are retained from the supplied checklist; current organizer limits/deadline were not newly verified. Final attachment acceptance and Nasser's separate submission approval remain pending. Do not upload to the form, contact organizers or Submit without authorization.

## Rebuild the package only

The optional packaging tools are PyMuPDF and python-pptx, separate from the pinned analysis environment:

```sh
python src/build_delivery.py --source-commit <verified-published-commit> --output /tmp/UrbanHeat-AlKhor-Delivery
```

The builder checks hashes and archive integrity; it does not analyze data or prove remote publication. Inspect live heads and verify the remote tree separately. Third-party link availability and organizer-form acceptance are not certified by packaging.
