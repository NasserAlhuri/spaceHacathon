"""Retrieve and de-identify a tiled OSM reference snapshot for this study window."""
from pathlib import Path
import json,urllib.request,urllib.parse,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'analysis-config.json').read_text());w,s,e,n=config['bbox_wgs84']
queries=[]
for y in range(4):
 for x in range(4):
  b=[w+(e-w)*x/4,s+(n-s)*y/4,w+(e-w)*(x+1)/4,s+(n-s)*(y+1)/4]
  queries.append('https://api.openstreetmap.org/api/0.6/map?bbox='+','.join(f'{v:.6f}' for v in b))
def fetch(url):
 req=urllib.request.Request(url,headers={'User-Agent':'UrbanHeatAI-research-pilot/1.0'})
 with urllib.request.urlopen(req,timeout=90) as r:return ET.fromstring(r.read())
parts=list(ThreadPoolExecutor(max_workers=3).map(fetch,queries))
nodes={};ways={}
for part in parts:
 for el in part.findall('node'):nodes[el.attrib['id']]=el
 for el in part.findall('way'):
  tags={t.attrib['k']:t.attrib['v'] for t in el.findall('tag')}
  if tags.get('building') not in [None,'no'] or tags.get('natural') in ['water','coastline'] or tags.get('landuse')=='grass':ways[el.attrib['id']]=el
needed={r.attrib['ref'] for el in ways.values() for r in el.findall('nd')}
out=ET.Element('osm',version='0.6',generator='UrbanHeat AI filtered public reference')
for key in sorted(needed,key=int):
 if key not in nodes:continue
 el=nodes[key];ET.SubElement(out,'node',{k:el.attrib[k] for k in ['id','lat','lon']})
for key in sorted(ways,key=int):
 el=ways[key];dest=ET.SubElement(out,'way',{k:el.attrib[k] for k in ['id','timestamp'] if k in el.attrib})
 for r in el.findall('nd'):ET.SubElement(dest,'nd',ref=r.attrib['ref'])
 for tag in el.findall('tag'):
  if tag.attrib['k'] in ['building','natural','landuse']:ET.SubElement(dest,'tag',tag.attrib)
ref=ROOT/'data/sample_input/reference';ref.mkdir(parents=True,exist_ok=True)
ET.ElementTree(out).write(ref/'osm-map.osm',encoding='utf-8',xml_declaration=True)
meta={'source':'OpenStreetMap contributors','download_date':config['osm_download_date'],'query_urls':queries,'bbox_wgs84':config['bbox_wgs84'],'licence':'ODbL 1.0','filter':'Building, water, grass and coastline ways plus referenced coordinates. Contributor identifiers and unrelated tags removed. Multipolygon relations not analysed.','ways':len(ways),'nodes':len(needed),'complete_node_references':all(k in nodes for k in needed)}
(ROOT/'metadata/reference-provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({k:meta[k] for k in ['ways','nodes','complete_node_references']}))
