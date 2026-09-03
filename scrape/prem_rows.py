# -*- coding: utf-8 -*-
from urllib.parse import quote
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep("""/* ---------- services: grouped clusters, no cards, no icons ---------- */
.svc{padding-bottom:clamp(64px,9vw,132px)}
.cluster{display:grid;grid-template-columns:minmax(0,.3fr) minmax(0,1fr) minmax(0,.6fr);
  gap:clamp(20px,3.4vw,56px);padding-block:clamp(30px,3.6vw,52px);border-top:1px solid var(--line)}
/* the photograph takes the column the copy was leaving empty, and stretches to
   whatever height its group runs to rather than setting one of its own */
.cpic{margin:0;position:relative;overflow:hidden;border-radius:18px;background:var(--bg-2);
  min-height:clamp(210px,24vw,400px);
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.07),var(--rim)}
.cpic img{width:100%;height:100%;object-fit:cover;transition:transform 1.1s var(--ez)}
.cpic figcaption{position:absolute;inset:auto 0 0 0;z-index:2;padding:26px 15px 13px;font-size:12.5px;
  color:#e6eaeb;background:linear-gradient(180deg,transparent,rgba(8,9,10,.8))}
@media (hover:hover) and (pointer:fine){.cluster:hover .cpic img{transform:scale(1.04)}}
.cluster h3{font-family:var(--b);font-weight:500;font-size:14px;letter-spacing:.02em;color:var(--fg-2);line-height:1.5}
.cluster ul{margin:0;padding:0;list-style:none;display:grid;gap:clamp(14px,1.6vw,22px)}
.cluster li{font-family:var(--d);font-weight:800;font-size:clamp(24px,3.4vw,44px);line-height:1.06;letter-spacing:-.035em}
.cluster li span{display:block;font-family:var(--b);font-weight:400;font-size:15.5px;line-height:1.55;letter-spacing:0;color:var(--fg-2);margin-top:9px;max-width:52ch}""",
"""/* ---------- services: one ruled run of rows ----------
   Each row is the whole thing at a glance: what it is, a picture of it, what it
   involves, and a way to ask for it. The row is the link, so the arrow is not
   decoration. */
.svc{padding-bottom:clamp(64px,9vw,132px)}
.rows{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.ghead{padding:clamp(26px,3vw,42px) clamp(10px,1.4vw,22px) clamp(8px,1vw,14px);
  font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#6f7679}
.ghead:first-child{padding-top:clamp(18px,2vw,28px)}
.row a{display:grid;align-items:center;text-decoration:none;position:relative;
  grid-template-columns:minmax(0,1.02fr) clamp(112px,12.5vw,186px) minmax(0,.88fr) 44px;
  gap:clamp(14px,2.2vw,38px);
  padding-block:clamp(16px,2vw,26px);padding-inline:clamp(10px,1.4vw,22px);
  border-bottom:1px solid var(--line);
  transition:background .45s var(--ez-out)}
.row a:hover{background:linear-gradient(90deg,rgba(18,196,222,.1),rgba(18,196,222,.015) 62%)}
.row a:focus-visible{outline-offset:-3px}
.rn{font-family:var(--d);font-weight:800;line-height:1.04;letter-spacing:-.034em;
  font-size:clamp(21px,2.6vw,38px)}
.rk{display:block;margin-top:7px;font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;
  color:#6f7679}
/* a stadium of the job itself, small enough that a soft source still holds up */
.rpic{margin:0;overflow:hidden;border-radius:999px;aspect-ratio:2.5/1;background:var(--bg-2);
  box-shadow:var(--lift-1),inset 0 0 0 1px rgba(255,255,255,.09)}
.rpic img{width:100%;height:100%;object-fit:cover;transition:transform .9s var(--ez)}
.rd{font-size:15px;line-height:1.55;color:var(--fg-2)}
.ra{justify-self:end;color:#6f7679;display:inline-flex;
  transition:color .35s var(--ez-out),transform .35s var(--ez-out)}
.ra svg{width:30px;height:30px;fill:none;stroke:currentColor;stroke-width:1.5;
  stroke-linecap:round;stroke-linejoin:round}
@media (hover:hover) and (pointer:fine){
  .row a:hover .rpic img{transform:scale(1.07)}
  .row a:hover .ra{color:var(--acc);transform:translateX(7px)}
}""", 'rows css')

ROWS = [
    ("Glass", [
        ("Interior and exterior windows", "Homes and businesses", "job-glass-wide.jpg", 1280, 722,
         "A squeegee on a pole clearing water off a commercial glass frontage",
         "Streak free, single storey up to multi storey, using purified water and a water-fed pole where the height calls for it.",
         "interior and exterior windows"),
        ("Screens and tracks", "Pulled, washed, re-set", "storefront.jpg", 1200, 1200,
         "A clean glass shopfront with door and window signage",
         "Screens pulled, washed and re-set. Sills and sliding tracks vacuumed and scrubbed out.",
         "screens and tracks"),
        ("Hard water stain removal", "Mineral etching", "ba-before.jpg", 390, 488,
         "A commercial glass frontage before cleaning, the panes hazy with dust and hard water film",
         "Mineral etching from sprinkler overspray and monsoon dust cut back off the glass.",
         "hard water stain removal"),
    ]),
    ("Film and panels", [
        ("Window tinting", "UV, heat and privacy film", "restaurant.jpg", 1400, 1750,
         "Looking out through a spotless full height restaurant window onto an Arizona parking lot",
         "UV and heat film to protect furnishings and hold the AC in, plus reflective film for privacy.",
         "window tinting"),
        ("Solar panel cleaning", "Output you paid for", "job-solar-sky.jpg", 540, 960,
         "A rooftop solar array on terracotta tile under a bank of cloud",
         "Dust and hard water film lifted off panels so the array stops losing output to grime.",
         "solar panel cleaning"),
    ]),
    ("Property", [
        ("Pressure washing", "Driveways to elevations", "job-pole-wide.jpg", 1280, 722,
         "A water-fed pole extended to the top of a commercial storefront, two cleaners working below it",
         "Driveways, walkways, patios and building exteriors brought back to colour.",
         "pressure washing"),
        ("Junk removal and hauling", "Loaded and taken away", "job-haul.jpg", 820, 1094,
         "A pile of dumped furniture and cardboard in a walled back yard before it was hauled away",
         "Monsoon debris, rental clear-outs and listing prep loaded up and taken away.",
         "junk removal"),
    ]),
]

out = ['<section class="svc wrap" id="services">', '  <ol class="rows">']
for group, rows in ROWS:
    out.append('    <li class="ghead">%s</li>' % group)
    for name, kick, img, w, h, alt, desc, topic in rows:
        body = quote("Hi, I'd like a quote for %s." % topic, safe='')
        out.append('    <li class="row rv"><a href="sms:+14808069455?&amp;body=%s">' % body)
        out.append('      <span><span class="rn">%s</span><span class="rk">%s</span></span>' % (name, kick))
        out.append('      <figure class="rpic"><img src="assets/%s" alt="%s" loading="lazy" width="%d" height="%d"></figure>' % (img, alt, w, h))
        out.append('      <span class="rd">%s</span>' % desc)
        out.append('      <span class="ra" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M4 12h15M13.5 6 20 12l-6.5 6"/></svg></span>')
        out.append('    </a></li>')
out.append('  </ol>')
out.append('</section>')
NEW = '\n'.join(out)

start = s.index('<section class="svc wrap" id="services">')
end = s.index('</section>', start) + len('</section>')
s = s[:start] + NEW + s[end:]
done.append('rows markup')

rep("""  .stats{grid-template-columns:repeat(2,1fr)}
  .cluster{grid-template-columns:1fr;gap:16px}""",
"""  .stats{grid-template-columns:repeat(2,1fr)}
  .row a{grid-template-columns:minmax(0,1fr) clamp(96px,14vw,150px) 34px;
    gap:clamp(12px,2.4vw,24px);row-gap:14px}
  .rd{grid-column:1 / -1;font-size:14.5px}""", 'rows mq')

rep("  .cpic{min-height:0;aspect-ratio:16/10;margin-top:6px}\n", "", 'drop cpic mq')

open(p, 'w', encoding='utf-8').write(s)
print('premium rows:', len(done), 'edits ->', ', '.join(done))
