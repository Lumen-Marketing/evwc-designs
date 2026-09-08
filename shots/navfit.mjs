import {open,sleep} from './cdp.mjs';
const page=process.argv[2];
const P=await open(1200,900);
for(const W of [780,800,860,900,960,1010,1024,1100,1280,1440]){
  await P.send('Emulation.setDeviceMetricsOverride',{width:W,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
  await sleep(1100);
  const r=await P.evalJS(`(()=>{const n=document.querySelector('.nav-in');if(!n)return 'no nav';
    const kids=[...n.children].filter(e=>getComputedStyle(e).display!=='none');
    const tops=new Set(kids.map(e=>Math.round(e.getBoundingClientRect().top)));
    const logo=n.querySelector('a,.logo,strong');
    const lh=logo?Math.round(logo.getBoundingClientRect().height):0;
    const sum=kids.reduce((a,e)=>a+e.getBoundingClientRect().width,0);
    return JSON.stringify({rows:tops.size,navH:Math.round(n.getBoundingClientRect().height),logoH:lh,
      kidsW:Math.round(sum),avail:Math.round(n.getBoundingClientRect().width)});})()`);
  console.log(String(W).padStart(5), r);
}
P.close();process.exit(0);
