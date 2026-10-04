"""Optional retrieval of exact source crops. Existing packaged inputs are sufficient offline."""
from pathlib import Path
import os,json,urllib.request,urllib.parse,xml.etree.ElementTree as ET
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
ROOT=Path(__file__).resolve().parents[1];BBOX=[51.538,25.360,51.556,25.379];DATA=ROOT/'data/sample_input'
SCENES=[(ROOT/'scene.json',DATA,['red','green','blue','nir','swir16','scl']),(ROOT/'landsat-scene.json',DATA/'landsat',['lwir11','qa_pixel','qa_radsat','qa','cdist'])]
for path in sorted((ROOT/'metadata/multidate').glob('*.json')):
 scene=json.loads(path.read_text());bands=['red','green','blue','nir','swir16','scl'] if scene['id'].startswith('S2') else ['lwir11','qa_pixel','qa_radsat','qa','cdist'];SCENES.append((path,DATA/'multidate'/scene['id'],bands))
SCENES.append((ROOT/'metadata/worldcover.json',DATA/'reference',['map']))
options=dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',GDAL_HTTP_TIMEOUT=60,GDAL_HTTP_MAX_RETRY=2)
if os.environ.get('SSL_CERT_FILE'):options['GDAL_CURL_CA_BUNDLE']=os.environ['SSL_CERT_FILE']
for meta,directory,bands in SCENES:
 scene=json.loads(meta.read_text());directory.mkdir(parents=True,exist_ok=True)
 for band in bands:
  target=directory/('worldcover2021.tif' if band=='map' else band+'.tif')
  if target.exists():continue
  url=scene['assets'][band]['href'];signed=url
  if 'blob.core.windows.net' in url:
   with urllib.request.urlopen('https://planetarycomputer.microsoft.com/api/sas/v1/sign?href='+urllib.parse.quote(url,safe=''),timeout=60) as s:signed=json.load(s)['href']
  with rasterio.Env(**options),rasterio.open(signed) as src:
   bounds=transform_bounds('EPSG:4326',src.crs,*BBOX);window=from_bounds(*bounds,src.transform).round_offsets().round_lengths();arr=src.read(1,window=window);profile=src.profile.copy();profile.update(driver='GTiff',height=arr.shape[0],width=arr.shape[1],transform=src.window_transform(window),compress='deflate')
   with rasterio.open(target,'w',**profile) as dst:dst.write(arr,1)
  print('Fetched',scene['id'],band)
# OSM is a live reference database. Keep the packaged 4 October snapshot for exact reproduction.
# Do not replace it with a later snapshot while claiming identical results.
print('Satellite crops ready. The filtered OSM snapshot is packaged, with source query recorded in metadata/reference-provenance.json.')
