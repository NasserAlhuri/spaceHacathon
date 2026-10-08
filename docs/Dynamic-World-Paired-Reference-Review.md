# Paired dated reference review — 8 October 2026

The assistant visual review of all 18 previously selected targets is complete: **72 views** from 1/26 September 2021 and 5/15 September 2026. It resolves the missing-2021-reference blocker, not the failed coverage or independent scientific review.

**Decision remains a limited experiment.** Primary confidence stays 0.60; common-window coverage remains 30.9385%, below the unchanged 50% gate. Unknown/excluded common support stays 69.0615%. No general urban-growth, vegetation-change or citywide-stability result is adopted. Original raw classified counts, inputs, tables and ranking are unchanged.

## Reference identity and inspection

The supplied ZIP passed CRC. The 20210901(1).tif copy is byte-identical to 20210901.tif and was ignored as requested. The two unique four-band UInt16 RGB/QA60 TIFFs and unchanged source CSV are preserved in data/dynamic_world/reference/2026-10-08/. All identities/sizes are recorded in metadata/dynamic-world-reference-manifest.json; full source/grid/target checks are in results/dynamic-world-reference-verification.json. No source TIFF was edited.

Both source IDs and precise acquisition timestamps match the original DW provenance locally: 1 September 2021 07:22:28 UTC and 26 September 2021 07:22:35 UTC. These are actual supplied Code Editor metadata, not an independent runtime asset query. Both grids are EPSG:32639, 1108 x 1057, 10 m, origin 544635/2845905, with red/green/blue/qa60 bands, nodata 65535. All 18 targets and 410 m contexts are present; QA60 is zero and recorded scene cloud is 0%. QA60 retains native 60 m information; these flags do not guarantee perfect visibility.

The 2021 RGB is a fixed 0..3500 DN display visualization. The 2026 original L2A bands use the same display stretch for context. L1C/L2A processing, clipping/saturation, 10 m mixtures and unknown geolocation uncertainty prevent using colour or brightness as quantitative land change. The renderer samples 2026 from its source geotransform to the DW target; the original source origin differs by 5 m. Enlarged 90 m details add no resolution. Contains modified Copernicus Sentinel data (2021, 2026).

## Actual outcome

- **8 clear broad visual patterns:** three apparent local water-like to exposed-surface differences (DWR-02/03/04), and five broadly consistent bare/water-looking targets (DWR-07/08/09/10/18). Clear visual pattern does not mean independent exact-class validation.
- **10 exact-class ambiguities:** existing structures/material mixes and coastal water/vegetation targets. Urban context can support a built interpretation while the precise 10 m material remains unresolved.
- **3 overlapping potential disagreement flags:** DWR-01 already shows recognisable structures in 2021, so the bare-to-new-built story is not clearly supported; DWR-11/12 look water-like and their flooded-vegetation labels remain ambiguous. These are not three confirmed model errors.

The three apparent water/exposed differences do not establish drying, fill, reclamation, ownership, cause or timing; the annual composite contains other dates. None enters a citywide change total. The 351 sensitivity classified pixels (301 water-to-bare, 50 bare-to-built) are retained original model counts, not validated change areas. All three apparent change targets have at least one primary Unknown label. Zero differing selected primary pixels is still not proof of citywide stability.

## All 18 recorded targets

### DWR-01 — ambiguous_exact_class

Coordinate: 25.6514497, 51.5506509. Primary: **Unknown → built**; sensitivity: bare → built.

Both 2021 dates already show the same recognisable shore-adjacent block/structure layout seen in 2026. The marked 10 m pixel is a bright mixed surface, not a clearly new building. No convincing bare-to-new-built event can be assigned at this target from these views.

Limit: Existing structure context conflicts with a simple before-bare/new-construction story; exact roof/paving/bare proportions, registration, L1C/L2A brightness and saturated display remain unresolved.

Disagreement status: potential_2021_bare_label_vs_existing_built_context.

[Four dated contexts](../results/dynamic-world-paired-context/page-1.png)

### DWR-02 — clear_visual_pattern

Coordinate: 25.6472300, 51.5193496. Primary: **water → Unknown**; sensitivity: water → bare.

The target lies within a coherent green-blue pond-like feature in both 2021 dates. The same location is bright exposed-looking ground in both 2026 views. The local water-like to exposed-surface pattern is visually supported.

Limit: Drying, fill, reclamation, management and exact material cannot be distinguished; after RGB is display-saturated and primary after classification is Unknown. No area or causal claim.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-1.png)

### DWR-03 — clear_visual_pattern

Coordinate: 25.6464314, 51.5153612. Primary: **water → Unknown**; sensitivity: water → bare.

A bounded dark pond-like feature contains the target in both 2021 dates; its shape is absent at the target in both 2026 contexts, which show bright exposed-looking ground. The broad local difference agrees with the sensitivity water-to-bare prediction.

Limit: Surface change is apparent, but mechanism, timing, exact bare class and a surveyed transition are unverified. Primary after remains Unknown; not citywide growth.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-1.png)

### DWR-04 — clear_visual_pattern

Coordinate: 25.6752016, 51.5253500. Primary: **Unknown → Unknown**; sensitivity: water → bare.

The target sits in a coherent dark elongated water-like feature along light banks on both 2021 dates. It is bright exposed-looking surface on both 2026 dates. A local water-like/exposed-surface difference is apparent.

Limit: Shallow water, wet sediment, tidal stage and drying/fill cannot be separated from these RGB views. Both primary labels remain Unknown; no adopted exact class or mechanism.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-2.png)

### DWR-05 — ambiguous_exact_class

Coordinate: 25.7162846, 51.5263278. Primary: **built → built**; sensitivity: built → built.

Street and building-block layout is recognisable at all four dates, broadly consistent with built context in both years. The exact central pixel mixes pale/grey roof, paving or bare material; a precise built class is not independently resolved.

Limit: 10 m material mixture, shadows and L1C/L2A contrast prevent exact target truth or a quantified stable-built area.

Disagreement status: none_obvious_in_context_exact_target_unresolved.

[Four dated contexts](../results/dynamic-world-paired-context/page-2.png)

### DWR-06 — ambiguous_exact_class

Coordinate: 25.7097570, 51.5334757. Primary: **built → built**; sensitivity: built → built.

Both years show an established street/building pattern. The marked target is a pale mixed pixel within that pattern. Stable built context is plausible, but target-level roof versus paving versus bare land is ambiguous.

Limit: Context agreement is not independent nine-class ground truth; no citywide stability inference.

Disagreement status: none_obvious_in_context_exact_target_unresolved.

[Four dated contexts](../results/dynamic-world-paired-context/page-2.png)

### DWR-07 — clear_visual_pattern

Coordinate: 25.7138213, 51.4813614. Primary: **bare → bare**; sensitivity: bare → bare.

The marked target and surrounding open desert are predominantly pale, bare-looking in all four dates. No obvious broad land-cover switch is visible; the broad appearance agrees with bare/bare.

Limit: Sparse vegetation and exact substrate remain below RGB resolution; apparent local consistency does not prove citywide stability or exact accuracy.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-3.png)

### DWR-08 — clear_visual_pattern

Coordinate: 25.6697515, 51.4541809. Primary: **bare → bare**; sensitivity: bare → bare.

All four dates show a predominantly bare-looking open surface at the target. Broad bare/bare appearance is consistent across the supplied dates without an obvious new structure or dense green cover.

Limit: Cannot rule out sparse vegetation or subpixel differences; RGB brightness differs between L1C and L2A.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-3.png)

### DWR-09 — clear_visual_pattern

Coordinate: 25.6946367, 51.5443713. Primary: **water → water**; sensitivity: water → water.

The target remains within a continuous dark water-like coastal area at all four dates. Broad water/water appearance agrees with the primary prediction.

Limit: Submerged vegetation, shallow-water bottom and tide cannot be assigned; colour differences are not vegetation change or quantitative reflectance.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-3.png)

### DWR-10 — clear_visual_pattern

Coordinate: 25.6736941, 51.5424825. Primary: **water → water**; sensitivity: water → water.

All four dates place the target within a continuous water-like coastal surface; dark/green patches surround it. Broad water context is plausible in both years without a clear target-scale conversion.

Limit: Patch texture may include shallow-water substrate or submerged vegetation; exact flooded-vegetation distinction and tide are unresolved. No vegetation absence claim.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-4.png)

### DWR-11 — ambiguous_exact_class

Coordinate: 25.6849550, 51.5496090. Primary: **Unknown → Unknown**; sensitivity: flooded_vegetation → flooded_vegetation.

Both years show a dark, fairly uniform water-like target next to a pale shore. The sensitivity flooded-vegetation label is not visibly identifiable at the marked pixel. Water-like appearance is a potential competing interpretation, not proof of a model error.

Limit: RGB alone cannot separate flooded/submerged vegetation, open water, shadow or tidal substrate; no botanical ground truth. Both primary labels stay Unknown.

Disagreement status: potential_flooded_vegetation_vs_water_like_RGB.

[Four dated contexts](../results/dynamic-world-paired-context/page-4.png)

### DWR-12 — ambiguous_exact_class

Coordinate: 25.6934336, 51.5521395. Primary: **Unknown → Unknown**; sensitivity: flooded_vegetation → flooded_vegetation.

The target is dark water-like beside a curving shore in both years. Nearby 2026 green/blue streaks do not resolve vegetation at the exact target. Flooded-vegetation/flooded-vegetation at 0.50 remains ambiguous.

Limit: The two 2026 SCL flags differ and have another taxonomy. Neither those flags nor colour establish exact vegetation truth; primary Unknown is retained.

Disagreement status: potential_flooded_vegetation_vs_water_like_RGB.

[Four dated contexts](../results/dynamic-world-paired-context/page-4.png)

### DWR-13 — ambiguous_exact_class

Coordinate: 25.6862203, 51.5493158. Primary: **Unknown → Unknown**; sensitivity: Unknown → Unknown.

Both years show dark coastal context with a lighter/greener nearby band; the centre remains dark. No precise flooded-vegetation reference or historical conversion is resolved from RGB.

Limit: Raw vegetation argmax is rejected even at 0.50; green appearance, submerged texture and display-processing differences cannot establish vegetation extent. Unknown remains.

Disagreement status: unresolved_not_a_confirmed_error.

[Four dated contexts](../results/dynamic-world-paired-context/page-5.png)

### DWR-14 — ambiguous_exact_class

Coordinate: 25.7011341, 51.5454972. Primary: **Unknown → Unknown**; sensitivity: Unknown → Unknown.

The same shoreline strip, dark centre and lighter water/bank context are recognisable in both years. Raw water-to-flooded-vegetation labels are very low confidence and no clear vegetation conversion can be established.

Limit: Tidal/wetness, shadow, vegetation and L1C/L2A colour differences are inseparable here; both primary and 0.50 labels remain Unknown.

Disagreement status: unresolved_not_a_confirmed_error.

[Four dated contexts](../results/dynamic-world-paired-context/page-5.png)

### DWR-15 — ambiguous_exact_class

Coordinate: 25.6855957, 51.5473199. Primary: **Unknown → Unknown**; sensitivity: Unknown → Unknown.

A similar dark coastal feature with a narrow pale element is visible in both years. Green surroundings and a 2026 vegetation SCL flag suggest possible vegetation context but do not establish a class at the exact target.

Limit: No species, inundation, canopy, shade or vegetation absence is established. Primary and sensitivity remain Unknown.

Disagreement status: unresolved_not_a_confirmed_error.

[Four dated contexts](../results/dynamic-world-paired-context/page-5.png)

### DWR-16 — ambiguous_exact_class

Coordinate: 25.6888291, 51.5519189. Primary: **Unknown → Unknown**; sensitivity: Unknown → Unknown.

Both years show a similar dark coastal strip next to a diagonal pale bank; no distinct tree crown is resolvable at the target. Raw flooded-vegetation-to-trees output is not visually validated.

Limit: Very low confidence, 10 m mixing and tide/processing effects prevent exact flooded vegetation versus tree attribution. Unknown in both years is appropriate.

Disagreement status: unresolved_not_a_confirmed_error.

[Four dated contexts](../results/dynamic-world-paired-context/page-6.png)

### DWR-17 — ambiguous_exact_class

Coordinate: 25.7102267, 51.5284940. Primary: **Unknown → Unknown**; sensitivity: Unknown → Unknown.

Road and building pattern is present in all dates, with a pale central road/paved/bare pixel. Raw built/built is contextually plausible, but exact material cannot be assigned and the primary rule rejects both years.

Limit: Low-confidence urban mixture is not repaired by contextual visual agreement; Unknown stays unchanged.

Disagreement status: none_obvious_in_context_exact_target_unresolved.

[Four dated contexts](../results/dynamic-world-paired-context/page-6.png)

### DWR-18 — clear_visual_pattern

Coordinate: 25.6515991, 51.5095054. Primary: **Unknown → Unknown**; sensitivity: bare → bare.

The target lies on a bright exposed-looking open surface in all four dates. Broad bare/bare appearance agrees with the sensitivity prediction, without an obvious broad conversion.

Limit: Display clipping limits material detail, and both confidences remain below 0.60. Visual plausibility does not promote primary Unknown or lower the threshold.

Disagreement status: none_obvious_at_broad_visual_level.

[Four dated contexts](../results/dynamic-world-paired-context/page-6.png)

## Remaining scientific work

This is a biased, convenience, same-source assistant review with descriptive reference interpretations, not independent ground truth or an accuracy design. No overall accuracy, surveyed transition total or confirmed exact-class error is estimated. Independent review of the paired interpretations and flags is still required. More independent, higher-resolution dated evidence is needed if exact coastal/urban labels or causal change claims are proposed. No repeat 2021 export is requested now.

The paired CSV has 18 actual review rows attributed to Codex; original primary/sensitivity predictions stay separate from descriptions. It does not certify any teammate task. Mohammed practises the presentation; Abdulrahman reviews the project and collects photographs/observations. Their confirmations and all unfinished member reviews remain pending. 2023, SamGeo and other models stay deferred. No organizer contact or hackathon submission has occurred.
