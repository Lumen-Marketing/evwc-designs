import {open,sleep} from './cdp.mjs';
const P=await open(1200,900);
for(const W of [780,820,860]){
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/02-site.html'});
  await sleep(1000);
  const r=await P.evalJS(`(()=>{const n=document.querySelector('.nav-in');
    const out=[...n.children].filter(e=>getComputedStyle(e).display!=='none').map(e=>{
      const b=e.getBoundingClientRect();const prev=e.style.whiteSpace;e.style.whiteSpace='nowrap';
      const nat=Math.round(e.scrollWidth);e.style.whiteSpace=prev;
      return (e.className||e.tagName)+':'+Math.round(b.width)+'(nat '+nat+')';});
    const cs=getComputedStyle(n);
    return JSON.stringify({avail:Math.round(n.getBoundingClientRect().width),gap:cs.gap,parts:out});})()`);
  console.log(String(W).padStart(5), r);
}
P.close();process.exit(0);
