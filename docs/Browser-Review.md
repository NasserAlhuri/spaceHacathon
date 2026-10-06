# Real-browser technical review — 6 October 2026

Status: passed after the readability fixes below. This is a technical browser check; it does not complete any teammate review or authorize hackathon submission.

## Method and coverage

The project checkpoint was read first. The tested baseline was public commit `61a3c9ec44434d8f50e6089940a44601b3f4b16e`; the current UI adds the repairs below. Real headless Chromium **151.0.7922.173** was launched with Playwright **1.62.0** against a localhost-only HTTP server. No synthetic DOM adapter was substituted for this browser test. The sandbox initially denied local socket creation; an approved execution allowed the local server and browser to run. No browser installation was needed.

| Check | Desktop, 1440 × 900 | Mobile emulation, 390 × 844 |
| --- | --- | --- |
| Two dates × five layers; image decode and active state | Passed | Passed |
| V04-23, V28-17 and V04-24 via selector and shortlist; values for both dates | Passed | Passed |
| Actual map selection at each site | Mouse clicks passed | Touch taps passed |
| Comparison: three rows, date updates, horizontal scroll, open/close | Passed | Passed |
| Actual CSV download: three sites × two dates, six rows, original values and optical dates | Passed | Passed |
| Zoom in/out, selected-cell focus, reset | Passed | Passed |
| Panning | Mouse drag passed | Emulated touch drag passed |
| Layer opacity, 0% to 100% | Passed | Passed |
| Readability, metric-card fit and page-width checks | Passed at 1440 and 1024 px | Passed at 390 and 320 px |
| JavaScript exceptions, console errors, failed requests, HTTP errors | Zero | Zero |

Each profile passed **24 groups of checks**. All original satellite values were checked against the existing `app/assets/data.json`; no analysis was run. The existing Node DOM-adapter test also passed after the UI changes.

## Defects found and repaired

1. At the original full extent, SVG labels were approximately 6.5 screen pixels on a 390 px phone and 5.2 px on a 320 px screen. Zooming enlarged the labels until text was clipped. Labels now remain approximately 13 screen pixels, use cell IDs in compact map frames and retain complete site names in the shortlist and inspection panel. Labels of visible cells are kept within the map extent and labels of out-of-view cells are hidden. Real-browser regression assertions check readable label sizes at full extent and readable, unclipped labels after focusing the selected cell.
2. The desktop map card stretched to match the much taller sidebar, creating a large empty white area, especially after inspecting a site. The map card now aligns to the start of its grid row. Mobile stacking is preserved.

The pre-repair browser record is [before.json](../results/browser-review/before.json). Both profiles failed the label-readability check before repair, with the other 23 groups passing. The completed browser record, source-file hashes and limitations are in [browser-review.json](../results/browser-review.json).

## Evidence

- [Desktop rendering](../results/browser-review/desktop.png)
- [Mobile rendering](../results/browser-review/mobile.png)
- [Mobile selected-site focus](../results/browser-review/mobile-focused.png)
- [Mobile comparison](../results/browser-review/mobile-comparison.png)

The actual CSV downloads remain in the local test-output directories. Their checksums are in the machine-readable report; they are identical between desktop and mobile. They are generated review exports, not replacements for any of the seven original result tables.

## Limits and pending human work

This checks one headless Chromium version and a touch-emulated viewport. It is not a physical Android/iPhone test, Safari/Firefox coverage, a screen-reader audit or a teammate's confirmation. Zoom buttons and touch drag were tested; two-finger pinch was not tested. The compact comparison table intentionally requires sideways scrolling. External Street View/source links, a hosted deployment and platform submission were not tested.

Mohammed's map review, Majed's slide/limitations review, Ali's demonstration rehearsal and the other assigned human checks remain pending until those members confirm them. Scientific, shade/use/access and ownership validation remain pending. All 35 input hashes and all seven original CSV table hashes were checked unchanged. Both backup branches remain at their recorded heads. Nothing was submitted to the hackathon.

## Reproduce without rerunning analysis

Use an existing Playwright installation and Chromium executable; they are optional UI-test tools and do not change the scientific requirements files. Serve only the supplied static assets through the test's local HTTP server:

```sh
python src/test_map_browser.py --chromium /usr/bin/chromium --output /tmp/urbanheat-browser-review
```

The runner writes screenshots, downloaded review CSVs and its JSON report only to the requested output directory. A restricted execution sandbox may require permission for localhost sockets and Chromium launch. A failed launch or failed check must be reported as failed, not a browser pass.
