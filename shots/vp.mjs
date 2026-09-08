import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const page=process.argv[2],W=+process.argv[3],H=+process.argv[4],Y=+process.argv[5],out=process.argv[6];
const P=await open(W,H);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:W<500});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2200);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(90);}
await P.evalJS(`scrollTo(0,${Y})`);await sleep(1000);
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/'+out,Buffer.from(s.data,'base64'));
P.close();process.exit(0);
