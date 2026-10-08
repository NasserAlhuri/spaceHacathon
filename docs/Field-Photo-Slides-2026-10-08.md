# Field photographs in the existing twelve-slide presentation

Updated 8 October 2026. Presentation preparation only; no analytical rerun or hackathon submission.

## Photographs and visible provenance

Slide 6 now shows one clear, individually inspected, original photograph for each presentation example. Images are editable native PowerPoint pictures and embedded JPEGs in the PDF. All three keep their full frames and original aspect ratios; the original image bytes are not edited or given injected EXIF.

| Example | Original received file | What the supplied frame shows |
| --- | --- | --- |
| V04-23 — bus-stop road | app/assets/site-photos/V04-23-01.jpeg | Roadside trees, a stop sign and sidewalk; no shelter visible in this frame. |
| V28-17 — stadium parking | app/assets/site-photos/V28-17-04.jpeg | Stadium and parking view beyond the sandy foreground; use is unmeasured. |
| V18-26 — jogging route | app/assets/site-photos/V18-26-02.jpeg | A marked paved path beside a road and sandy ground. |

The visible common caption states **8 October 2026, 13:00–14:00 Qatar (UTC+3), shared capture window**. Photographer: **Abdulrahman Almohannadi**. The source is **Nasser's explicit user confirmation, not EXIF**. The caption applies to all three photographs. **Exact per-file time remains Unknown**; no minute is assigned to an individual frame. Precise camera coordinates and compass viewing bearing also remain Unknown. Source confirmation is metadata/site-media-capture-confirmation-2026-10-08.json.

These are descriptive views, not measurements of user counts, use times, detailed/all-day shade, route geometry, plant species or historical land-cover accuracy. Abdulrahman's attributed local reports remain separate from descriptive photo observations. The completed supplied eleven-photo/one-video collection does not complete his project review.

## Preserved design and results

Both formats retain **12 slides/pages**, the same order, slide dimensions, background, title/body/footer colours, and existing theme. Slide 6 retains its original title and ranking disclaimer and replaces its displayed context figure with three photographs. The original context figure and original deck/PDF are preserved at the previous public commit `9fa71a86c9d44b4303c36eac9c1fc2f4b91e7596`; the original figure bytes also remain in the PPTX archive. Full context-map assets and numerical results remain in the project.

The table on slide 8 is unchanged, including every value, style and position. Only its stale pending-photo paragraph changes. Slide 11 distinguishes completed photo collection from pending project/member review and rehearsal. Slide 12 adds photographer/capture provenance in its previously empty body shape. The other eight slides remain unchanged. The external-AI, NDVI diagnostic and limited Dynamic World disclosures remain intact.

The spoken script now has **394 whitespace-separated words** in twelve sections with cues totalling 180 seconds. At 135 words/minute, estimated speech is 175.11 seconds, leaving 4.89 seconds for transitions. Timing is a preparation estimate; Mohammed's actual timed rehearsal remains pending. Slide 6 introduces the photographs and shared date/window. Judge answers remain applicable and unchanged.

## Checks and limits

Current evidence: results/field-photo-slides-verification-2026-10-08.json. PDF slides 6/8/11/12 were rendered and individually inspected at 1280 × 720 presentation scale; no obvious clipping, unreadable case labels or overlaps were seen. The slide 6 preview is results/field-photo-slide-review/slide-6.png. Automated checks compare PDF/PPTX text, image bytes, page boundaries, unchanged table XML, untouched PPTX components, and rendered pixels outside changed regions. All original inputs, seven analytical CSVs, full app/standalone preview, original media, historical exports/references, analysis and ranking remain unchanged.

**Native desktop PowerPoint and LibreOffice are unavailable and were not used.** PPTX was parsed and checked structurally; no native PowerPoint rendering or PDF-export equivalence is claimed. The PDF retains its original pages with targeted figure/text replacement using PyMuPDF and the existing Noto Sans PDF font style. PowerPoint retains its existing Bitstream Charter text style. A member should open the editable deck on the actual presentation computer to check font substitution and projection. That acceptance remains pending.

The app/preview bytes are unchanged, so the latest matching real Chromium HTTP/offline desktop/mobile evidence is retained in results/site-media-capture-verification-2026-10-08.json; no new browser run is needed or claimed. Physical devices and ChatGPT embedded preview remain unverified. Primary Dynamic World coverage still fails the unchanged 50% gate at 30.9385%, with confidence 0.60 and Unknown/excluded 69.0615%; independent scientific validation remains pending. No additional model or analysis was run, no thresholds changed and nothing was submitted.

## Reproduce presentation preparation only

Preserve the baseline docs/UrbanHeat-AlKhor-Pitch.pdf and .pptx from commit 9fa71a86 in an external directory before using the optional presentation environment (python-pptx, PyMuPDF and lxml):

```sh
python src/add_field_photos_to_presentation.py --baseline /tmp/preserved-9fa71a86 --project /path/to/project
```

This updates presentation files only. It does not run analysis, alter original photographs, rebuild the map or submit anything. Packaging is separate; see Delivery-Guide.md. Final file sizes/checksums, exact ZIP contents and public branch/tree verification are recorded by the external delivery verification after guarded non-force publication. Both backup branches and earlier delivery folders remain preserved.
