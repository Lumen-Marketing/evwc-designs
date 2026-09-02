import {open,sleep} from './cdp.mjs';
import {writeFileSync} from 'node:fs';
const P=await open(1280,1800);
await P.send('Page.navigate',{url:'https://www.instagram.com/eastvalleywindowcleaningllc/'});
await sleep(9000);
await P.evalJS(`window.scrollTo(0,2000)`); await sleep(3000);
await P.evalJS(`window.scrollTo(0,5000)`); await sleep(3000);
const out=await P.evalJS(`JSON.stringify({
  links:[...new Set([...document.querySelectorAll('a[href*="/p/"],a[href*="/reel/"]')].map(a=>a.getAttribute('href')))],
  imgs:[...document.querySelectorAll('img')].map(i=>({s:i.currentSrc||i.src,w:i.naturalWidth,h:i.naturalHeight,alt:(i.alt||'').slice(0,140)})),
  title:document.title,
  desc:(document.querySelector('meta[property="og:description"]')||{}).content||''
})`);
writeFileSync('grid.json',out||'{}');
const d=JSON.parse(out||'{}');
console.log('TITLE:',d.title);
console.log('DESC:',d.desc);
console.log('LINKS('+(d.links||[]).length+'):',(d.links||[]).join(' '));
console.log('IMGS:');for(const i of (d.imgs||[]))console.log('  ',i.w+'x'+i.h,'|',i.alt.slice(0,80),'|',i.s.slice(0,60));
P.close();process.exit(0);
