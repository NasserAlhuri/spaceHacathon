// Prepared inspection helper; not executed here. No export tasks, threshold tuning or rankings.
// Source IDs come from the immutable real provenance CSV; their asset readback is pending.
var SOURCES = ["COPERNICUS/S2_HARMONIZED/20210901T070619_20210901T071620_T39RWJ", "COPERNICUS/S2_HARMONIZED/20210926T070641_20210926T072035_T39RWJ", "COPERNICUS/S2_HARMONIZED/20260905T070619_20260905T071117_T39RWJ", "COPERNICUS/S2_HARMONIZED/20260915T070619_20260915T071117_T39RWJ"];
var CANDIDATES = [{"sample_id": "DW-01", "longitude": 51.5129704, "latitude": 25.6930348, "predicted_before": "water", "predicted_after": "water"}, {"sample_id": "DW-02", "longitude": 51.5476595, "latitude": 25.6726815, "predicted_before": "water", "predicted_after": "water"}, {"sample_id": "DW-03", "longitude": 51.53411, "latitude": 25.7178817, "predicted_before": "built", "predicted_after": "built"}, {"sample_id": "DW-04", "longitude": 51.5283122, "latitude": 25.7142005, "predicted_before": "built", "predicted_after": "built"}, {"sample_id": "DW-05", "longitude": 51.5543156, "latitude": 25.711395, "predicted_before": "bare", "predicted_after": "bare"}, {"sample_id": "DW-06", "longitude": 51.4578842, "latitude": 25.6740744, "predicted_before": "bare", "predicted_after": "bare"}, {"sample_id": "DW-07", "longitude": 51.5438234, "latitude": 25.7056553, "predicted_before": "Unknown", "predicted_after": "Unknown"}, {"sample_id": "DW-08", "longitude": 51.5009522, "latitude": 25.6551504, "predicted_before": "Unknown", "predicted_after": "Unknown"}];
SOURCES.forEach(function(id) {
  var image = ee.Image(id);
  print('Reference source and actual acquisition UTC', id,
    ee.Date(image.get('system:time_start')).format('YYYY-MM-dd HH:mm:ss'),
    'Scene cloud percentage (not local clear-pixel proof)', image.get('CLOUDY_PIXEL_PERCENTAGE'));
  Map.addLayer(image, {bands:['B4','B3','B2'], min:0,max:3500}, id, false);
});
var points = ee.FeatureCollection(CANDIDATES.map(function(c) {
  return ee.Feature(ee.Geometry.Point([c.longitude,c.latitude]), c);
}));
Map.addLayer(points.style({color:'ffff00',pointSize:4}), {}, 'Unvalidated sample targets', true);
Map.setCenter(51.50,25.68,12);
print('Record actual image visibility, dates, labels, disagreements and ambiguity. No overall accuracy or accepted change is implied.');
print('These stable/Unknown candidates do not replace changed, vegetation and coastal checks. 0.50 changed candidates require the two annual TIFFs.');
