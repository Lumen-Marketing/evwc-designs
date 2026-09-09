// Does every nav's content actually FIT its own container at each width?
// A clipped label does not show up as page overflow, because the gate has
// overflow:hidden, so measure scrollWidth against clientWidth on the bar's
// own boxes.
import {open,sleep} from './cdp.mjs';
const files=process.argv[2]?[process.argv[2]]:['01-mesic.html','02-site.html','03-plate.html'];
for (const f of files) {
  const out=[];
  for (const W of [901,1000,1100,1180,1181,1260,1360,1440,1920]) {
    const P=await open(W,760);
    await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:760,deviceScaleFactor:1,mobile:false});
    await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
    await sleep(2400);
    await P.evalJS("document.fonts.ready").catch(()=>{});
    const r=await P.send('Runtime.evaluate',{expression:`(()=>{
      const boxes=[...document.querySelectorAll('#nav .gate,#nav .nav-in,#nav .tblock,#nav .nav-links')];
      let worst=0;
      boxes.forEach(b=>{ worst=Math.max(worst, b.scrollWidth-b.clientWidth); });
      return worst;})()`,returnByValue:true});
    out.push(W+':'+(r.result.value>0?('CLIP'+r.result.value):'ok'));
    P.close();
  }
  console.log(f.padEnd(15)+out.join('  '));
}
process.exit(0);
