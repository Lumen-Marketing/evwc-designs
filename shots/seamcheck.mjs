import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/02-site.html'});
await sleep(2400);
const r=await P.send('Runtime.evaluate',{expression:`(()=>{
  const m=document.querySelector('.hero .sp-media').getBoundingClientRect();
  const g=document.querySelector('#nav .gate').getBoundingClientRect();
  const seam=document.querySelector('#nav .nav-in');
  return 'hero media left='+Math.round(m.left)+'  gate left='+Math.round(g.left);})()`,returnByValue:true});
console.log(r.result.value);
P.close();process.exit(0);
