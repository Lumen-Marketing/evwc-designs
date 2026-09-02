import {open,sleep} from './cdp.mjs';
const P=await open(1440,940);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/02-broadsheet.html'});
await sleep(3000);
const r=await P.evalJS(`(()=>{
 const h=document.querySelector('h1');const cs=getComputedStyle(h);
 const s=document.createElement('span');
 s.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;font-family:'+cs.fontFamily+';font-weight:'+cs.fontWeight+';font-size:'+cs.fontSize+';letter-spacing:'+cs.letterSpacing+';text-transform:uppercase';
 s.textContent='VIEWS START HERE';document.body.appendChild(s);
 const w=s.getBoundingClientRect().width;
 const s2=document.createElement('span');s2.style.cssText=s.style.cssText;s2.textContent='CRYSTAL CLEAR';document.body.appendChild(s2);
 return JSON.stringify({fs:cs.fontSize,avail:Math.round(h.getBoundingClientRect().width),
   lineWide:Math.round(w),lineOne:Math.round(s2.getBoundingClientRect().width),
   h1h:Math.round(h.getBoundingClientRect().height)});})()`);
console.log(r);
P.close();process.exit(0);
