# -*- coding: utf-8 -*-
p = '02-broadsheet.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep("""/* a wide plate of the work, offset straight down so it stays on the centre line */
.pband{margin:0;position:relative;isolation:isolate}
.pband::before,.pband::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.pband::before{background:var(--deep);transform:translate(0,24px)}
.pband::after{background:var(--cyan);transform:translate(0,12px)}
.pband-in{position:relative;z-index:1;padding:10px;border-radius:var(--r-card);background:var(--limestone);
  box-shadow:var(--lift-3)}
.pband .m{position:relative;border-radius:calc(var(--r-card) - 10px);overflow:hidden;aspect-ratio:21/9;
  background:var(--deep)}
.pband img{width:100%;height:100%;object-fit:cover}
.pband .cap{position:absolute;left:clamp(16px,2vw,26px);bottom:clamp(16px,2vw,26px);
  background:var(--limestone);border-radius:var(--r-pill);padding:9px 19px;font-size:12.5px;
  font-weight:700;letter-spacing:.1em;text-transform:uppercase}""",
"""/* three tall plates of the work, one per family of jobs, each a link into the
   schedule below. The colour planes step down behind the row rather than behind
   each card, so the group reads as one object. */
.trio{position:relative;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));
  gap:clamp(12px,1.6vw,22px);isolation:isolate}
.trio::before,.trio::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.trio::before{background:var(--deep);transform:translate(0,26px)}
.trio::after{background:var(--cyan);transform:translate(0,13px)}
.tcard{position:relative;z-index:1;margin:0;display:block;text-decoration:none;color:inherit;
  padding:9px;border-radius:var(--r-card);background:var(--limestone);box-shadow:var(--lift-3);
  transition:transform .5s var(--ez-out),box-shadow .5s var(--ez-out)}
.tcard .m{position:relative;overflow:hidden;border-radius:calc(var(--r-card) - 9px);
  aspect-ratio:3/4;background:var(--deep)}
.tcard img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--ez)}
.tcard .m::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 42%,rgba(10,15,18,.86))}
.tcard .lab{position:absolute;z-index:2;left:clamp(14px,1.6vw,22px);right:clamp(14px,1.6vw,22px);
  bottom:clamp(14px,1.6vw,22px);color:var(--chalk)}
.tcard .lab .ic{width:44px;height:44px;border-radius:var(--r-sm);display:grid;place-items:center;
  background:rgba(255,255,255,.14);color:var(--cyan);margin-bottom:14px;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.28)}
.tcard .lab .ic svg{width:22px;height:22px}
.tcard .lab b{display:block;font-family:var(--d);font-weight:400;text-transform:uppercase;
  letter-spacing:.02em;line-height:1;font-size:clamp(20px,2.1vw,30px)}
.tcard .lab span{display:block;margin-top:9px;font-size:14px;line-height:1.45;color:#d5e1e5}
@media (hover:hover) and (pointer:fine){
  .tcard:hover{transform:translateY(-7px);box-shadow:var(--lift-3),0 0 0 2px var(--cyan)}
  .tcard:hover img{transform:scale(1.05)}
}""", 'trio css')

TRIO = [
    ('job-squeegee.jpg', 540, 720,
     'A squeegee on a pole drawing an arc of water down a commercial glass frontage',
     '<rect x="3" y="3" width="18" height="18" rx="1.5"/><path d="M12 3v18M3 12h18"/>',
     'Glass', 'Windows in and out, screens, tracks and hard water stains.'),
    ('job-solar-sky.jpg', 540, 960,
     'A rooftop solar array on terracotta tile under a bank of cloud',
     '<path d="M3 16 6 6h12l3 10H3Z"/><path d="M3 16v3h18v-3M9 6l-1 10M15 6l1 10"/>',
     'Film and panels', 'UV and privacy film, and solar arrays washed back to output.'),
    ('job-haul.jpg', 820, 1094,
     'A pile of dumped furniture and cardboard in a walled back yard before it was hauled away',
     '<path d="M3 7h18l-1.4 13H4.4L3 7Z"/><path d="M8.5 7V4.5h7V7M10 11v5M14 11v5"/>',
     'Property', 'Pressure washing, plus junk and monsoon debris hauled away.'),
]

cards = []
for img, w, h, alt, path, name, desc in TRIO:
    cards.append(
'''      <a class="tcard" href="#services">
        <div class="m"><img src="assets/%s" alt="%s" loading="lazy" width="%d" height="%d">
          <span class="lab"><span class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg></span><b>%s</b><span>%s</span></span>
        </div>
      </a>''' % (img, alt, w, h, path, name, desc))

rep("""    <figure class="pband">
      <div class="pband-in">
        <div class="m"><img src="assets/job-pole-wide.jpg" alt="A water-fed pole extended to the top of a commercial storefront, two cleaners working below it" loading="lazy" width="1280" height="722"><span class="cap">Two storey reach, no ladder</span></div>
      </div>
    </figure>""",
"""    <div class="trio">
%s
    </div>""" % '\n'.join(cards), 'trio markup')

rep("  .ctaband{grid-template-columns:1fr;gap:clamp(26px,5vw,40px)}",
    "  .trio{grid-template-columns:1fr;gap:clamp(14px,3vw,20px)}\n  .tcard .m{aspect-ratio:16/10}\n  .ctaband{grid-template-columns:1fr;gap:clamp(26px,5vw,40px)}",
    'trio mq')

open(p, 'w', encoding='utf-8').write(s)
print('basic trio:', len(done), 'edits ->', ', '.join(done))
