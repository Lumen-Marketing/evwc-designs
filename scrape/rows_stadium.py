# -*- coding: utf-8 -*-
# Back to the stadium beside the type, but at roughly twice the size. Filling the
# whole band meant cropping portrait phone frames to a 7:1 letterbox, which reads
# as stretched however it is treated; a 2:1 stadium is a crop the source can
# actually carry.
import re
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

start = s.index('/* ---------- services: one run of photographic bands ----------')
end = s.index('/* ---------- full-bleed break ---------- */')
NEW = """/* ---------- services: one ruled run of rows ----------
   Each row is the whole thing at a glance: what it is, a picture of it, what it
   involves, and a way to ask for it. The row is the link, so the arrow is not
   decoration. The stadium runs about twice the size it started at: big enough to
   carry a face and a tool, small enough that the crop stays honest to a portrait
   phone frame. */
.svc{padding-bottom:clamp(64px,9vw,132px)}
.rows{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.ghead{padding:clamp(28px,3.2vw,46px) clamp(10px,1.4vw,22px) clamp(9px,1.1vw,15px);
  font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#6f7679}
.ghead:first-child{padding-top:clamp(18px,2vw,28px)}
.row a{display:grid;align-items:center;text-decoration:none;position:relative;
  grid-template-columns:minmax(0,1.1fr) clamp(184px,20.5vw,306px) minmax(0,.95fr) 44px;
  gap:clamp(14px,2vw,36px);
  padding-block:clamp(18px,2.3vw,32px);padding-inline:clamp(10px,1.4vw,22px);
  border-bottom:1px solid var(--line);
  transition:background .45s var(--ez-out)}
.row a:hover{background:linear-gradient(90deg,rgba(18,196,222,.1),rgba(18,196,222,.015) 62%)}
.row a:focus-visible{outline-offset:-3px}
.rn{font-family:var(--d);font-weight:800;line-height:1.04;letter-spacing:-.034em;
  font-size:clamp(21px,2.6vw,38px)}
.rk{display:block;margin-top:7px;font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;
  color:#6f7679}
/* a stadium of the job itself, sitting slightly proud of the row */
.rpic{margin:0;overflow:hidden;border-radius:999px;aspect-ratio:2/1;background:var(--bg-2);
  box-shadow:var(--lift-2),inset 0 0 0 1px rgba(255,255,255,.1);
  transition:box-shadow .5s var(--ez-out),transform .5s var(--ez-out)}
.rpic img{width:100%;height:100%;object-fit:cover;
  filter:saturate(.92) contrast(1.02);
  transition:transform .9s var(--ez),filter .6s var(--ez-out)}
.rd{font-size:15px;line-height:1.55;color:var(--fg-2)}
.ra{justify-self:end;color:#6f7679;display:inline-flex;
  transition:color .35s var(--ez-out),transform .35s var(--ez-out)}
.ra svg{width:30px;height:30px;fill:none;stroke:currentColor;stroke-width:1.5;
  stroke-linecap:round;stroke-linejoin:round}
@media (hover:hover) and (pointer:fine){
  .row a:hover .rpic{transform:translateY(-3px);
    box-shadow:var(--lift-3),inset 0 0 0 1px rgba(18,196,222,.5)}
  .row a:hover .rpic img{transform:scale(1.06);filter:saturate(1.05) contrast(1)}
  .row a:hover .ra{color:var(--acc);transform:translateX(7px)}
}

"""
s = s[:start] + NEW + s[end:]
done.append('rows css')

# the band goes back to being a thumbnail; the focal points stay, they are what
# keeps a portrait frame from cropping to somebody's knees
ALT = {
    'job-glass-wide.jpg': 'A squeegee on a pole clearing water off a commercial glass frontage',
    'job-squeegee.jpg':   'A squeegee drawing an arc of water down a pane of glass',
    'ba-before.jpg':      'A commercial glass frontage before cleaning, the panes hazy with dust and hard water film',
    'restaurant.jpg':     'Looking out through a spotless full height restaurant window onto an Arizona parking lot',
    'job-solar-sky.jpg':  'A rooftop solar array on terracotta tile under a bank of cloud',
    'job-pole-wide.jpg':  'A water-fed pole extended to the top of a commercial storefront, two cleaners working below it',
    'job-haul.jpg':       'A pile of dumped furniture and cardboard in a walled back yard before it was hauled away',
}

def thumb(m):
    inner = m.group(1)
    f = re.search(r'assets/([^"]+)', inner).group(1)
    inner = inner.replace(' class="hi"', '')
    inner = re.sub(r'alt="[^"]*"', 'alt="%s"' % ALT[f], inner)
    return '<figure class="rpic">%s</figure>' % inner

s, n = re.subn(r'<figure class="rbg" aria-hidden="true">(.*?)</figure>', thumb, s)
assert n == 7, n
done.append('%d thumbnails' % n)

rep("""  .row a{grid-template-columns:minmax(0,1fr) 34px;
    gap:clamp(12px,2.4vw,24px);row-gap:13px;align-items:start;
    padding-block:clamp(24px,5vw,34px)}
  .row a>span:first-child{grid-column:1;grid-row:1}
  .ra{grid-column:2;grid-row:1;align-self:center}
  .rd{grid-column:1 / -1;grid-row:2;font-size:14.5px}
  .rbg::before{background:
    linear-gradient(90deg,rgba(8,9,10,.93),rgba(8,9,10,.84) 52%,rgba(8,9,10,.7)),
    linear-gradient(180deg,rgba(8,9,10,.6),transparent 34%,transparent 66%,rgba(8,9,10,.66))}""",
"""  .row a{grid-template-columns:minmax(0,1fr) clamp(150px,22vw,220px) 34px;
    gap:clamp(12px,2.4vw,26px);row-gap:16px;align-items:start;
    padding-block:clamp(20px,3.4vw,28px)}
  .row a>span:first-child{grid-column:1;grid-row:1}
  .rpic{grid-column:2;grid-row:1;align-self:center}
  .ra{grid-column:3;grid-row:1;align-self:center}
  .rd{grid-column:1 / -1;grid-row:2;font-size:14.5px}""", 'rows mq')

open(p, 'w', encoding='utf-8').write(s)
print('stadium:', len(done), 'edits ->', ', '.join(done))
