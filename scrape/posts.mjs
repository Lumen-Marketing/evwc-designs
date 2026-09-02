import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const PATHS=['/eastvalleywindowcleaningllc/p/DVu3BtPj1Ng/','/eastvalleywindowcleaningllc/p/DOFipK1kafC/',
'/little_ley_little_la/p/DMB30eMPjTW/','/eastvalleywindowcleaningllc/reel/DG8Opp4R9e6/',
'/eastvalleywindowcleaningllc/p/DG7NLtQRbTC/','/eastvalleywindowcleaningllc/p/C8vKmhcSCeI/',
'/eastvalleywindowcleaningllc/p/C8YQBItP1G1/','/eastvalleywindowcleaningllc/reel/C3j11U1Ot1i/',
'/eastvalleywindowcleaningllc/reel/C0joTZTuT9r/','/eastvalleywindowcleaningllc/p/Cwqc4pbywfS/',
'/eastvalleywindowcleaningllc/p/CuikViHxzJK/'];
const P=await open(1500,1100);
await P.send('Network.enable');
const all=[];
for(const path of PATHS){
  P.evs.length=0;
  await P.send('Page.navigate',{url:'https://www.instagram.com'+path});
  await sleep(7000);
  const raw=await P.evalJS(`(()=>{
    const imgs=[...document.querySelectorAll('img')].filter(i=>/t51\.|t39\./.test(i.src)).map(i=>({src:i.currentSrc||i.src,w:i.naturalWidth,h:i.naturalHeight,alt:(i.alt||'').slice(0,150)}));
    const vids=[...document.querySelectorAll('video')].map(v=>({src:v.currentSrc||v.src||'',poster:v.poster||''}));
    const m=n=>{const e=document.querySelector('meta[property="'+n+'"]');return e?e.content:''};
    return JSON.stringify({imgs,vids,ogv:m('og:video'),ogvs:m('og:video:secure_url'),cap:m('og:description'),title:m('og:title')});})()`);
  let d={imgs:[],vids:[]};try{d=JSON.parse(raw);}catch(e){}
  const vidReqs=P.evs.filter(e=>e.method==='Network.requestWillBeSent'&&/\.mp4|video\/|t50\.|t66\./.test(e.params?.request?.url||'')).map(e=>e.params.request.url);
  const code=path.split('/').filter(Boolean).pop();
  console.log('\n== '+code+' ('+path.split('/')[2]+')');
  console.log('   imgs:',d.imgs.map(i=>i.w+'x'+i.h).join(' '));
  console.log('   <video>:',d.vids.length,'| og:video:',(d.ogv||d.ogvs||'NONE').slice(0,70),'| mp4 net reqs:',vidReqs.length);
  if(vidReqs.length)console.log('   MP4:',vidReqs[0].slice(0,120));
  console.log('   cap:',(d.cap||'').slice(0,150));
  all.push({code,path,...d,vidReqs});
}
writeFileSync('posts.json',JSON.stringify(all,null,1));
P.close();process.exit(0);
