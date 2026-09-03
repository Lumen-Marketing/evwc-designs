// Drive the deck: click a pill / arrow and capture the result.
// node shots/deckclick.mjs <page> <selector-to-click> <out.png> [width]
import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const page=process.argv[2], click=process.argv[3], out=process.argv[4], W=Number(process.argv[5]||1440);
const P=await open(W,940);
await P.send('Page.navigate',{url:'file:///C:/Users/tagal/evwc-designs/'+page});
await sleep(2500);
const h=Number(await P.evalJS(`document.body.scrollHeight`));
for(let y=0;y<h;y+=600){await P.evalJS(`scrollTo(0,${y})`);await sleep(120);}
await sleep(1800);
const top=Number(await P.evalJS(`Math.round(document.querySelector('[data-deck]').getBoundingClientRect().top+scrollY)`));
await P.evalJS(`scrollTo(0,${top-150})`);
await sleep(600);
const r=await P.evalJS(`(function(){var e=document.querySelector(${JSON.stringify(click)});if(!e)return 'MISS';e.click();return 'ok'})()`);
console.log('click', click, '->', r);
await sleep(1300);
const st=await P.evalJS(`JSON.stringify({cap:document.querySelector('.dcap b').textContent,count:document.querySelector('.dcount').textContent,playing:[].slice.call(document.querySelectorAll('[data-deck] video')).map(function(v){return v.paused?'paused':'playing'})})`);
console.log(st);
const s=await P.send('Page.captureScreenshot',{format:'png'});
writeFileSync('shots/'+out,Buffer.from(s.data,'base64'));
P.close();process.exit(0);
