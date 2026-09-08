// With cdnjs blocked, the gallery components must still work: they are not
// motion, they are the control surface.
import {open,sleep} from './cdp.mjs';
const P=await open(1440,900);
await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
await P.send('Network.enable');
await P.send('Network.setBlockedURLs',{urls:['*cdnjs.cloudflare.com*']});
const page=process.argv[2];
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});await sleep(3000);
const dh=Number(await P.evalJS('document.body.scrollHeight'));
for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(80);}
const sel=page.startsWith('02')?'.projx':'.rail';
const top=Number(await P.evalJS(`Math.round(document.querySelector('${sel}').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${top-120})`);await sleep(800);
const btn=page.startsWith('02')?'.pnav.next':'.rnav[data-d="1"]';
const read=page.startsWith('02')?'.pcount':'.readout';
const before=await P.evalJS(`document.querySelector('${read}').textContent`);
const r=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelector('${btn}').getBoundingClientRect();return{x:b.x+b.width/2,y:b.y+b.height/2}})())`));
for(const t of ['mousePressed','mouseReleased'])await P.send('Input.dispatchMouseEvent',{type:t,x:r.x,y:r.y,button:'left',clickCount:1});
await sleep(1100);
const after=await P.evalJS(`document.querySelector('${read}').textContent`);
const vis=await P.evalJS(page.startsWith('02')
  ? `getComputedStyle(document.querySelector('.frame[data-on]')).opacity`
  : `getComputedStyle(document.querySelector('.station[data-at]')).opacity`);
console.log(page,'gsap=',await P.evalJS('typeof window.gsap'),' readout',before,'->',after,' activeOpacity',vis);
P.close();process.exit(0);
