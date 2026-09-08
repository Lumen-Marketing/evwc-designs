import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
const JS = "JSON.stringify([].map.call(document.querySelectorAll('body section, body div.hang'),function(sec){var b=sec.getBoundingClientRect();if(b.height<80)return null;var fam='stack';var all=sec.querySelectorAll('*');for(var i=0;i<all.length;i++){var k=all[i],c=getComputedStyle(k);if(c.display==='grid'&&k.getBoundingClientRect().width>480){var t=c.gridTemplateColumns;if(t&&t!=='none'){var n=t.split(' ').length;if(n>=2){fam=n+'-col';break;}}}}return ((sec.id||sec.className||'sec')+'').slice(0,20)+' :: '+fam;}).filter(Boolean))";
for(const page of ['01-mesic.html','02-site.html','03-plate.html','04-burst.html']){
  await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
  await sleep(2400);
  const r = await P.evalJS(JS);
  console.log('=== '+page+' ===');
  console.log(r ? JSON.parse(r).join('\n') : 'no result');
  console.log('');
}
P.close();process.exit(0);
