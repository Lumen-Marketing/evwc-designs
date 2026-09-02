import {open,sleep} from './cdp.mjs';
const page=process.argv[2]||'01-daylight.html';
const sel=process.argv[3]||'.plate,.plate-in,.plate-in img,.hero,.hero .in';
const P=await open(1440,940);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(3000);
const r=await P.evalJS(`JSON.stringify(${JSON.stringify(sel)}.split(',').map(function(q){
  var e=document.querySelector(q.trim()); if(!e) return {q:q.trim(),miss:true};
  var b=e.getBoundingClientRect(), c=getComputedStyle(e);
  return {q:q.trim(),
    box:Math.round(b.width)+'x'+Math.round(b.height)+' @'+Math.round(b.left)+','+Math.round(b.top),
    pos:c.position, ar:c.aspectRatio, h:c.height, w:c.width, top:c.top, bottom:c.bottom,
    objfit:c.objectFit, disp:c.display};
}))`);
JSON.parse(r).forEach(x=>console.log(JSON.stringify(x)));
P.close();process.exit(0);
