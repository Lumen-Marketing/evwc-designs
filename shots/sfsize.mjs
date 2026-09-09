import {open,sleep} from './cdp.mjs';
for (const f of ['01-mesic.html','02-site.html','03-plate.html']) {
  const P=await open(1440,900);
  await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
  await sleep(1900);
  const r=await P.send('Runtime.evaluate',{expression:`(()=>{
    return [...document.querySelectorAll('img[src*="storefront.jpg"]')]
      .filter(i=>!i.src.includes('poster'))
      .map(i=>{const b=i.getBoundingClientRect();return Math.round(b.width)+'x'+Math.round(b.height)}).join('  ');
  })()`,returnByValue:true});
  console.log(f.padEnd(16)+r.result.value);
  P.close();
}
process.exit(0);
