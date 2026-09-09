import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+process.argv[2]});
await sleep(2200);
for (const id of ['#services','#work','#reviews','#area']) {
  await P.evalJS(`document.querySelector('${id}').scrollIntoView()`);
  await sleep(700);
  const r=await P.send('Runtime.evaluate',{expression:`[...document.querySelectorAll('#navlinks a')].map(a=>a.getAttribute('aria-current')?('['+a.textContent+']'):a.textContent).join(' ')`,returnByValue:true});
  console.log(id.padEnd(11)+' -> '+r.result.value);
}
P.close();process.exit(0);
