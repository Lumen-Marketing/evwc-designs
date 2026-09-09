// scrollWidth only counts overflow at the END edge. This gate is
// justify-content:flex-end, so its content overflows to the LEFT and
// scrollWidth reports zero while the first label is being cut in half.
// Measure the children's own left edges against the box instead.
import {open,sleep} from './cdp.mjs';
for (const W of [1181,1240,1300,1360,1440,1520,1561,1600,1700,1920]) {
  const P=await open(W,760);
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:760,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/02-site.html'});
  await sleep(2400);
  const r=await P.send('Runtime.evaluate',{expression:`(()=>{
    const g=document.querySelector('#nav .gate');const gb=g.getBoundingClientRect();
    let worst=0;
    g.querySelectorAll('a,button').forEach(e=>{
      const b=e.getBoundingClientRect();
      if(getComputedStyle(e).display==='none')return;
      worst=Math.min(worst, Math.round(b.left-gb.left));
    });
    const need=[...g.children].reduce((a,c)=>a+c.getBoundingClientRect().width,0)
      + parseFloat(getComputedStyle(g).paddingLeft)
      + parseFloat(getComputedStyle(g).columnGap||0)*([...g.children].length-1);
    return Math.round(need)+'/'+Math.round(gb.width)+' cut='+worst;})()`,returnByValue:true});
  console.log(W+': '+r.result.value);
  P.close();
}
process.exit(0);
