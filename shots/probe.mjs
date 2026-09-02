// Finds what actually makes a page scroll sideways.
//
// A plain "right edge past clientWidth" sweep is useless on these pages: it
// reports every frame inside the drag filmstrip and every item in a marquee,
// all of which are legitimately clipped or scrollable. This walks up from each
// candidate and discards it if ANY ancestor clips on the x axis.
import { spawn } from 'node:child_process';
import { resolve, dirname } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const EXPR = `(() => {
  const de = document.documentElement, W = de.clientWidth;
  const clipsX = (el) => {
    const s = getComputedStyle(el);
    return s.overflowX === 'hidden' || s.overflowX === 'clip' ||
           s.overflowX === 'auto' || s.overflowX === 'scroll';
  };
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    const r = el.getBoundingClientRect();
    if (r.width <= 0 || r.height <= 0) continue;
    if (r.right <= W + 1 && r.left >= -1) continue;
    let p = el.parentElement, clipped = false;
    while (p && p !== de) { if (clipsX(p)) { clipped = true; break; } p = p.parentElement; }
    if (clipped) continue;
    out.push({
      sel: el.tagName.toLowerCase() + (el.className ? '.' + el.className.toString().trim().split(/\\s+/).join('.') : ''),
      l: Math.round(r.left), r: Math.round(r.right),
      pos: getComputedStyle(el).position,
      parent: el.parentElement ? el.parentElement.tagName.toLowerCase() + '.' + (el.parentElement.className.toString().trim().split(/\\s+/)[0] || '') : '',
    });
  }
  return JSON.stringify({
    clientWidth: W, scrollWidth: de.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    htmlOverflowX: getComputedStyle(de).overflowX,
    bodyOverflowX: getComputedStyle(document.body).overflowX,
    culprits: out.slice(0, 14),
  }, null, 1);
})()`;

const file = process.argv[2];
const width = Number(process.argv[3] || 1440);
const url = pathToFileURL(resolve(REPO, file)).href;
const port = 9000 + Math.floor(Math.random() * 4000);
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--hide-scrollbars',
  `--user-data-dir=${process.env.TEMP}/ps-probe-${port}`,
  `--remote-debugging-port=${port}`, `--window-size=${width},940`, 'about:blank',
], { stdio: 'ignore' });

let list;
for (let i = 0; i < 45; i++) {
  try { list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json(); break; }
  catch { await sleep(200); }
}
const ws = new WebSocket(list.find((t) => t.type === 'page').webSocketDebuggerUrl);
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
await send('Emulation.setDeviceMetricsOverride', { width, height: 940, deviceScaleFactor: 1, mobile: width < 500 });
await send('Page.navigate', { url });
await sleep(2600);
const r = await send('Runtime.evaluate', { expression: EXPR, returnByValue: true });
console.log(file, '@', width + 'px');
console.log(r.result.value);
ws.close(); chrome.kill();
spawn('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' });
process.exit(0);
