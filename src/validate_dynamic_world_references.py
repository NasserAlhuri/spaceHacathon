"""Verify supplied reference identities, date metadata, grid and target QA.

This checker cannot establish image interpretation, independent ground truth or
scientific release readiness. Never edits references or original analysis.
"""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np
import rasterio
from validate_dynamic_world_rasters import GRID

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'metadata/dynamic-world-reference-manifest.json').read_text())
    files = manifest['unique_original_files']
    for name, record in files.items():
        data = (ROOT / name).read_bytes()
        assert len(data) == record['bytes'], name
        assert hashlib.sha256(data).hexdigest() == record['sha256'], name
    folder = ROOT / 'data/dynamic_world/reference/2026-10-08'
    with (folder / 'AlKhor_Sentinel2_Reference_provenance.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    with (ROOT / 'data/dynamic_world/raw/2026-10-07/AlKhor_DW_provenance.csv').open(newline='') as f:
        dw_rows = list(csv.DictReader(f))
    declared = {r['source_sentinel2_id']: r for r in dw_rows}
    targets = json.loads((ROOT / 'results/dynamic-world-scientific-sample-selection.json').read_text())['samples']
    report = {'status': 'reference_file_metadata_grid_and_target_checks_passed', 'files': [],
              'independent_remote_asset_readback': False,
              'capture_dates_source': 'Original user-supplied Code Editor provenance; not independently queried by this runtime',
              'scientific_release': False, 'qa_limit': 'QA60 native 60 m bits and 0% scene cloud are screening evidence, not perfect cloud/visibility truth',
              'duplicate': manifest['excluded_duplicate'], 'sample_count': len(targets)}
    for row, date in zip(rows, ['20210901', '20210926']):
        assert row['source_asset_id'].startswith('COPERNICUS/S2_HARMONIZED/' + date)
        assert row['source_asset_id'] in declared
        assert row['acquired_utc'] == declared[row['source_asset_id']]['acquired_utc']
        assert row['acquired_utc'][:10].replace('-', '') == date
        assert row['crs'] == 'EPSG:32639' and row['grid_transform'] == '10,0,544635,0,-10,2845905'
        assert [float(row[k]) for k in ['rgb_stretch_min','rgb_stretch_max','rgb_display_max']] == [0,3500,255]
        assert [int(row[k]) for k in ['nodata','qa60_cloud_bit','qa60_cirrus_bit','qa60_native_resolution_m']] == [65535,10,11,60]
        with rasterio.open(folder / f'AlKhor_Sentinel2_Reference_{date}.tif') as s:
            assert s.crs.to_epsg() == 32639 and s.transform == GRID
            assert (s.height,s.width,s.count) == (1057,1108,4)
            assert s.descriptions == ('red','green','blue','qa60')
            assert s.dtypes == ('uint16',)*4 and s.nodata == 65535
            a = s.read(); valid = np.all(a != 65535,axis=0)
            assert np.all(a[:3,valid] <= 255)
            target_qa=[]
            for p in targets:
                r,c=p['row'],p['col']; assert valid[r,c]
                assert GRID*(c+.5,r+.5) == (p['easting'],p['northing'])
                context=a[:,r-20:r+21,c-20:c+21]
                assert context.shape == (4,41,41) and np.all(context!=65535)
                target_qa.append({'sample_id':p['sample_id'],'qa60':int(a[3,r,c]),
                                  'cloud_or_cirrus_flag':bool(a[3,r,c]&3072)})
            report['files'].append({'filename':s.name.split('/')[-1], 'source_asset_id':row['source_asset_id'],
                'acquired_utc':row['acquired_utc'],'scene_cloud_percent':float(row['scene_cloud_percent']),
                'shape':[s.height,s.width],'crs':str(s.crs),'transform':list(s.transform)[:6],
                'bands':list(s.descriptions),'dtype':'UInt16','nodata':s.nodata,
                'all_grid_finite_valid_samples':int(valid.sum()),
                'valid_rgb_channel_samples_at_255':int((a[:3,valid]==255).sum()),
                'qa60_values':np.unique(a[3]).tolist(),
                'flagged_cloud_cirrus_valid_samples':int(((a[3]&3072!=0)&valid).sum()),
                'targets':target_qa})
    report['display_limits'] = '2021 exported display RGB at fixed 0..3500 DN -> 0..255; L1C and 2026 L2A brightness/colour are not quantitative change evidence. Clipping and 10 m mixtures limit exact labels.'
    (ROOT/'results/dynamic-world-reference-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Three unique files match recorded SHA256; dated source rows match original DW provenance; both grids and all 18 context/target checks passed. Classification truth is not checked by this program.')


if __name__ == '__main__':
    main()
