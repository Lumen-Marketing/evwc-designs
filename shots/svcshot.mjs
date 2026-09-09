import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const W=+(process.argv[3]||1440);
const P=await open(W,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+process.argv[2]});
await sleep(2000);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(70);}
await P.evalJS('scrollTo(0,0)');await sleep(800);
const g=await P.send('Runtime.evaluate',{expression:`(()=>{const s=document.querySelector('#services');const b=s.getBoundingClientRect();return JSON.stringify({y:Math.round(b.top+scrollY),h:Math.round(b.height)})})()`,returnByValue:true});
const {y,h}=JSON.parse(g.result.value);
const s=await P.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:true,clip:{x:0,y,width:W,height:Math.min(h,4000),scale:1}});
writeFileSync('shots/'+process.argv[4],Buffer.from(s.data,'base64'));
console.log('section y='+y+' h='+h);
P.close();process.exit(0);
