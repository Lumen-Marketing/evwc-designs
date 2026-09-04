// Pixel-level contrast for text that sits on a photograph, a gradient or glass.
//
// The CSS-level check cannot resolve those backgrounds, so it silently passes
// anything laid over an image. This one measures the declared text colour
// against the pixels actually behind it, taking the worst decile rather than
// the average: a white headline is only as readable as the brightest patch of
// sky it crosses.
//
// House method: take the MEDIAN luminance of the sampled box and compare it
// against the exact text colour. Background pixels outnumber glyph pixels in
// any real text box, so the median lands on the background and needs no
// second render pass.
//
// Two traps that made earlier attempts useless, both recorded here so they are
// not walked into again:
//   * Taking the brightest decile instead of the median measures the GLYPHS of
//     a white headline, so everything scores 1:1.
//   * captureBeyondViewport composites fixed layers and running animations at
//     the wrong offsets, so a clip in page coordinates lands on the section
//     above or below.
//   * A CLIPPED capture over a backdrop-filter pane comes back blank white, so
//     every glass element scored a clean 1:1 and looked like a pass. Capture
//     the whole viewport, which composites correctly, and crop in Node.
import { spawn } from 'node:child_process';
import { rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { PNG } from './png.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const COLLECT = String.raw`(async () => {
  const step = Math.round(innerHeight * .8);
  for (let y = 0; y < document.body.scrollHeight; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); }
  scrollTo(0, 0); await new Promise(r => setTimeout(r, 300));
  await Promise.all([...document.images].map(i => Promise.race([i.decode().catch(() => {}), new Promise(r => setTimeout(r, 1500))])));
  const parse = s => (s.match(/[\d.]+/g) || []).map(Number);
  const rows = [];
  const all = [...document.querySelectorAll('body *')];
  for (let idx = 0; idx < all.length; idx++) {
    const el = all[idx];
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 1)) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.opacity === '0') continue;
    let node = el, photo = false;
    while (node && node !== document.documentElement) {
      const s2 = getComputedStyle(node);
      if (s2.backgroundImage && s2.backgroundImage !== 'none') { photo = true; break; }
      const c = parse(s2.backgroundColor);
      if (c.length >= 3 && (c[3] === undefined || c[3] > .92)) break;
      node = node.parentElement;
    }
    if (!photo) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 6 || r.height < 6 || r.width > 1440 || r.height > 900) continue;
    const size = parseFloat(cs.fontSize), wt = parseInt(cs.fontWeight, 10) || 400;
    rows.push({
      idx,
      x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY),
      w: Math.round(r.width), h: Math.round(r.height),
      fg: parse(cs.color).slice(0, 3), size, wt,
      sel: el.tagName.toLowerCase() + '.' + (el.className.toString().trim().split(/\s+/)[0] || ''),
      text: el.textContent.trim().slice(0, 40),
    });
  }
  return JSON.stringify(rows.slice(0, 70));
})()`;

const lin = (c) => { c /= 255; return c <= .04045 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4); };
const L = (r, g, b) => .2126 * lin(r) + .7152 * lin(g) + .0722 * lin(b);

async function run(file) {
  const port = 9000 + Math.floor(Math.random() * 4000);
  const profile = `${process.env.TEMP || '/tmp'}/ev-px-${port}`;
  const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
    '--allow-file-access-from-files', '--force-prefers-reduced-motion', `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`,
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
    await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 940, deviceScaleFactor: 1, mobile: false });
    await send('Page.navigate', { url: pathToFileURL(resolve(REPO, file)).href });
    await sleep(2600);

    const raw = await send('Runtime.evaluate', { expression: COLLECT, awaitPromise: true, returnByValue: true });
    const rows = JSON.parse(raw.result.value);

    const bad = [];
    for (const r of rows) {
      // captureBeyondViewport composites fixed layers and running animations at
      // the wrong offsets, so a clip in page coordinates lands on the section
      // above or below. Scroll the element into view and clip in VIEWPORT
      // coordinates read back after the scroll settles.
      await send('Runtime.evaluate', { expression: `scrollTo(0, ${Math.max(0, r.y - 300)})` });
      await sleep(320);
      const live = await send('Runtime.evaluate', {
        expression: `JSON.stringify((() => {
          const e = document.querySelectorAll('body *')[${r.idx}];
          if (!e) return null;
          const b = e.getBoundingClientRect();
          return { x: b.left, y: b.top, w: b.width, h: b.height };
        })())`, returnByValue: true,
      });
      const lb = JSON.parse(live.result.value || 'null');
      if (!lb || lb.w < 4 || lb.h < 4 || lb.y < 0 || lb.y + lb.h > 940) continue;
      // full viewport, then crop: a clip over glass returns a blank frame
      const shot = await send('Page.captureScreenshot', { format: 'png' });
      if (!shot || !shot.data) continue;
      let px;
      try { px = PNG(Buffer.from(shot.data, 'base64')); } catch { continue; }
      const x0 = Math.max(0, Math.round(lb.x)), y0 = Math.max(0, Math.round(lb.y));
      const x1 = Math.min(px.width, x0 + Math.round(lb.w)), y1 = Math.min(px.height, y0 + Math.round(lb.h));
      const ls = [];
      for (let y = y0; y < y1; y++) {
        for (let x = x0; x < x1; x++) {
          const i = (y * px.width + x) * 4;
          ls.push(L(px.data[i], px.data[i + 1], px.data[i + 2]));
        }
      }
      if (!ls.length) continue;
      ls.sort((a, b) => a - b);
      const fgL = L(r.fg[0], r.fg[1], r.fg[2]);
      const bgL = ls[Math.floor(ls.length * .5)];   // median = the background
      const ratio = (Math.max(fgL, bgL) + .05) / (Math.min(fgL, bgL) + .05);
      const large = r.size >= 24 || (r.size >= 18.66 && r.wt >= 700);
      const need = large ? 3 : 4.5;
      if (process.env.DEBUG) console.log(`    dbg ${r.sel.padEnd(16)} n=${ls.length} fgL=${fgL.toFixed(3)} bgL=${bgL.toFixed(3)} ratio=${ratio.toFixed(2)}`);
      if (ratio < need) bad.push({ ...r, ratio: +ratio.toFixed(2), need });
    }
    return { bad, checked: rows.length };
  } finally {
    try { ws && ws.close(); } catch {}
    chrome.kill();
    spawn('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' });
    await sleep(400);
    try { rmSync(profile, { recursive: true, force: true, maxRetries: 5 }); } catch {}
  }
}

for (const f of process.argv.slice(2)) {
  const { bad, checked } = await run(f);
  console.log(`\n=== ${f} === ${checked} text nodes on photography`);
  if (!bad.length) { console.log('  all clear'); continue; }
  bad.sort((a, b) => a.ratio - b.ratio).forEach((r) => {
    console.log(`  ${String(r.ratio).padStart(5)}:1 (needs ${r.need})  ${r.sel.padEnd(20)} ${r.size}px  ${JSON.stringify(r.text)}`);
  });
}
process.exit(0);
