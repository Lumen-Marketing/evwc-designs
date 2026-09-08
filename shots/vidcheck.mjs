import {open,sleep} from './cdp.mjs';
const page=process.argv[2], block=process.argv[3]==='nocdn';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
if(block){await P.send('Network.enable');await P.send('Network.setBlockedURLs',{urls:['*cdnjs.cloudflare.com*']});}
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(3000);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(110);}
let rep=[];
for(const i of [0,1]){
  const y=Number(await P.evalJS(`(()=>{const v=document.querySelectorAll('video')[${i}];if(!v)return -1;const b=v.getBoundingClientRect();return Math.round(b.top+scrollY-260);})()`));
  if(y<0){rep.push('no video '+i);continue;}
  await P.evalJS(`scrollTo(0,${y})`);await sleep(1600);
  rep.push('video'+i+' playing='+await P.evalJS(`(()=>{const v=document.querySelectorAll('video')[${i}];return !v.paused && v.readyState>2;})()`));
}
console.log(page, block?'nocdn':'normal', rep.join('  '));
P.close();process.exit(0);
