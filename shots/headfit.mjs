// Solve every section heading's font size from a MEASUREMENT instead of a guess.
//
// The failure this exists to stop: a heading capped in `ch`, or sized by eye,
// wraps to three short lines against an empty right hand side. `ch` is the
// advance of a zero, roughly 0.40em on a condensed display face, so a 13ch cap
// on a 74px headline lands near a third of the row.
//
// Method: clone the heading, set it to 100px on one unwrapped line, measure the
// real string in its real typeface, then work the size back so the string fills
// the target share of ITS OWN box. Measuring against the page container instead
// passes anything sitting in a grid column, which is how the contact headings
// got away with wrapping to four lines inside a 361px box.
import { spawn } from 'node:child_process';
import { rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const TARGET = Number(process.env.TARGET || 92);   // percent of the box to fill

const SOLVE = String.raw`(async () => {
  await document.fonts.ready;
  await new Promise(r => setTimeout(r, 200));
  const out = [];
  const probe = document.createElement('div');
  // inline-block, not block: an absolutely positioned block still resolves
  // width against its containing block in some cases and the measurement comes
  // back as the page width rather than the string width
  probe.style.cssText = 'position:absolute;left:-99999px;top:0;white-space:nowrap;visibility:hidden;display:inline-block;width:auto;max-width:none;padding:0;margin:0;border:0';
  document.body.appendChild(probe);

  for (const h of document.querySelectorAll('h1, h2, .say')) {
    const cs = getComputedStyle(h);
    const size = parseFloat(cs.fontSize);
    if (size < 26) continue;
    const box = h.getBoundingClientRect();
    if (box.width < 140) continue;

    // the natural one-line width of this exact string in this exact face.
    // Never use the font shorthand here: when it fails to parse, the whole
    // assignment is dropped and the probe silently measures at the default
    // 16px, which reports every heading as needing a 900px font size.
    probe.style.fontFamily = cs.fontFamily;
    probe.style.fontWeight = cs.fontWeight;
    probe.style.fontStyle = cs.fontStyle;
    probe.style.fontSize = '100px';
    probe.style.letterSpacing = (parseFloat(cs.letterSpacing) / size).toFixed(4) + 'em';
    probe.style.textTransform = cs.textTransform;
    probe.style.fontStretch = cs.fontStretch;
    probe.style.fontVariationSettings = cs.fontVariationSettings;
    probe.textContent = h.textContent.replace(/\s+/g, ' ').trim();
    const natural = probe.getBoundingClientRect().width;

    // current fill, from the real line boxes
    const range = document.createRange();
    range.selectNodeContents(h);
    const rects = [...range.getClientRects()].filter(r => r.width > 1 && r.height > 1);
    const widest = rects.length ? Math.max(...rects.map(r => r.width)) : 0;
    const tops = [...new Set(rects.map(r => Math.round(r.top)))].sort((a, b) => a - b);
    const lines = tops.filter((t, i) => i === 0 || t - tops[i - 1] > 4).length;

    out.push({
      text: h.textContent.replace(/\s+/g, ' ').trim().slice(0, 54),
      cls: (h.className.toString().trim().split(/\s+/)[0] || h.tagName.toLowerCase()),
      size: Math.round(size * 10) / 10,
      boxW: Math.round(box.width),
      natural100: Math.round(natural),
      fillPct: Math.round(widest / box.width * 100),
      lines,
      // the size at which this string fills TARGET% of its own box on one line
      onelinePx: Math.round(box.width * ${TARGET} / 100 / natural * 100),
    });
  }
  probe.remove();
  return JSON.stringify(out);
})()`;

async function run(file, width) {
  const port = 9000 + Math.floor(Math.random() * 4000);
  const profile = `${process.env.TEMP || '/tmp'}/ev-fit-${port}`;
  const chrome = spawn(CHROME, ['--headless=new', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
    '--allow-file-access-from-files', '--force-prefers-reduced-motion',
    `--user-data-dir=${profile}`, `--remote-debugging-port=${port}`,
    `--window-size=${width},940`, 'about:blank'], { stdio: 'ignore' });
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
    await send('Emulation.setDeviceMetricsOverride', { width, height: 940, deviceScaleFactor: 1, mobile: false });
    await send('Page.navigate', { url: pathToFileURL(resolve(REPO, file)).href });
    await sleep(2400);
    const r = await send('Runtime.evaluate', { expression: SOLVE, awaitPromise: true, returnByValue: true });
    return JSON.parse(r.result.value);
  } finally {
    try { ws && ws.close(); } catch {}
    chrome.kill();
    spawn('taskkill', ['/PID', String(chrome.pid), '/T', '/F'], { stdio: 'ignore' });
    await sleep(350);
    try { rmSync(profile, { recursive: true, force: true, maxRetries: 5 }); } catch {}
  }
}

for (const file of process.argv.slice(2)) {
  const rows = await run(file, 1440);
  console.log(`\n======== ${file} ========  target fill ${TARGET}%`);
  console.log('  now%  ln  size   box   nat@100   fits at   text');
  for (const r of rows) {
    const flag = (r.lines === 1 && r.fillPct >= 84 && r.fillPct <= 97) ? '  ' : '<<';
    console.log(`  ${String(r.fillPct).padStart(3)}%  ${r.lines}  ${String(r.size).padStart(5)} ${String(r.boxW).padStart(5)}  nat${String(r.natural100).padStart(5)}  ${String(r.onelinePx).padStart(5)}px ${flag}  ${JSON.stringify(r.text)}`);
  }
}
process.exit(0);
