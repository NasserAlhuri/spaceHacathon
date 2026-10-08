"""Select spatial diagnostic samples and render dated 2026 context read-only.

This is a convenience review, not an accuracy sample or paired change validation.
This is the retained pre-reference selection/2026-only renderer. The current
paired review uses render_dynamic_world_paired_review.py; do not rerun this
selector over completed review metadata. Original analytical inputs
and all export rasters are only read. Classes below the primary rule stay Unknown.
"""
import csv
import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from PIL import Image, ImageDraw
from validate_dynamic_world_rasters import GRID, CLASS_NAMES, finite_support, region_centres, accepted

ROOT=Path(__file__).resolve().parents[1]


def select_components(mask, count):
    chosen=[]
    pixels=np.flatnonzero(mask)
    # Small change/vegetation strata use exact 8-connected components. Large
    # stable/Unknown strata use deterministic separated quantiles without a new
    # optional dependency or any change to pinned baseline requirements.
    if len(pixels)<=50000:
        width=mask.shape[1];height=mask.shape[0];remaining=set(pixels.tolist());components=[]
        while remaining:
            seed=min(remaining);remaining.remove(seed);stack=[seed];members=[]
            while stack:
                current=stack.pop();members.append(current);row,col=divmod(current,width)
                for dr in [-1,0,1]:
                    for dc in [-1,0,1]:
                        rr,cc=row+dr,col+dc
                        if (dr or dc) and 0<=rr<height and 0<=cc<width:
                            n=rr*width+cc
                            if n in remaining:remaining.remove(n);stack.append(n)
            values=np.asarray(members);rows,cols=values//width,values%width
            k=((rows-rows.mean())**2+(cols-cols.mean())**2).argmin()
            components.append((int(rows[k]),int(cols[k]),len(members)))
        for point in sorted(components,key=lambda p:(-p[2],p[0],p[1])):
            if all((point[0]-p[0])**2+(point[1]-p[1])**2>=30**2 for p in chosen):chosen.append(point)
            if len(chosen)==count:break
    # Stable classes can be one large connected component: use separated quantiles.
    if len(chosen)<count:
        rows,cols=np.where(mask)
        for fraction in [.2,.8,.4,.6]:
            if not len(rows):break
            k=min(int(len(rows)*fraction),len(rows)-1);point=(int(rows[k]),int(cols[k]),0)
            if all((point[0]-p[0])**2+(point[1]-p[1])**2>=30**2 for p in chosen):chosen.append(point)
            if len(chosen)==count:break
    return chosen


def main():
    raw=ROOT/'data/dynamic_world/raw/2026-10-07'
    data={}
    for year in [2021,2026]:
        with rasterio.open(raw/f'AlKhor_DynamicWorld_September_{year}.tif') as s:data[year]=s.read()
    region=region_centres(data[2021].shape[1:]);region[:22]=False;region[-22:]=False;region[:,:22]=False;region[:,-22:]=False
    finite={y:finite_support(b,region) for y,b in data.items()}
    primary={y:accepted(b,finite[y],.6) for y,b in data.items()}
    sensitivity={y:accepted(b,finite[y],.5) for y,b in data.items()}
    common=sensitivity[2021]&sensitivity[2026]
    pair=data[2021][11]*9+data[2026][11]
    scl=np.zeros(region.shape,dtype='uint8')
    with rasterio.open(ROOT/'data/sample_input/multidate/S2B_39RWJ_20260915_0_L2A/scl.tif') as src:
        reproject(src.read(1),scl,src_transform=src.transform,src_crs=src.crs,
            dst_transform=GRID,dst_crs='EPSG:32639',resampling=Resampling.nearest)
    groups=[('sensitivity_bare_to_built',common&(pair==69),3),
        ('sensitivity_water_to_bare',common&(pair==7),3)]
    for code,name in [(60,'stable_built_primary'),(70,'stable_bare_primary'),(0,'stable_water_primary')]:
        groups.append((name,primary[2021]&primary[2026]&(pair==code),2))
    groups += [('stable_flooded_vegetation_sensitivity',common&(pair==30),2),
        ('vegetation_raw_label_rejected_at_primary',finite[2026]&(~primary[2026])&np.isin(data[2026][11],[1,2,3,4,5]),2),
        ('Unknown_with_dated_SCL_vegetation_context',finite[2026]&(~primary[2026])&(scl==4),2),
        ('Unknown_built_bare_context',finite[2026]&(~primary[2026])&(scl==5)&np.isin(data[2026][11],[6,7]),2)]
    points=[]
    transform=Transformer.from_crs(32639,4326,always_xy=True)
    for group,mask,count in groups:
        for row,col,size in select_components(mask,count):
            x,y=GRID*(col+.5,row+.5);lon,lat=transform.transform(x,y)
            p={'sample_id':f'DWR-{len(points)+1:02}','stratum':group,'longitude':round(lon,7),'latitude':round(lat,7),
                'easting':x,'northing':y,'row':row,'col':col,'component_pixels':size,
                'reference_2021':'missing; not reviewed','reference_2026':'2026-09-05 and 2026-09-15 packaged RGB',
                'status':'paired scientific review pending; no accepted change'}
            for year in [2021,2026]:
                label=int(data[year][11,row,col])
                p[f'raw_label_{year}']=CLASS_NAMES[label]
                p[f'primary_label_{year}']=CLASS_NAMES[label] if primary[year][row,col] else 'Unknown'
                p[f'sensitivity_label_{year}']=CLASS_NAMES[label] if sensitivity[year][row,col] else 'Unknown'
                p[f'confidence_{year}']=float(data[year][10,row,col]);p[f'observation_count_{year}']=int(data[year][9,row,col])
                p[f'p_built_{year}']=float(data[year][6,row,col]);p[f'p_bare_{year}']=float(data[year][7,row,col])
            points.append(p)
    with (ROOT/'metadata/dynamic-world-scientific-samples.csv').open('w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(points[0]));w.writeheader();w.writerows(points)
    images=ROOT/'results/dynamic-world-scientific-context';images.mkdir(exist_ok=True)
    for page in range((len(points)+4)//5):
        selected=points[page*5:(page+1)*5]
        canvas=Image.new('RGB',(1100,100+len(selected)*240),'#f6f7f7');draw=ImageDraw.Draw(canvas)
        draw.text((12,10),'Actual DW samples; 2026-only context. No 2021 RGB / paired validation. Predictions remain unvalidated.',fill='#111111')
        for i,p in enumerate(selected):
            top=50+i*240
            draw.text((12,top),f"{p['sample_id']}: {p['stratum']}",fill='#111111')
            draw.text((12,top+22),f"0.50: {p['sensitivity_label_2021']} -> {p['sensitivity_label_2026']}",fill='#111111')
            draw.text((12,top+44),f"0.60: {p['primary_label_2021']} -> {p['primary_label_2026']}",fill='#111111')
            draw.text((12,top+66),f"Confidence: {p['confidence_2021']:.4f} / {p['confidence_2026']:.4f}",fill='#111111')
            draw.text((12,top+88),f"{p['latitude']:.7f}, {p['longitude']:.7f}; component {p['component_pixels']} px",fill='#111111')
            for j,date in enumerate(['20260905','20260915']):
                base=ROOT/f'data/sample_input/multidate/S2B_39RWJ_{date}_0_L2A'
                bands=[]
                for name in ['red','green','blue']:
                    with rasterio.open(base/f'{name}.tif') as s:
                        row,col=s.index(p['easting'],p['northing'])
                        bands.append(s.read(1,window=rasterio.windows.Window(col-20,row-20,41,41),boundless=True,fill_value=0))
                rgb=np.clip(np.stack(bands,axis=-1)/3500,0,1)
                image=Image.fromarray((rgb*255).astype('uint8')).resize((180,180),Image.Resampling.NEAREST)
                d=ImageDraw.Draw(image);d.rectangle((88,88,92,92),outline='#ffcc00',width=1)
                x=600+j*240;canvas.paste(image,(x,top+20))
                draw.text((x,top),f'{date[:4]}-{date[4:6]}-{date[6:]} Sentinel-2 L2A',fill='#111111')
                with rasterio.open(base/'scl.tif') as s:p[f'scl_{date}']=int(next(s.sample([(p['easting'],p['northing'])]))[0])
                draw.text((x,top+208),f"SCL {p[f'scl_{date}']}; 410 m context",fill='#111111')
        draw.text((12,canvas.height-30),'Gold: approx. 10 m target. Contains modified Copernicus Sentinel data (2026). No overall accuracy estimate.',fill='#111111')
        canvas.save(images/f'page-{page+1}.png')
    report={'status':'samples_prepared_for_visual_diagnostic','sample_count':len(points),'samples':points,
        'selection':'largest 8-connected components for small change/vegetation strata; separated quantiles for large stable/Unknown strata; 300 m within-stratum spacing where available; convenience review only',
        '2021_RGB':'missing; no historical label accepted','2026_source_dates':['2026-09-05','2026-09-15'],
        'independence':'Source Sentinel context is not independent ground truth; SCL is a screening aid, not class truth',
        'matched_support':'same original probability/count thresholds; primary Unknown retained',
        'baseline_analysis':'read-only; no rerun or ranking changes','scientific_release':False}
    (ROOT/'results/dynamic-world-scientific-sample-selection.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'Prepared {len(points)} unvalidated samples and dated 2026 context; no 2021 imagery or accepted change claim.')


if __name__=='__main__':main()
