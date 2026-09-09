// Top of the page at rest and after scrolling, for every direction.
// The stuck shot uses a short viewport, because a clip on captureScreenshot
// is in PAGE coordinates: after a scroll it captures the top of the document,
// not what the sticky bar is painting over.
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const W=+(process.argv[2]||1440);
const only=process.argv[3];
const files=only?[only]:['01-mesic.html','02-site.html','03-plate.html'];
for (const f of files) {
  const P=await open(W,900);
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
  await sleep(2200);
  let s=await P.send('Page.captureScreenshot',{format:'png',clip:{x:0,y:0,width:W,height:215,scale:1}});
  writeFileSync('shots/nav-'+f.slice(0,2)+'-top.png',Buffer.from(s.data,'base64'));
  await P.evalJS('scrollTo(0,1600)'); await sleep(900);
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:215,deviceScaleFactor:1,mobile:false});
  await sleep(500);
  s=await P.send('Page.captureScreenshot',{format:'png'});
  writeFileSync('shots/nav-'+f.slice(0,2)+'-stuck.png',Buffer.from(s.data,'base64'));
  P.close();
}
console.log('ok');
process.exit(0);
