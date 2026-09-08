import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/02-site.html'});await sleep(3200);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(90);}
const top=Number(await P.evalJS(`Math.round(document.querySelector('.projx').getBoundingClientRect().top+scrollY)`));
const sheetY=Number(await P.evalJS(`Math.round(document.querySelector('.sheet').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${sheetY-620})`);await sleep(900);
async function click(sel){const r=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelector('${sel}').getBoundingClientRect();return{x:b.x+b.width/2,y:b.y+b.height/2}})())`));
  for(const t of ['mousePressed','mouseReleased'])await P.send('Input.dispatchMouseEvent',{type:t,x:r.x,y:r.y,button:'left',clickCount:1});}
async function state(){return await P.evalJS(`(()=>{const on=[...document.querySelectorAll('.frame')].findIndex(f=>f.hasAttribute('data-on'));
  return on+' | '+document.querySelector('.pcount').textContent+' | '+document.querySelector('.pcap b').textContent
  +' | cur cell '+[...document.querySelectorAll('.cell')].findIndex(c=>c.getAttribute('aria-current')==='true')
  +' | playing '+[...document.querySelectorAll('.projx video')].filter(v=>!v.paused).length;})()`);}
console.log('start      ', await state());
await click('.cell[data-i="2"]'); await sleep(1100); console.log('cell 03    ', await state());
await click('.pnav.next');        await sleep(1100); console.log('next       ', await state());
await click('.pnav.prev');        await sleep(1100); console.log('prev       ', await state());
await click('.pnav.prev');        await sleep(1100); console.log('prev       ', await state());
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/g02-clicked.png',Buffer.from(s.data,'base64'));
P.close();process.exit(0);
