// Screenshot a vertical band of the page. Usage: node shots/crop.mjs <page> <w> <y> <h> <out>
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const page=process.argv[2],W=+process.argv[3],Y=+process.argv[4],H=+process.argv[5],out=process.argv[6];
const P=await open(W,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:W<500});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2200);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(90);}
await P.evalJS('scrollTo(0,0)');await sleep(900);
const s=await P.send('Page.captureScreenshot',{format:'png',clip:{x:0,y:Y,width:W,height:H,scale:1}});
writeFileSync('shots/'+out,Buffer.from(s.data,'base64'));
P.close();process.exit(0);
