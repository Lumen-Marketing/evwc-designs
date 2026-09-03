// Hero at one width. Usage: node shots/hero.mjs <page> <w> <h> <out>
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const page=process.argv[2], W=+process.argv[3], H=+process.argv[4], out=process.argv[5];
const P=await open(W,H);
await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:H,deviceScaleFactor:1,mobile:W<500});
if(W<760){await P.send('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5});
  await P.send('Emulation.setEmulatedMedia',{features:[{name:'hover',value:'none'},{name:'pointer',value:'coarse'}]});}
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2600);
console.log(out,'scrollW',await P.evalJS('document.documentElement.scrollWidth'),'client',await P.evalJS('document.documentElement.clientWidth'),
  'heroH',await P.evalJS('Math.round(document.querySelector(".hero").getBoundingClientRect().height)'),
  'btnBottom',await P.evalJS('Math.round(document.querySelector(".hero .btn").getBoundingClientRect().bottom)'));
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/'+out,Buffer.from(s.data,'base64'));
P.close();process.exit(0);
