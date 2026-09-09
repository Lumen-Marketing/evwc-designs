import {open,sleep} from './cdp.mjs';
const P=await open(1100,760);
await P.send('Emulation.setDeviceMetricsOverride',{width:1100,height:760,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/03-plate.html'});
await sleep(1700);
const r=await P.send('Runtime.evaluate',{expression:`(()=>{
  return [...document.querySelectorAll('#nav .nav-in,#nav .nav-links,#nav .nav-right')]
   .map(b=>b.className+' sw='+b.scrollWidth+' cw='+b.clientWidth+' ovf='+getComputedStyle(b).overflowX).join(' | ');})()`,returnByValue:true});
console.log(r.result.value);
P.close();process.exit(0);
