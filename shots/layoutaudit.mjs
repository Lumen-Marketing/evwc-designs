// Two numbers per page.
//   2-col      how many sections put their content in the same two column shape
//   edge       how many sections have a picture running to the viewport edge
// The first one is what said the four pages had one rhythm. The second is what
// tells you a page is actually built as a split screen rather than as cards in
// a gutter.
import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
const JS = "JSON.stringify([].map.call(document.querySelectorAll('body section, body div.hang'),function(sec){var b=sec.getBoundingClientRect();if(b.height<80)return null;var fam='stack';var all=sec.querySelectorAll('*');for(var i=0;i<all.length;i++){var k=all[i],c=getComputedStyle(k);if(c.display==='grid'&&k.getBoundingClientRect().width>480){var t=c.gridTemplateColumns;if(t&&t!=='none'){var n=t.split(' ').length;if(n>=2){fam=n+'-col';break;}}}}var W=document.documentElement.clientWidth;var edge=[].some.call(sec.querySelectorAll('img,video,iframe'),function(m){var r=m.getBoundingClientRect();return r.width>240&&r.height>160&&(r.left<=2||r.right>=W-2);});return ((sec.id||sec.className||'sec')+'').slice(0,18)+' :: '+fam+(edge?'  media-to-edge':'');}).filter(Boolean))";
for(const page of ['01-mesic.html','02-site.html','03-plate.html','04-burst.html']){
  await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
  await sleep(2400);
  const rows=JSON.parse(await P.evalJS(JS));
  const two=rows.filter(r=>r.includes(':: 2-col')).length;
  const edge=rows.filter(r=>r.includes('media-to-edge')).length;
  console.log('=== '+page+'   sections '+rows.length+',  2-col '+two+',  media-to-edge '+edge);
  console.log(rows.join('\n')+'\n');
}
P.close();process.exit(0);
