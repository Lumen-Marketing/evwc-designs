import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
for(const page of ['01-mesic.html','02-site.html','03-plate.html']){
  const out=[];
  for(const W of [505,780,880,1024,1280,1440,1920]){
    await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:W<500});
    await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
    await sleep(1600);
    const sw=Number(await P.evalJS('document.documentElement.scrollWidth'));
    const cw=Number(await P.evalJS('document.documentElement.clientWidth'));
    out.push(W+':'+(sw-cw<=0?'ok':'OVER '+(sw-cw)));
  }
  console.log(page.padEnd(15), out.join('  '));
}
P.close();process.exit(0);
