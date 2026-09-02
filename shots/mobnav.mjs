import {open,sleep} from './cdp.mjs';
const pages=['01-control.html','02-broadsheet.html','03-hazard.html'];
for(const pg of pages){
  const P=await open(390,844);
  await P.send('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:2,mobile:true});
  await P.send('Emulation.setTouchEmulationEnabled',{enabled:true,maxTouchPoints:5});
  await P.send('Emulation.setEmulatedMedia',{features:[{name:'hover',value:'none'},{name:'pointer',value:'coarse'}]});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+pg});
  await sleep(2600);
  const r=await P.evalJS(`(()=>{
    const b=document.getElementById('burger');const br=b.getBoundingClientRect();
    const onscreen = br.right<=innerWidth+1 && br.left>=-1 && br.width>=40 && br.height>=40;
    b.click();
    return new Promise(res=>setTimeout(()=>{
      const links=[...document.querySelectorAll('.nlinks a,.npill a')];
      const vis=links.filter(a=>{const r=a.getBoundingClientRect();return r.width>0&&r.height>0&&r.right<=innerWidth+1&&r.left>=-1});
      const cta=document.querySelector('.ncta');const cr=cta.getBoundingClientRect();
      const ctaVis=cr.width>0&&cr.height>0&&cr.right<=innerWidth+1&&cr.bottom<=innerHeight+400;
      // smallest tap target anywhere
      const small=[...document.querySelectorAll('a[href],button')].map(e=>{const q=e.getBoundingClientRect();
        return {t:(e.textContent||'').trim().slice(0,22)||e.className,w:Math.round(q.width),h:Math.round(q.height)}})
        .filter(x=>x.w>0&&x.h>0&&(x.h<44)).slice(0,6);
      res(JSON.stringify({burgerOnScreen:onscreen,burgerBox:Math.round(br.width)+'x'+Math.round(br.height)+' @x'+Math.round(br.left),
        linksTotal:links.length,linksVisible:vis.length,ctaVisible:ctaVis,ctaTop:Math.round(cr.top),small}));
    },420));})()`);
  const d=JSON.parse(r);
  const ok=d.burgerOnScreen&&d.linksVisible===d.linksTotal&&d.ctaVisible&&d.small.length===0;
  console.log((ok?'OK  ':'FAIL')+' '+pg,JSON.stringify(d));
  P.close();
}
process.exit(0);
