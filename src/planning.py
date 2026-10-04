"""Open land-cover baseline, independent contributed-map checks and investigation priorities."""
from pathlib import Path
import runpy,contextlib,io,json,csv,xml.etree.ElementTree as ET
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.warp import reproject,Resampling,transform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results';REF=ROOT/'data/sample_input/reference'
with contextlib.redirect_stdout(io.StringIO()): d=runpy.run_path(str(ROOT/'src/coastal_multidate.py'))
OS,OT,OC,TS,TT,TC=d['OS'],d['OT'],d['OC'],d['TS'],d['TT'],d['TC'];common=d['common'];accepted=d['accepted']
xml=ET.parse(REF/'osm-map.osm').getroot();nodes={n.attrib['id']:(float(n.attrib['lon']),float(n.attrib['lat'])) for n in xml.findall('node')}
polygons={'building':[],'water':[],'grass':[]};features=[]
for w in xml.findall('way'):
 tags={t.attrib['k']:t.attrib['v'] for t in w.findall('tag')};refs=[n.attrib['ref'] for n in w.findall('nd')]
 group='building' if tags.get('building') not in [None,'no'] else 'water' if tags.get('natural')=='water' else 'grass' if tags.get('landuse')=='grass' else None
 if group is None or len(refs)<4 or refs[0]!=refs[-1] or not all(k in nodes for k in refs):continue
 xy=[nodes[k] for k in refs];xs,ys=transform('EPSG:4326',OC,[p[0] for p in xy],[p[1] for p in xy]);geom={'type':'Polygon','coordinates':[[list(p) for p in zip(xs,ys)]]}
 # Keep only polygons whose center-sampled raster touches the exact optical window.
 m=rasterize([(geom,1)],out_shape=OS,transform=OT,fill=0,dtype='uint8')
 if not m.any():continue
 polygons[group].append((geom,1));features.append({'type':'Feature','properties':{'osm_way_id':int(w.attrib['id']),'reference_class':group,'last_edit':w.attrib.get('timestamp'),'source':'OpenStreetMap contributors'},'geometry':{'type':'Polygon','coordinates':[[list(p) for p in xy]]}})
json.dump({'type':'FeatureCollection','features':features},open(OUT/'osm-reference.geojson','w'),indent=2)
masks={k:rasterize(v,out_shape=OS,transform=OT,fill=0,dtype='uint8').astype(bool) if v else np.zeros(OS,bool) for k,v in polygons.items()}
with rasterio.open(REF/'worldcover2021.tif') as src:
 wc=np.zeros(OS,dtype='uint8');reproject(src.read(1),wc,src_transform=src.transform,src_crs=src.crs,dst_transform=OT,dst_crs=OC,resampling=Resampling.nearest)
# Edge-eroded OSM polygon interiors avoid obvious mixed boundary pixels. Labels come from OSM, never predictions.
def erode(m):
 r=m.copy()
 for dy in [-1,0,1]:
  for dx in [-1,0,1]:
   shifted=np.zeros_like(m);h,w=m.shape;y0=max(0,dy);y1=min(h,h+dy);x0=max(0,dx);x1=min(w,w+dx)
   shifted[y0:y1,x0:x1]=m[y0-dy:y1-dy,x0-dx:x1-dx];r&=shifted
 return r
rng=np.random.default_rng(20261004);sample_rows=[];checks=[];latest=d['records'][-1]
for kind,m in masks.items():
 core=erode(m)
 # Remove contradictory tags and source-obscured locations before testing.
 for other,om in masks.items():
  if other!=kind:core&=~om
 if kind in ['grass','building']:core&=latest['land']
 candidates=np.argwhere(core);rng.shuffle(candidates);chosen=[]
 for r,c in candidates:
  if all((r-rr)**2+(c-cc)**2>=100 for rr,cc in chosen):chosen.append((int(r),int(c)))
  if len(chosen)>=30:break
 for r,c in chosen:
  x,y=OT*(c+.5,r+.5);lon,lat=transform(OC,'EPSG:4326',[x],[y]);water=bool(d['unionwater'][r,c]);green=bool(latest['ndvi'][r,c]>=.3)
  sample_rows.append({'sample_id':f'{kind}-{len([s for s in sample_rows if s["reference_class"]==kind])+1:02d}','reference_class':kind,'reference_source':'OSM contributed polygon interior, downloaded 2026-10-04','longitude':lon[0],'latitude':lat[0],'optical_row':r,'optical_column':c,'screened_water':int(water),'ndvi':float(latest['ndvi'][r,c]),'ndvi_green_at_0_3':int(green),'worldcover2021_class':int(wc[r,c]),'human_confirmed':'pending'})
 rows=[s for s in sample_rows if s['reference_class']==kind]
 checks.append({'reference_class':kind,'eligible_core_10m_pixels':int(core.sum()),'spaced_samples':len(rows),'screened_water_percent':round(float(np.mean([s['screened_water'] for s in rows])*100),1) if rows else None,'ndvi_green_percent':round(float(np.mean([s['ndvi_green_at_0_3'] for s in rows])*100),1) if rows else None,'worldcover_built_up_percent':round(float(np.mean([s['worldcover2021_class']==50 for s in rows])*100),1) if rows else None})
# Independent contributed shoreline geometry. Water lies to the right of an OSM coastline way.
from shapely.geometry import LineString,Point
from shapely.ops import unary_union
coastlines=[]
for way in xml.findall('way'):
 tags={t.attrib['k']:t.attrib['v'] for t in way.findall('tag')};refs=[n.attrib['ref'] for n in way.findall('nd')]
 if tags.get('natural')!='coastline' or not all(k in nodes for k in refs):continue
 xy=[nodes[k] for k in refs];xs,ys=transform('EPSG:4326',OC,[p[0] for p in xy],[p[1] for p in xy]);coastlines.append(LineString(list(zip(xs,ys))))
allcoast=unary_union(coastlines);offshore=[]
for line in coastlines:
 for at in np.arange(50,line.length,100):
  a=line.interpolate(max(0,at-5));b=line.interpolate(min(line.length,at+5));pt=line.interpolate(at);dx=b.x-a.x;dy=b.y-a.y;length=np.hypot(dx,dy)
  if length==0:continue
  x=pt.x+60*dy/length;y=pt.y-60*dx/length
  if allcoast.distance(Point(x,y))<40:continue
  c,r=~OT*(x,y);r,c=int(np.floor(r)),int(np.floor(c))
  if 0<=r<OS[0] and 0<=c<OS[1] and all((r-rr)**2+(c-cc)**2>=100 for rr,cc in offshore):offshore.append((r,c))
rng.shuffle(offshore);offshore=offshore[:30]
for i,(r,c) in enumerate(offshore,1):
 x,y=OT*(c+.5,r+.5);lon,lat=transform(OC,'EPSG:4326',[x],[y]);sample_rows.append({'sample_id':f'coastal-water-{i:02d}','reference_class':'coastal_water','reference_source':'OSM coastline right side at 60m, >=40m from any mapped coast','longitude':lon[0],'latitude':lat[0],'optical_row':r,'optical_column':c,'screened_water':int(d['unionwater'][r,c]),'ndvi':float(latest['ndvi'][r,c]),'ndvi_green_at_0_3':int(latest['ndvi'][r,c]>=.3),'worldcover2021_class':int(wc[r,c]),'human_confirmed':'pending'})
checks.append({'reference_class':'coastal_water','eligible_core_10m_pixels':None,'spaced_samples':len(offshore),'screened_water_percent':round(float(np.mean([d['unionwater'][r,c] for r,c in offshore])*100),1) if offshore else None,'ndvi_green_percent':round(float(np.mean([latest['ndvi'][r,c]>=.3 for r,c in offshore])*100),1) if offshore else None,'worldcover_built_up_percent':None})
with open(OUT/'reference-samples.csv','w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=list(sample_rows[0]));writer.writeheader();writer.writerows(sample_rows)
# Matched supports: average mapped building indicators only where optical land is observed.
build30=d['avg'](masks['building']&latest['land']);wc30=d['avg']((wc==50)&latest['land'])
rows=[]
for original in d['rows']:
 p=dict(original);r,c=[int(x) for x in p['cell_id'][1:].split('-')];win=np.s_[r*10:min(r*10+10,TS[0]),c*10:min(c*10+10,TS[1])];v=common[win];den=latest['landfrac'][win][v].sum()
 p['mapped_building_pct']=float(build30[win][v].sum()/den*100);p['worldcover2021_built_pct']=float(wc30[win][v].sum()/den*100);p['retained_cell_pct']=float(v.mean()*100)
 p['mean_date_median_temp_c']=float(np.mean([p['temp_c_'+rec['date']] for rec in accepted]));p['mean_date_green_pixel_pct']=float(np.mean([p['vegetation_pct_'+rec['date']] for rec in accepted]));rows.append(p)
def rank(values):
 a=np.asarray(values);return np.array([((a<x).sum()+.5*(a==x).sum())/len(a) for x in a])
heat=rank([p['mean_date_median_temp_c'] for p in rows]);green=rank([p['mean_date_green_pixel_pct'] for p in rows]);built=rank([p['mapped_building_pct'] for p in rows])
for i,p in enumerate(rows):p['investigation_score']=float(100*(.5*heat[i]+.3*(1-green[i])+.2*built[i]))
order=sorted(range(len(rows)),key=lambda i:(-rows[i]['investigation_score'],rows[i]['cell_id']))
for place,i in enumerate(order,1):rows[i]['investigation_rank']=place
# Stability across NDVI, water buffer, QA, cell coverage and weight choices, with the SAME two dates.
scenarios=[];ranks_by_id={p['cell_id']:[] for p in rows}
for buffer,qa,ndvi,min_samples in [(60,2,t,25) for t in [.2,.3,.4]]+[(b,2,.3,25) for b in [30,100]]+[(60,q,.3,25) for q in [2.5,3]]+[(60,2,.3,50)]:
 inlandfrac=d['avg'](d['inland'](buffer));m=np.logical_and.reduce([rec['base']&(rec['uq']<=qa)&(inlandfrac>=.9) for rec in accepted]);eligible=[]
 for p in rows:
  r,c=[int(x) for x in p['cell_id'][1:].split('-')];w=np.s_[r*10:min(r*10+10,TS[0]),c*10:min(c*10+10,TS[1])];v=m[w]
  if v.sum()<min_samples:continue
  temp=np.mean([np.median(rec['temp'][w][v]) for rec in accepted]);greens=[]
  for rec in accepted:
   gf=d['avg'](rec['land']&(rec['ndvi']>=ndvi));greens.append(gf[w][v].sum()/rec['landfrac'][w][v].sum()*100)
  bc=build30[w][v].sum()/latest['landfrac'][w][v].sum()*100;eligible.append((p['cell_id'],temp,np.mean(greens),bc))
 if not eligible:continue
 h=rank([p[1] for p in eligible]);g=rank([p[2] for p in eligible]);b=rank([p[3] for p in eligible]);scores=100*(.5*h+.3*(1-g)+.2*b);ix=sorted(range(len(eligible)),key=lambda i:(-scores[i],eligible[i][0]));top=[eligible[i][0] for i in ix[:3]]
 for n,i in enumerate(ix,1):ranks_by_id[eligible[i][0]].append(n)
 scenarios.append({'buffer_m':buffer,'qa_max_k':qa,'ndvi_threshold':ndvi,'min_cell_samples':min_samples,'common_samples':int(m.sum()),'eligible_cells':len(eligible),'top3':','.join(top)})
for weights in [(1,0,0),(.5,.5,0),(1/3,1/3,1/3)]:
 scores=100*(weights[0]*heat+weights[1]*(1-green)+weights[2]*built);ix=sorted(range(len(rows)),key=lambda i:(-scores[i],rows[i]['cell_id']));top=[rows[i]['cell_id'] for i in ix[:3]]
 for n,i in enumerate(ix,1):ranks_by_id[rows[i]['cell_id']].append(n)
 scenarios.append({'buffer_m':60,'qa_max_k':2,'ndvi_threshold':.3,'min_cell_samples':25,'common_samples':int(common.sum()),'eligible_cells':len(rows),'top3':','.join(top),'weights':str(weights)})
for p in rows:
 ranks=ranks_by_id[p['cell_id']];p['scenario_best_rank']=min(ranks) if ranks else None;p['scenario_worst_rank']=max(ranks) if ranks else None;p['scenarios_eligible']=len(ranks);p['scenario_top3_count']=sum(r<=3 for r in ranks);p['recommendation']='Inspect pedestrian use, current shade and planting feasibility before choosing an intervention.'
for name,rr in [('planning-cells.csv',sorted(rows,key=lambda x:x['investigation_rank'])),('planning-sensitivity.csv',scenarios)]:
 fields=list(dict.fromkeys(k for row in rr for k in row))
 with open(OUT/name,'w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rr)
features=d['features']
for f in features:f['properties'].update(next(p for p in rows if p['cell_id']==f['properties']['cell_id']))
json.dump({'type':'FeatureCollection','features':features},open(OUT/'planning-cells.geojson','w'),indent=2)
report={'scope':'Exploratory shortlist for site investigation; not a heat-health risk model or intervention prescription.','score':'0.50 heat percentile + 0.30 inverse green-pixel percentile + 0.20 mapped-building percentile; 0-100 relative only within this pilot.','osm_download_date':'2026-10-04','osm_scope':'Closed tagged ways only, center-pixel rasterisation; multipolygon relations and unmapped buildings may be missed. Not total building density or paved area.','osm_polygon_counts':{k:len(v) for k,v in polygons.items()},'reference_checks':checks,'validation_limit':'OSM positive polygon checks are independent contributed reference checks for optical rules, not a representative accuracy assessment or field truth. WorldCover uses some OSM auxiliary inputs, so building agreement is not independent model validation. Reference ages vary; human confirmations pending.','common_samples':int(common.sum()),'common_footprint_km2':round(float(common.sum()*900/1e6),4),'reported_cells':len(rows),'top3':sorted(rows,key=lambda x:x['investigation_rank'])[:3],'sensitivity_scenarios':len(scenarios),'worldcover_scope':'2021 historical CatBoost-derived land cover, not current segmentation. Class 50 merges buildings, roads and structures.','unresolved':'No independent thermal calibration, air temperature, population, shade, heat-health validation or causal cooling estimate.'}
json.dump(report,open(OUT/'planning-summary.json','w'),indent=2)
# Actual evidence plots, not decorative imagery.
e=[OT.c,OT.c+OS[1]*10,OT.f-OS[0]*10,OT.f];te=[TT.c,TT.c+TS[1]*30,TT.f-TS[0]*30,TT.f]
fig,axs=plt.subplots(1,3,figsize=(15,6),facecolor='white')
axs[0].imshow(latest['rgb'],extent=e);axs[0].imshow(np.where(masks['building'],1,np.nan),extent=e,cmap=ListedColormap(['#f4516c']),vmin=0,vmax=1,alpha=.8);axs[0].set_title('Mapped building footprints · OSM')
cat=np.where(wc==80,0,np.where(wc==50,1,np.where(np.isin(wc,[10,20,30,40,90,95]),2,3)))
axs[1].imshow(cat,extent=e,cmap=ListedColormap(['#167fba','#ef476f','#1f9a65','#c3b59e']),vmin=0,vmax=3);axs[1].set_title('Historical land cover · WorldCover 2021')
score=np.full(TS,np.nan)
for p in rows:
 r,c=[int(x) for x in p['cell_id'][1:].split('-')];w=np.s_[r*10:min(r*10+10,TS[0]),c*10:min(c*10+10,TS[1])];score[w]=np.where(common[w],p['investigation_score'],np.nan)
im=axs[2].imshow(score,extent=te,cmap='magma',vmin=0,vmax=100,interpolation='nearest');axs[2].set_title('Relative investigation score · pilot only')
for p in report['top3']:
 r,c=[int(x) for x in p['cell_id'][1:].split('-')];x,y=TT*(c*10+5,r*10+5);axs[2].text(x,y,p['cell_id'],ha='center',color='white',fontsize=8,bbox={'facecolor':'#11263c','alpha':.8,'edgecolor':'none','pad':2})
for ax in axs:ax.set_xlabel('UTM east (m)');ax.set_xticks([]);ax.set_yticks([])
fig.colorbar(im,ax=axs[2],fraction=.035,pad=.02,label='Relative score')
fig.suptitle('UrbanHeat AI · land-cover baseline and planning shortlist',fontsize=17,fontweight='bold')
fig.text(.5,.055,'WorldCover: blue water, pink built-up, green vegetation, beige other · OSM footprints are contributed and may be incomplete\nShortlist requires site checks for pedestrian use, shade, ownership and planting feasibility. No health-risk or cooling benefit inferred.',ha='center',fontsize=10)
fig.subplots_adjust(bottom=.18,top=.84,wspace=.25);fig.savefig(OUT/'planning-map.png',dpi=160);plt.close(fig)
print(json.dumps({'cells':len(rows),'footprint_km2':report['common_footprint_km2'],'checks':checks,'top3':[p['cell_id'] for p in report['top3']]},indent=2))

# Review sheet shows source imagery and sample positions, without prediction labels.
fig,axs=plt.subplots(4,6,figsize=(12,9),facecolor='white')
for ax,sample in zip(axs.ravel(),sample_rows[:24]):
 r,c=sample['optical_row'],sample['optical_column'];y0=max(0,r-5);y1=min(OS[0],r+6);x0=max(0,c-5);x1=min(OS[1],c+6);ax.imshow(latest['rgb'][y0:y1,x0:x1]);ax.plot(c-x0,r-y0,'+',color='yellow',markersize=10);ax.set_title(sample['sample_id'],fontsize=10);ax.axis('off')
fig.suptitle('Reference review samples · Sentinel-2 RGB · 30 September 2026',fontsize=15);fig.tight_layout(rect=[0,0,1,.95]);fig.savefig(OUT/'reference-review.png',dpi=150);plt.close(fig)
