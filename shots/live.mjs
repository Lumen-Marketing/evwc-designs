import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const BASE='https://lumen-marketing.github.io/evwc-designs/';
const pages=[['','live-g.png'],['01-daylight.html','live-d1.png'],['02-broadsheet.html','live-d2.png'],['03-hazard.html','live-d3.png']];
for(const [p,out] of pages){
  const P=await open(1440,940);
  await P.send('Page.navigate',{url:BASE+p});
  await sleep(5000);
  await P.evalJS(`(async()=>{const s=Math.round(innerHeight*.75);
    for(let y=0;y<document.body.scrollHeight;y+=s){scrollTo(0,y);await new Promise(r=>setTimeout(r,380));}
    scrollTo(0,0);await new Promise(r=>setTimeout(r,700));})()`);
  await sleep(1500);
  const info=await P.evalJS(`JSON.stringify({
    sw:document.documentElement.scrollWidth, cw:document.documentElement.clientWidth,
    h:document.body.scrollHeight,
    fonts:[...new Set([...document.querySelectorAll('h1,body')].map(e=>getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g,'')))],
    broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.getAttribute('src')),
    vids:[...document.querySelectorAll('video')].map(v=>({f:(v.currentSrc||'').split('/').pop(),w:v.videoWidth,ready:v.readyState,t:Math.round(v.currentTime*100)/100,err:v.error?v.error.code:null,off:!!v.dataset.off})),
    frames:document.querySelectorAll('iframe').length
  })`);
  const d=JSON.parse(info);
  const badV=d.vids.filter(v=>!(v.w>0&&v.ready>=2&&!v.err&&(v.off||v.t>0)));
  const parked=d.vids.filter(v=>v.off).length;
  await P.evalJS(`scrollTo(0,0)`); await sleep(500);
  const s=await P.send('Page.captureScreenshot',{format:'png'});
  writeFileSync('shots/'+out,Buffer.from(s.data,'base64'));
  console.log((p||'index').padEnd(20),
    'scrollW='+d.sw+'/'+d.cw+(d.sw>d.cw+2?' SIDEWAYS':''),
    'page='+d.h+'px','fonts='+d.fonts.join('/'),
    'imgsBroken='+d.broken.length,'videos='+d.vids.length,'parked='+parked,'videoFail='+badV.length,
    d.frames?('iframes='+d.frames):'');
  if(d.broken.length)console.log('   BROKEN:',d.broken.join(', '));
  if(badV.length)console.log('   VIDEO FAIL:',JSON.stringify(badV));
  P.close();
}
process.exit(0);
