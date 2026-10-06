"""Render evidence figures for the local-review deck from packaged assets."""
from pathlib import Path
import json
import numpy as np
import rasterio
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def main():
 data=json.loads((ROOT/'app/assets/data.json').read_text());review=json.loads((ROOT/'app/local-review.json').read_text())
 image=np.asarray(Image.open(ROOT/'app/assets/satellite.jpg'))
 cells={c['id']:c for c in data['cells']};width,height=data['width'],data['height']
 def satellite(ax):
  ax.imshow(image,extent=[0,width,height,0]);ax.set_xlabel('East within crop (m)');ax.set_ylabel('South within crop (m)');ax.tick_params(labelsize=9)
 def cell(ax,identifier,label=True):
  c=cells[identifier];points=np.array(c['points']);ax.add_patch(Polygon(points,closed=True,fill=False,edgecolor='#ffcc52',linewidth=2));x,y=points.mean(axis=0)
  if label:ax.text(x,y,identifier,color='white',fontsize=10,ha='center',va='center',bbox=dict(facecolor='#163d46',alpha=.9,pad=3))
 fig=plt.figure(figsize=(14,7),facecolor='#f7f6f1');gs=fig.add_gridspec(2,2,width_ratios=[1,1.45]);overview=fig.add_subplot(gs[:,0]);near=fig.add_subplot(gs[0,1]);stadium=fig.add_subplot(gs[1,1])
 satellite(overview);overview.set_title('Analyst-defined study window',fontsize=13);overview.add_patch(Polygon(review['study_boundary_points'],closed=True,fill=False,edgecolor='#33d6bf',linewidth=2,linestyle='--'))
 for c in review['cells']:cell(overview,c['cell_id'],False)
 overview.annotate('V04-23 / V04-24\nHospital road and land',(7200,1350),(1000,800),color='white',fontsize=10,arrowprops=dict(arrowstyle='->',color='white'),bbox=dict(facecolor='#163d46',alpha=.9,pad=4))
 overview.annotate('V28-17\nStadium parking',(5250,8550),(500,9600),color='white',fontsize=10,arrowprops=dict(arrowstyle='->',color='white'),bbox=dict(facecolor='#163d46',alpha=.9,pad=4))
 satellite(near);near.set_xlim(6400,7800);near.set_ylim(1800,900);cell(near,'V04-23');cell(near,'V04-24');near.set_title('Bus-stop road and adjacent hospital land',fontsize=13)
 with rasterio.open(ROOT/'data/sample_input/landsat/lwir11.tif') as src:
  from rasterio.warp import transform
  x,y=transform('EPSG:4326',src.crs,[51.5145504],[25.7175476]);x=x[0]-src.transform.c;y=src.transform.f-y[0]
 near.plot(x,y,'o',color='#33d6bf',markersize=7);near.annotate('Street View camera\nMarch 2023 reference',(x,y),(x-500,y+320),fontsize=9,color='white',arrowprops=dict(arrowstyle='->',color='white'),bbox=dict(facecolor='#163d46',alpha=.9,pad=3))
 satellite(stadium);stadium.set_xlim(4650,5950);stadium.set_ylim(9000,8100);cell(stadium,'V28-17');stadium.set_title('Reported event-dependent stadium parking',fontsize=13)
 fig.subplots_adjust(left=.05,right=.98,top=.92,bottom=.14,hspace=.58,wspace=.32)
 fig.text(.5,.045,'Base: packaged Sentinel-2, 30 September 2026 · Gold: 300 m cells · Teal dashed: study boundary\nLocal names and use are team-member observations; visits pending. Camera is not a surveyed stop point. Contains modified Copernicus Sentinel data (2026).',ha='center',fontsize=10)
 fig.savefig(ROOT/'results/local-review-map.png',dpi=160);plt.close(fig)
 # This figure replaces the rejected-scene panel with an explicit note, without changing data.
 fig,axs=plt.subplots(1,2,figsize=(13,6),facecolor='#f7f6f1')
 for ax,date in zip(axs,data['dates']):
  with rasterio.open(ROOT/f'results/common-temp-{date}.tif') as src:a=src.read(1,masked=True)
  ax.set_facecolor('#d2dde5');im=ax.imshow(a,cmap='inferno',vmin=30,vmax=60,interpolation='nearest');ax.set_title(date+' · accepted',fontsize=16);ax.set_xticks([]);ax.set_yticks([])
 fig.subplots_adjust(left=.04,right=.88,top=.86,bottom=.22,wspace=.15);cax=fig.add_axes([.91,.26,.018,.5]);fig.colorbar(im,cax=cax,label='Satellite surface temperature (°C)')
 fig.text(.5,.12,'6 September excluded: 0% of historical urban inland support passed the strict filters.\n94.4379 km² of common inland sample footprints. Grey: excluded or missing observations.',ha='center',fontsize=11)
 fig.text(.5,.035,'Morning surface observations, not air temperature. Native thermal detail about 100 m, delivered at 30 m.\nDate differences do not establish long-term cooling. Landsat imagery courtesy of USGS.',ha='center',fontsize=10)
 fig.savefig(ROOT/'results/accepted-temperature-review.png',dpi=160);plt.close(fig)
 print('Rendered two local-review evidence figures')
if __name__=='__main__':main()
