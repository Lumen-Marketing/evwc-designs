# -*- coding: utf-8 -*-
# 03 Plate is milled metal, so its motion is a MACHINE, not a camera. Light
# travels across the faces on rails, plates seat with a hard stop rather than a
# soft blur, and the sheared teal field is fed in from its leading edge. Nothing
# drifts, because nothing on a machine drifts.
p = '03-plate.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------------ CSS -----
rep(""".hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 50%;z-index:0;opacity:.66}""",
""".hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:60% 50%;z-index:0;opacity:.66}
/* headroom for the traverse, so the frame edge never shows at either end */
.hero>img{top:-8%;height:116%}""", 'hero headroom')

# GSAP writes `transform` for the traverse, so the hover polish takes the
# independent `scale` property and the two multiply instead of overwriting.
rep(""".plate img{width:100%;height:100%;object-fit:cover;transition:transform .85s cubic-bezier(.16,1,.3,1)}
.plate:hover img{transform:scale(1.045)}""",
""".plate img{width:100%;height:100%;object-fit:cover;transition:scale .85s cubic-bezier(.16,1,.3,1)}
.plate:hover img{scale:1.045}""", 'plate hover')

rep(""".rv{opacity:0;transform:translateY(24px);filter:blur(6px);""",
"""/* ---------- MOTION: the machine ----------
   The one device this direction owns. Every milled face already carries a fixed
   specular sweep; here the light bar actually TRAVELS across it as the face
   crosses the viewport, which is what a brushed surface does under a moving
   light. Driven by --sx off ScrollTrigger, composited as a transform, and
   clipped by the plate's own overflow. */
.plate,.milled{--sx:0}
.plate::after,.milled::before{
  content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(100deg,
    transparent 30%, rgba(255,255,255,.02) 42%, rgba(255,255,255,.085) 50%,
    rgba(255,255,255,.02) 58%, transparent 70%);
  transform:translate3d(calc(var(--sx) * 210% - 105%),0,0);
  will-change:transform}
.milled{position:relative;overflow:hidden}
/* the caption is a machined face in its own right, so the bar passes behind it */
.plate figcaption{z-index:2}
/* the carriage: each headline line travels in and hard stops */
.ln{display:block;overflow:hidden;padding-bottom:.12em;margin-bottom:-.12em}
.ln>i{display:block;font-style:inherit}
.rv{opacity:0;transform:translateY(24px);filter:blur(6px);""", 'specular css')

# ---------------------------------------------------------------- markup -----
rep("""    <h1>Crystal clear views.<em>Start here.</em></h1>""",
    """    <h1><span class="ln"><i>Crystal clear views.</i></span><em class="ln"><i>Start here.</i></em></h1>""",
    'headline carriage')

rep("""<script>
(function(){
  "use strict";
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;""",
"""<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
(function(){
  "use strict";
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;""", 'gsap tags')

# ---------------------------------------------------------------- script -----
rep("""  document.querySelectorAll('[data-count]').forEach(function(n){ sio.observe(n); });""",
"""  document.querySelectorAll('[data-count]').forEach(function(n){ sio.observe(n); });

  /* ---------- MOTION: the machine ----------
     Its own scope on purpose: a bare return here would also skip the clip
     autoplay below it, so reduced motion or a CDN that never answers would
     silently leave both reels paused.

     Four moves, all scroll-LINKED rather than one-shot, none of them pinning
     the page or taking the scroll off the visitor. Entry states are set by GSAP
     at runtime and never in the stylesheet, so with no GSAP the page renders
     complete instead of blank. */
  (function(){
  if(reduce || !window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  var HARD = 'power4.out';   /* a machine stops. It does not ease out forever. */

  /* 1. THE DEVICE. A light bar travels across every milled face as that face
        crosses the viewport. One custom property per element, composited. */
  gsap.utils.toArray('.plate,.milled').forEach(function(el){
    gsap.fromTo(el, {'--sx':0}, {'--sx':1, ease:'none',
      scrollTrigger:{trigger:el, start:'top bottom', end:'bottom top', scrub:.4}});
  });

  /* 2. the traverse. The hero plate tracks slowly against the type across its
        own scroll, inside the 8% headroom the stylesheet gives it. */
  gsap.fromTo('.hero>img', {yPercent:-2.8}, {yPercent:2.8, ease:'none',
    scrollTrigger:{trigger:'.hero', start:'top top', end:'bottom top', scrub:.6}});

  /* 3. the carriage. Both headline lines run in from the left and hard stop,
        then the rest of the block seats behind them. On load: it is the first
        thing read, so it does not wait for a scroll. */
  gsap.timeline({defaults:{ease:HARD}})
    .from('.hero h1 .ln > i', {xPercent:-14, opacity:0, duration:.95, stagger:.08})
    .from('.hero .lede', {y:16, opacity:0, duration:.7}, '-=.6')
    .from('.hero-act > *', {y:14, opacity:0, duration:.6, stagger:.07}, '-=.5')
    .from('.spec', {y:20, opacity:0, duration:.75}, '-=.5');

  /* 4. plates seat. Short travel, hard stop, one beat apart down the run. No
        blur anywhere in this direction: a blurred edge is a lens, and there is
        no lens in a machine shop. */
  gsap.utils.toArray('.ba, .proj, .revs, .svcs').forEach(function(row){
    var kids = row.querySelectorAll(':scope > *');
    if(!kids.length) return;
    gsap.from(kids, {y:40, opacity:0, duration:.85, ease:HARD, stagger:.06,
      scrollTrigger:{trigger:row, start:'top 86%'}});
  });

  /* 5. the sheared field is fed in from its leading edge as it arrives. It
        keeps its own shear, so the clip is written against that polygon. */
  var field = document.querySelector('.field');
  if(field) gsap.fromTo(field,
    {clipPath:'polygon(0 var(--shear),42% 0,42% calc(100% - var(--shear)),0 100%)'},
    {clipPath:'polygon(0 var(--shear),100% 0,100% calc(100% - var(--shear)),0 100%)',
     ease:'none',
     scrollTrigger:{trigger:field, start:'top 92%', end:'top 40%', scrub:.5}});

  /* webfonts land after first paint and every start/end above is a percentage
     of a measured height, so the triggers have to be recomputed once. */
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ ScrollTrigger.refresh(); });
  addEventListener('load', function(){ ScrollTrigger.refresh(); });
  })();""", 'motion script')

open(p, 'w', encoding='utf-8').write(s)
print('03 motion:', len(done), 'edits ->', ', '.join(done))
