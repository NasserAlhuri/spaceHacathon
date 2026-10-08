// Prepared only, not executed in this runtime. Use Nasser's already authorized Code Editor.
// Specific missing evidence: two small dated 2021 RGB/QA exports for the 18 recorded targets.
// No Dynamic World rerun, threshold adjustment, new model, original data/rank overwrite,
// organizer contact or submission. Asset readback and scientific review remain pending.
var CREATE_REFERENCE_EXPORTS = false; // Inspect source dates/visibility first, then enable.
var REGION = ee.Geometry.Rectangle([51.445,25.635,51.555,25.730],null,false);
var CRS = 'EPSG:32639';
var TRANSFORM = [10,0,544635,0,-10,2845905];
var SOURCES = [
  'COPERNICUS/S2_HARMONIZED/20210901T070619_20210901T071620_T39RWJ',
  'COPERNICUS/S2_HARMONIZED/20210926T070641_20210926T072035_T39RWJ'
];
var provenance = [];
SOURCES.forEach(function(id) {
  var source=ee.Image(id);
  var acquisition=ee.Date(source.get('system:time_start'));
  var name=id.split('/').pop().slice(0,8);
  print('Actual source identity/date/cloud metadata; verify before using',id,
    acquisition.format('YYYY-MM-dd HH:mm:ss'),source.get('CLOUDY_PIXEL_PERCENTAGE'));
  Map.addLayer(source,{bands:['B4','B3','B2'],min:0,max:3500},id,false);
  // Display RGB only: fixed 0..3500 DN stretch to 0..255. Never used as reflectance
  // analysis. QA60 cloud/cirrus bits retain native 60 m information at the 10 m grid.
  var rgb=source.visualize({bands:['B4','B3','B2'],min:0,max:3500})
    .rename(['red','green','blue']).toUint16();
  var image=rgb.addBands(source.select('QA60').unmask(65535).rename('qa60').toUint16())
    .clip(REGION).unmask({value:65535,sameFootprint:false});
  provenance.push(ee.Feature(null,{source_asset_id:id,
    acquired_utc:acquisition.format('YYYY-MM-dd HH:mm:ss'),
    scene_cloud_percent:source.get('CLOUDY_PIXEL_PERCENTAGE'),
    rgb_stretch_min:0,rgb_stretch_max:3500,rgb_display_max:255,
    qa60_native_resolution_m:60,qa60_cloud_bit:10,qa60_cirrus_bit:11,
    nodata:65535,crs:CRS,grid_transform:TRANSFORM.join(','),
    role:'dated 2021 reference visualization; not independent ground truth or accepted change'}));
  if(CREATE_REFERENCE_EXPORTS) Export.image.toDrive({image:image,
    description:'AlKhor_Sentinel2_Reference_'+name,folder:'UrbanHeat-Dated-Reference',
    region:REGION,crs:CRS,crsTransform:TRANSFORM,maxPixels:2e7,
    fileFormat:'GeoTIFF',formatOptions:{cloudOptimized:true,noData:65535}});
});
print('Missing-reference provenance (inspect actual metadata)',ee.FeatureCollection(provenance));
if(CREATE_REFERENCE_EXPORTS) Export.table.toDrive({collection:ee.FeatureCollection(provenance),
  description:'AlKhor_Sentinel2_Reference_provenance',folder:'UrbanHeat-Dated-Reference',fileFormat:'CSV'});
Map.centerObject(REGION,12);
print('Two four-band UInt16 window exports are expected to total about 19 MB uncompressed, below the 32 MiB attachment limit together. Check actual sizes.');
print('Inspect recorded scientific sample coordinates from metadata/dynamic-world-scientific-samples.csv. Retain Unknown for missing/cloudy/ambiguous references; paired scientific validation is still required.');
