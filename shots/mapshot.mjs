import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const page=process.argv[2],out=process.argv[3];
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2500);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(90);}
const top=Number(await P.evalJS(`Math.round(document.querySelector('#area').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${top-30})`);
await sleep(6500);   // the embed needs a moment
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/'+out,Buffer.from(s.data,'base64'));
console.log(page,'area top',top);
P.close();process.exit(0);
