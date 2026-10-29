const form=document.querySelector('#farm'), output=document.querySelector('#output'), button=document.querySelector('#submit');
let latest=null;
const names={N:'Nitrogen',P:'Phosphorus',K:'Potassium',temperature:'Temperature',humidity:'Humidity',ph:'Soil pH',rainfall:'Rainfall'};
function el(tag,text,cls){const node=document.createElement(tag);if(text!==undefined)node.textContent=text;if(cls)node.className=cls;return node;}
document.querySelector('#sample').onclick=()=>{const sample={N:90,P:42,K:43,temperature:20.88,humidity:82,ph:6.5,rainfall:203,state:'Madhya Pradesh',city:'Indore',season:'Kharif'};for(const [k,v] of Object.entries(sample))form.elements[k].value=v;document.querySelector('#error').textContent='';};
form.onsubmit=async event=>{event.preventDefault();button.disabled=true;document.querySelector('#error').textContent='';try{
 const payload=Object.fromEntries(new FormData(form));for(const k of Object.keys(names))payload[k]=Number(payload[k]);
 const response=await fetch('/api/recommend',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const data=await response.json();if(!response.ok)throw Error(data.error||'Request failed');latest={inputs:payload,...data};render(data);
}catch(error){document.querySelector('#error').textContent=error.message;}finally{button.disabled=false;}};
function render(data){output.replaceChildren();output.hidden=false;document.querySelector('#placeholder').hidden=true;const best=data.recommendations[0];
 const hero=el('div',undefined,'recommendation');hero.append(el('p','02 / YOUR RECOMMENDATION','eyebrow'),el('p',best.crop,'crop'),el('p',`Ranking score ${best.score}/100 · Neighbour support ${best.neighbor_support}%`,'score'),el('p',`${data.location.city||'Your farm'}, ${data.location.state} · ${data.season}`,'score'),el('span',best.season_match?'No season penalty':'Season mismatch','badge'),el('span',best.regional_preference?'Regional preference applied':'No regional preference applied','badge'));output.append(hero);
 const detail=el('div',undefined,'panel details');detail.append(el('h3','How your readings compare'));const table=el('table');const header=el('tr');for(const h of ['Factor','Your value','Crop dataset range','Match'])header.append(el('th',h));table.append(header);
 for(const reason of best.reasons){const row=el('tr');row.append(el('td',names[reason.feature]),el('td',String(reason.value)),el('td',`${reason.low} – ${reason.high}`),el('td',reason.within?'Within':'Outside',reason.within?'ok':'warn'));table.append(row);}detail.append(table,el('p','Ranges describe dataset examples, not agronomic safety limits.','note'));
 detail.append(el('h3','Other nearby crop matches'));if(data.recommendations.length===1)detail.append(el('p','All nine nearest examples agree on one crop.','note'));
 for(const crop of data.recommendations.slice(1)){const row=el('div',undefined,'alternative');row.append(el('span',crop.crop),el('span',`${crop.score}/100`));detail.append(row);}
 for(const warning of data.warnings)detail.append(el('p',warning,'warnings'));
 detail.append(el('p',data.notice,'note'));const download=el('button','Download analysis (JSON)','quiet export');download.type='button';download.onclick=()=>{const blob=new Blob([JSON.stringify(latest,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=el('a');a.href=url;a.download='agromind-analysis.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};detail.append(download);output.append(detail);
}
