# Site observations and photographs

The existing local-review panel now supports photographs and structured evidence status. No photographs were received for this revision; every gallery correctly shows **Evidence pending**. No stock image, invented capture date or inferred user count is used.

Abdulrahman reviews the project and collects photos/observations. For each supplied photograph, record the file, observer, capture date/time, exact location or route segment, viewing direction and a factual caption. Mark missing fields Unknown. Record the source/permission for public use and remove unnecessary identifiable faces or plates before publishing. Do not redistribute Street View imagery without applicable permission; existing Street View remains a dated external reference.

Add actual permitted image files under `app/assets/site-photos/`, and entries to the corresponding `photos` array in `app/local-review.json`:

```json
{
  "src": "assets/site-photos/<actual-filename>.jpg",
  "observer": "<confirmed observer or null>",
  "captured_at": "<actual date/time with timezone or null>",
  "location": "<confirmed coordinates/route segment or null>",
  "caption": "<what this particular image shows or null>"
}
```

This is a schema example, not a received photograph. Never insert a placeholder entry into the gallery. The renderer permits only local site-photo paths, escapes text and displays Unknown for missing metadata. The preview builder embeds these assets when actually supplied. The integration test uses a labelled synthetic fixture outside the project to test the renderer; it is never packaged as site evidence.

## New attributed reports

- V18-26: Abdulrahman identifies a jogging route, services across the road, sand and mangroves on the reported right side, and no path shade from nearby mangroves. Dated evidence, viewing direction, the full route and business coordinates are pending. User counts/use times and all-day shade are not measured.
- V24-07: Abdulrahman reports unused land next to a bus hub, with no pedestrians in the supplied observation. Its time is unspecified; do not infer absence of use at other times. Satellite rank remains 4/373, with scenario range 2–76.

The jogging reference point (25.681077, 51.524704) is geometrically inside V18-26 and retained in the existing mask. The supplied shortened map link could not be independently resolved. The 2021 WorldCover label at that point is built; no historical mangrove-labelled pixel is inside the cell under the native-cell inspection. The nearest packaged historical mangrove pixel is about 191 m from the supplied point and outside reported cell geometry. Historical labels are not current ground evidence. These checks do not locate all current trees or establish why detected greenery is low. Route, businesses, sand and current mangrove geometry need dated evidence.

## Selection and preservation

The satellite top three remain V04-23, V28-17 and V04-24. The presentation uses V04-23, V28-17 and V18-26 to illustrate different uses; it does not claim these are the three highest-ranked sites. Hospital land remains available in the map, review and complete results. The map review adds the two reports without replacing the original three records or re-ranking any cells. Original site-visit confirmations apply to the original three; they are not extended to new locations without confirmation.

The review CSV now has ten rows: five sites × two dates. It adds visit/photo/geometry statuses and unknowns while retaining the satellite values. This is a review export; the seven original analytical CSV tables are untouched.
