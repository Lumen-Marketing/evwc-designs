# -*- coding: utf-8 -*-
# 02's recent work was a seven plate grid. A grid shows everything at once and
# nothing at size, which on a trades page is the wrong trade: the photography IS
# the product. This direction is film stock, so the component is a PROJECTOR.
# One frame at a time at full size, a contact sheet of the reel underneath, and
# a film cut between them.
#
# It must not repeat 01, which already owns the drag filmstrip, and it must not
# be the same component as 03. 03 travels along a line; this one replaces the
# picture in place. Different interaction model, not a restyle.
p = '02-site.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------------ CSS -----
OLD_CSS_START = '.gal{display:grid;grid-template-columns:1fr 1fr;gap:clamp(14px,2vw,24px);margin-top:48px}'
i = s.index(OLD_CSS_START)
j = s.index('@media (max-width:720px){', i)
NEW_CSS = """/* ---------- RECENT WORK: the projector ----------
   One frame at a time, projected at full width, with the reel laid out as a
   contact sheet under it. Frames are stacked and crossfaded rather than moved,
   because a projector changes the picture in place; the outgoing frame goes
   soft on its way out, which is the same film cut the rest of this direction
   uses. Every source is a phone frame at a different aspect, so each one keeps
   a hand set object-position and the crop lands on the work. */
.projx{margin-top:clamp(30px,4vw,48px)}
.stage{position:relative;aspect-ratio:3/2;overflow:hidden;background:#000;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 50px 110px -50px rgba(0,0,0,.95)}
.frame{position:absolute;inset:0;margin:0;opacity:0;filter:blur(9px);transform:scale(1.025);
  transition:opacity .5s cubic-bezier(.16,1,.3,1),filter .5s cubic-bezier(.16,1,.3,1),
             transform .7s cubic-bezier(.16,1,.3,1);
  pointer-events:none}
.frame[data-on]{opacity:1;filter:none;transform:none;pointer-events:auto}
.frame img,.frame video{width:100%;height:100%;object-fit:cover;display:block}
/* the gate: a soft edge at the foot so the caption always has a field */
.stage::after{content:"";position:absolute;left:0;right:0;bottom:0;height:52%;z-index:2;
  pointer-events:none;background:linear-gradient(180deg,rgba(7,12,20,0),rgba(7,12,20,.9))}
.pcap{position:absolute;left:0;right:0;bottom:0;z-index:3;
  padding:clamp(18px,2.6vw,34px);display:flex;align-items:flex-end;
  gap:clamp(14px,2vw,26px);flex-wrap:wrap}
.pcap b{display:block;font-family:'Big Shoulders Display',sans-serif;
  font-size:clamp(24px,3.4vw,44px);font-weight:800;text-transform:uppercase;
  letter-spacing:.03em;color:#fff;line-height:1}
.pcap span{display:block;margin-top:6px;font-size:14.5px;color:var(--fg-2);max-width:46ch}
.pcount{margin-left:auto;font-family:'Big Shoulders Display',sans-serif;font-weight:700;
  font-size:15px;letter-spacing:.22em;color:rgba(255,255,255,.66);
  font-variant-numeric:tabular-nums;white-space:nowrap}
/* the gate arms. 48px, so they clear the 44px minimum on a touch screen. */
.pnav{position:absolute;top:50%;z-index:4;transform:translateY(-50%);
  width:48px;height:48px;display:grid;place-items:center;cursor:pointer;
  border:1px solid rgba(255,255,255,.34);background:rgba(7,12,20,.5);color:#fff;
  -webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);
  transition:background .25s,border-color .25s,transform .25s}
.pnav:hover{background:rgba(7,12,20,.78);border-color:#fff}
.pnav:active{transform:translateY(-50%) scale(.94)}
.pnav svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}
.pnav.prev{left:clamp(12px,1.6vw,20px)}
.pnav.next{right:clamp(12px,1.6vw,20px)}
/* the contact sheet. Numbered, because a reel is numbered. */
.sheet{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));
  gap:clamp(8px,1vw,14px);margin-top:clamp(10px,1.4vw,18px)}
.cell{position:relative;padding:0;border:0;cursor:pointer;background:#000;
  aspect-ratio:3/2;overflow:hidden;opacity:.42;
  transition:opacity .35s cubic-bezier(.16,1,.3,1),box-shadow .35s cubic-bezier(.16,1,.3,1);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.1)}
.cell img{width:100%;height:100%;object-fit:cover;display:block}
.cell:hover{opacity:.78}
.cell[aria-current="true"]{opacity:1;box-shadow:inset 0 0 0 2px var(--blue)}
.cell .num{position:absolute;left:0;top:0;z-index:2;padding:4px 7px;
  font-family:'Big Shoulders Display',sans-serif;font-weight:700;font-size:12px;
  letter-spacing:.12em;color:#fff;background:rgba(7,12,20,.66);
  font-variant-numeric:tabular-nums}
@media (max-width:760px){
  .stage{aspect-ratio:4/3}
  .pcap{padding:16px}
  /* seven thumbnails at a phone's width would be 40px each, under the touch
     minimum and too small to read. They become a snapping strip instead. */
  .sheet{display:flex;overflow-x:auto;overscroll-behavior-x:contain;
    scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;
    margin-inline:calc(var(--pad) * -1);padding-inline:var(--pad);
    scrollbar-width:none}
  .sheet::-webkit-scrollbar{display:none}
  .cell{flex:0 0 92px;scroll-snap-align:center}
}
"""
s = s[:i] + NEW_CSS + s[j:]
done.append('projector css')

# the old gallery rules that lived past the media query go too
import re
s2, n = re.subn(r'@media \(max-width:720px\)\{\.gal[^\n]*\n', '', s)
s = s2
done.append('dropped %d stale gal rules' % n)

# ---------------------------------------------------------------- markup -----
SHOTS = [
    ('img',   'assets/plate-pole.jpg', 900, 1200, '50% 62%',
     'A water-fed pole worked across an arched upper window',
     'Residential upper glass', 'Arched second storey windows, worked from the ground.'),
    ('video', 'assets/reel-solar.mp4', 540, 960, '50% 50%',
     'A solar array being rinsed',
     'Solar array rinse', 'Dust and hard water film lifted off.', 'assets/poster-solar.jpg'),
    ('video', 'assets/reel-storefront-wide.mp4', 1280, 722, '50% 45%',
     'Storefront glazing being cleaned',
     'Commercial storefront', 'Mesa. Exterior glass, frames and screens.', 'assets/poster-storefront-wide.jpg'),
    ('img',   'assets/restaurant.jpg', 1400, 1750, '50% 42%',
     'Restaurant frontage glazing after cleaning',
     'Restaurant frontage', 'Street-facing glass, cleaned before service.'),
    ('img',   'assets/storefront.jpg', 1200, 1200, '50% 50%',
     'Retail entry glazing, doors and sidelights',
     'Retail entry', 'Doors, sidelights and the frames around them.'),
    ('img',   'assets/junk-yard.jpg', 820, 1094, '50% 55%',
     'A yard cleared of monsoon debris',
     'Junk removal', 'Monsoon debris loaded up and taken away.'),
    ('img',   'assets/rig.jpg', 1200, 1200, '50% 50%',
     'The work van and equipment',
     'The rig', 'Everything on one van, on the route daily.'),
]

frames, cells = [], []
for k, sh in enumerate(SHOTS):
    kind, src, w, h, pos, alt, title, desc = sh[:8]
    on = ' data-on' if k == 0 else ''
    if kind == 'img':
        media = ('<img src="%s" width="%d" height="%d" %s style="object-position:%s" alt="%s">'
                 % (src, w, h, 'fetchpriority="high"' if k == 0 else 'loading="lazy"', pos, alt))
        thumb = src
    else:
        poster = sh[8]
        media = ('<video src="%s" poster="%s" muted loop playsinline preload="none" '
                 'width="%d" height="%d" style="object-position:%s" aria-label="%s"></video>'
                 % (src, poster, w, h, pos, alt))
        thumb = poster
    frames.append('        <figure class="frame"%s data-i="%d" aria-roledescription="slide" '
                  'aria-label="%d of 7, %s">%s</figure>' % (on, k, k + 1, title, media))
    cells.append('        <button class="cell" type="button" data-i="%d" aria-current="%s" '
                 'aria-label="Show frame %d, %s"><img src="%s" width="%d" height="%d" loading="lazy" alt="">'
                 '<span class="num">%02d</span></button>'
                 % (k, 'true' if k == 0 else 'false', k + 1, title, thumb, w, h, k + 1))

ARROW = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5 8 12l7 7"/></svg>',
         '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>')

NEW_MARKUP = """    <div class="projx" role="group" aria-roledescription="carousel" aria-label="Recent work">
      <div class="stage">
%s
        <p class="pcap" aria-live="polite"><span><b>Residential upper glass</b><span>Arched second storey windows, worked from the ground.</span></span><span class="pcount">01 / 07</span></p>
        <button class="pnav prev" type="button" aria-label="Previous frame">%s</button>
        <button class="pnav next" type="button" aria-label="Next frame">%s</button>
      </div>
      <div class="sheet">
%s
      </div>
    </div>""" % ('\n'.join(frames), ARROW[0], ARROW[1], '\n'.join(cells))

start = s.index('    <div class="gal">')
end = s.index('    <div class="hero-act" style="margin-top:40px">', start)
s = s[:start] + NEW_MARKUP + '\n' + s[end:]
done.append('projector markup')

# ---------------------------------------------------------------- script -----
# the old gallery reveal and the clip observer both pointed at .gal
rep("""  gsap.utils.toArray('.gal').forEach(function(g){
    gsap.fromTo(g.querySelectorAll('.shot'), {y:56, opacity:0}, {
      y:0, opacity:1, duration:1, ease:EASE, stagger:.07,
      scrollTrigger:{trigger:g, start:'top 84%'}
    });
  });""",
"""  gsap.utils.toArray('.projx').forEach(function(g){
    gsap.fromTo(g.querySelector('.stage'), {y:52, opacity:0},
      {y:0, opacity:1, duration:1, ease:EASE, scrollTrigger:{trigger:g, start:'top 84%'}});
    gsap.fromTo(g.querySelectorAll('.cell'), {y:26, opacity:0},
      {y:0, opacity:1, duration:.8, ease:EASE, stagger:.05,
       scrollTrigger:{trigger:g, start:'top 78%'}});
  });""", 'motion targets')

rep("""    var vids=[].slice.call(document.querySelectorAll('.gal video'));""",
    """    var vids=[].slice.call(document.querySelectorAll('.projx video'));""", 'clip selector')

rep("""    vids.forEach(function(v){ v.preload='metadata'; vo.observe(v); });
  })();""",
"""    vids.forEach(function(v){ v.preload='metadata'; vo.observe(v); });
  })();

  /* ---------- the projector ----------
     One frame is shown at a time and the others are stacked behind it at
     opacity 0, so changing frame is a crossfade rather than a move. Only the
     frame on screen is allowed to decode: a paused clip three frames back is
     work nobody is watching. Driven by clicks, the two gate arms, the arrow
     keys and a horizontal swipe, because a gallery that only answers a hover
     is not a control. */
  (function(){
    var box = document.querySelector('.projx');
    if(!box) return;
    var frames = [].slice.call(box.querySelectorAll('.frame'));
    var cells  = [].slice.call(box.querySelectorAll('.cell'));
    var cap    = box.querySelector('.pcap');
    var capT   = cap.querySelector('b');
    var capD   = cap.querySelector('b + span');
    var count  = box.querySelector('.pcount');
    var cur = 0;
    var META = frames.map(function(f){
      var l = f.getAttribute('aria-label').split(', ');
      return l.slice(1).join(', ');
    });
    var DESC = [__DESCS__];

    function show(n){
      n = (n + frames.length) % frames.length;
      if(n === cur) return;
      cur = n;
      frames.forEach(function(f,i){
        if(i === n) f.setAttribute('data-on',''); else f.removeAttribute('data-on');
        var v = f.querySelector('video');
        if(v){ if(i === n){ v.preload='metadata'; v.play().catch(function(){}); } else if(!v.paused) v.pause(); }
      });
      cells.forEach(function(c,i){ c.setAttribute('aria-current', String(i === n)); });
      capT.textContent = META[n];
      capD.textContent = DESC[n];
      count.textContent = String(n+1).padStart(2,'0') + ' / 07';
      var active = cells[n];
      if(active && active.scrollIntoView) active.scrollIntoView({block:'nearest', inline:'center', behavior:'smooth'});
    }

    cells.forEach(function(c){ c.addEventListener('click', function(){ show(+c.dataset.i); }); });
    box.querySelector('.pnav.prev').addEventListener('click', function(){ show(cur-1); });
    box.querySelector('.pnav.next').addEventListener('click', function(){ show(cur+1); });
    box.addEventListener('keydown', function(e){
      if(e.key === 'ArrowLeft'){ e.preventDefault(); show(cur-1); }
      if(e.key === 'ArrowRight'){ e.preventDefault(); show(cur+1); }
    });
    var sx = null;
    var stage = box.querySelector('.stage');
    stage.addEventListener('touchstart', function(e){ sx = e.touches[0].clientX; }, {passive:true});
    stage.addEventListener('touchend', function(e){
      if(sx === null) return;
      var dx = e.changedTouches[0].clientX - sx; sx = null;
      if(Math.abs(dx) > 42) show(cur + (dx < 0 ? 1 : -1));
    }, {passive:true});
  })();""".replace('__DESCS__', ', '.join(repr(sh[7]) for sh in SHOTS)), 'projector script')

open(p, 'w', encoding='utf-8').write(s)
print('02 projector:', len(done), 'edits ->', ', '.join(done))
