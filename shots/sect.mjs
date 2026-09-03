// Capture one section, with every reveal already fired.
// Usage: node shots/sect.mjs <page> <selector> <out.png> [width]
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const page=process.argv[2]||'01-daylight.html';
const sel=process.argv[3]||'#reels';
const out=process.argv[4]||'sect.png';
const W=Number(process.argv[5]||1440);
const H=Number(process.argv[6]||940);
const P=await open(W,H);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2500);
const h=Number(await P.evalJS(`document.body.scrollHeight`));
for(let y=0;y<h;y+=600){await P.evalJS(`scrollTo(0,${y})`);await sleep(140);}
await sleep(2200);
const top=Number(await P.evalJS(`Math.round(document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect().top+scrollY)`));
const hh=Number(await P.evalJS(`Math.round(document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect().height)`));
console.log(sel,'top',top,'height',hh);
let i=0;
const PAD=Number(process.env.PAD||0);
for(let y=top-PAD;y<top+hh;y+=H){
  await P.evalJS(`scrollTo(0,${y})`);
  await sleep(700);
  const s=await P.send('Page.captureScreenshot',{format:'png'});
  writeFileSync('shots/'+out.replace('.png',`-${++i}.png`),Buffer.from(s.data,'base64'));
}
P.close();process.exit(0);
