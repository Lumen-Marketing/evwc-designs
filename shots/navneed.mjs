import {open,sleep} from './cdp.mjs';
for (const W of [1060,1100,1140,1180,1220,1260,1300]) {
  const P=await open(W,760);
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:760,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/03-plate.html'});
  await sleep(1400);
  const r=await P.send('Runtime.evaluate',{expression:`(()=>{const n=document.querySelector('#nav .nav-in');
    const kids=[...n.children].filter(c=>getComputedStyle(c).display!=='none'&&!c.className.match(/^b[23]$/));
    const want=kids.reduce((a,c)=>a+c.getBoundingClientRect().width,0);
    const gap=parseFloat(getComputedStyle(n).gap)*(kids.length-1);
    const ovf=document.documentElement.scrollWidth-document.documentElement.clientWidth;
    return Math.round(want+gap)+' / '+Math.round(n.clientWidth)+'  pageovf='+ovf;})()`,returnByValue:true});
  console.log(W+': '+r.result.value);
  P.close();
}
process.exit(0);
