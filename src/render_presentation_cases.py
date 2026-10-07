"""Plot presentation-only site references from existing map imagery and geometry."""
import argparse
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from pyproj import Transformer


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    data=json.loads((root/'app/assets/data.json').read_text())
    reviews=json.loads((root/'app/local-review.json').read_text())
    cells={c['id']:c for c in data['cells']}
    extent=[0,data['width'],data['height'],0]
    image=Image.open(root/'app/assets/satellite.jpg')
    fig,axes=plt.subplots(1,3,figsize=(14,4.7))
    for ax,cid,title in zip(axes,['V04-23','V28-17','V18-26'],['Bus-stop road','Stadium parking','Reported jogging route']):
        cell=cells[cid];points=cell['points']
        x=sum(p[0] for p in points)/len(points);y=sum(p[1] for p in points)/len(points)
        ax.imshow(image,extent=extent);ax.add_patch(Polygon(points,fill=False,color='#fff05c',linewidth=2))
        ax.set_xlim(x-450,x+450);ax.set_ylim(y+450,y-450)
        ax.set_title(f'{cid} · {title}',fontsize=13)
        ax.set_xticks([]);ax.set_yticks([])
        if cid=='V18-26':
            xx,yy=Transformer.from_crs(4326,32639,always_xy=True).transform(51.524704,25.681077)
            # Existing app coordinates are metres from the packaged raster origin.
            ax.plot(xx-544635,2845905-yy,'o',color='#00ffff',markersize=7,label='Supplied point; route unknown')
            ax.legend(loc='lower left',fontsize=8)
        else:ax.text(.03,.03,'Cell outline; precise site extent unknown',transform=ax.transAxes,fontsize=8,backgroundcolor='white')
    fig.suptitle('Team-selected presentation examples; satellite ranking unchanged',fontsize=15)
    fig.text(.5,.01,'Existing September 2026 satellite context; no new photograph or surveyed route. Cell values are not point measurements.',ha='center',fontsize=9)
    fig.tight_layout(rect=[0,.06,1,.91]);args.output.parent.mkdir(parents=True,exist_ok=True)
    fig.savefig(args.output,dpi=180);plt.close(fig)


if __name__=='__main__':main()
