"""Audit one reported cell without changing the tested screening or ranking.

Uses the same packaged optical scaling, grid and averaging as the main workflow.
Requires regenerated common-temp rasters. Run from any working directory.
"""
from pathlib import Path
import json
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, transform_geom, transform
from rasterio.features import geometry_mask

ROOT = Path(__file__).resolve().parents[1]

def audit():
    with rasterio.open(ROOT / 'data/sample_input/red.tif') as src:
        shape, optical_transform, optical_crs = src.shape, src.transform, src.crs
    with rasterio.open(ROOT / 'data/sample_input/landsat/lwir11.tif') as src:
        thermal_shape, thermal_transform, thermal_crs = src.shape, src.transform, src.crs
    features = json.loads((ROOT / 'results/planning-cells.geojson').read_text())['features']
    feature = next(f for f in features if f['properties']['cell_id'] == 'V04-23')
    polygon = transform_geom('EPSG:4326', optical_crs, feature['geometry'])
    inside = geometry_mask([polygon], out_shape=shape, transform=optical_transform, invert=True)

    def load(path):
        dest = np.full(shape, np.nan, dtype='float32')
        with rasterio.open(path) as src:
            reproject(src.read(1).astype('float32'), dest, src_transform=src.transform,
                      src_crs=src.crs, src_nodata=src.nodata, dst_transform=optical_transform,
                      dst_crs=optical_crs, dst_nodata=np.nan, resampling=Resampling.nearest)
        return dest

    def average(array):
        dest = np.zeros(thermal_shape, dtype='float32')
        reproject(array.astype('float32'), dest, src_transform=optical_transform,
                  src_crs=optical_crs, dst_transform=thermal_transform,
                  dst_crs=thermal_crs, resampling=Resampling.average)
        return dest

    rows = []
    for optical_date, thermal_date, sid in [
        ('2026-09-15', '2026-09-14', 'S2B_39RWJ_20260915_0_L2A'),
        ('2026-09-30', '2026-09-30', None),
    ]:
        directory = ROOT / 'data/sample_input/multidate' / sid if sid else ROOT / 'data/sample_input'
        meta_path = ROOT / 'metadata/multidate' / f'{sid}.json' if sid else ROOT / 'scene.json'
        metadata = json.loads(meta_path.read_text())
        reflectance = {}
        for band in ['red', 'nir']:
            band_meta = metadata['assets'][band]['raster:bands'][0]
            offset = 0 if metadata['properties'].get('earthsearch:boa_offset_applied') else band_meta.get('offset', 0)
            reflectance[band] = load(directory / f'{band}.tif') * band_meta.get('scale', 1) + offset
        denominator = reflectance['nir'] + reflectance['red']
        ndvi = np.divide(reflectance['nir'] - reflectance['red'], denominator,
                         out=np.full(shape, np.nan), where=denominator > .01)
        land = np.isin(load(directory / 'scl.tif'), [4, 5]) & np.isfinite(ndvi)
        values = ndvi[inside & land]
        with rasterio.open(ROOT / f'results/common-temp-{thermal_date}.tif') as src:
            common = src.read(1, masked=True)
            common = (~np.ma.getmaskarray(common)) & np.isfinite(common.filled(np.nan))
        window = np.s_[40:50, 230:240]  # V04-23: row 4, column 23 of 300 m cells
        retained = common[window]
        land_fraction = average(land)
        percentages = {}
        for threshold in [.2, .3, .4]:
            fraction = average(land & (ndvi >= threshold))
            percentages[str(threshold)] = float(fraction[window][retained].sum() /
                                               land_fraction[window][retained].sum() * 100)
        original = feature['properties']['vegetation_pct_' + thermal_date]
        assert abs(percentages['0.3'] - original) < 1e-6, 'Audit differs from packaged result'
        rows.append({'optical_date': optical_date, 'thermal_date': thermal_date,
                     'optical_scene_id': metadata['id'],
                     'pixel_centres_inside_polygon': int(inside.sum()),
                     'clear_land_pixel_centres': int(len(values)),
                     'ndvi_min': float(values.min()), 'ndvi_max': float(values.max()),
                     'ndvi_median': float(np.median(values)),
                     'pixel_counts_by_threshold': {str(t): int((values >= t).sum()) for t in [.2, .3, .4]},
                     'matched_support_green_percent_by_threshold': percentages,
                     'original_green_percent': original, 'common_30m_samples': int(retained.sum())})
    camera = {'latitude': 25.7175476, 'longitude': 51.5145504,
              'coordinate_type': 'Street View camera position; not a surveyed bus-stop coordinate',
              'image_capture_month': '2023-03',
              'source_url': 'https://maps.app.goo.gl/gPEzxW3NFqErPWNP8'}
    x, y = transform('EPSG:4326', thermal_crs, [camera['longitude']], [camera['latitude']])
    col, row = (~thermal_transform) * (x[0], y[0])
    camera['inside_V04_23'] = bool(230 <= col <= 240 and 40 <= row <= 50)
    assert camera['inside_V04_23']
    report = {'cell_id': 'V04-23', 'audit_recorded': '2026-10-06', 'threshold': .3,
              'geometry_scope': 'Full cell polygon. Centre-in-polygon pixel counts differ slightly from area-weighted matched thermal support at boundaries.',
              'dates': rows, 'street_view_reference': camera,
              'finding': 'The original zero is reproduced on matched support. No clear-land pixel centre inside the polygon reaches NDVI 0.30 on either accepted optical date.',
              'interpretation': 'Zero detected green pixels is not an inventory of trees. Mixed pixels, spectral conditions and the different imagery dates may contribute; no single cause is established.',
              'decision': 'Keep the tested threshold and ranking. Record local observations separately; obtain current site evidence.'}
    (ROOT / 'results/local-greenery-audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'cell': report['cell_id'], 'original_result_reproduced': True,
                      'camera_inside_cell': camera['inside_V04_23'], 'dates': rows}, indent=2))

if __name__ == '__main__':
    audit()
