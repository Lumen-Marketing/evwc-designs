import {readFileSync,writeFileSync} from 'node:fs';
const posts=JSON.parse(readFileSync('posts.json','utf8'));
const UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36','Referer':'https://www.instagram.com/'};
const seen=new Set();const man=[];
for(const p of posts){
  const big=(p.imgs||[]).filter(i=>i.w>=1000);
  for(const im of big){
    const key=(im.src.match(/\/([0-9]+_[0-9]+_[0-9]+_n\.(?:jpg|webp))/)||[])[1]||im.src.slice(-44);
    if(seen.has(key))continue;seen.add(key);
    const r=await fetch(im.src,{headers:UA});
    if(!r.ok){console.log('FAIL',p.code,r.status);continue;}
    const b=Buffer.from(await r.arrayBuffer());
    const n=`IMG-${p.code}-${im.w}x${im.h}.jpg`;
    writeFileSync('raw/'+n,b);
    man.push({file:n,code:p.code,w:im.w,h:im.h,alt:im.alt,cap:p.cap});
    console.log('ok',n,Math.round(b.length/1024)+'KB','|',im.alt.slice(0,60));
  }
}
// profile picture upsize attempt
const grid=JSON.parse(readFileSync('grid.json','utf8'));
const pfp=grid.imgs.find(i=>/profile picture/i.test(i.alt));
if(pfp){for(const u of [pfp.s.replace('s150x150','s640x640'),pfp.s.replace('s150x150','s1080x1080'),pfp.s]){
  const r=await fetch(u,{headers:UA});
  if(r.ok){const b=Buffer.from(await r.arrayBuffer());writeFileSync('raw/PFP.jpg',b);console.log('pfp ok',Math.round(b.length/1024)+'KB',u.includes('640')?'640':u.includes('1080')?'1080':'150');break;}
  else console.log('pfp',r.status);}}
writeFileSync('manifest.json',JSON.stringify(man,null,1));
