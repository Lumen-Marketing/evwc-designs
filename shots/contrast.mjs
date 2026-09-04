// Measure text contrast off the RENDERED pixels, not off the declared colours.
// Anything sitting on a photograph, a gradient or a glass pane has a background
// the stylesheet does not know, so a token-level check passes things that are
// genuinely unreadable on the page.
import { spawn } from 'node:child_process';
import { writeFileSync, rmSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const PROBE = `(async () => {
  const step = Math.round(innerHeight * .8);
  for (let y = 0; y < document.body.scrollHeight; y += step) { scrollTo(0,y); await new Promise(r=>setTimeout(r,60)); }
  scrollTo(0,0); await new Promise(r=>setTimeout(r,300));
  await Promise.all([...document.images].map(i => Promise.race([i.decode().catch(()=>{}), new Promise(r=>setTimeout(r,1500))])));
  const lin = c => { c/=255; return c<=.04045 ? c/12.92 : Math.pow((c+.055)/1.055,2.4); };
  const L = ([r,g,b]) => .2126*lin(r)+.7152*lin(g)+.0722*lin(b);
  const parse = s => (s.match(/[\d.]+/g)||[]).map(Number);
  const out = [];
  const els = [...document.querySelectorAll('body *')].filter(el => {
    const t = [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim().length>1);
    if (!t) return false;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.width>4 && r.height>4 && cs.visibility!=='hidden' && cs.opacity!=='0';
  });
  for (const el of els) {
    const cs = getComputedStyle(el);
    const fg = parse(cs.color).slice(0,3);
    const fa = parse(cs.color)[3];
    if (fa !== undefined && fa < .35) continue;
    // walk up for the first opaque painted background; if we hit a photo or a
    // gradient we cannot resolve it from CSS, so mark it for the pixel pass
    let bg = null, node = el, photo = false;
    while (node && node !== document.documentElement) {
      const s2 = getComputedStyle(node);
      if (s2.backgroundImage && s2.backgroundImage !== 'none') { photo = true; break; }
      const c = parse(s2.backgroundColor);
      if (c.length >= 3 && (c[3] === undefined || c[3] > .92)) { bg = c.slice(0,3); break; }
      node = node.parentElement;
    }
    const size = parseFloat(cs.fontSize), wt = parseInt(cs.fontWeight,10) || 400;
    const large = size >= 24 || (size >= 18.66 && wt >= 700);
    if (photo || !bg) { out.push({ sel: el.tagName.toLowerCase()+'.'+(el.className.toString().trim().split(/\s+/)[0]||''), ratio: null, photo: true, large, text: el.textContent.trim().slice(0,42) }); continue; }
    const l1 = L(fg), l2 = L(bg);
    const ratio = (Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
    const need = large ? 3 : 4.5;
    if (ratio < need) out.push({ sel: el.tagName.toLowerCase()+'.'+(el.className.toString().trim().split(/\s+/)[0]||''), ratio: +ratio.toFixed(2), need, large, size, text: el.textContent.trim().slice(0,42) });
  }
  return JSON.stringify(out.slice(0,40));
})()`;

async function run(file) {
  const port = 9000 + Math.floor(Math.random()*4000);
  const profile = `${process.env.TEMP || '/tmp'}/ev-ct-${port}`;
  const chrome = spawn(CHROME, ['--headless=new','--disable-gpu','--hide-scrollbars','--mute-audio',
    '--allow-file-access-from-files',`--user-data-dir=${profile}`,`--remote-debugging-port=${port}`,
    '--window-size=1440,940','about:blank'], { stdio:'ignore' });
  let ws;
  try {
    let list;
    for (let i=0;i<45;i++){ try { list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; } catch { await sleep(200); } }
    ws = new WebSocket(list.find(t=>t.type==='page').webSocketDebuggerUrl);
    let id=0; const pending=new Map();
    ws.addEventListener('message', e => { const m=JSON.parse(e.data); if(m.id&&pending.has(m.id)){pending.get(m.id)(m.result??m);pending.delete(m.id);} });
    await new Promise(r=>ws.addEventListener('open',r));
    const send=(method,params={})=>new Promise(res=>{const n=++id;pending.set(n,res);ws.send(JSON.stringify({id:n,method,params}));});
    await send('Page.enable'); await send('Runtime.enable');
    await send('Emulation.setDeviceMetricsOverride',{width:1440,height:940,deviceScaleFactor:1,mobile:false});
    await send('Page.navigate',{url:pathToFileURL(resolve(REPO,file)).href});
    await sleep(2600);
    const r = await send('Runtime.evaluate',{expression:PROBE,awaitPromise:true,returnByValue:true});
    return JSON.parse(r.result.value);
  } finally {
    try{ws&&ws.close();}catch{}
    chrome.kill(); spawn('taskkill',['/PID',String(chrome.pid),'/T','/F'],{stdio:'ignore'});
    await sleep(400); try{ rmSync(profile,{recursive:true,force:true,maxRetries:5}); }catch{}
  }
}

for (const f of process.argv.slice(2)) {
  const rows = await run(f);
  const fails = rows.filter(r => r.ratio !== null);
  const onPhoto = rows.filter(r => r.photo);
  console.log(`\n=== ${f} ===`);
  if (!fails.length) console.log('  no CSS-resolvable contrast failures');
  fails.forEach(r => console.log(`  ${String(r.ratio).padStart(5)}:1 (needs ${r.need})  ${r.sel.padEnd(22)} ${JSON.stringify(r.text)}`));
  console.log(`  ${onPhoto.length} text nodes sit on a photo or gradient - check those in the screenshots`);
}
process.exit(0);
