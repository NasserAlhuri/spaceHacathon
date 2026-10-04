"""Coastal-mask audit, sensitivity and comparison on fixed common footprints."""
from pathlib import Path
import json,csv
import numpy as np
import rasterio
from rasterio.warp import reproject,Resampling,transform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import MaxNLocator
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';META=ROOT/'metadata/multidate'
PAIRS=[('2026-09-06','S2B_39RWJ_20260905_0_L2A','LC08_L2SP_162042_20260906_02_T1'),('2026-09-14','S2B_39RWJ_20260915_0_L2A','LC09_L2SP_162042_20260914_02_T1'),('2026-09-30',None,None)]
with rasterio.open(ROOT/'data/sample_input/red.tif') as src:OT=src.transform;OC=src.crs;OS=src.shape
with rasterio.open(ROOT/'data/sample_input/landsat/lwir11.tif') as src:TT=src.transform;TC=src.crs;TS=src.shape;TP=src.profile.copy()
def load(path,shape,trans,crs,method=Resampling.nearest):
 with rasterio.open(path) as src:
  dest=np.full(shape,np.nan,dtype='float32')
  reproject(src.read(1).astype('float32'),dest,src_transform=src.transform,src_crs=src.crs,src_nodata=src.nodata,dst_transform=trans,dst_crs=crs,dst_nodata=np.nan,resampling=method)
 return dest
def avg(a):
 d=np.zeros(TS,dtype='float32');reproject(a.astype('float32'),d,src_transform=OT,src_crs=OC,dst_transform=TT,dst_crs=TC,resampling=Resampling.average);return d
def onopt(a):
 d=np.zeros(OS,dtype='float32');reproject(a.astype('float32'),d,src_transform=TT,src_crs=TC,dst_transform=OT,dst_crs=OC,resampling=Resampling.nearest);return d>.5
def dilate(a,radius):
 out=np.zeros_like(a);h,w=a.shape
 for dy in range(-radius,radius+1):
  for dx in range(-radius,radius+1):
   if dx*dx+dy*dy>radius*radius:continue
   y0=max(0,dy);y1=min(h,h+dy);x0=max(0,dx);x1=min(w,w+dx)
   out[y0:y1,x0:x1]|=a[y0-dy:y1-dy,x0-dx:x1-dx]
 return out
records=[];unionwater=np.zeros(OS,dtype=bool);persistentland=np.ones(OS,dtype=bool)
for date,sid,lid in PAIRS:
 om=json.load(open(META/f'{sid}.json' if sid else ROOT/'scene.json'))
 lm=json.load(open(META/f'{lid}.json' if lid else ROOT/'landsat-scene.json'))
 op=ROOT/'data/sample_input/multidate'/sid if sid else ROOT/'data/sample_input'
 lp=ROOT/'data/sample_input/multidate'/lid if lid else ROOT/'data/sample_input/landsat'
 scl=load(op/'scl.tif',OS,OT,OC)
 reflect={}
 for b in ['red','green','blue','nir','swir16']:
  a=load(op/f'{b}.tif',OS,OT,OC,Resampling.bilinear if b=='swir16' else Resampling.nearest)
  meta=om['assets'][b]['raster:bands'][0];offset=0 if om['properties'].get('earthsearch:boa_offset_applied') else meta.get('offset',0)
  reflect[b]=a*meta.get('scale',1)+offset
 def ratio(a,b):return np.divide(a-b,a+b,out=np.full(OS,np.nan),where=(a+b)>.01)
 ndvi=ratio(reflect['nir'],reflect['red']);mndwi=ratio(reflect['green'],reflect['swir16'])
 land=np.isin(scl,[4,5])&np.isfinite(ndvi)
 swater=scl==6;candidate=(mndwi>.2)&(ndvi<.1)&np.isfinite(ndvi)
 raw=load(lp/'lwir11.tif',TS,TT,TC)
 # QA zeros are meaningful; source nodata=1 (QA fill) becomes nan and is excluded explicitly.
 qraw=load(lp/'qa_pixel.tif',TS,TT,TC);q=np.nan_to_num(qraw,nan=1).astype('uint16')
 rad=load(lp/'qa_radsat.tif',TS,TT,TC);uq=load(lp/'qa.tif',TS,TT,TC)*.01;dist=load(lp/'cdist.tif',TS,TT,TC)*.01
 water=(q&128)!=0;bad=(q&63)!=0
 meta=lm['assets']['lwir11']['raster:bands'][0];temp=raw*meta['scale']+meta['offset']-273.15
 base=np.isfinite(temp)&(~bad)&(~water)&(rad==0)&np.isfinite(uq)&(dist>=1)
 combinedwater=swater|candidate|onopt(water)
 unionwater|=combinedwater;persistentland&=land
 lf=avg(land);gf=avg(land&(ndvi>=.3))
 known=np.isin(scl,[4,5,6]);qa_water_opt=onopt(water)
 audit={'date':date,'optical_scene_id':om['id'],'optical_date':om['properties']['datetime'][:10],'thermal_scene_id':lm['id'],'thermal_date':lm['properties']['datetime'][:10],'sentinel_clear_land_percent':round(float(land.mean()*100),2),'sentinel_water_percent':round(float(swater.mean()*100),2),'sentinel_uncertain_percent':round(float((~known).mean()*100),2),'landsat_water_percent_on_optical_grid':round(float(qa_water_opt.mean()*100),2),'scl_water_vs_landsat_water_disagreement_known_pixels_percent':round(float(((swater!=qa_water_opt)&known).sum()/known.sum()*100),2),'scl_clear_land_flagged_water_by_other_checks_percent':round(float((land&(candidate|qa_water_opt)).sum()/max(1,land.sum())*100),2),'thermal_nodata_percent':round(float((~np.isfinite(temp)).mean()*100),2),'qa_cloud_shadow_snow_fill_percent':round(float(bad.mean()*100),2)}
 records.append({'date':date,'ndvi':ndvi,'land':land,'landfrac':lf,'greenfrac':gf,'temp':temp,'uq':uq,'base':base,'audit':audit,'rgb':np.clip(np.stack([reflect['red'],reflect['green'],reflect['blue']],axis=-1)/.35,0,1)**(1/1.8)})
# Same fixed conservative inland mask across all dates; no invented coastline boundary.
def inland(buffer):
 result=persistentland&(~dilate(unionwater,buffer//10))
 n=(buffer+9)//10
 if n: result[:n,:]=False;result[-n:,:]=False;result[:,:n]=False;result[:,-n:]=False
 return result
strictopt=inland(60)
strictfrac=avg(strictopt)
for rec in records:
 rec['baseline']=rec['base']&(rec['uq']<=2)&(rec['landfrac']>=.7)
 rec['strict']=rec['base']&(rec['uq']<=2)&(strictfrac>=.9)
accepted=[r for r in records if r['strict'].any()]
common=np.logical_and.reduce([r['strict'] for r in accepted]) if accepted else np.zeros(TS,dtype=bool)
for r in records:r['accepted']=bool(r['strict'].any())
sens=[]
for buffer in [0,30,60,100]:
 lf=avg(inland(buffer))
 for uncertainty in [2,2.5,3]:
  m=np.logical_and.reduce([r['base']&(r['uq']<=uncertainty)&(lf>=.9) for r in records])
  sens.append({'buffer_m':buffer,'st_qa_max_k':uncertainty,'common_30m_samples':int(m.sum()),'common_sample_footprint_km2':round(float(m.sum()*900/1e6),4)})
audits=[]
for rec in records:
 a=rec['audit'];cm=common if rec['accepted'] else np.zeros(TS,dtype=bool);a['thermal_comparison_status']='accepted' if rec['accepted'] else 'excluded: no samples pass combined quality and inland filters';a.update({'baseline_samples':int(rec['baseline'].sum()),'strict_samples':int(rec['strict'].sum()),'common_samples':int(cm.sum()),'baseline_median_surface_temp_c':round(float(np.median(rec['temp'][rec['baseline']])),2) if rec['baseline'].any() else None,'strict_median_surface_temp_c':round(float(np.median(rec['temp'][rec['strict']])),2) if rec['strict'].any() else None,'common_median_surface_temp_c':round(float(np.median(rec['temp'][cm])),2) if cm.any() else None,'common_median_st_qa_k':round(float(np.median(rec['uq'][cm])),2) if cm.any() else None,'common_vegetation_percent':round(float(rec['greenfrac'][cm].sum()/rec['landfrac'][cm].sum()*100),2) if cm.any() else None})
 audits.append(a)
rows=[];features=[]
for r in range(0,TS[0],10):
 for c in range(0,TS[1],10):
  rr=min(r+10,TS[0]);cc=min(c+10,TS[1]);win=np.s_[r:rr,c:cc];v=common[win]
  if v.sum()<25:continue
  props={'cell_id':f'V{r//10:02d}-{c//10:02d}','common_30m_samples':int(v.sum())}
  for rec in accepted:
   k=rec['date'];props['temp_c_'+k]=float(np.median(rec['temp'][win][v]));props['vegetation_pct_'+k]=float(rec['greenfrac'][win][v].sum()/rec['landfrac'][win][v].sum()*100);props['st_qa_k_'+k]=float(np.median(rec['uq'][win][v]))
  rows.append(props)
  xy=[TT*(c,r),TT*(cc,r),TT*(cc,rr),TT*(c,rr),TT*(c,r)]
  xs,ys=transform(TC,'EPSG:4326',[p[0] for p in xy],[p[1] for p in xy])
  features.append({'type':'Feature','properties':props,'geometry':{'type':'Polygon','coordinates':[list(map(list,zip(xs,ys)))]}})
correlations={}
if len(rows)>2:
 for rec in accepted:
  d=rec['date'];correlations[d]=round(float(np.corrcoef([p['temp_c_'+d] for p in rows],[p['vegetation_pct_'+d] for p in rows])[0,1]),3)
report={'validation_status':'Consistency and visual quality audit only; no independent ground-truth accuracy assessment.','strict_mask':'Clear land in all 3 Sentinel dates; exclude union of SCL water, Landsat QA water and spectral water candidates; add 60m exclusion buffer and remove crop-border halo; >=90% inland optical footprint; ST_QA<=2K; cloud distance>=1km; cloud/shadow/fill/snow/water/saturation excluded.','spectral_water_rule':'MNDWI >0.20 and NDVI <0.10, illustrative uncalibrated flag, SWIR native20m resampled to10m.','accepted_thermal_dates':[r['date'] for r in accepted],'common_30m_samples':int(common.sum()),'common_sample_footprint_km2':round(float(common.sum()*900/1e6),4),'reported_fixed_300m_cells':len(rows),'cell_threshold':'At least 25 common delivered30m samples per cell (>=0.0225km2); thermal native100m, samples spatially dependent.','dates':audits,'sensitivity_scope':'All 3 thermal dates required; this differs from primary comparison of the 2 accepted dates.','sensitivity':sens,'descriptive_cell_pearson_r':correlations,'interpretation':'Only 3 September morning scenes; optical matches within 1 day for first2. Seasonal trends, causal cooling, ground-truth temperature and health risk are not established. Different weather, sensor, emissivity and masking affect values.'}
json.dump(report,open(OUT/'coastal-multidate-summary.json','w'),indent=2)
for name,data in [('coastal-date-audit.csv',audits),('coastal-sensitivity.csv',sens),('multidate-grid.csv',rows)]:
 with open(OUT/name,'w') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]) if data else ['cell_id']);w.writeheader();w.writerows(data)
json.dump({'type':'FeatureCollection','features':features},open(OUT/'multidate-grid.geojson','w'),indent=2)
profile=TP.copy();profile.update(dtype='uint8',count=1,nodata=0,compress='deflate')
with rasterio.open(OUT/'common-inland-mask.tif','w',**profile) as dst:dst.write(common.astype('uint8'),1)
for rec in records:
 profile=TP.copy();profile.update(dtype='float32',count=1,nodata=-9999,compress='deflate')
 a=np.where(common if rec['accepted'] else np.zeros(TS,dtype=bool),rec['temp'],-9999).astype('float32')
 with rasterio.open(OUT/f"common-temp-{rec['date']}.tif",'w',**profile) as dst:dst.write(a,1)
# Audit figure: visual context, source flags, and retained thermal footprints.
fig,axs=plt.subplots(1,3,figsize=(14,6),facecolor='#f7f8fa')
e=[OT.c,OT.c+OS[1]*10,OT.f-OS[0]*10,OT.f];te=[TT.c,TT.c+TS[1]*30,TT.f-TS[0]*30,TT.f]
axs[0].imshow(records[-1]['rgb'],extent=e);axs[0].set_title('30 Sep satellite view')
flags=np.zeros(OS);flags[~persistentland]=1;flags[unionwater]=2;flags[strictopt]=3
cmap=ListedColormap(['#e8c791','#8d96a5','#7eb7d0','#2b9669'])
axs[1].imshow(flags,extent=e,cmap=cmap,vmin=0,vmax=3,interpolation='nearest');axs[1].set_title('Coastal screening across dates')
axs[2].imshow(np.where(common,1,np.nan),extent=te,cmap=ListedColormap(['#2b9669']),vmin=0,vmax=1,interpolation='nearest');axs[2].set_facecolor('#e8edf0');axs[2].set_title(f'Common thermal footprints · {int(common.sum())}')
for ax in axs:ax.set_xlabel('UTM east (m)');ax.ticklabel_format(style='plain');ax.tick_params(labelsize=8);ax.xaxis.set_major_locator(MaxNLocator(4))
fig.suptitle('The Pearl · coastal-mask quality check',fontsize=18,fontweight='bold',y=.97)
fig.text(.5,.065,'Blue: water flags · Grey: uncertain/not persistent land · Tan: additional shoreline exclusion · Green: retained inland area\nConservative 60 m buffer; consistency check only, not verified coastline or ground-truth classification.',ha='center',fontsize=10)
fig.subplots_adjust(top=.83,bottom=.19,wspace=.27);fig.savefig(OUT/'coastal-audit.png',dpi=160);plt.close(fig)
fig,axs=plt.subplots(1,3,figsize=(14,6),facecolor='#f7f8fa');lo=35;hi=50
for ax,rec in zip(axs,records):
 ax.set_facecolor('#e8edf0');im=ax.imshow(np.where(common if rec['accepted'] else np.zeros(TS,dtype=bool),rec['temp'],np.nan),extent=te,cmap='inferno',vmin=lo,vmax=hi,interpolation='nearest');ax.set_title(rec['date']+(' · '+str(rec['audit']['common_median_surface_temp_c'])+'°C median' if rec['accepted'] else ' · excluded by QA'));ax.set_xlabel('UTM east (m)');ax.ticklabel_format(style='plain');ax.tick_params(labelsize=8);ax.xaxis.set_major_locator(MaxNLocator(4))
fig.suptitle('Surface temperature · 3 dates checked · 2 pass the uncertainty filter',fontsize=17,fontweight='bold',y=.97)
fig.subplots_adjust(top=.82,bottom=.19,wspace=.3,right=.87)
cax=fig.add_axes([.9,.25,.018,.45]);fig.colorbar(im,cax=cax,label='Satellite surface temperature (°C)')
fig.text(.5,.06,'Morning Landsat observations · 100 m thermal detail on a 30 m grid · Same colour scale\nWater/coastal/uncertain pixels excluded; date-to-date differences are not a long-term warming trend or proof of vegetation cooling.',ha='center',fontsize=10)
fig.savefig(OUT/'multidate-temperature.png',dpi=160);plt.close(fig)
print(json.dumps(report,indent=2))
