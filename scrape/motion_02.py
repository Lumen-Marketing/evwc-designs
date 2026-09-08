# -*- coding: utf-8 -*-
# 02 Site is film stock, so its motion is a CAMERA, not a set of fades.
# The plate is pushed and drifted against the type, the title lands like a title
# card, the frames open on a shutter, and a scrub bar tracks position along the
# reel. GSAP owns `transform`; the hover polish moves to the independent `scale`
# property so the two compose instead of overwriting each other.
p = '02-site.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------------ CSS -----
rep(""".hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:48% 52%;z-index:0}""",
""".hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:48% 52%;z-index:0}
/* headroom for the camera push. The plate drifts inside this margin, so the
   frame edge is never exposed at either end of the travel. */
.hero>img{top:-9%;height:118%}""", 'hero img headroom')

# GSAP writes `transform`. The hover polish moves to `scale`, which is its own
# property and multiplies with the transform rather than replacing it.
rep(""".chapshot img{width:100%;height:clamp(300px,34vw,460px);object-fit:cover;display:block;
  transition:transform 1s cubic-bezier(.16,1,.3,1)}""",
""".chapshot img{width:100%;height:clamp(300px,34vw,460px);object-fit:cover;display:block;
  transition:scale 1s cubic-bezier(.16,1,.3,1)}""", 'chapshot img transition')

rep(""".shot img{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.16,1,.3,1)}
.shot:hover img{transform:scale(1.05)}""",
""".shot img{width:100%;height:100%;object-fit:cover;transition:scale .9s cubic-bezier(.16,1,.3,1)}
.shot:hover img{scale:1.05}""", 'shot img hover')

rep(""".shot video{width:100%;height:100%;object-fit:cover;transition:transform .9s cubic-bezier(.16,1,.3,1)}
.shot:hover video{transform:scale(1.05)}""",
""".shot video{width:100%;height:100%;object-fit:cover;transition:scale .9s cubic-bezier(.16,1,.3,1)}
.shot:hover video{scale:1.05}""", 'shot video hover')

rep(""".hang .wshot:hover img{transform:scale(1.045)}""",
    """.hang .wshot:hover img{scale:1.045}""", 'wshot hover')

rep(""".rv{opacity:0;transform:translateY(26px);filter:blur(7px);""",
"""/* ---------- MOTION: the camera ----------
   Two lines of the headline ride up out of a mask, like a title card. The mask
   carries a little padding under it because the display face runs at .84 line
   height and a bare overflow:hidden would shear the descender off "views". */
.ln{display:block;overflow:hidden;padding-bottom:.14em;margin-bottom:-.14em}
.ln>i{display:block;font-style:inherit}
/* a scrub bar along the top of the reel. It reports position and nothing else,
   which is the only reason it is on the page. */
.scrub{position:fixed;left:0;top:0;height:2px;width:100%;z-index:70;pointer-events:none;
  background:linear-gradient(90deg,var(--blue),var(--blue-2));
  transform:scaleX(0);transform-origin:0 50%;will-change:transform}
.rv{opacity:0;transform:translateY(26px);filter:blur(7px);""", 'motion css')

# ---------------------------------------------------------------- markup -----
rep("""    <h1>Crystal clear views<em>start here.</em></h1>""",
    """    <h1><span class="ln"><i>Crystal clear views</i></span><em class="ln"><i>start here.</i></em></h1>""",
    'headline masks')

# the gallery is taken over by GSAP, so it drops the CSS reveal it shared with
# the text blocks. One element, one owner.
for L in 'abcdefg':
    rep('<figure class="shot %s rv" style="margin:0">' % L,
        '<figure class="shot %s" style="margin:0">' % L, 'shot %s' % L)

rep("""<script>
(function(){
  "use strict";
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;""",
"""<span class="scrub" aria-hidden="true"></span>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script>
(function(){
  "use strict";
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;""", 'gsap tags')

# ---------------------------------------------------------------- script -----
rep("""  document.querySelectorAll('[data-count]').forEach(function(n){ sio.observe(n); });""",
"""  document.querySelectorAll('[data-count]').forEach(function(n){ sio.observe(n); });

  /* ---------- MOTION: the camera ----------
     Every move below is scroll-LINKED rather than a one-shot fade, which is the
     difference the page was missing. Four moves, no pinning and no scroll
     hijack: a push on the hero plate, a title card, a shutter on each chapter
     frame, and the gallery riding up as the grid crosses.

     Entry states are set by GSAP at runtime, never in the stylesheet, so if the
     CDN never answers the page renders complete instead of blank. Reduced
     motion skips the whole block and the CSS reveals carry it. */
  if(reduce || !window.gsap || !window.ScrollTrigger) return;
  gsap.registerPlugin(ScrollTrigger);
  var EASE = 'expo.out';

  /* 1. the camera push. The plate drifts and closes in across the hero's own
        scroll, inside the 9% headroom the stylesheet gives it. */
  gsap.fromTo('.hero>img', {yPercent:-3.2, scale:1.02}, {
    yPercent:3.2, scale:1.09, ease:'none',
    scrollTrigger:{trigger:'.hero', start:'top top', end:'bottom top', scrub:.6}
  });

  /* 2. the title card. On load, not on scroll: it is the first thing read. */
  var tl = gsap.timeline({defaults:{ease:EASE}});
  tl.from('.hero h1 .ln > i', {yPercent:112, duration:1.15, stagger:.09})
    .from('.hero .lede', {y:22, opacity:0, duration:.9}, '-=.72')
    .from('.hero-act > *', {y:18, opacity:0, duration:.8, stagger:.08}, '-=.66')
    .from('.hcard', {y:26, opacity:0, duration:.9}, '-=.7');

  /* 3. the shutter. Each chapter frame opens from its foot as it crosses, and
        the picture inside settles at the same time. clip-path so the frame's
        own hover scale is left alone. */
  gsap.utils.toArray('.chapshot').forEach(function(f){
    gsap.fromTo(f,
      {clipPath:'inset(0% 0% 34% 0%)'},
      {clipPath:'inset(0% 0% 0% 0%)', ease:'none',
       scrollTrigger:{trigger:f, start:'top 88%', end:'top 46%', scrub:.5}});
  });

  /* 4. the gallery rides up as the grid crosses, each frame a beat behind the
        one before it, so the block arrives as a sequence rather than a slab. */
  gsap.utils.toArray('.gal').forEach(function(g){
    gsap.from(g.querySelectorAll('.shot'), {
      y:56, opacity:0, duration:1, ease:EASE, stagger:.07,
      scrollTrigger:{trigger:g, start:'top 84%'}
    });
  });

  /* 5. position along the reel. Transform only, so it costs one composite. */
  var bar = document.querySelector('.scrub');
  if(bar) gsap.to(bar, {scaleX:1, ease:'none',
    scrollTrigger:{trigger:document.documentElement, start:'top top', end:'bottom bottom', scrub:.25}});

  /* webfonts land after first paint and every start/end above is a percentage
     of a measured height, so the triggers have to be recomputed once. */
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ ScrollTrigger.refresh(); });
  addEventListener('load', function(){ ScrollTrigger.refresh(); });""", 'motion script')

open(p, 'w', encoding='utf-8').write(s)
print('02 motion:', len(done), 'edits ->', ', '.join(done))
