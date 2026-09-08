# -*- coding: utf-8 -*-
# 03's recent work was seven bolted plates on a twelve column grid. Same problem
# as 02: everything at once, nothing at size. This direction is milled metal, so
# the component is an INDEXING RAIL. Plates sit on a track and you travel along
# it one station at a time, with a machined control block and a station readout.
#
# Deliberately not the same component as 02's projector. 02 replaces the picture
# in place; this one moves along a line. And it is not 01's drag filmstrip: this
# indexes to fixed stations and reports which one you are at, the way a machine
# does, rather than being flung.
#
# Built on native scroll-snap rather than a JS-translated track, so touch drag,
# trackpad, momentum and keyboard all come from the browser and there is no
# drag handler to fight the page's own scrolling.
p = '03-plate.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------------ CSS -----
i = s.index('.proj{display:grid;grid-template-columns:repeat(12,1fr);')
j = s.index('\n', s.index('.proj .r6 .plate>div,.proj .r7 .plate>div{'))
NEW_CSS = """/* ---------- RECENT WORK: the indexing rail ----------
   Stations on a track. You travel along it rather than reading a grid, the
   plate at the station is at full size, and a machined block reports where you
   are. Native scroll-snap does the travelling: touch drag, trackpad, momentum
   and keyboard all come free, and there is no drag handler to fight the page's
   own scroll. */
.rail{display:flex;gap:clamp(14px,2vw,24px);margin-top:44px;
  overflow-x:auto;overscroll-behavior-x:contain;
  scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;
  scroll-padding-inline:0;scrollbar-width:none;
  /* the track runs off both edges of the column, so the rail reads as longer
     than the page rather than as a box with things in it */
  margin-inline:calc(var(--pad) * -1);padding-inline:var(--pad)}
.rail::-webkit-scrollbar{display:none}
.station{flex:0 0 clamp(268px,46vw,620px);margin:0;scroll-snap-align:start;
  opacity:.5;transition:opacity .45s cubic-bezier(.2,.9,.2,1)}
.station[data-at]{opacity:1}
.station .plate>div{height:clamp(230px,30vw,400px)}
.station .plate>div img,.station .plate>div video{width:100%;height:100%;object-fit:cover;display:block}
/* the control block: back and forward bolted either side of the readout */
.railctl{display:flex;align-items:stretch;gap:0;margin-top:clamp(18px,2.2vw,28px);
  width:max-content;background:var(--steel-2);box-shadow:var(--bevel)}
.rnav{width:56px;min-height:56px;display:grid;place-items:center;cursor:pointer;
  border:0;background:transparent;color:#fff;
  transition:background .25s,color .25s,transform .18s}
.rnav:hover{background:rgba(255,255,255,.07)}
.rnav:active{transform:scale(.94)}
.rnav[disabled]{opacity:.32;cursor:default;transform:none}
.rnav svg{width:19px;height:19px;fill:none;stroke:currentColor;stroke-width:2;
  stroke-linecap:round;stroke-linejoin:round}
.readout{display:grid;place-items:center;padding:0 clamp(16px,2vw,26px);
  font-family:'Saira Condensed',sans-serif;font-weight:700;font-size:17px;
  letter-spacing:.2em;color:#fff;font-variant-numeric:tabular-nums;white-space:nowrap;
  border-inline:1px solid rgba(0,0,0,.55);
  box-shadow:inset 1px 0 0 rgba(255,255,255,.07),inset -1px 0 0 rgba(255,255,255,.07)}
/* the station strip. Seven marks, the one you are at lit. */
.ticks{display:flex;gap:5px;align-items:center;margin-top:14px}
.ticks i{display:block;width:26px;height:3px;background:rgba(255,255,255,.17);
  transition:background .35s cubic-bezier(.2,.9,.2,1)}
.ticks i[data-at]{background:var(--bright)}
@media (max-width:760px){
  .station{flex:0 0 min(84vw,420px)}
  .ticks i{width:18px}
}
"""
s = s[:i] + NEW_CSS + s[j+1:]
done.append('rail css')

# ---------------------------------------------------------------- markup -----
start = s.index('    <div class="proj">')
end = s.index('  </div>\n</section>', start)
STATIONS = [
    ('video', 'assets/reel-storefront-wide.mp4', 'assets/poster-storefront-wide.jpg', 1280, 722,
     'Storefront glazing being cleaned', 'Commercial storefront', 'Mesa. Exterior glass, frames and screens.'),
    ('video', 'assets/reel-solar.mp4', 'assets/poster-solar.jpg', 540, 960,
     'A solar array being rinsed', 'Solar array rinse', 'Dust and hard water film lifted off.'),
    ('img', 'assets/restaurant.jpg', None, 1400, 1750,
     'Restaurant frontage glazing after cleaning', 'Restaurant frontage', 'Street-facing glass, cleaned before service.'),
    ('img', 'assets/hero-pole.jpg', None, 1200, 1600,
     'A water-fed pole reaching upper storey glass', 'Two storey residential', 'Water-fed pole, no ladder on the landscaping.'),
    ('img', 'assets/storefront.jpg', None, 1200, 1200,
     'Retail entry glazing, doors and sidelights', 'Retail entry', 'Doors, sidelights and the frames around them.'),
    ('img', 'assets/junk-yard.jpg', None, 820, 1094,
     'A yard cleared of monsoon debris', 'Junk removal', 'Monsoon debris loaded up and taken away.'),
    ('img', 'assets/rig.jpg', None, 1200, 1200,
     'The work van and equipment', 'The rig', 'Everything on one van, on the route daily.'),
]
rows = []
for k, (kind, src, poster, w, h, alt, title, desc) in enumerate(STATIONS):
    at = ' data-at' if k == 0 else ''
    if kind == 'img':
        media = ('<img src="%s" width="%d" height="%d" loading="lazy" alt="%s">' % (src, w, h, alt))
    else:
        media = ('<video src="%s" poster="%s" muted loop playsinline preload="none" '
                 'width="%d" height="%d" aria-label="%s"></video>' % (src, poster, w, h, alt))
    rows.append(
"""      <figure class="station"%s data-i="%d" aria-roledescription="slide" aria-label="%d of 7, %s">
        <div class="plate bolts"><span class="b2"></span><span class="b3"></span>
          <div>%s</div>
          <figcaption><b>%s</b>%s</figcaption>
        </div>
      </figure>""" % (at, k, k + 1, title, media, title, desc))

NEW_MARKUP = """    <div class="rail" role="group" aria-roledescription="carousel" aria-label="Recent work" tabindex="0">
%s
    </div>
    <div class="railctl">
      <button class="rnav" type="button" data-d="-1" aria-label="Previous station" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5 8 12l7 7"/></svg></button>
      <span class="readout" aria-live="polite">01 / 07</span>
      <button class="rnav" type="button" data-d="1" aria-label="Next station"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
    </div>
    <div class="ticks" aria-hidden="true"><i data-at></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
""" % '\n'.join(rows)
s = s[:start] + NEW_MARKUP + s[end:]
done.append('rail markup')

# ---------------------------------------------------------------- script -----
rep("""  gsap.utils.toArray('.ba, .proj, .revs, .svcs').forEach(function(row){""",
    """  gsap.utils.toArray('.ba, .revs, .svcs').forEach(function(row){""", 'motion targets')

rep("""  /* 1. THE DEVICE. A light bar travels across every milled face as that face
        crosses the viewport. One custom property per element, composited. */""",
"""  /* the rail travels sideways under its own control, so its plates seat on
     arrival rather than on a scroll trigger that would fight the track */
  gsap.fromTo('.rail .station', {y:34, opacity:0}, {y:0, opacity:1, duration:.8,
    ease:HARD, stagger:.05, clearProps:'opacity',
    scrollTrigger:{trigger:'.rail', start:'top 86%'}});

  /* 1. THE DEVICE. A light bar travels across every milled face as that face
        crosses the viewport. One custom property per element, composited. */""", 'rail seating')

rep("""    var vids=[].slice.call(document.querySelectorAll('.proj video'));
    if(!vids.length) return;
    if(reduce){ vids.forEach(function(v){ v.removeAttribute('loop'); v.load(); }); return; }
    if(!('IntersectionObserver' in window)){ vids.forEach(function(v){ v.play().catch(function(){}); }); return; }
    var vo=new IntersectionObserver(function(es){
      es.forEach(function(e){
        var v=e.target;
        if(e.isIntersecting) v.play().catch(function(){}); else if(!v.paused) v.pause();
      });
    },{threshold:.3});
    vids.forEach(function(v){ v.preload='metadata'; vo.observe(v); });
  })();""",
"""    var rail=document.querySelector('.rail');
    if(!rail) return;
    var vids=[].slice.call(rail.querySelectorAll('video'));
    if(!vids.length) return;
    if(reduce){ vids.forEach(function(v){ v.removeAttribute('loop'); v.load(); }); return; }
    if(!('IntersectionObserver' in window)){ return; }
    // a clip decodes only when it is BOTH the station you are at and on screen
    new IntersectionObserver(function(es){
      rail.dataset.live = es[0].isIntersecting ? '1' : '';
      vids.forEach(function(v){
        var at = v.closest('.station').hasAttribute('data-at');
        if(rail.dataset.live && at){ v.preload='metadata'; v.play().catch(function(){}); }
        else if(!v.paused) v.pause();
      });
    },{threshold:.25}).observe(rail);
  })();

  /* ---------- the indexing rail ----------
     Scroll position is the source of truth, so a drag, a flick, a trackpad and
     the two buttons all end up in the same place with no state to keep in sync.
     The readout, the ticks, the dimming and which clip is allowed to run are
     all read back off scrollLeft. */
  (function(){
    var rail=document.querySelector('.rail');
    if(!rail) return;
    var stations=[].slice.call(rail.querySelectorAll('.station'));
    var out=document.querySelector('.readout');
    var ticks=[].slice.call(document.querySelectorAll('.ticks i'));
    var navs=[].slice.call(document.querySelectorAll('.rnav'));
    var vids=[].slice.call(rail.querySelectorAll('video'));
    var cur=-1, raf=0;

    function step(){
      // measured, not assumed: the station width is a clamp and the gap is a
      // clamp, so the travel per press has to come off the live layout
      if(stations.length<2) return rail.clientWidth;
      return stations[1].offsetLeft - stations[0].offsetLeft;
    }
    function nearest(){
      var x=rail.scrollLeft, best=0, d=Infinity;
      stations.forEach(function(st,i){
        var dd=Math.abs(st.offsetLeft - rail.offsetLeft - x);
        if(dd<d){ d=dd; best=i; }
      });
      // at the far end the last station can never reach the left edge, so the
      // readout would stick one short of seven. Snap it when the track bottoms out.
      if(rail.scrollLeft >= rail.scrollWidth - rail.clientWidth - 2) best = stations.length-1;
      return best;
    }
    function paint(){
      var n=nearest();
      if(n===cur) return;
      cur=n;
      stations.forEach(function(st,i){ if(i===n) st.setAttribute('data-at',''); else st.removeAttribute('data-at'); });
      ticks.forEach(function(t,i){ if(i===n) t.setAttribute('data-at',''); else t.removeAttribute('data-at'); });
      out.textContent=String(n+1).padStart(2,'0')+' / 07';
      navs[0].disabled = n===0;
      navs[1].disabled = n===stations.length-1;
      vids.forEach(function(v){
        var at=v.closest('.station').hasAttribute('data-at');
        if(at && rail.dataset.live){ v.preload='metadata'; v.play().catch(function(){}); }
        else if(!v.paused) v.pause();
      });
    }
    rail.addEventListener('scroll', function(){
      if(raf) return;
      raf=requestAnimationFrame(function(){ raf=0; paint(); });
    }, {passive:true});
    navs.forEach(function(b){
      b.addEventListener('click', function(){
        rail.scrollBy({left: step() * (+b.dataset.d), behavior:'smooth'});
      });
    });
    rail.addEventListener('keydown', function(e){
      if(e.key==='ArrowLeft'){ e.preventDefault(); rail.scrollBy({left:-step(), behavior:'smooth'}); }
      if(e.key==='ArrowRight'){ e.preventDefault(); rail.scrollBy({left: step(), behavior:'smooth'}); }
    });
    addEventListener('resize', function(){ cur=-1; paint(); });
    paint();
  })();""", 'rail script')

open(p, 'w', encoding='utf-8').write(s)
print('03 rail:', len(done), 'edits ->', ', '.join(done))
