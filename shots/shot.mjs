// Screenshot + sanity probe for the Pane Solutions directions.
//
// Traps this harness exists to avoid (each one cost real time on earlier builds):
//
//   * Random port AND its own --user-data-dir per run. With a fixed port a new
//     launch silently reattaches to a leftover Chrome and captures the OLD page.
//
//   * Scroll the whole page and await decode() on every image before shooting.
//     img.complete goes true well before the pixels exist, so a fixed wait
//     reaches the capture with photo boxes still blank — which reads as a
//     layout bug that isn't there.
//
//   * A deadline on every decode. decode() on a lazy image the scroll never
//     brought into view does not reject, it waits for a load that is not
//     coming, and the probe then answers nothing at all.
//
//   * VIEWPORT SLICES, never one tall capture. Direction 1 has a position:fixed
//     mix-blend-mode grain layer and every page has a backdrop-filter nav;
//     Chrome hangs indefinitely compositing those into a single 8000px shot.
//     Scrolling and capturing viewport-sized frames is the only reliable way.
//
//   * Kill the browser tree, not the launcher. Chrome forks a renderer per tab
//     and on Windows killing the launcher orphans both; a sweep leaves dozens
//     of live chrome.exe behind and each later run gets slower until it stops
//     answering at all.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
const WAIT = Number(process.env.WAIT || 520);

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const SETTLE = `(async () => {
  const step = Math.round(innerHeight * 0.8);
  for (let y = 0; y < document.body.scrollHeight; y += step) {
    scrollTo(0, y); await new Promise(r => setTimeout(r, 80));
  }
  scrollTo(0, 0); await new Promise(r => setTimeout(r, 240));
  const imgs = [...document.images];
  await Promise.all(imgs.map(i => Promise.race([
    i.decode().catch(() => {}), new Promise(r => setTimeout(r, 2000)),
  ])));
  const de = document.documentElement;
  const broken = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => i.getAttribute('src'));
  const over = [...document.querySelectorAll('body *')]
    .filter(el => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && r.height > 0 && (r.right > de.clientWidth + 2 || r.left < -2);
    })
    .slice(0, 8)
    .map(el => {
      const r = el.getBoundingClientRect();
      return el.tagName.toLowerCase() + '.' + (el.className.toString().trim().split(/\\s+/)[0] || '?')
        + ' [' + Math.round(r.left) + '\u2192' + Math.round(r.right) + ']';
    });
  return JSON.stringify({
    innerWidth, scrollWidth: de.scrollWidth, clientWidth: de.clientWidth,
    height: document.body.scrollHeight, broken, over,
    h1: (document.querySelector('h1')||{}).innerText || '',
    fonts: [...new Set([...document.querySelectorAll('h1,body')]
      .map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/["']/g, '')))],
  });
})()`;

async function run(file, { width, height, out, slices = 0, wait = 2400 }) {
  const url = pathToFileURL(resolve(REPO, file)).href;
  const port = 9000 + Math.floor(Math.random() * 4000);
  const profile = `${process.env.TEMP || '/tmp'}/ps-cdp-${port}`;
  const chrome = spawn(CHROME, [
    '--headless=new', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
    '--allow-file-access-from-files',
    `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`,
    `--window-size=${width},${height}`, 'about:blank',
  ], { stdio: 'ignore' });

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
      const n = ++id; pending.set(n, res);
      ws.send(JSON.stringify({ id: n, method, params }));
    });

    await send('Page.enable'); await send('Runtime.enable');
    await send('Emulation.setDeviceMetricsOverride',
      { width, height, deviceScaleFactor: 1, mobile: width < 500 });
    // setDeviceMetricsOverride alone does NOT change the pointer, so hover:none
    // rules never applied and touch fallbacks looked broken in every mobile
    // capture. Emulate the coarse pointer explicitly.
    if (width < 500) {
      await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
      await send('Emulation.setEmulatedMedia',
        { features: [{ name: 'hover', value: 'none' }, { name: 'pointer', value: 'coarse' }] });
    }
    await send('Page.navigate', { url });
    await sleep(wait);

    const probe = await send('Runtime.evaluate',
      { expression: SETTLE, awaitPromise: true, returnByValue: true });
    const info = JSON.parse(probe.result.value);

    mkdirSync(HERE, { recursive: true });
    const n = slices || 1;
    for (let i = 0; i < n; i++) {
      const y = Math.min(i * height, Math.max(0, info.height - height));
      await send('Runtime.evaluate', { expression: `scrollTo(0,${y})` });
      await sleep(WAIT);
      const shot = await send('Page.captureScreenshot', { format: 'png' });
      const name = slices ? out.replace('.png', `-${i + 1}.png`) : out;
      writeFileSync(resolve(HERE, name), Buffer.from(shot.data, 'base64'));
      if (y + height >= info.height) break;
    }
    return info;
  } finally {
    try { ws && ws.close(); } catch {}
    chrome.kill();
    spawn('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' });
    await sleep(150);
  }
}

const W = Number(process.env.W || 1440);
const SL = Number(process.env.SLICES || 5);
const only = process.argv[2];
const JOBS = [
  ['index.html', 'g.png'],
  ['01-daylight.html', 'd1.png'],
  ['02-broadsheet.html', 'd2.png'],
  ['03-hazard.html', 'd3.png'],
].filter(([f]) => !only || f.includes(only));

for (const [file, out] of JOBS) {
  try {
    const i = await run(file, { width: W, height: 940, out, slices: SL });
    const flag = (i.scrollWidth > i.clientWidth + 2) ? '  \u26a0 SIDEWAYS' : '  ok';
    console.log(`${out.padEnd(8)} ${i.clientWidth}w page=${i.height}px scrollW=${i.scrollWidth}${flag}  fonts=${i.fonts.join('/')}`);
    if (i.h1) console.log('   h1:', JSON.stringify(i.h1.replace(/\n/g, ' / ')));
    if (i.broken.length) console.log('   \u26a0 BROKEN IMAGES:', i.broken.join(', '));
    if (i.over.length) console.log('   \u26a0 past right edge:', i.over.join(' | '));
  } catch (e) { console.log(out, 'FAILED', e.message); }
}
process.exit(0);
