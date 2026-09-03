import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const P=await open(1440,1000);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/01-daylight.html'});
await sleep(2400);
const h=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<h;y+=600){await P.evalJS(`scrollTo(0,${y})`);await sleep(110);}
const top=Number(await P.evalJS(`Math.round(document.querySelector('.ba').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${top-90})`);await sleep(2200);
console.log('after auto pass, tag =',await P.evalJS(`document.querySelector('.ba-tag').textContent`));
// press BEFORE
const r=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelector('.ba-seg button[data-state=before]').getBoundingClientRect();return{x:b.x+b.width/2,y:b.y+b.height/2}})())`));
for(const t of ['mousePressed','mouseReleased'])await P.send('Input.dispatchMouseEvent',{type:t,x:r.x,y:r.y,button:'left',clickCount:1});
await sleep(900);
console.log('after pressing BEFORE, tag =',await P.evalJS(`document.querySelector('.ba-tag').textContent`),
  'beforeOff=',await P.evalJS(`document.querySelector('.ba-frame img[data-state=before]').hasAttribute('data-off')`),
  'pressed=',await P.evalJS(`document.querySelector('.ba-seg button[data-state=before]').getAttribute('aria-pressed')`));
let s1=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/ba-before.png',Buffer.from(s1.data,'base64'));
// click the frame itself to flip back
const f=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelector('.ba-frame').getBoundingClientRect();return{x:b.x+b.width/2,y:b.y+b.height/2}})())`));
for(const t of ['mousePressed','mouseReleased'])await P.send('Input.dispatchMouseEvent',{type:t,x:f.x,y:f.y,button:'left',clickCount:1});
await sleep(900);
console.log('after clicking the frame, tag =',await P.evalJS(`document.querySelector('.ba-tag').textContent`));
P.close();process.exit(0);
