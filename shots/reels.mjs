import {open,sleep} from './cdp.mjs';
const page=process.argv[2]||'01-daylight.html';
const P=await open(1440,940);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(3000);
// walk the page so IntersectionObserver fires for every bay
await P.evalJS(`(async()=>{const s=Math.round(innerHeight*.7);
  for(let y=0;y<document.body.scrollHeight;y+=s){scrollTo(0,y);await new Promise(r=>setTimeout(r,420));}
  scrollTo(0,0);await new Promise(r=>setTimeout(r,600));})()`);
await sleep(1200);
const r=await P.evalJS(`JSON.stringify([...document.querySelectorAll('video')].map(v=>({
  src:(v.currentSrc||'').split('/').pop(), w:v.videoWidth, h:v.videoHeight,
  dur:Math.round(v.duration*10)/10, t:Math.round(v.currentTime*100)/100,
  paused:v.paused, muted:v.muted, loop:v.loop, ready:v.readyState,
  err:v.error?v.error.code:null, off:!!v.dataset.off,
  box:Math.round(v.getBoundingClientRect().width)+'x'+Math.round(v.getBoundingClientRect().height)
})))`);
const vids=JSON.parse(r);
console.log(page);
let bad=0;
for(const v of vids){
  // a clip the deck has parked off to the side is meant to be paused; assert it
  // decodes and is correctly configured, then prove it plays in the sweep below
  const base = v.w>0 && v.ready>=2 && !v.err && v.muted && v.loop;
  const ok = v.off ? base : (base && v.t>0);
  if(!ok) bad++;
  console.log(' ',ok?(v.off?'PARK':'OK  '):'FAIL',(v.src||'?').padEnd(28),v.w+'x'+v.h,'dur='+v.dur,'t='+v.t,'paused='+v.paused,'muted='+v.muted,'loop='+v.loop,'ready='+v.ready,'box='+v.box,v.err?('ERR '+v.err):'');
}

// bring every deck slide to focus in turn: each clip must actually start
const pills=Number(await P.evalJS(`document.querySelectorAll('.pill,.tab,.rail-tab').length`));
if(pills){
  await P.evalJS(`document.querySelector('[data-deck]').scrollIntoView({block:'center'})`);
  await sleep(700);
  for(let i=0;i<pills;i++){
    await P.evalJS(`document.querySelectorAll('.pill,.tab,.rail-tab')[${i}].click()`);
    await sleep(900);
  }
  const swept=JSON.parse(await P.evalJS(`JSON.stringify([...document.querySelectorAll('[data-deck] video')].map(v=>({
    src:(v.currentSrc||'').split('/').pop(), t:Math.round(v.currentTime*100)/100})))`));
  for(const v of swept){
    const ok=v.t>0; if(!ok) bad++;
    console.log(' ',ok?'PLAYED':'NEVER ',(v.src||'?').padEnd(28),'t='+v.t,'(after focus sweep)');
  }
}
console.log(vids.length+' videos, '+bad+' failing');
P.close();process.exit(0);
