"""Read-only Dynamic World grid/probability checks. Raw exports are never rewritten.

Optional dependencies are available in the retained scientific environment.
Finite study support is mandatory; declared nodata alone is insufficient.
Earth Engine CSV areas and projected pixel-count areas are separate conventions.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from affine import Affine
from pyproj import Transformer

GRID = Affine(10, 0, 544635, 0, -10, 2845905)
BBOX = (51.445, 25.635, 51.555, 25.730)
SUM_TOLERANCE = 0.0001  # Numerical precision check, not confidence/coverage tuning.


def region_centres(shape, transform=GRID):
    rows, cols = np.indices(shape)
    x = transform.c + (cols + .5)*transform.a
    y = transform.f + (rows + .5)*transform.e
    lon, lat = Transformer.from_crs(32639, 4326, always_xy=True).transform(x, y)
    return (lon >= BBOX[0]) & (lon <= BBOX[2]) & (lat >= BBOX[1]) & (lat <= BBOX[3])


def finite_support(bands, region, nodata=-9999):
    return region & np.all(np.isfinite(bands) & (bands != nodata), axis=0)


def check_bands(bands, region):
    if bands.shape[0] != 12:
        raise ValueError('Expected nine probability bands, count, confidence and class')
    support = finite_support(bands, region)
    if not support.any():
        raise ValueError('No finite in-region annual observations')
    p = bands[:9, support]
    count, confidence, label = bands[9:, support]
    if np.any((p < 0) | (p > 1)):
        raise ValueError('Probability outside [0,1]')
    deviation = float(np.abs(p.sum(axis=0, dtype=np.float64) - 1).max())
    if deviation > SUM_TOLERANCE:
        raise ValueError('Probability sum exceeds documented numerical tolerance')
    if np.any(count < 0) or np.any(count != np.floor(count)):
        raise ValueError('Noninteger or negative observation count')
    if np.any(np.abs(confidence-p.max(axis=0)) > 1e-6):
        raise ValueError('Confidence differs from maximum probability')
    if np.any(label != p.argmax(axis=0)):
        raise ValueError('Class differs from first maximum-probability index')
    return support, {'finite_in_region_pixels': int(support.sum()),
        'nonfinite_pixels': int((~np.all(np.isfinite(bands),axis=0)).sum()),
        'probability_sum_max_absolute_deviation': deviation,
        'probability_sum_numerical_tolerance': SUM_TOLERANCE,
        'valid_observation_count_range': [int(count.min()),int(count.max())],
        'confidence_equals_max': True, 'class_equals_argmax': True}


def accepted(bands, support, threshold):
    return support & (bands[9] >= 3) & (bands[10] >= threshold)


def safe_transition(before, after, support_before, support_after, threshold=.6):
    common = accepted(before,support_before,threshold) & accepted(after,support_after,threshold)
    result = np.full(common.shape,255,dtype=np.uint8)
    result[common] = (before[11,common]*9+after[11,common]).astype(np.uint8)
    return result, common


def verify(exports, manifest):
    report = {'status':'partial_raster_checks_annual_files_missing','publication_ready':False,
        'raster_checks':{}, 'missing_files':[], 'scientific_review':'pending',
        'region_rule':'Projected pixel centres transformed into unchanged WGS84 study rectangle; finite annual support also mandatory',
        'area_rule':'Raster counts use projected 100 m2 pixels for diagnostics only. Scientific coverage display uses unmodified Earth Engine CSV pixelArea sums.',
        'boundary_note':'Centre-based rectangle checks may differ at clipped edge pixels; do not interpret border codes as transitions.'}
    arrays, supports = {}, {}
    transition = None
    shape = None
    for name, item in manifest['files'].items():
        if not name.endswith('.tif'):
            continue
        path = exports/name
        if not path.exists():
            report['missing_files'].append(name)
            continue
        payload = path.read_bytes()
        if len(payload) != item['bytes'] or hashlib.sha256(payload).hexdigest() != item['sha256']:
            raise ValueError(f'Raw export checksum differs: {name}')
        with rasterio.open(path) as src:
            if src.crs != rasterio.crs.CRS.from_epsg(32639) or src.transform != GRID or (src.width,src.height) != (1108,1057):
                raise ValueError(f'Wrong CRS, transform or dimensions: {name}')
            shape = (src.height,src.width)
            data = src.read()
            summary = {'bytes':len(payload),'sha256':item['sha256'],
                'crs':str(src.crs),'transform':list(src.transform)[:6],
                'width':src.width,'height':src.height,'band_count':src.count,
                'dtypes':list(src.dtypes),'declared_nodata':src.nodata,
                'band_descriptions':list(src.descriptions)}
            region = region_centres(shape,src.transform)
            if 'September_' in name:
                if src.count != 12 or set(src.dtypes) != {'float32'} or src.nodata != -9999:
                    raise ValueError('Incorrect annual encoding')
                year=int(name.rsplit('_',1)[1].split('.')[0])
                supports[year], numerical = check_bands(data,region)
                arrays[year]=data
                summary.update(numerical)
            else:
                if src.count != 1 or src.dtypes[0] != 'uint8' or src.nodata != 255:
                    raise ValueError('Incorrect transition encoding')
                transition=data[0]
                if not np.isin(transition,[*range(81),255]).all():
                    raise ValueError('Unexpected transition code')
                summary['raw_code_counts']={str(k):int(v) for k,v in zip(*np.unique(transition,return_counts=True))}
                summary['outside_rectangle_pixels']=int((~region).sum())
                summary['outside_rectangle_non_nodata_pixels']=int(((~region)&(transition!=255)).sum())
                summary['outside_region_display']='must be Unknown; raw border codes are not evidence'
                summary['annual_finite_support_comparison']='pending until both annual files are available'
            report['raster_checks'][name]=summary
    if set(arrays) == {2021,2026} and transition is not None:
        expected,common=safe_transition(arrays[2021],arrays[2026],supports[2021],supports[2026])
        if np.any(transition[common] != expected[common]) or np.any(transition[(supports[2021]&supports[2026])&(~common)] != 255):
            raise ValueError('Primary transition disagrees with finite accepted annual support')
        report['primary_transition_check']={'status':'passed_on_finite_study_support',
            'ignored_nonfinite_or_outside_pixels':int((~(supports[2021]&supports[2026])).sum()),
            'ignored_border_non_nodata_pixels':int(((~(supports[2021]&supports[2026]))&(transition!=255)).sum())}
        with (exports/'AlKhor_DW_transitions.csv').open(newline='') as handle:
            table=list(csv.DictReader(handle))
        counts=[]
        for threshold in [.5,.6,.7]:
            codes,mask=safe_transition(arrays[2021],arrays[2026],supports[2021],supports[2026],threshold)
            raster_positive=set(int(c) for c in np.unique(codes[mask]))
            csv_positive={int(r['from_code'])*9+int(r['to_code']) for r in table if float(r['confidence_threshold'])==threshold and float(r['area_m2'])>0}
            # Edge conventions differ: exact areas are not claimed here.
            counts.append({'threshold':threshold,'matched_pixels':int(mask.sum()),
                'changed_pixels':int((mask&(arrays[2021][11]!=arrays[2026][11])).sum()),
                'positive_transition_categories_equal_csv':raster_positive==csv_positive,
                'projected_count_area_m2':int(mask.sum())*100})
        report['threshold_pixel_diagnostics']=counts
        report['status']='raster_integrity_checked_scientific_release_blocked'
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--exports',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    try:
        report=verify(args.exports,json.loads(args.manifest.read_text()))
    except (ValueError, rasterio.errors.RasterioError) as error:
        args.output.write_text(json.dumps({'status':'raster_integrity_failed','publication_ready':False,'error':str(error)},indent=2)+'\n')
        raise SystemExit(str(error))
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
