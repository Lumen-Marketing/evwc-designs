// The wipe must sweep itself once, then answer the pointer and the keyboard.
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const P=await open(1440,900);
for(const page of ['01-mesic.html','02-site.html','03-plate.html']){
  await P.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false});
  await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
  await sleep(2600);
  const dh=Number(await P.evalJS('document.body.scrollHeight'));
  for(let y=0;y<dh;y+=500){await P.evalJS(`scrollTo(0,${y})`);await sleep(80);}
  const top=Number(await P.evalJS(`Math.round(document.querySelector('.wipe').getBoundingClientRect().top+scrollY)`));
  await P.evalJS(`scrollTo(0,${top-140})`);
  await sleep(2600);                       // let the self sweep finish
  const afterSweep=await P.evalJS(`document.querySelector('.wipe').style.getPropertyValue('--x')`);
  // drag: press near the left third and release
  const r=JSON.parse(await P.evalJS(`JSON.stringify((()=>{const b=document.querySelector('.wipe').getBoundingClientRect();return{x1:b.x+b.width*0.5,x2:b.x+b.width*0.22,y:b.y+b.height/2};})())`));
  await P.send('Input.dispatchMouseEvent',{type:'mousePressed',x:r.x1,y:r.y,button:'left',clickCount:1});
  await P.send('Input.dispatchMouseEvent',{type:'mouseMoved',x:r.x2,y:r.y,button:'left'});
  await P.send('Input.dispatchMouseEvent',{type:'mouseReleased',x:r.x2,y:r.y,button:'left',clickCount:1});
  await sleep(500);
  const afterDrag=await P.evalJS(`document.querySelector('.wipe').style.getPropertyValue('--x')`);
  const valtext=await P.evalJS(`document.querySelector('.w-range').getAttribute('aria-valuetext')`);
  console.log(page.padEnd(15),'sweep ->',afterSweep,' drag ->',afterDrag,' |',valtext);
  const s=await P.send('Page.captureScreenshot',{format:'png'});
  writeFileSync('shots/wipe-'+page.slice(0,2)+'.png',Buffer.from(s.data,'base64'));
}
P.close();process.exit(0);
