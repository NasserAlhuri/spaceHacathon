# Site observations and photographs

On 8 October 2026, Nasser supplied eleven photographs and one video. The original files are in `app/assets/site-photos/`; the original uploaded ZIP is retained separately without duplication. All filenames have an exact existing site ID, so no mapping question or guessed location was needed. V04-23 has five photographs, V28-17 four, and V18-26 two photographs plus a video. V04-24 and V24-07 remain **Evidence pending**. See [individual observations and limits](Site-Media-Receipt-2026-10-08.md) and `metadata/site-media-receipt-2026-10-08.json` for original filenames, bytes, hashes and archive CRCs.

The gallery displays every received file and embeds the same bytes in the standalone preview. Native video controls, inline mobile playback and original-file download are supported. Site association comes from the filename; it does not locate the camera within the 300 m cell. **Capture date/time, photographer, precise camera coordinates and viewing bearing are Unknown.** No EXIF was supplied for the photographs, and no capture timestamp was present in the video. ZIP timestamps and receipt date are not capture dates. Captions describe visible content and are attributed to Codex visual inspection; original local observations remain attributed to Abdulrahman.

Images show views at unspecified times, not measured user counts, use times, all-day shade or historical land-change truth. Some tree shadows are visible in stadium-path views, while the bus-stop views show trees and a sign without a visible shelter. Do not generalize these snapshots to whole-cell shade or site use. The route video shows sandy ground and vegetation; species and mangrove boundaries remain unverified. Existing Street View stays an external March 2023 reference.

Use `photos` and `videos` arrays in `app/local-review.json`; each entry records `src`, `original_filename`, factual `caption`, `observer`, `captured_at`, `location`, `viewing_direction`, `site_association`, `association_basis`, receipt date and SHA256. Missing capture fields are `Unknown`. Permitted flat local filenames under `assets/site-photos/` are JPEG/PNG/WebP for photos and MP4/WebM for videos. Text is escaped and unsafe paths rejected. Software fixtures are created only in temporary copies and never delivered as evidence.

Abdulrahman's project review, remaining photo collection and capture metadata remain pending until individually confirmed. Media receipt does not complete member reviews or independently confirm a visit to an added site.

## New attributed reports

- V18-26: Abdulrahman identifies a jogging route, services across the road, sand and mangroves on the reported right side, and no path shade from nearby mangroves. Two photographs and one video are received; confirmed capture dates/times, viewing bearing, the full route and business coordinates remain pending. User counts/use times and all-day shade are not measured.
- V24-07: Abdulrahman reports unused land next to a bus hub, with no pedestrians in the supplied observation. Its time is unspecified; do not infer absence of use at other times. Satellite rank remains 4/373, with scenario range 2–76.

The jogging reference point (25.681077, 51.524704) is geometrically inside V18-26 and retained in the existing mask. The supplied shortened map link could not be independently resolved. The 2021 WorldCover label at that point is built; no historical mangrove-labelled pixel is inside the cell under the native-cell inspection. The nearest packaged historical mangrove pixel is about 191 m from the supplied point and outside reported cell geometry. Historical labels are not current ground evidence. These checks do not locate all current trees or establish why detected greenery is low. Route, businesses, sand and current mangrove geometry need dated evidence.

## Selection and preservation

The satellite top three remain V04-23, V28-17 and V04-24. The presentation uses V04-23, V28-17 and V18-26 to illustrate different uses; it does not claim these are the three highest-ranked sites. Hospital land remains available in the map, review and complete results. The map review adds the two reports without replacing the original three records or re-ranking any cells. Original site-visit confirmations apply to the original three; they are not extended to new locations without confirmation.

The review CSV now has ten rows: five sites × two dates. It adds visit/photo/geometry statuses and unknowns while retaining the satellite values. This is a review export; the seven original analytical CSV tables are untouched.
