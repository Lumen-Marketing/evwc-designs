// How much of each page is actually photography, and how hard is the asset pool
// working? Counts distinct sources, repeats, and the share of page area covered
// by an image, video or map.
import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
const JS = "JSON.stringify((function(){var seen={},area=0,big=0,fullbleed=0;var W=document.documentElement.clientWidth;var H=document.body.scrollHeight;[].forEach.call(document.querySelectorAll('img,video,iframe'),function(m){var r=m.getBoundingClientRect();if(r.width<40||r.height<40)return;var src=(m.currentSrc||m.src||m.getAttribute('src')||'').split('/').pop().split('?')[0];seen[src]=(seen[src]||0)+1;area+=r.width*r.height;if(r.width*r.height>W*300)big++;if(r.width>=W-2)fullbleed++;});return{docArea:W*H,area:Math.round(area),n:Object.keys(seen).length,uses:seen,big:big,fullbleed:fullbleed};})())";
for(const page of ['01-mesic.html','02-site.html','03-plate.html']){
  await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
  await sleep(2200);
  const dh=Number(await P.evalJS('document.body.scrollHeight'));
  for(let y=0;y<dh;y+=600){await P.evalJS(`scrollTo(0,${y})`);await sleep(70);}
  await sleep(600);
  const d=JSON.parse(await P.evalJS(JS));
  const repeats=Object.entries(d.uses).filter(([k,v])=>v>1);
  console.log(page.padEnd(15),
    'distinct='+d.n,
    'placements='+Object.values(d.uses).reduce((a,b)=>a+b,0),
    'photo share='+(100*d.area/d.docArea).toFixed(0)+'%',
    'large='+d.big,
    'full-bleed='+d.fullbleed,
    repeats.length?('  repeated: '+repeats.map(([k,v])=>k+'x'+v).join(' ')):'');
}
P.close();process.exit(0);
