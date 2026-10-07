"""Prepare clearly unreviewed stable/Unknown candidates from the real transition file.

Context uses immutable dated 2026 Sentinel-2 inputs. No 2021 reference image is
available here, no changes are validated, and no teammate acceptance is inferred.
"""
import csv
import json
from pathlib import Path
import numpy as np
import rasterio
from pyproj import Transformer
from PIL import Image, ImageDraw
from validate_dynamic_world_rasters import region_centres

ROOT=Path(__file__).resolve().parents[1]
NAMES=['water','trees','grass','flooded_vegetation','crops','shrub_and_scrub','built','bare','snow_and_ice']


def main():
    with rasterio.open(ROOT/'data/dynamic_world/raw/2026-10-07/AlKhor_DW_transition_2021_2026.tif') as src:
        codes=src.read(1);grid=src.transform
        region=region_centres(codes.shape,grid)
    candidates=[]
    # Two separated row quantiles per available stable class. Convenience diagnostic,
    # never a probability sample or a claim of representative overall accuracy.
    for code in [0,60,70,255]:
        rr,cc=np.where(region&(codes==code))
        for q in [.25,.75]:
            k=min(len(rr)-1,int(len(rr)*q));row,col=int(rr[k]),int(cc[k])
            x,y=grid*(col+.5,row+.5)
            lon,lat=Transformer.from_crs(32639,4326,always_xy=True).transform(x,y)
            candidates.append({'sample_id':f'DW-{len(candidates)+1:02}',
                'longitude':round(lon,7),'latitude':round(lat,7),'easting':x,'northing':y,
                'transition_row':row,'transition_col':col,'primary_transition_code':code,
                'predicted_before':NAMES[code//9] if code!=255 else 'Unknown',
                'predicted_after':NAMES[code%9] if code!=255 else 'Unknown',
                'selection':'two separated row quantiles per stable/Unknown stratum; convenience diagnostics only',
                'prediction_source':'unmodified primary transition export; annual finite support verification pending',
                'reference_2021':'unavailable; not reviewed','reference_2026':'packaged Sentinel-2 L2A 2026-09-05 and 2026-09-15',
                'status':'unreviewed_candidate; no change accepted'})
    target=ROOT/'metadata/dynamic-world-review-candidates.csv'
    with target.open('w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(candidates[0]));w.writeheader();w.writerows(candidates)
    canvas=Image.new('RGB',(1120,8*220+110),'#f6f7f7');draw=ImageDraw.Draw(canvas)
    draw.text((15,10),'2026-only visual diagnostics; 2021 reference and annual finite-support checks are missing.',fill='#111111')
    draw.text((15,30),'Gold box: approximately 10 m target. Classification predictions are unvalidated; Unknown stays Unknown.',fill='#111111')
    for i,c in enumerate(candidates):
        top=70+i*220
        draw.text((10,top),f"{c['sample_id']} predicted {c['predicted_before']} -> {c['predicted_after']} at 0.60",fill='#111111')
        draw.text((10,top+20),f"{c['latitude']:.7f}, {c['longitude']:.7f}; code {c['primary_transition_code']}",fill='#111111')
        for j,date in enumerate(['20260905','20260915']):
            base=ROOT/f'data/sample_input/multidate/S2B_39RWJ_{date}_0_L2A'
            arrays=[]
            for band in ['red','green','blue']:
                with rasterio.open(base/f'{band}.tif') as s:
                    row,col=s.index(c['easting'],c['northing'])
                    patch=s.read(1,window=rasterio.windows.Window(col-20,row-20,41,41),boundless=True,fill_value=0)
                    arrays.append(patch)
            # Fixed reflectance stretch for all thumbnails; no classification tuning.
            rgb=np.clip(np.stack(arrays,axis=-1)/3500,0,1)
            image=Image.fromarray((rgb*255).astype('uint8')).resize((164,164),Image.Resampling.NEAREST)
            d=ImageDraw.Draw(image);d.rectangle((80,80,84,84),outline='#ffcc00',width=1)
            x=570+j*240;canvas.paste(image,(x,top+20))
            draw.text((x,top),f'{date[:4]}-{date[4:6]}-{date[6:]} Sentinel-2 L2A',fill='#111111')
            with rasterio.open(base/'scl.tif') as s:
                v=next(s.sample([(c['easting'],c['northing'])]))[0]
            c['scl_'+date]=int(v)
            draw.text((x,top+190),f'SCL at target: {int(v)}; 410 m context',fill='#111111')
    draw.text((15,canvas.height-30),'Contains modified Copernicus Sentinel data (2026). Same upstream imagery is not independent ground truth.',fill='#111111')
    canvas.save(ROOT/'results/dynamic-world-2026-diagnostic-context.png')
    (ROOT/'results/dynamic-world-review-selection.json').write_text(json.dumps({'status':'candidates_prepared_not_validated',
        'candidates':candidates,'changed_candidates_0_50':'pending annual composites; do not infer changed locations from a stable 0.60 raster',
        'vegetation_review':'required; absence from accepted transition classes is not absence from the city',
        'scientific_release':False},indent=2)+'\n')
    print('Eight unreviewed stable/Unknown candidates prepared; no 2021 imagery or changed-location validation claimed.')


if __name__=='__main__':main()
