'use strict';
const $=id=>document.getElementById(id);
const NS='http://www.w3.org/2000/svg';
let data=null,state={date:'2026-09-30',layer:'priority',cell:null},view={x:0,y:0,w:1830,h:2100},drag=null,dragged=false;
const info={buildings:{title:'Mapped building footprint',unit:'%',description:'OSM mapped building pixels within retained land. Downloaded 5 October 2026. Mapping may be incomplete.'},priority:{title:'Investigation priority',unit:'score',description:'Relative screening score within this pilot. Weights: 50% surface heat, 30% low green signal, 20% mapped buildings. Site inspection is required.'},temperature:{title:'Surface temperature',unit:'°C',description:'Estimated surface temperature that morning. This is not air temperature or a health-risk score.'},greenery:{title:'Green pixel share',unit:'%',description:'Share of clear-land pixels passing NDVI ≥0.30. The threshold is provisional and sensitive to mixed pixels.'},uncertainty:{title:'Temperature uncertainty',unit:'K',description:'Landsat ST_QA estimate. Higher values mean less certainty. Not a confidence interval.'}};
function render(){
 if(!data)return;
 const meta=data.layers[state.layer],text=info[state.layer];
 $('layer-image').setAttribute('href',`assets/${state.layer}-${state.date}.png`);
 $('layer-image').style.opacity=Number($('opacity').value)/100;
 $('map-caption').textContent=state.layer==='priority'?'Planning shortlist · accepted dates':state.layer==='buildings'?'Mapped buildings · downloaded 5 October 2026':`${new Date(state.date+'T12:00:00Z').toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'})} · ${text.title.toLowerCase()}`;
 $('legend-title').textContent=text.title;$('legend-units').textContent=text.unit;
 $('gradient').style.background=`linear-gradient(90deg,${meta.colors.join(',')})`;
 $('legend-min').textContent=`${meta.min.toFixed(state.layer==='uncertainty'?1:0)} ${text.unit}`;
 $('legend-max').textContent=`${meta.max.toFixed(state.layer==='uncertainty'?1:0)} ${text.unit}`;
 $('legend-description').textContent=text.description;
 document.querySelectorAll('[data-layer]').forEach(b=>{const active=b.dataset.layer===state.layer;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
 renderCell();
}
function renderCell(){
 $('selection').replaceChildren();
 if(!state.cell){$('cell-badge').textContent='No selection';$('cell-details').innerHTML='<p class="empty">Select a cell to see temperature, greenery and uncertainty together.</p>';$('cell-select').value='';return;}
 const cell=data.cells.find(c=>c.id===state.cell),v=cell.values[state.date];
 $('cell-select').value=cell.id;$('cell-badge').textContent=cell.id;
 const polygon=document.createElementNS(NS,'polygon');polygon.setAttribute('points',cell.points.map(p=>p.join(',')).join(' '));$('selection').append(polygon);
 const planningText=cell.planning?`<div class="metric"><span>Investigation rank</span><strong>${cell.planning.investigation_rank} of ${data.planning.reported_cells}</strong></div><p class="cell-note">Rank ${cell.planning.scenario_best_rank}–${cell.planning.scenario_worst_rank} across ${cell.planning.scenarios_eligible} settings. Observed coverage: ${cell.planning.retained_cell_pct.toFixed(0)}%. ${cell.planning.recommendation}</p>`:'<p class="cell-note">Context cell: it does not pass the urban candidate screen. No investigation rank is assigned. Incomplete building mapping and historical land cover can affect eligibility.</p>';
 $('cell-details').innerHTML=`<div class="metrics"><div class="metric"><span>Surface temperature</span><strong>${v.temperature.toFixed(1)}°C</strong></div><div class="metric"><span>Green pixel share</span><strong>${v.greenery.toFixed(1)}%</strong></div><div class="metric"><span>Temperature uncertainty</span><strong>${v.uncertainty.toFixed(2)} K</strong></div></div><div class="metric"><span>Mapped building footprint</span><strong>${v.buildings.toFixed(1)}%</strong></div><div class="metric"><span>Historical built-up land (2021)</span><strong>${v.historicalBuilt.toFixed(1)}%</strong></div>${planningText}<p class="cell-note">${cell.samples} retained 30 m samples in this 300 m cell. Same inland footprints on accepted dates. Temperature and uncertainty are cell medians.</p>`;

}
function selectCell(id){if(!data.cells.some(c=>c.id===id))throw new Error('Unknown cell.');state.cell=id;renderCell();$('map-status').textContent=`Selected ${id} · values shown in “Inspect an area”.`;}
function setMapView(input){
 if(!data)throw new Error('Map is still loading.');
 if(input===null||typeof input!=='object'||Array.isArray(input))throw new Error('Expected an object.');
 for(const k of Object.keys(input))if(!['date','layer','cell_id'].includes(k))throw new Error('Unknown input field.');
 if(input.date!==undefined&&!data.dates.includes(input.date))throw new Error('Choose an accepted observation date.');
 if(input.layer!==undefined&&!Object.hasOwn(info,input.layer))throw new Error('Unknown layer.');
 if(input.cell_id!==undefined&&!data.cells.some(c=>c.id===input.cell_id))throw new Error('Unknown cell.');
 // Validate every supplied field before changing visible state.
 if(input.date!==undefined)state.date=input.date;if(input.layer!==undefined)state.layer=input.layer;if(input.cell_id!==undefined)state.cell=input.cell_id;
 $('date').value=state.date;render();return {date:state.date,layer:state.layer,cell_id:state.cell,values:state.cell?data.cells.find(c=>c.id===state.cell).values[state.date]:null};
}
function point(event){return new DOMPoint(event.clientX,event.clientY).matrixTransform($('map').getScreenCTM().inverse());}
function updateView(){
 view.x=Math.max(-data.width*.1,Math.min(data.width*1.1-view.w,view.x));view.y=Math.max(-data.height*.1,Math.min(data.height*1.1-view.h,view.y));
 $('map').setAttribute('viewBox',`${view.x} ${view.y} ${view.w} ${view.h}`);
 const rect=$('map').getBoundingClientRect();$('scale-line').style.width=`${300*Math.min(rect.width/view.w,rect.height/view.h)}px`;
}
function zoom(factor,center){if(!data)return;const c=center??{x:view.x+view.w/2,y:view.y+view.h/2};const nw=Math.max(data.width/5,Math.min(data.width,view.w*factor));const f=nw/view.w;view={x:c.x-(c.x-view.x)*f,y:c.y-(c.y-view.y)*f,w:nw,h:view.h*f};updateView();}
function inside(p,cell){const xs=cell.points.map(q=>q[0]),ys=cell.points.map(q=>q[1]);return p.x>=Math.min(...xs)&&p.x<=Math.max(...xs)&&p.y>=Math.min(...ys)&&p.y<=Math.max(...ys);}
function inspectPoint(p){
 const row=Math.floor(p.y/30),col=Math.floor(p.x/30);
 if(row<0||col<0||row>=data.rasterShape[0]||col>=data.rasterShape[1]||!data.mask[row*data.rasterShape[1]+col]){state.cell=null;renderCell();$('map-status').textContent='Excluded footprint: no retained observation to report.';return;}
 const cell=data.cells.find(c=>inside(p,c));
 if(cell)selectCell(cell.id);else{state.cell=null;renderCell();$('map-status').textContent='Retained pixels, but insufficient coverage for a reported cell.';}
}
$('date').addEventListener('change',e=>setMapView({date:e.target.value}));
document.querySelectorAll('[data-layer]').forEach(b=>b.addEventListener('click',()=>setMapView({layer:b.dataset.layer})));
$('cell-select').addEventListener('change',e=>{if(e.target.value)selectCell(e.target.value);else{state.cell=null;renderCell();}});
$('opacity').addEventListener('input',()=>{$('opacity-value').textContent=$('opacity').value+'%';render();});
$('zoom-in').addEventListener('click',()=>zoom(.8));$('zoom-out').addEventListener('click',()=>zoom(1.25));$('reset').addEventListener('click',()=>{if(data){view={x:0,y:0,w:data.width,h:data.height};updateView();}});
$('map').addEventListener('wheel',e=>{if(!data)return;e.preventDefault();zoom(e.deltaY>0?1.12:.89,point(e));},{passive:false});
$('map').addEventListener('pointerdown',e=>{if(!data||e.button>0)return;drag={id:e.pointerId,start:{x:e.clientX,y:e.clientY},matrix:$('map').getScreenCTM().inverse(),view:{...view}};dragged=false;$('map').setPointerCapture(e.pointerId);});
$('map').addEventListener('pointermove',e=>{if(!drag||e.pointerId!==drag.id)return;const dx=e.clientX-drag.start.x,dy=e.clientY-drag.start.y;if(Math.hypot(dx,dy)>5)dragged=true;if(dragged){const a=new DOMPoint(drag.start.x,drag.start.y).matrixTransform(drag.matrix),b=new DOMPoint(e.clientX,e.clientY).matrixTransform(drag.matrix);view={...drag.view,x:drag.view.x-(b.x-a.x),y:drag.view.y-(b.y-a.y)};updateView();}});
$('map').addEventListener('pointerup',e=>{if(!drag||e.pointerId!==drag.id)return;const wasDragged=dragged;drag=null;if(!wasDragged)inspectPoint(point(e));});
$('map').addEventListener('pointercancel',()=>{drag=null;});
$('map').addEventListener('keydown',e=>{if(!data)return;if(e.key==='+'||e.key==='='){e.preventDefault();zoom(.8);}else if(e.key==='-'){e.preventDefault();zoom(1.25);}else if(e.key.startsWith('Arrow')){e.preventDefault();const d=view.w*.1;if(e.key==='ArrowLeft')view.x-=d;if(e.key==='ArrowRight')view.x+=d;if(e.key==='ArrowUp')view.y-=d;if(e.key==='ArrowDown')view.y+=d;updateView();}});
window.addEventListener('resize',()=>{if(data)updateView();});
async function initialize(){
 try{const response=await fetch('assets/data.json');if(!response.ok)throw new Error('Dataset unavailable');data=await response.json();view={x:0,y:0,w:data.width,h:data.height};
 for(const c of data.cells){const polygon=document.createElementNS(NS,'polygon');polygon.setAttribute('points',c.points.map(p=>p.join(',')).join(' '));$('cells').append(polygon);const option=document.createElement('option');option.value=c.id;option.textContent=c.id+(c.urbanCandidate?' · urban candidate':' · context');$('cell-select').append(option);}
 $('date').replaceChildren();for(const date of [...data.dates].reverse()){const option=document.createElement('option');option.value=date;option.textContent=new Date(date+'T12:00:00Z').toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric',timeZone:'UTC'});$('date').append(option);}state.date=data.dates.at(-1);$('date').value=state.date;
 $('date-count').textContent=data.dates.length+' dates';
 for(const id of ['base','mask-image','layer-image']){$(id).setAttribute('width',data.width);$(id).setAttribute('height',data.height);}
 $('footprint-stat').textContent=data.planning.urban_candidate_sample_footprint_km2.toFixed(2)+' km² urban';$('cell-count').textContent=data.planning.reported_cells+' urban candidates · '+data.cells.length+' observed cells';
 const list=$('priority-list');for(const c of data.cells.filter(c=>c.urbanCandidate).sort((a,b)=>a.planning.investigation_rank-b.planning.investigation_rank).slice(0,3)){const button=document.createElement('button');button.textContent=`${c.planning.investigation_rank}. ${c.id} · rank ${c.planning.scenario_best_rank}–${c.planning.scenario_worst_rank} in tested settings`;button.addEventListener('click',()=>selectCell(c.id));list.append(button);}
 render();updateView();
 const context=document.modelContext;
 if(context?.registerTool){try{await context.registerTool({name:'configure_urbanheat_map',title:'Explore the UrbanHeat map',description:'Select an accepted observation date, map layer or reported comparison cell. Returns the visible selection and values.',inputSchema:{type:'object',properties:{date:{type:'string',enum:data.dates},layer:{type:'string',enum:Object.keys(info)},cell_id:{type:'string',enum:data.cells.map(c=>c.id)}},additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute:setMapView});}catch(e){console.warn('Map tool registration unavailable.');}}
 }catch(e){$('map-caption').textContent='The map data could not load.';$('map-status').textContent='Please reload the page.';document.querySelectorAll('select,input,.layer-buttons button').forEach(x=>x.disabled=true);}
}
initialize();
