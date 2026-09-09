// The bar at a narrow width, with the drawer open, so the offset is verified
// by a real click rather than by forcing a class.
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const W=+(process.argv[2]||505);
for (const f of ['01-mesic.html','02-site.html','03-plate.html']) {
  const P=await open(W,760);
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:760,deviceScaleFactor:1,mobile:true});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
  await sleep(2200);
  await P.evalJS("document.getElementById('burger').click()");
  await sleep(900);
  const s=await P.send('Page.captureScreenshot',{format:'png'});
  writeFileSync('shots/navmob-'+f.slice(0,2)+'.png',Buffer.from(s.data,'base64'));
  const r=await P.send('Runtime.evaluate',{expression:`(()=>{const n=document.getElementById('nav').getBoundingClientRect();const d=document.getElementById('drawer').getBoundingClientRect();return 'nav h='+Math.round(n.height)+' drawer top='+Math.round(d.top)+' gap='+Math.round(d.top-n.height)})()`,returnByValue:true});
  console.log(f.padEnd(15)+r.result.value);
  P.close();
}
process.exit(0);
