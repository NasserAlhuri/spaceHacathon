from pathlib import Path
import runpy,contextlib,io,json
import numpy as np
import rasterio
from rasterio.warp import reproject,Resampling
from rasterio.transform import Affine
from pyproj import Transformer
from PIL import Image
from matplotlib import colormaps
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):planning=runpy.run_path(str(root/'src/planning.py'));data=planning['d']
site=root/'app/assets';site.mkdir(parents=True,exist_ok=True)
TT=data['TT'];TS=data['TS'];common=data['common'];records=data['accepted'];OT=data['OT'];OC=data['OC'];TC=data['TC']
# One fixed projected extent for base imagery, layer rasters and cell outlines.
base_shape=(TS[0]*3,TS[1]*3);BT=Affine(10,0,TT.c,0,-10,TT.f)
latest=data['records'][-1]['rgb'];base=np.zeros((*base_shape,3),dtype='float32')
for k in range(3):reproject(latest[:,:,k],base[:,:,k],src_transform=OT,src_crs=OC,dst_transform=BT,dst_crs=TC,resampling=Resampling.bilinear)
Image.fromarray((np.clip(base,0,1)*255).astype('uint8')).save(site/'satellite.jpg',quality=92)
config={'width':TS[1]*30,'height':TS[0]*30,'dates':[r['date'] for r in records],'cells':[],'summary':data['report'],'attribution':'Contains modified Copernicus Sentinel data (2026). Landsat imagery courtesy of USGS.','layers':{'temperature':{'min':30,'max':60,'unit':'°C','colors':['#000004','#57106e','#bc3754','#f98e09','#fcffa4']},'greenery':{'min':0,'max':100,'unit':'%','colors':['#ffffe5','#e4f4ae','#77c679','#238443','#005a32']},'uncertainty':{'min':1.5,'max':2,'unit':'K','colors':['#edf8fb','#9ebcda','#8856a7','#810f7c','#4d004b']}}}
for rec in records:
 date=rec['date']
 greenery=np.divide(rec['greenfrac'],rec['landfrac'],out=np.full(TS,np.nan),where=rec['landfrac']>0)*100
 for layer,arr,cmap,lo,hi in [('temperature',rec['temp'],'inferno',30,60),('greenery',greenery,'YlGn',0,100),('uncertainty',rec['uq'],'BuPu',1.5,2)]:
  rgba=(colormaps[cmap](np.clip((arr-lo)/(hi-lo),0,1))*255).astype('uint8');rgba[:,:,3]=np.where(common,255,0)
  Image.fromarray(rgba).save(site/f'{layer}-{date}.png')
excluded=np.zeros((*TS,4),dtype='uint8');excluded[:,:,:3]=[210,221,229];excluded[:,:,3]=np.where(common,0,225);Image.fromarray(excluded).save(site/'excluded.png')
for layer,cmap in [('temperature','inferno'),('greenery','YlGn'),('uncertainty','BuPu')]:
 config['layers'][layer]['colors']=['#'+''.join(f'{int(v*255):02x}' for v in colormaps[cmap](float(t))[:3]) for t in np.linspace(0,1,9)]
# Exact raster sample lookup: don't mislabel a masked click as a measured cell.
config['planning']=planning['report']
config['layers']['buildings']={'min':0,'max':100,'unit':'%','colors':['#fff5f0','#fb6a4a','#67000d']}
config['layers']['priority']={'min':0,'max':100,'unit':'score','colors':['#000004','#b5367a','#fcfdbf']}
score=np.full(TS,np.nan)
for p in planning['rows']:
 r,c=[int(x) for x in p['cell_id'][1:].split('-')];score[r*10:min(r*10+10,TS[0]),c*10:min(c*10+10,TS[1])]=p['investigation_score']
for name,arr,cmap in [('buildings',np.divide(planning['build30'],data['records'][-1]['landfrac'],out=np.zeros(TS),where=data['records'][-1]['landfrac']>0)*100,'Reds'),('priority',score,'magma')]:
 config['layers'][name]['colors']=['#'+''.join(f'{int(v*255):02x}' for v in colormaps[cmap](float(t))[:3]) for t in np.linspace(0,1,9)]
 for date in config['dates']:
  rgba=(colormaps[cmap](np.clip(np.nan_to_num(arr)/100,0,1))*255).astype('uint8');rgba[:,:,3]=np.where(common&np.isfinite(arr),255,0);Image.fromarray(rgba).save(site/f'{name}-{date}.png')
config['mask']=common.astype('uint8').ravel().tolist();config['rasterShape']=list(TS)
trans=Transformer.from_crs('EPSG:4326',TC,always_xy=True)
context_by_id={p['cell_id']:p for p in planning['all_context_rows']}
for f in data['features']:
 points=[]
 for lon,lat in f['geometry']['coordinates'][0][:-1]:
  x,y=trans.transform(lon,lat);points.append([round(x-TT.c,3),round(TT.f-y,3)])
 p=context_by_id[f['properties']['cell_id']];cell={'id':p['cell_id'],'points':points,'samples':p['common_30m_samples'],'values':{}}
 for date in config['dates']:cell['values'][date]={'temperature':p['temp_c_'+date],'greenery':p['vegetation_pct_'+date],'uncertainty':p['st_qa_k_'+date],'buildings':p['mapped_building_pct'],'historicalBuilt':p['worldcover2021_built_pct']}
 cell['urbanCandidate']=p['urban_candidate']
 cell['planning']={k:p[k] for k in ['investigation_score','investigation_rank','scenario_best_rank','scenario_worst_rank','scenarios_eligible','scenario_top3_count','retained_cell_pct','recommendation']} if p['urban_candidate'] else None
 config['cells'].append(cell)
(site/'data.json').write_text(json.dumps(config,separators=(',',':')))
print('Created aligned satellite image, transparent layers and',len(config['cells']),'interactive cells.')
