import {open,sleep} from './cdp.mjs';
const page=process.argv[2]||'01-daylight.html';
const sel=(process.argv[3]||'.hinge').split(',').map(s=>s.trim());
const P=await open(1440,940);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2500);
// walk the page so every IntersectionObserver has fired, then settle
await P.evalJS(`(function(){var h=document.body.scrollHeight;for(var y=0;y<h;y+=700)scrollTo(0,y);return 1})()`);
await sleep(2500);
await P.evalJS(`scrollTo(0,0)`);
await sleep(900);
const r=await P.evalJS(`JSON.stringify(${JSON.stringify(sel)}.map(function(q){
  var e=document.querySelector(q); if(!e) return {q:q,miss:true};
  var b=e.getBoundingClientRect(), c=getComputedStyle(e);
  return {q:q, w:Math.round(b.width), h:Math.round(b.height),
    x:Math.round(b.left+scrollX), y:Math.round(b.top+scrollY),
    op:c.opacity, vis:c.visibility, disp:c.display, color:c.color,
    cls:e.className, txt:(e.textContent||'').trim().slice(0,40)};
}))`);
JSON.parse(r).forEach(x=>console.log(JSON.stringify(x)));
P.close();process.exit(0);
