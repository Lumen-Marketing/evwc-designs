import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/03-plate.html'});await sleep(3200);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(90);}
const top=Number(await P.evalJS(`Math.round(document.querySelector('.rail').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${top-110})`);await sleep(900);
async function click(sel){const r=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelector('${sel}').getBoundingClientRect();return{x:b.x+b.width/2,y:b.y+b.height/2}})())`));
  for(const t of ['mousePressed','mouseReleased'])await P.send('Input.dispatchMouseEvent',{type:t,x:r.x,y:r.y,button:'left',clickCount:1});}
async function st(){return await P.evalJS(`(()=>{const n=document.querySelector('.readout').textContent;
 const at=[...document.querySelectorAll('.station')].findIndex(s=>s.hasAttribute('data-at'));
 const tk=[...document.querySelectorAll('.ticks i')].findIndex(t=>t.hasAttribute('data-at'));
 const nv=[...document.querySelectorAll('.rnav')].map(b=>b.disabled?'off':'on').join('/');
 const pl=[...document.querySelectorAll('.rail video')].filter(v=>!v.paused).length;
 return n+' | station '+at+' | tick '+tk+' | nav '+nv+' | playing '+pl;})()`);}
console.log('start ', await st());
for(let k=0;k<7;k++){ await click('.rnav[data-d="1"]'); await sleep(950); console.log('next  ', await st()); }
for(let k=0;k<2;k++){ await click('.rnav[data-d="-1"]'); await sleep(950); console.log('prev  ', await st()); }
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/g03-indexed.png',Buffer.from(s.data,'base64'));
P.close();process.exit(0);
