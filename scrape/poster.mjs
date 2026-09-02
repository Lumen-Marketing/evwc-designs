import {open,sleep} from './cdp.mjs';
import {readdirSync,writeFileSync} from 'node:fs';
const files=readdirSync('raw').filter(f=>f.endsWith('.mp4'));
const P=await open(900,1400);
for(const f of files){
  const url='file:///C:/Users/tagal/evwc-designs/scrape/raw/'+f;
  await P.send('Page.navigate',{url:'about:blank'}); await sleep(400);
  await P.send('Page.navigate',{url:'data:text/html,<style>html,body{margin:0;background:#000}video{display:block;width:720px}</style><video src="'+url+'" muted></video>'});
  await sleep(2000);
  for(const t of [0.6, 2.5]){
    await P.evalJS(`(async()=>{const v=document.querySelector('video');v.currentTime=${t};await new Promise(r=>v.onseeked=r);})()`);
    await sleep(1200);
    const r=await P.send('Page.captureScreenshot',{format:'jpeg',quality:88,clip:{x:0,y:0,width:720,height:1280,scale:1}});
    if(r&&r.data) writeFileSync(`raw/POSTER-${f.replace('REEL-','').replace('-dash-1.mp4','')}-t${t}.jpg`,Buffer.from(r.data,'base64'));
  }
  console.log('shot',f);
}
P.close();process.exit(0);
