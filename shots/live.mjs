import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const BASE='https://lumen-marketing.github.io/evwc-designs/';
// the set was replaced on 2026-09-05; this list still named the three that
// were retired, so every run was silently loading 404 pages and passing.
const pages=[['','live-g.png'],['01-mesic.html','live-d1.png'],['02-site.html','live-d2.png'],['03-plate.html','live-d3.png'],['04-burst.html','live-d4.png']];
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
    vids:[...document.querySelectorAll('video')].map(v=>({f:(v.currentSrc||'').split('/').pop(),w:v.videoWidth,ready:v.readyState,t:Math.round(v.currentTime*100)/100,err:v.error?v.error.code:null,off:(function(){
      if(v.dataset.off)return true;
      // the projector and the rail park every clip that is not the frame or the
      // station you are on, and a parked clip is preload="none" on purpose. It
      // has no width and readyState 0, which is correct, not a failure. The
      // interaction tests (galtest.mjs, railtest.mjs) are what prove a parked
      // clip plays when it is selected.
      var f=v.closest('.frame'); if(f) return !f.hasAttribute('data-on');
      var st=v.closest('.station'); if(st) return !st.hasAttribute('data-at');
      return false;})()})),
    frames:document.querySelectorAll('iframe').length
  })`);
  const d=JSON.parse(info);
  // a parked clip only has to be error free; a playing one has to have decoded
  const badV=d.vids.filter(v=> v.off ? !!v.err : !(v.w>0&&v.ready>=2&&!v.err&&v.t>0));
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
