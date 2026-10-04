"""Checks that can detect actual data/support/QA and packaging errors."""
from pathlib import Path
import json,csv
import rasterio,numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
r=json.loads((OUT/'coastal-multidate-summary.json').read_text());p=json.loads((OUT/'planning-summary.json').read_text())
with rasterio.open(OUT/'common-inland-mask.tif') as s:mask=s.read(1)==1;tf=s.transform
assert int(mask.sum())==r['common_30m_samples']==p['common_samples']
assert abs(mask.sum()*abs(tf.a*tf.e)/1e6-p['common_footprint_km2'])<.00005
for date,folder in [('2026-09-14',ROOT/'data/sample_input/multidate/LC09_L2SP_162042_20260914_02_T1'),('2026-09-30',ROOT/'data/sample_input/landsat')]:
 with rasterio.open(folder/'lwir11.tif') as s:raw=s.read(1);assert s.transform==tf
 with rasterio.open(folder/'qa_pixel.tif') as s:q=s.read(1)
 with rasterio.open(folder/'qa_radsat.tif') as s:rad=s.read(1)
 with rasterio.open(folder/'qa.tif') as s:uq=s.read(1)*.01
 with rasterio.open(OUT/f'common-temp-{date}.tif') as s:stored=s.read(1)
 computed=raw.astype('float64')*.00341802+149-273.15
 assert np.max(np.abs(stored[mask]-computed[mask]))<.001
 assert not ((q[mask]&191)!=0).any() and not (rad[mask]!=0).any() and not (uq[mask]>2).any()
rows=list(csv.DictReader(open(OUT/'planning-cells.csv')));assert len(rows)==p['reported_cells'];assert len({x['cell_id'] for x in rows})==len(rows)
assert all(0<=float(x['investigation_score'])<=100 and 0<=float(x['mapped_building_pct'])<=100.001 for x in rows)
samples=list(csv.DictReader(open(OUT/'reference-samples.csv')));assert all(x['reference_source'].startswith('OSM') and x['human_confirmed']=='pending' for x in samples)
mapdata=json.loads((ROOT/'app/assets/data.json').read_text());assert sum(mapdata['mask'])==int(mask.sum()) and len(mapdata['cells'])==len(rows)
print(json.dumps({'samples':int(mask.sum()),'cells':len(rows),'source_checks':len(samples),'status':'pass'}))
