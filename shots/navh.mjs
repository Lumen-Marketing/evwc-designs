import {open,sleep} from './cdp.mjs';
for (const W of [505,760,900,1010,1440]) {
  const line=[];
  for (const f of ['01-mesic.html','02-site.html','03-plate.html']) {
    const P=await open(W,900);
    await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
    await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
    await sleep(1700);
    const r=await P.send('Runtime.evaluate',{expression:`Math.round(document.getElementById('nav').getBoundingClientRect().height)`,returnByValue:true});
    line.push(f.slice(0,2)+':'+r.result.value);
    P.close();
  }
  console.log(W+'  '+line.join('  '));
}
process.exit(0);
