// Nasser successfully exported the two-year workflow in Code Editor on 2026-10-07.
// This corrected revision is locally syntax-checked; its new exports are not claimed.
// Paste into an authorized Earth Engine Code Editor. Use your own selected project.
// Review Console coverage, provenance, sensitivity and source imagery before export.
// This module never reads or replaces the original thermal/NDVI ranking pipeline.
var YEARS = [2021, 2026]; // Add 2023 only after the two-year comparison is suitable.
var CLASSES = ['water', 'trees', 'grass', 'flooded_vegetation', 'crops',
  'shrub_and_scrub', 'built', 'bare', 'snow_and_ice'];
var COLORS = ['419bdf', '397d49', '88b053', '7a87c6', 'e49635',
  'dfc35a', 'c4281b', 'a59b8f', 'b39fe1'];
var CRS = 'EPSG:32639';
var TRANSFORM = [10, 0, 544635, 0, -10, 2845905];
var REGION = ee.Geometry.Rectangle([51.445, 25.635, 51.555, 25.730], null, false);
var THRESHOLDS = [0.5, 0.6, 0.7];
var MIN_OBSERVATIONS = 3;
var CREATE_EXPORT_TASKS = false; // Enable only after inspecting actual outputs.
var area = ee.Image.pixelArea().reproject({crs: CRS, crsTransform: TRANSFORM}).clip(REGION);
function total(image) {
  return ee.Number(image.rename('area').reduceRegion({reducer: ee.Reducer.sum(),
    geometry: REGION, crs: CRS, crsTransform: TRANSFORM, maxPixels: 2e7}).get('area', 0));
}
var windowArea = total(area);
var composites = {};
var provenance = ee.FeatureCollection([]);
YEARS.forEach(function(year) {
  var start = ee.Date.fromYMD(year, 9, 1);
  var end = start.advance(1, 'month');
  var collection = ee.ImageCollection('GOOGLE/DYNAMICWORLD/V1')
    .filterBounds(REGION).filterDate(start, end).sort('system:time_start');
  print('Actual scene count ' + year, collection.size());
  // A masked fallback guarantees named bands for an empty collection; not fake data.
  var empty = ee.Image.constant([0,0,0,0,0,0,0,0,0]).rename(CLASSES)
    .toFloat().updateMask(ee.Image.constant(0));
  var clean = collection.map(function(image) {
    var p = image.select(CLASSES);
    return p.updateMask(p.mask().reduce(ee.Reducer.min()))
      .copyProperties(image, image.propertyNames());
  });
  // Verified runtime correction supplied by Nasser: never mix MaskOnly fallback
  // images with the real Float probability collection.
  var safe = ee.ImageCollection(ee.Algorithms.If(
    collection.size().gt(0), clean, ee.ImageCollection([empty])
  ));
  var mean = safe.mean().reproject({crs: CRS, crsTransform: TRANSFORM}).clip(REGION);
  var count = safe.select('water').count().unmask(0)
    .reproject({crs: CRS, crsTransform: TRANSFORM}).clip(REGION).rename('observation_count');
  var confidence = mean.reduce(ee.Reducer.max()).rename('confidence');
  var label = mean.toArray().arrayArgmax().arrayGet([0]).rename('class');
  composites[year] = {mean: mean, count: count, confidence: confidence, label: label};
  var rows = ee.FeatureCollection(collection.toList(collection.size()).map(function(item) {
    var image = ee.Image(item);
    return ee.Feature(null, {year: year, dataset: 'GOOGLE/DYNAMICWORLD/V1',
      image_index: image.get('system:index'),
      asset_id: ee.String('GOOGLE/DYNAMICWORLD/V1/').cat(ee.String(image.get('system:index'))),
      source_sentinel2_id: ee.String('COPERNICUS/S2_HARMONIZED/')
        .cat(ee.String(image.get('system:index'))),
      acquired_utc: ee.Date(image.get('system:time_start')).format('YYYY-MM-dd HH:mm:ss'),
      dynamicworld_algorithm_version: image.get('dynamicworld_algorithm_version'),
      qa_algorithm_version: image.get('qa_algorithm_version'), crs: CRS,
      grid_transform: TRANSFORM.join(','), start_inclusive: start.format('YYYY-MM-dd'),
      end_exclusive: end.format('YYYY-MM-dd')});
  }));
  provenance = provenance.merge(rows);
  Map.addLayer(label.updateMask(count.gte(MIN_OBSERVATIONS).and(confidence.gte(0.6))),
    {min: 0, max: 8, palette: COLORS}, year + ' September classes (unknown transparent)', year === 2026);
  Map.addLayer(count, {min: 0, max: 10}, year + ' valid observation count', false);
  if (CREATE_EXPORT_TASKS) {
    Export.image.toDrive({image: mean.rename(CLASSES.map(function(n){return 'p_' + n;}))
      .addBands(count).addBands(confidence).addBands(label).toFloat().clip(REGION)
      .unmask({value: -9999, sameFootprint: false}),
      description: 'AlKhor_DynamicWorld_September_' + year, folder: 'UrbanHeat-DynamicWorld',
      region: REGION, crs: CRS, crsTransform: TRANSFORM, maxPixels: 2e7,
      fileFormat: 'GeoTIFF', formatOptions: {cloudOptimized: true, noData: -9999}});
  }
});
var whole = [], matched = [], transitions = [], diagnostics = [];
THRESHOLDS.forEach(function(threshold) {
  var accepted = {};
  YEARS.forEach(function(year) {
    var c = composites[year];
    accepted[year] = c.count.gte(MIN_OBSERVATIONS).and(c.confidence.gte(threshold)).unmask(0);
    var validArea = total(area.multiply(accepted[year]));
    diagnostics.push(ee.Feature(null, {year: year, confidence_threshold: threshold,
      minimum_observations: MIN_OBSERVATIONS, window_area_m2: windowArea,
      observed_area_m2: total(area.multiply(c.count.gt(0))),
      accepted_area_m2: validArea, unknown_area_m2: windowArea.subtract(validArea),
      accepted_fraction: validArea.divide(windowArea), review_status: 'manual validation pending'}));
    CLASSES.forEach(function(name, code) {
      whole.push(ee.Feature(null, {year: year, class_code: code, class_name: name,
        confidence_threshold: threshold, support: 'whole_window_accepted',
        area_m2: total(area.multiply(accepted[year]).multiply(c.label.eq(code).unmask(0)))}));
    });
    whole.push(ee.Feature(null, {year: year, class_code: 255, class_name: 'unknown',
      confidence_threshold: threshold, support: 'whole_window',
      area_m2: windowArea.subtract(validArea)}));
  });
  // Default two-year comparison; adding 2023 produces all chronological pairs.
  YEARS.forEach(function(before, i) { YEARS.slice(i + 1).forEach(function(after) {
    var common = accepted[before].and(accepted[after]);
    var commonArea = total(area.multiply(common));
    var fraction = commonArea.divide(windowArea);
    print('Matched fraction ' + before + ' to ' + after + ' threshold ' + threshold, fraction);
    CLASSES.forEach(function(name, code) {
      var a = total(area.multiply(common).multiply(composites[before].label.eq(code).unmask(0)));
      var b = total(area.multiply(common).multiply(composites[after].label.eq(code).unmask(0)));
      matched.push(ee.Feature(null, {before_year: before, after_year: after, class_code: code,
        class_name: name, confidence_threshold: threshold, before_m2: a, after_m2: b,
        change_m2: b.subtract(a), common_support_m2: commonArea,
        excluded_window_m2: windowArea.subtract(commonArea),
        common_window_fraction: fraction, coverage_screen_pass: fraction.gte(0.5),
        review_status: 'DO NOT PUBLISH before imagery/manual validation'}));
      CLASSES.forEach(function(target, next) {
        transitions.push(ee.Feature(null, {before_year: before, after_year: after,
          from_code: code, from_class: name, to_code: next, to_class: target,
          confidence_threshold: threshold, area_m2: total(area.multiply(common)
            .multiply(composites[before].label.eq(code).unmask(0))
            .multiply(composites[after].label.eq(next).unmask(0)))}));
      });
    });
    if (CREATE_EXPORT_TASKS && threshold === 0.6) {
      Export.image.toDrive({image: composites[before].label.multiply(9)
        .add(composites[after].label).updateMask(common).toUint8().clip(REGION)
        .unmask({value: 255, sameFootprint: false}),
        description: 'AlKhor_DW_transition_' + before + '_' + after,
        folder: 'UrbanHeat-DynamicWorld', region: REGION, crs: CRS,
        crsTransform: TRANSFORM, maxPixels: 2e7, fileFormat: 'GeoTIFF',
        formatOptions: {noData: 255}});
    }
  }); });
});
var outputs = {provenance: provenance, coverage: ee.FeatureCollection(diagnostics),
  whole_window_areas: ee.FeatureCollection(whole), matched_changes: ee.FeatureCollection(matched),
  transitions: ee.FeatureCollection(transitions)};
Object.keys(outputs).forEach(function(name) {
  print(name + ' (unvalidated candidates)', outputs[name]);
  if (CREATE_EXPORT_TASKS) Export.table.toDrive({collection: outputs[name],
    description: 'AlKhor_DW_' + name, folder: 'UrbanHeat-DynamicWorld', fileFormat: 'CSV'});
});
Map.centerObject(REGION, 12);
print('Workflow diagnostics only: inspect actual task status and exports. Export creation enabled:', CREATE_EXPORT_TASKS);
print('Primary threshold remains 0.60; common support must pass the unchanged provisional 50% gate. Dated-imagery scientific review is required.');
