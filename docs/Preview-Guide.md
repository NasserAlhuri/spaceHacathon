# Open the complete UrbanHeat map preview

## Why the original single-file preview stayed at Loading

Nasser confirmed that Web preview opened `Index.html`. The original `app/index.html` depends on sibling `style.css`, `app.js`, `local-review.json` and `assets/`. Opening or transporting only the HTML does not carry those files with it. Missing CSS produces an unstyled page; missing JavaScript leaves the initial Loading satellite layers text. The ChatGPT preview's actual requests were not available to inspect, so this is a resource-path diagnosis from the reported symptoms, not a claim that its network log was inspected.

The previous test server was local to the cloud environment and temporary. Its localhost URL is not a public preview URL and does not point to the cloud app from Nasser's own browser. Do not use that URL as evidence of a working ChatGPT preview.

## Recommended: the standalone file

1. Download the updated `UrbanHeat-AlKhor-Project.zip` delivery package, or the standalone `UrbanHeat-AlKhor-Preview.html` supplied in the chat.
2. Extract the ZIP. Use Open with → Chrome or Edge on `UrbanHeat-AlKhor/preview/UrbanHeat-AlKhor-Preview.html`, or on the separately downloaded standalone HTML.
3. The formatted map should show 30 September 2026, the Priorities layer, and 1,111 observed cells. Switch dates/layers, select sites, compare them or download the ten-row location review CSV.

The same standalone HTML is kept in `preview/UrbanHeat-AlKhor-Preview.html`. It embeds CSS, JavaScript, the existing satellite/local-review JSON and 23 images (the twelve original satellite/map images plus eleven actual site photographs) and one actual site video. It uses the same existing values and UI, with only preview resource delivery changed. External source/Street View links still need internet. The map itself needs no external requests.

If an enterprise browser blocks local HTML files, serve the downloaded file's folder on your own computer with `python -m http.server 8000 --bind 127.0.0.1`, then open `http://localhost:8000/UrbanHeat-AlKhor-Preview.html` on that same computer. This is a local fallback, not a cloud preview or deployment.

## Original multi-file app

From the project root on your own computer:

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory app
```

Open `http://localhost:8000/` on that computer. Serve the entire app directory, including its assets, rather than opening or sending `index.html` alone. Cloud services need a supported forwarding URL; no such user-facing endpoint was verified in this session.

## Packaging and technical checks

```sh
python src/build_preview.py --output /tmp/UrbanHeat-AlKhor-Preview.html
python src/test_preview.py /tmp/UrbanHeat-AlKhor-Preview.html --output /tmp/urbanheat-preview-check
```

The builder reads existing app files only. It does not invoke notebooks, fetch data, recompute figures or modify original results. It fails if source resource markers have changed instead of producing an incomplete package.

The latest gallery revision is checked in real Chromium 151 on desktop 1440 × 900 and mobile emulation 390 × 844, through local HTTP and with the standalone content offline. All 23 embedded images decode and the received video plays to the end with its portrait rotation. Both dates/five layers, five sites, comparison, ten-row CSV, zoom/pan/reset, narrow layouts and receipt/Unknown metadata are checked. Current evidence is results/site-media-verification-2026-10-08.json. Prior browser reports remain historical; no synthetic fixture is included as evidence.

Packaging exposed a separate initial-layout defect: when the preview's map rectangle initially had zero size, label calculations wrote Infinity SVG coordinates. `updateView` now skips zero-size layout and initialization schedules another layout update on the next animation frame. Source data, analysis, seven original CSV tables and backup branches are preserved.

Limits: managed Chromium blocks `file://` navigation, so the generated content was tested using Playwright's supported `set_content` API in offline mode. No claim is made that the ChatGPT Web preview UI itself, browser forwarding, a physical phone or another browser was tested. Members' own reviews remain pending. Nothing was submitted to the hackathon. See `results/preview-verification.json` for the checks and exact package/source hashes.
