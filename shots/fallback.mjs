// Two ways the motion must not break the page:
//   reduce  - the visitor asked for no motion
//   nocdn   - cdnjs never answers
import {open,sleep} from './cdp.mjs';
const page=process.argv[2], mode=process.argv[3];
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
if(mode==='reduce') await P.send('Emulation.setEmulatedMedia',{features:[{name:'prefers-reduced-motion',value:'reduce'}]});
if(mode==='nocdn'){ await P.send('Network.enable'); await P.send('Network.setBlockedURLs',{urls:['*cdnjs.cloudflare.com*']}); }
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(3200);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(110);}
await sleep(1200);
const out=await P.evalJS(`(()=>{
  let hidden=0,names=[];
  document.querySelectorAll('body *').forEach(e=>{
    const c=getComputedStyle(e); if(c.display==='none'||c.visibility==='hidden')return;
    const b=e.getBoundingClientRect(); if(!b.width||!b.height)return;
    if(parseFloat(c.opacity)<0.9){hidden++; if(names.length<8)names.push(e.tagName+'.'+e.className);}
  });
  const v=[...document.querySelectorAll('video')];
  return JSON.stringify({gsap:typeof window.gsap, hiddenCount:hidden, hidden:names,
    videos:v.length, playing:v.filter(x=>!x.paused).length,
    scrollW:document.documentElement.scrollWidth, clientW:document.documentElement.clientWidth});})()`);
console.log(page, mode, out);
P.close();process.exit(0);
