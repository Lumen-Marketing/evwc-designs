// Verify interactive pieces by a REAL click, not by forcing the state with
// setAttribute. Forcing it hides the fact that the click path was never tested,
// which is how a palette switcher shipped once without ever having been clicked.
//
// Dispatches a trusted-enough CDP Input event at the element's real screen
// coordinates and reads the resulting state back out of the DOM.
import { spawn } from 'node:child_process';
import { rmSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function session(file, fn) {
  const port = 9000 + Math.floor(Math.random() * 4000);
  const profile = `${process.env.TEMP || '/tmp'}/ev-click-${port}`;
  const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
    '--allow-file-access-from-files', `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`,
    '--window-size=1440,940', 'about:blank'], { stdio: 'ignore' });
  let ws;
  try {
    let list;
    for (let i = 0; i < 45; i++) {
      try { list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; }
      catch { await sleep(200); }
    }
    ws = new WebSocket(list.find((t) => t.type === 'page').webSocketDebuggerUrl);
    let id = 0; const pending = new Map();
    ws.addEventListener('message', (e) => {
      const m = JSON.parse(e.data);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result ?? m); pending.delete(m.id); }
    });
    await new Promise((r) => ws.addEventListener('open', r));
    const send = (method, params = {}) => new Promise((res) => {
      const n = ++id; pending.set(n, res); ws.send(JSON.stringify({ id: n, method, params }));
    });
    await send('Page.enable'); await send('Runtime.enable');
    await send('Page.navigate', { url: pathToFileURL(resolve(REPO, file)).href });
    await sleep(2800);

    const evalJs = async (expr) => {
      const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
      return r.result ? r.result.value : undefined;
    };
    const clickSel = async (sel) => {
      // scroll-behavior:smooth is set on <html> in these pages, so reading the
      // rect straight after scrollIntoView returns coordinates the element has
      // already left, and the click lands on empty ground. Force instant
      // scrolling, let it settle, THEN measure.
      await evalJs(`(()=>{const s=document.createElement('style');
        s.textContent='html{scroll-behavior:auto!important}*{transition:none!important}';
        document.head.appendChild(s);})()`);
      await evalJs(`(()=>{const e=document.querySelector(${JSON.stringify(sel)});
        if(e) e.scrollIntoView({block:'center',behavior:'instant'});})()`);
      await sleep(400);
      const box = await evalJs(`JSON.stringify((()=>{const e=document.querySelector(${JSON.stringify(sel)});
        if(!e) return null; const b=e.getBoundingClientRect();
        return {x:b.left+b.width/2, y:b.top+b.height/2};})())`);
      const p = JSON.parse(box || 'null');
      if (!p) return false;
      for (const type of ['mousePressed', 'mouseReleased']) {
        await send('Input.dispatchMouseEvent', { type, x: p.x, y: p.y, button: 'left', clickCount: 1 });
      }
      await sleep(900);
      return true;
    };
    const shot = async (name) => {
      const s = await send('Page.captureScreenshot', { format: 'png' });
      if (s && s.data) writeFileSync(resolve(HERE, name), Buffer.from(s.data, 'base64'));
    };
    return await fn({ evalJs, clickSel, shot });
  } finally {
    try { ws && ws.close(); } catch {}
    chrome.kill();
    spawn('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' });
    await sleep(350);
    try { rmSync(profile, { recursive: true, force: true, maxRetries: 5 }); } catch {}
  }
}

// 1. the chooser's Desktop / Mobile segmented toggle
await session('index.html', async ({ evalJs, clickSel, shot }) => {
  const before = await evalJs(`document.querySelectorAll('.stage.desktop').length + '/' + document.querySelectorAll('.stage.mobile').length`);
  const ok = await clickSel('#seg button[data-mode="mobile"]');
  await sleep(1400);
  const after = await evalJs(`document.querySelectorAll('.stage.desktop').length + '/' + document.querySelectorAll('.stage.mobile').length`);
  const pressed = await evalJs(`document.querySelector('#seg button[data-mode="mobile"]').getAttribute('aria-pressed')`);
  const w = await evalJs(`(()=>{const f=document.querySelector('.stage iframe'); return f? f.style.width : 'none';})()`);
  const veiled = await evalJs(`document.querySelectorAll('.stage.live').length`);
  await shot('_click-mobile.png');
  console.log(`chooser toggle   clicked=${ok}  desktop/mobile ${before} -> ${after}  aria-pressed=${pressed}  iframe width=${w}  stages revealed=${veiled}`);
});

// 2. the veil has to swallow the first click on a preview
await session('index.html', async ({ evalJs, clickSel, shot }) => {
  const before = await evalJs(`document.querySelectorAll('.stage.live').length`);
  await clickSel('.stage .veil');
  const after = await evalJs(`document.querySelectorAll('.stage.live').length`);
  console.log(`chooser veil     live stages ${before} -> ${after} (expect 0 -> 1)`);
});

// 3. 01's accordion strip: a real tap has to open a panel
await session('01-mesic.html', async ({ evalJs, clickSel }) => {
  const before = await evalJs(`document.querySelectorAll('#accord .pnl.open').length + ':' + [...document.querySelectorAll('#accord .pnl')].findIndex(p=>p.classList.contains('open'))`);
  await clickSel('#accord .pnl:nth-child(4)');
  const after = await evalJs(`document.querySelectorAll('#accord .pnl.open').length + ':' + [...document.querySelectorAll('#accord .pnl')].findIndex(p=>p.classList.contains('open'))`);
  console.log(`01 accordion     open count:index ${before} -> ${after} (expect the index to move to 3)`);
});

// 4. the filmstrip arrows have to actually scroll the reel
await session('01-mesic.html', async ({ evalJs, clickSel }) => {
  const before = await evalJs(`(()=>{const r=document.getElementById('reel'); r.scrollIntoView({block:'center'}); return r.scrollLeft;})()`);
  await clickSel('#rnext');
  const after = await evalJs(`document.getElementById('reel').scrollLeft`);
  console.log(`01 filmstrip     scrollLeft ${before} -> ${Math.round(after)} (expect it to increase)`);
});

// 5. every mobile drawer opens from its burger
for (const f of ['01-mesic.html', '02-site.html', '03-plate.html', '04-burst.html']) {
  await session(f, async ({ evalJs, clickSel }) => {
    await evalJs(`(()=>{const s=document.createElement('style');s.textContent='@media(min-width:0px){.burger{display:grid!important}}';document.head.appendChild(s);})()`);
    await sleep(200);
    const before = await evalJs(`document.getElementById('drawer').className`);
    await clickSel('#burger');
    const after = await evalJs(`document.getElementById('drawer').className`);
    console.log(`${f.padEnd(16)} drawer "${before}" -> "${after}"`);
  });
}
process.exit(0);
