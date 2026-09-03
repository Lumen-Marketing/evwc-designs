import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const P=await open(1440,940);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/01-daylight.html'});
await sleep(2500);
const h=Number(await P.evalJS(`document.body.scrollHeight`));
for(let y=0;y<h;y+=600){await P.evalJS(`scrollTo(0,${y})`);await sleep(120);}
await sleep(1500);
const top=Number(await P.evalJS(`Math.round(document.querySelector('#services').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${top-30})`);await sleep(700);
const r=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelectorAll('.row a')[1].getBoundingClientRect();return{x:b.x+b.width*0.5,y:b.y+b.height/2}})())`));
await P.send('Input.dispatchMouseEvent',{type:'mouseMoved',x:r.x,y:r.y});
await sleep(1400);
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/hoverrow.png',Buffer.from(s.data,'base64'));
P.close();process.exit(0);
