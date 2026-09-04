// The measured half of the pre-flight. Screenshots catch what is ugly; these
// catch what is broken. Everything here is a rule with a number attached:
//
//   heading fill      section headings should be one line at 89 to 93% of the row
//   block fill        any multi line text block should reach 84% of ITS OWN box,
//                     measured per column, because measuring against the page
//                     container silently passes anything inside a grid cell
//   overflow          zero sideways scroll at 505, 780, 880, 1024, 1280, 1440
//   dead space        no vertical gap larger than 220px between painted content
//   photo grounds     at most two sections whose GROUND is a photograph
//   eyebrows          at or under ceil(sections / 3)
//
// Reveal animations are frozen with --force-prefers-reduced-motion, otherwise
// every .rv block measures as a zero height box that has not entered yet.
import { spawn } from 'node:child_process';
import { rmSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const REPO = resolve(HERE, '..');
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const WIDTHS = [505, 780, 880, 1024, 1280, 1440];

const MEASURE = String.raw`(async () => {
  const step = Math.round(innerHeight * .8);
  for (let y = 0; y < document.body.scrollHeight; y += step) { scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); }
  scrollTo(0, 0); await new Promise(r => setTimeout(r, 250));
  await Promise.all([...document.images].map(i => Promise.race([i.decode().catch(() => {}), new Promise(r => setTimeout(r, 1200))])));

  const de = document.documentElement;
  const out = { w: innerWidth, scrollW: de.scrollWidth, clientW: de.clientWidth, over: [], heads: [], blocks: [], gaps: [], grounds: 0, eyebrows: 0, sections: 0 };

  // anything painting past the right edge
  out.over = [...document.querySelectorAll('body *')].filter(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    if (getComputedStyle(el).position === 'fixed') return false;
    // a marquee is meant to run off the edge
    if (el.closest('.ticker, .tick-track, .grain, .vig, .scan, .rays')) return false;
    return r.right > de.clientWidth + 2 || r.left < -2;
  }).slice(0, 6).map(el => {
    const r = el.getBoundingClientRect();
    return el.tagName.toLowerCase() + '.' + (el.className.toString().trim().split(/\s+/)[0] || '?') + ' [' + Math.round(r.left) + ' to ' + Math.round(r.right) + ']';
  });

  // how much of its own box each text block fills
  const range = document.createRange();
  const fill = (el) => {
    const box = el.getBoundingClientRect();
    if (box.width < 120) return null;
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter(r => r.width > 1 && r.height > 1);
    if (!rects.length) return null;
    // Group rects into LINES before measuring. A line holding an inline <b> or
    // <em> produces several rects, and taking the widest rect measures the
    // widest fragment instead of the widest line, which reports a full width
    // heading as filling 60% of its row.
    const lines = [];
    for (const r of rects) {
      const row = lines.find(l => Math.abs(l.top - r.top) <= 4);
      if (row) { row.left = Math.min(row.left, r.left); row.right = Math.max(row.right, r.right); }
      else lines.push({ top: r.top, left: r.left, right: r.right });
    }
    const widest = Math.max(...lines.map(l => l.right - l.left));
    return { pct: Math.round(widest / box.width * 100), lines: lines.length, boxW: Math.round(box.width) };
  };

  for (const h of document.querySelectorAll('h1, h2, .say, .sh')) {
    const f = fill(h);
    if (!f) continue;
    out.heads.push({ ...f, size: Math.round(parseFloat(getComputedStyle(h).fontSize)), text: h.textContent.trim().slice(0, 46) });
  }
  for (const p of document.querySelectorAll('p, li, .lede, figcaption')) {
    const f = fill(p);
    if (!f || f.lines < 2 || f.boxW < 300) continue;
    out.blocks.push({ ...f, text: p.textContent.trim().slice(0, 46) });
  }

  // a section whose GROUND is a photograph: a direct img/video child painted
  // behind the content, or a background-image that resolves to a file
  const secs = [...document.querySelectorAll('body > section, body > div.hang, body > footer')];
  out.sections = secs.length;
  for (const s of secs) {
    const direct = [...s.children].find(c => (c.tagName === 'IMG' || c.tagName === 'VIDEO'));
    if (direct) {
      const cs = getComputedStyle(direct);
      if (cs.position === 'absolute' || cs.position === 'fixed') {
        // A picture blurred past legibility is a colour field, not a
        // photographic scroll moment, which is what the cap is actually about.
        const b = /blur\(([\d.]+)px\)/.exec(cs.filter || '');
        if (!b || parseFloat(b[1]) < 12) out.grounds++;
      }
      continue;
    }
    const bg = getComputedStyle(s).backgroundImage;
    if (bg && /url\(["']?(?!data:)/.test(bg)) out.grounds++;
  }
  out.eyebrows = document.querySelectorAll('.eyebrow, .k, .ck, .kicker, .sec-label').length;

  // vertical dead space: walk painted boxes down the page and flag big holes
  const painted = [...document.querySelectorAll('body *')].filter(el => {
    const r = el.getBoundingClientRect();
    if (r.width < 40 || r.height < 8) return false;
    const cs = getComputedStyle(el);
    if (cs.position === 'fixed' || cs.visibility === 'hidden') return false;
    if (el.closest('.grain, .vig, .scan, .rays')) return false;
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    const isMedia = el.tagName === 'IMG' || el.tagName === 'VIDEO' || el.tagName === 'BUTTON' || el.tagName === 'A';
    return hasText || isMedia;
  }).map(el => { const r = el.getBoundingClientRect(); return { t: r.top + scrollY, b: r.bottom + scrollY }; })
    .sort((a, b) => a.t - b.t);
  let reach = 0;
  for (const p of painted) {
    if (p.t - reach > 220 && reach > 0) out.gaps.push({ from: Math.round(reach), to: Math.round(p.t), px: Math.round(p.t - reach) });
    reach = Math.max(reach, p.b);
  }
  return JSON.stringify(out);
})()`;

async function run(file, width) {
  const port = 9000 + Math.floor(Math.random() * 4000);
  const profile = `${process.env.TEMP || '/tmp'}/ev-audit-${port}`;
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
    await send('Emulation.setDeviceMetricsOverride', { width, height: 940, deviceScaleFactor: 1, mobile: width < 500 });
    await send('Page.navigate', { url: pathToFileURL(resolve(REPO, file)).href });
    await sleep(2400);
    const r = await send('Runtime.evaluate', { expression: MEASURE, awaitPromise: true, returnByValue: true });
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
  console.log(`\n======== ${file} ========`);
  for (const w of WIDTHS) {
    const m = await run(file, w);
    const side = m.scrollW > m.clientW + 2 ? `SIDEWAYS +${m.scrollW - m.clientW}px` : 'no sideways scroll';
    console.log(`  ${String(w).padStart(4)}px  ${side}`);
    if (m.over.length) console.log(`         past right edge: ${m.over.join(' | ')}`);
    if (w !== 1440) continue;

    console.log(`         sections=${m.sections}  photographic grounds=${m.grounds} (cap 2)  eyebrows=${m.eyebrows} (cap ${Math.ceil(m.sections / 3)})`);
    const badHead = m.heads.filter((h) => h.size >= 26 && (h.lines > 1 || h.pct < 84));
    if (!badHead.length) console.log('         headings: all one line and filling their measure');
    badHead.forEach((h) => console.log(`         HEAD ${String(h.pct).padStart(3)}% ${h.lines} lines ${h.size}px in ${h.boxW}px  ${JSON.stringify(h.text)}`));
    const badBlock = m.blocks.filter((b) => b.pct < 84);
    if (badBlock.length) badBlock.slice(0, 6).forEach((b) => console.log(`         BLOCK ${String(b.pct).padStart(3)}% of ${b.boxW}px  ${JSON.stringify(b.text)}`));
    if (m.gaps.length) m.gaps.slice(0, 6).forEach((g) => console.log(`         GAP ${g.px}px of dead space at y=${g.from}`));
    else console.log('         no dead space over 220px');
  }
}
process.exit(0);
