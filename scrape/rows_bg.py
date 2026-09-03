# -*- coding: utf-8 -*-
import re
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---------------------------------------------------------------- CSS -------
rep("""/* ---------- services: one ruled run of rows ----------
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
}""",
"""/* ---------- services: one run of photographic bands ----------
   The picture of the job IS the row. It sits behind the type, held back with a
   sideways scrim and desaturated at rest so seven of them in a column still read
   as one calm list; on hover the row it belongs to comes up to full colour and
   pushes in slightly, so only the one you are pointing at is loud. */
.svc{padding-bottom:clamp(64px,9vw,132px)}
.rows{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.ghead{padding:clamp(30px,3.4vw,48px) clamp(10px,1.4vw,22px) clamp(10px,1.2vw,16px);
  font-size:13px;letter-spacing:.15em;text-transform:uppercase;color:#6f7679}
.ghead:first-child{padding-top:clamp(18px,2vw,28px)}
.row a{display:grid;align-items:center;text-decoration:none;position:relative;
  isolation:isolate;overflow:hidden;
  grid-template-columns:minmax(0,1.16fr) minmax(0,1fr) 44px;
  gap:clamp(16px,2.6vw,52px);
  padding-block:clamp(28px,3.6vw,52px);padding-inline:clamp(18px,2.2vw,34px);
  border-bottom:1px solid rgba(255,255,255,.11)}
.row a:focus-visible{outline-offset:-3px}
/* the photograph, filling the band */
.rbg{position:absolute;inset:0;z-index:-1;margin:0;overflow:hidden;background:var(--bg-2);
  box-shadow:inset 0 0 0 0 var(--acc);
  transition:box-shadow .5s var(--ez-out)}
.rbg img{width:100%;height:100%;object-fit:cover;transform:scale(1.05);
  filter:grayscale(.6) brightness(.44) contrast(1.06);
  transition:transform 1.3s var(--ez),filter .7s var(--ez-out)}
/* held back sideways so the name always has a dark field under it, and top and
   bottom so consecutive bands do not run into one another */
.rbg::before,.rbg::after{content:"";position:absolute;inset:0;pointer-events:none}
.rbg::before{background:
  linear-gradient(90deg,rgba(8,9,10,.94),rgba(8,9,10,.8) 44%,rgba(8,9,10,.52)),
  linear-gradient(180deg,rgba(8,9,10,.6),transparent 34%,transparent 66%,rgba(8,9,10,.66));
  transition:opacity .6s var(--ez-out)}
.rbg::after{background:linear-gradient(90deg,rgba(18,196,222,.2),rgba(18,196,222,.02) 58%);
  opacity:0;transition:opacity .5s var(--ez-out)}
.rn{font-family:var(--d);font-weight:800;line-height:1.04;letter-spacing:-.034em;
  font-size:clamp(22px,2.7vw,40px);text-shadow:0 2px 26px rgba(0,0,0,.85)}
.rk{display:block;margin-top:8px;font-size:12.5px;letter-spacing:.09em;text-transform:uppercase;
  color:rgba(242,243,243,.62);text-shadow:0 1px 16px rgba(0,0,0,.85)}
.rd{font-size:15px;line-height:1.55;color:#dde2e3;text-shadow:0 1px 16px rgba(0,0,0,.8)}
.ra{justify-self:end;color:rgba(242,243,243,.5);display:inline-flex;
  transition:color .35s var(--ez-out),transform .35s var(--ez-out)}
.ra svg{width:30px;height:30px;fill:none;stroke:currentColor;stroke-width:1.5;
  stroke-linecap:round;stroke-linejoin:round}
@media (hover:hover) and (pointer:fine){
  .row a:hover .rbg img{transform:scale(1.11);filter:grayscale(0) brightness(.6) contrast(1.02)}
  .row a:hover .rbg::before{opacity:.8}
  .row a:hover .rbg::after{opacity:1}
  .row a:hover .rbg{box-shadow:inset 4px 0 0 0 var(--acc)}
  .row a:hover .ra{color:var(--acc);transform:translateX(7px)}
}""", 'rows css')

# ------------------------------------------------------------- markup -------
# the thumbnail figure becomes the band behind the row
POS = {
    'job-glass-wide.jpg': '50% 44%',
    'storefront.jpg':     '50% 50%',
    'ba-before.jpg':      '50% 40%',
    'restaurant.jpg':     '50% 38%',
    'job-solar-sky.jpg':  '50% 46%',
    'job-pole-wide.jpg':  '50% 40%',
    'job-haul.jpg':       '50% 50%',
}

def band(m):
    inner = m.group(1)
    f = re.search(r'assets/([^"]+)', inner).group(1)
    inner = inner.replace('<img ', '<img style="object-position:%s" ' % POS.get(f, '50% 45%'), 1)
    return '<figure class="rbg" aria-hidden="true">%s</figure>' % inner

s, n = re.subn(r'<figure class="rpic">(.*?)</figure>', band, s)
print('bands:', n)
assert n == 7, n
done.append('%d bands' % n)

# the row is now: name block, band, description, arrow -> band is out of flow,
# so nothing else needs re-ordering. Fix the small-screen grid.
rep("""  .row a{grid-template-columns:minmax(0,1fr) clamp(96px,14vw,150px) 34px;
    gap:clamp(12px,2.4vw,24px);row-gap:14px;align-items:start}
  .row a>span:first-child{grid-column:1;grid-row:1}
  .rpic{grid-column:2;grid-row:1;align-self:center}
  .ra{grid-column:3;grid-row:1;align-self:center}
  .rd{grid-column:1 / -1;grid-row:2;font-size:14.5px}""",
"""  .row a{grid-template-columns:minmax(0,1fr) 34px;
    gap:clamp(12px,2.4vw,24px);row-gap:13px;align-items:start;
    padding-block:clamp(24px,5vw,34px)}
  .row a>span:first-child{grid-column:1;grid-row:1}
  .ra{grid-column:2;grid-row:1;align-self:center}
  .rd{grid-column:1 / -1;grid-row:2;font-size:14.5px}
  .rbg::before{background:
    linear-gradient(90deg,rgba(8,9,10,.93),rgba(8,9,10,.84) 52%,rgba(8,9,10,.7)),
    linear-gradient(180deg,rgba(8,9,10,.6),transparent 34%,transparent 66%,rgba(8,9,10,.66))}""",
    'rows mq')

open(p, 'w', encoding='utf-8').write(s)
print('rows bg:', len(done), 'edits ->', ', '.join(done))
