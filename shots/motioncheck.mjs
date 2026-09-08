// Every element GSAP touches must end up visible. Walks the page like a reader,
// then reports anything still at opacity 0 or displaced.
import {open,sleep} from './cdp.mjs';
const page=process.argv[2], W=+(process.argv[3]||1440);
const P=await open(W,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:W<500});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(3000);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=420){await P.evalJS(`scrollTo(0,${y})`);await sleep(150);}
await sleep(1400);
const out=await P.evalJS(`(()=>{
  const bad=[];
  document.querySelectorAll('body *').forEach(e=>{
    const c=getComputedStyle(e);
    if(c.display==='none'||c.visibility==='hidden')return;
    const b=e.getBoundingClientRect();
    if(!b.width||!b.height)return;
    if(parseFloat(c.opacity)<0.9 && e.style.opacity!=='' ) bad.push('opacity '+c.opacity+' -> '+e.tagName+'.'+e.className);
    const m=c.transform;
    if(m&&m!=='none'&&e.style.transform!==''){const p=m.match(/matrix\(([^)]+)\)/);
      if(p){const v=p[1].split(',').map(Number); if(Math.abs(v[5])>2) bad.push('y '+v[5].toFixed(0)+'px -> '+e.tagName+'.'+e.className);}}
  });
  return JSON.stringify({triggers:window.ScrollTrigger?ScrollTrigger.getAll().length:0,
    scrollW:document.documentElement.scrollWidth,clientW:document.documentElement.clientWidth,
    stuck:bad.slice(0,14),count:bad.length});})()`);
console.log(page, W+'w', out);
P.close();process.exit(0);
