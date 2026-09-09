// Measure the services row: heading fill, header dead band, per-card structure.
import {open,sleep} from './cdp.mjs';
const W=+(process.argv[3]||1440);
const P=await open(W,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+process.argv[2]});
await sleep(2000);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(70);}
await P.evalJS('scrollTo(0,0)');await sleep(600);
const out=await P.evalJS(`(()=>{
  const sec=document.querySelector('#services');
  const wrap=sec.querySelector('.wrap');
  const r=n=>{const b=n.getBoundingClientRect();return {w:Math.round(b.width),h:Math.round(b.height),t:Math.round(b.top+scrollY)}};
  const h=sec.querySelector('.sh');
  const rng=document.createRange();rng.selectNodeContents(h);
  const hw=Math.round(rng.getBoundingClientRect().width);
  const cards=[...sec.querySelectorAll('.pcard')].map(c=>({
    r:r(c), kids:[...c.children].map(k=>k.tagName.toLowerCase()).join('>'),
    img:r(c.querySelector('img')), words:c.querySelector('p').textContent.trim().split(/\s+/).length
  }));
  return JSON.stringify({sec:r(sec),wrap:r(wrap),heading:{text:h.textContent.trim(),inkW:hw,measure:r(wrap).w,fill:+(hw/r(wrap).w*100).toFixed(1),blockH:r(h).h},
    cards},null,1);
})()`);
console.log(out);
P.close();process.exit(0);
