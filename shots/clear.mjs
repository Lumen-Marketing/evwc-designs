// clearance between the hung plate and the next detail's drawn boundary
import {open,sleep} from './cdp.mjs';
for (const W of [1024,1120,1280,1440,1920]) {
  const P=await open(W,900);
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/01-mesic.html'});
  await sleep(1700);
  const r=await P.send('Runtime.evaluate',{expression:`(()=>{
    const cap=document.querySelector('.det.lead .cap').getBoundingClientRect();
    const nx=document.querySelector('.detpair .vp').getBoundingClientRect();
    return Math.round(nx.top - 9 - cap.bottom);
  })()`,returnByValue:true});
  console.log(W+': '+r.result.value+'px');
  P.close();
}
process.exit(0);
