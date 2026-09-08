// Vertical gaps between named elements, measured on the rendered page.
// Usage: node shots/gap.mjs <page> <width> [height]
import {open,sleep} from './cdp.mjs';
const page=process.argv[2], W=+(process.argv[3]||1440), H=+(process.argv[4]||900);
const P=await open(W,H);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:W<500});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2200);
// walk the page so every .rv reveal fires, or a translateY(26px) is measured as a gap
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(90);}
await P.evalJS('scrollTo(0,0)');await sleep(900);
const out=await P.evalJS(`(()=>{
  const r=s=>{const e=document.querySelector(s);if(!e)return null;const b=e.getBoundingClientRect();
    return {top:Math.round(b.top+scrollY),bottom:Math.round(b.bottom+scrollY),h:Math.round(b.height)};};
  const sels=${JSON.stringify(process.argv.slice(5))};
  const o={};sels.forEach(s=>o[s]=r(s));
  o._vh=innerHeight;o._scrollW=document.documentElement.scrollWidth;o._clientW=document.documentElement.clientWidth;
  return JSON.stringify(o,null,1);})()`);
console.log(W+'w', out);
P.close();process.exit(0);
