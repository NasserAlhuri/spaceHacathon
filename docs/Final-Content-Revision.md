# Final content revision — 8 October 2026

The three wording/status corrections in the [supplied review](Final-Content-External-Review-2026-10-08.md) are applied to the same twelve-slide presentation, matching PDF, three-minute script, judge answers, unsent submission draft/checklist and directly affected documentation. The supplied review describes source `865c7f2d8465e77b6451dbf16dda1149b17237d7`; it is retained unchanged as external evidence, not claimed as a new check of these revised files.

## Corrected explanations

1. **External AI:** WorldCover supplies AI land-cover data in the heat-screening workflow; Dynamic World supplies it in a separate historical experiment. Quality checks/ranking are rule based, no new model was trained, and Dynamic World does not feed the original score. Slide 5, its spoken section, the judge answer, README/PoC and submission summary now agree.
2. **Vegetation diagnostic:** Slide 9 explicitly states NDVI >=0.30 at 24/25 grass references and 0/30 building references. The judge answer explains that 0/30 is not building-detection accuracy. Separate historical WorldCover class 50 agreement is 25/30 building references; all 30 coastal references are excluded from retained thermal support. These counts were checked directly against the untouched reference CSV. None is independently measured overall accuracy.
3. **Current review status:** Slide 10 and its spoken section distinguish completed assistant review of 18 targets across four dates from pending independent scientific validation. The checklist separately marks verified reference retrieval/technical checks and assistant review complete, while independent validation, member reviews and actual timed rehearsal remain pending. README now distinguishes completed technical Chromium checks from unverified physical-device/member acceptance.

The 72 figure refers to dated views (18 targets × four dates), not independent sites. Eight clear broad patterns are not eight confirmed model classes or 8/18 accuracy. Three potential disagreement flags overlap ambiguous cases and are not confirmed errors. Confidence remains 0.60; common-window coverage remains 30.9385%, below the unchanged 50% gate; Unknown/excluded common support remains 69.0615%. The comparison remains a limited experiment with no general urban-growth, vegetation-change or citywide-stability finding.

## What verifies the revised artifacts

| Artifact | Latest matching evidence | Scope and limits |
|---|---|---|
| [Twelve-page PDF](UrbanHeat-AlKhor-Pitch.pdf) and [editable twelve-slide PPTX](UrbanHeat-AlKhor-Pitch.pptx) | [Final content verification](../results/final-content-revision-verification.json) | Four text nodes in slides 5/9/10 change. All other PPTX parts and non-text XML/font/geometry/theme/media are unchanged. All 89 paragraph/table-cell checks match corresponding PDF pages; text spans stay inside pages. Nine page renders are identical; changed-page pixels outside the reviewed text regions are identical. |
| [Changed slide renders](../results/final-content-slide-review/) | Slides 5, 9 and 10 rendered and visually inspected | Final PDF has no obvious overlap/clipping. The initial unsupported non-ASCII comparison glyph was replaced with ASCII >= in both formats. Desktop PowerPoint was not opened; no native PowerPoint rendering/export is claimed. |
| [Three-minute script](Three-Minute-Presentation.md) | Word/section/timing checks in final content verification | 386 spoken whitespace-separated words. About 135 words/minute over 171 seconds plus nine seconds of transitions is a planning estimate. Cues total 180 seconds; actual Mohammed rehearsal duration is not measured and remains pending. |
| [Judge answers](Judge-Questions.md), [draft](Submission-Draft.md), [checklist](Submission-Checklist.md), README/PoC/handover | Final content verification and current local-link/status checks | Correct AI scopes, NDVI diagnostics and completed/pending distinctions; no invented member completion or submission. |
| Unchanged app and [standalone preview](../preview/UrbanHeat-AlKhor-Preview.html) | [Paired-review technical evidence](../results/dynamic-world-paired-review-verification.json) | Latest retained 29 Chromium HTTP groups per desktop/mobile profile and offline checks match exact current bytes. Preview SHA256 `b3056be7afc295687c7efebf6d541624da2e64f02234ece38a8983dabc05691e`. No browser rerun for this wording-only revision. Physical devices, other browsers, embedded ChatGPT preview and member acceptance remain unverified. |
| Original analysis/input/output data | Original hash manifests and retained expanded workflow evidence | 35 input files and seven original tables still match. Analysis/ranking/eligibility/thresholds, all raw exports/reference imagery and sample predictions are unchanged. No new model, image export or analysis run. |

The older `results/preview-verification.json`, earlier presentation/delivery reports and prior checkpoint sections are preserved historical evidence. Their older artifact hashes must not be described as validation of this revised presentation. `results/dynamic-world-paired-review-verification.json` remains current for the unchanged app/preview and the paired-review milestone; this final content report supersedes its then-unchanged presentation description.

Final source commit, public-tree/ZIP matching, sizes and checksums are recorded in the external delivery verification after guarded non-force publication. Older delivery folders, the pre-revision local files and both backup branches are preserved. PDF <=50 MB and optional ZIP <=200 MB are retained recorded limits, not a fresh live-form check. Final form/attachment acceptance and Nasser's separate approval remain pending. No organizer contact, form attachment upload or hackathon submission occurred.

## Reproduce the content-only revision

The original PDF/PPTX can be obtained from the recorded baseline commit. With those files stored outside the output directory:

```bash
python src/revise_final_presentation.py --baseline-pptx /path/to/baseline/UrbanHeat-AlKhor-Pitch.pptx --baseline-pdf /path/to/baseline/UrbanHeat-AlKhor-Pitch.pdf --output /path/to/revised
```

The utility preserves the original OOXML components, changes four exact text nodes and redraws only the matching PDF paragraphs at existing font size/colour/baseline. It requires PyMuPDF/lxml and Noto Sans Regular for matching the original PDF; these presentation tools do not alter pinned scientific dependencies. It does not certify desktop PowerPoint layout, independently validate classes, run analysis or submit anything.
