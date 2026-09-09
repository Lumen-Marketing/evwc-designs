// The band above the hamburger breakpoint, where a nav carrying a phone link
// and a CTA has scrolled a page sideways before.
import {open,sleep} from './cdp.mjs';
for (const f of ['01-mesic.html','02-site.html','03-plate.html']) {
  const out=[];
  for (const W of [901,940,980,1010,1040,1060,1100,1160,1240]) {
    const P=await open(W,760);
    await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:760,deviceScaleFactor:1,mobile:false});
    await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
    await sleep(1500);
    const r=await P.send('Runtime.evaluate',{expression:`(()=>{const n=document.getElementById('nav');
      const kids=[...n.querySelectorAll('.nav-in,.tblock')][0];
      const over=document.documentElement.scrollWidth-document.documentElement.clientWidth;
      const rows=new Set([...kids.children].filter(c=>getComputedStyle(c).display!=='none').map(c=>Math.round(c.getBoundingClientRect().top)));
      return over+'|'+rows.size})()`,returnByValue:true});
    const [over,rows]=r.result.value.split('|');
    out.push(W+':'+(over>0?('OVF'+over):(rows>1?'WRAP':'ok')));
    P.close();
  }
  console.log(f.padEnd(15)+out.join('  '));
}
process.exit(0);
