import {open,sleep} from './cdp.mjs';
import {readdirSync} from 'node:fs';
const files=readdirSync('raw').filter(f=>f.endsWith('.mp4'));
const P=await open(800,600);
for(const f of files){
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/scrape/raw/'+f});
  await sleep(2500);
  const r=await P.evalJS(`(()=>{const v=document.querySelector('video');if(!v)return 'no video el';
    return JSON.stringify({w:v.videoWidth,h:v.videoHeight,dur:Math.round(v.duration*10)/10,err:v.error?v.error.code:null,state:v.readyState});})()`);
  console.log(f.padEnd(34), r);
}
P.close();process.exit(0);
