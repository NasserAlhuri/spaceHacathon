/** Exercise map state and user controls without a network or external deployment. */
import fs from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const html=await fs.readFile(path.join(root,'app/index.html'),'utf8');
const source=await fs.readFile(path.join(root,'app/app.js'),'utf8');
const dataset=JSON.parse(await fs.readFile(path.join(root,'app/assets/data.json'),'utf8'));
const reviews=JSON.parse(await fs.readFile(path.join(root,'app/local-review.json'),'utf8'));
class Element {
 constructor(){this.children=[];this.style={};this.attributes={};this.events={};this.textContent='';this.innerHTML='';this.value='';this.hidden=false;this.disabled=false;this.classList={toggle(){}};}
 append(node){this.children.push(node);} replaceChildren(...nodes){this.children=nodes;} setAttribute(k,v){this.attributes[k]=v;} addEventListener(k,fn){this.events[k]=fn;} click(){this.events.click?.({target:this});} getBoundingClientRect(){return {width:900,height:700};}
}
async function environment(withReview=true){
 const elements=new Map([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new Element()]));elements.get('comparison').hidden=true;elements.get('opacity').value='100';
 const buttons=['temperature','greenery','buildings','priority','uncertainty'].map(layer=>{const b=new Element();b.dataset={layer};return b;});
 const document={getElementById(id){assert(elements.has(id),`Missing HTML element ${id}`);return elements.get(id);},createElement(){return new Element();},createElementNS(){return new Element();},querySelectorAll(selector){return selector==='[data-layer]'||selector==='select,input,.layer-buttons button'?buttons:[];},modelContext:{async registerTool(tool){document.registered=tool;}}};
 const sandbox={document,window:{addEventListener(){}},console,Date,Math,Object,Number,String,Error,Blob,URL,setTimeout,fetch:async filename=>({ok:filename==='assets/data.json'||withReview,json:async()=>structuredClone(filename==='assets/data.json'?dataset:reviews)})};
 const context=vm.createContext(sandbox);vm.runInContext(source.replace(/initialize\(\);\s*$/,'globalThis.mapReady=initialize();'),context);await context.mapReady;return {context,elements,document};
}
const {context,elements,document}=await environment();
assert.match(elements.get('cell-count').textContent,/373 urban candidates.*1111 observed cells/);
assert.equal(elements.get('priority-list').children.length,3);assert.equal(elements.get('case-study-list').children.length,reviews.cells.length);assert.equal(elements.get('cell-select').children.length,1111);
for(const review of reviews.cells){for(const date of dataset.dates){for(const layer of ['temperature','greenery','buildings','priority','uncertainty']){const result=context.setMapView({cell_id:review.cell_id,date,layer});assert.equal(result.cell_id,review.cell_id);assert.equal(result.values.temperature,dataset.cells.find(c=>c.id===review.cell_id).values[date].temperature);assert.equal(/Nasser confirms site visits/.test(elements.get('cell-details').innerHTML),Boolean(review.site_confirmation));assert.match(elements.get('cell-details').innerHTML,/Evidence pending/);assert(elements.get('cell-details').innerHTML.includes(review.name));assert(elements.get('cell-details').innerHTML.includes(date==='2026-09-14'?'2026-09-15':date));assert(await fs.stat(path.join(root,`app/assets/${layer}-${date}.png`)));}}}
const before=context.setMapView({cell_id:'V04-23',date:'2026-09-30',layer:'priority'});assert.throws(()=>context.setMapView({cell_id:'not-a-cell',date:'2026-09-14'}));assert.equal(context.setMapView({}).date,before.date);
elements.get('comparison-toggle').click();assert.equal(elements.get('comparison').hidden,false);assert.equal(elements.get('comparison-body').children.length,reviews.cells.length);
context.setMapView({date:'2026-09-14'});assert.match(elements.get('comparison-date').textContent,/2026-09-14/);
const csv=context.reviewCsv();assert.equal(csv.split('\r\n').length,reviews.cells.length*dataset.dates.length+1);assert.match(csv,/"2026-09-14","2026-09-15"/);assert.match(csv,/"site visit confirmed; detailed assessment pending"/);
elements.get('focus-selection').click();assert.match(elements.get('map').attributes.viewBox,/2214/);
const other=dataset.cells.find(c=>!c.urbanCandidate);context.selectCell(other.id);assert.match(elements.get('cell-details').innerHTML,/Context cell/);assert(!elements.get('cell-details').innerHTML.includes('Team-member observations'));
const missing=await environment(false);assert.equal(missing.elements.get('comparison-toggle').disabled,true);assert.match(missing.elements.get('review-status').textContent,/unavailable/);assert.equal(missing.context.setMapView({cell_id:'V04-23'}).cell_id,'V04-23');
const hostile=reviews.cells[0].name;reviews.cells[0].name='<img src=x onerror=alert(1)>';const escaped=await environment();escaped.context.selectCell('V04-23');assert(escaped.elements.get('cell-details').innerHTML.includes('&lt;img'));assert(!escaped.elements.get('cell-details').innerHTML.includes('<img src=x'));reviews.cells[0].name=hostile;
assert.equal(document.registered.name,'configure_urbanheat_map');
await fs.writeFile(path.join(root,'results/local-map-check.json'),JSON.stringify({checked_at:'2026-10-07',status:'passed',method:'Node VM with DOM adapter; control/state checks, not a full browser visual or touch-device test',checks:['1111 observed cells and 373 candidates available','five local reports across two dates and five layers; original top three retained','matching layer assets','invalid-input state unchanged','comparison updates with date','ten CSV rows with paired dates and visit/photo/geometry statuses; original visits not extended to new sites','selected-cell focus','context cells remain accessible','missing local-review metadata keeps satellite controls available','local evidence text safely escaped']},null,2)+'\n');
console.log('Map control and evidence checks passed; full browser visual and touch-device review remains separate.');
