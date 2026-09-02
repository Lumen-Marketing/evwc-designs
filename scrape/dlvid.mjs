import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
const posts=JSON.parse(readFileSync('posts.json','utf8'));
mkdirSync('raw',{recursive:true});
const UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36','Referer':'https://www.instagram.com/'};
const strip=u=>{const x=new URL(u);x.searchParams.delete('bytestart');x.searchParams.delete('byteend');return x.toString();};
for(const p of posts){
  if(!p.vidReqs||!p.vidReqs.length) continue;
  const bases=[...new Set(p.vidReqs.map(strip))];
  let i=0;
  for(const u of bases){
    const tag=/t16|m69/.test(u)?'prog':'dash';
    try{
      const r=await fetch(u,{headers:UA});
      if(!r.ok){console.log('  ',r.status,p.code);continue;}
      const b=Buffer.from(await r.arrayBuffer());
      const f=`raw/REEL-${p.code}-${tag}-${++i}.mp4`;
      writeFileSync(f,b);
      // report mp4 box types at head
      let off=0,boxes=[];while(off<Math.min(b.length,400)&&boxes.length<6){const sz=b.readUInt32BE(off);const t=b.toString('latin1',off+4,off+8);boxes.push(t+':'+sz);if(sz<8)break;off+=sz;}
      console.log('OK',f,(b.length/1048576).toFixed(2)+'MB',boxes.join(' '));
    }catch(e){console.log('  ERR',p.code,e.message);}
  }
}
