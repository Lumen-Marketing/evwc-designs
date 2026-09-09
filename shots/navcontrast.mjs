// Contrast for the nav labels, sampled off the RENDERED pixels. The gate on 02
// is a tint over a photograph, so no token pair can answer this.
import {open,sleep} from './cdp.mjs';
import {writeFileSync,unlinkSync} from 'node:fs';
import {execSync} from 'node:child_process';
const lin=c=>{c/=255;return c<=.04045?c/12.92:Math.pow((c+.055)/1.055,2.4)};
const L=([r,g,b])=>.2126*lin(r)+.7152*lin(g)+.0722*lin(b);
const files=['01-mesic.html','02-site.html','03-plate.html'];
for (const f of files) {
  const P=await open(1440,900);
  await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+f});
  await sleep(2600);
  const meta=await P.send('Runtime.evaluate',{expression:`(()=>{
    const sel='#nav a, #nav b, #nav small, #nav span';
    return JSON.stringify([...document.querySelectorAll(sel)]
      .filter(e=>e.textContent.trim() && e.offsetWidth>8)
      .map(e=>{const r=e.getBoundingClientRect();
        return {t:e.textContent.trim().slice(0,22),c:getComputedStyle(e).color,
                x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)}}));})()`,returnByValue:true});
  const nodes=JSON.parse(meta.result.value);
  const rows=[];
  for (const n of nodes) {
    if (n.w<4||n.h<4) continue;
    const shot=await P.send('Page.captureScreenshot',{format:'png',clip:{x:n.x,y:n.y,width:n.w,height:n.h,scale:1}});
    writeFileSync('shots/_px.png',Buffer.from(shot.data,'base64'));
    const px=JSON.parse(execSync('python -c "'+
      'from PIL import Image;import json;'+
      "im=Image.open('shots/_px.png').convert('RGB');"+
      'p=list(im.getdata());'+
      "print(json.dumps(p))"+'"',{maxBuffer:1<<28}).toString());
    const lum=px.map(L).sort((a,b)=>a-b);
    // background pixels outnumber glyph pixels, so the median IS the ground
    const bg=lum[Math.floor(lum.length/2)];
    const m=n.c.match(/[\d.]+/g).map(Number);
    const fg=L(m)*(m[3]===undefined?1:1);
    const ratio=(Math.max(bg,fg)+.05)/(Math.min(bg,fg)+.05);
    rows.push({t:n.t,c:n.c,r:+ratio.toFixed(2)});
  }
  try{unlinkSync('shots/_px.png')}catch(e){}
  rows.sort((a,b)=>a.r-b.r);
  console.log('=== '+f);
  rows.slice(0,6).forEach(r=>console.log('   '+String(r.r).padStart(6)+'  '+r.t));
  P.close();
}
process.exit(0);
