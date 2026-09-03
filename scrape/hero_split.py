# -*- coding: utf-8 -*-
# The hero was a frosted card sitting on muddy footage: generic glassmorphism, a
# rotated edge label, and a tilted photo plate falling off the bottom of the
# frame. All three are stock AI-design tells and the photograph, which is the
# whole product here, was unreadable. Rebuilt as two planes with no container.
import re
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------------ CSS -----
start = s.index('/* ---------- hero: three physical planes, back / mid / front ---------- */')
end = s.index('.acts{display:flex;')
NEW = """/* ---------- hero: two planes, the type crossing in front of the footage ----------
   No panel, no blur, no container. The left plane is the page's own black and
   the right plane is the footage, bleeding off the top, right and bottom of the
   frame. The headline is laid across both columns, so its long line passes in
   front of the footage's edge, and the black plane throws a shadow onto it. The
   crossing and the shadow are the depth. A card would only have hidden the
   photograph, which is the thing being sold. */
.hero{position:relative;isolation:isolate;min-height:min(92dvh,940px);
  display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.78fr);align-items:center}
.hero-media{grid-area:1/2/2/3;position:relative;align-self:stretch;overflow:hidden;
  background:var(--bg-2)}
.hero-media video{width:100%;height:100%;object-fit:cover;object-position:50% 40%;
  transform:scale(1.04);will-change:transform}
/* the seam. The black feathers a long way across the footage so the type keeps a
   field to sit on and the two planes interlock instead of butting together */
.hero-media::before{content:"";position:absolute;inset:0;z-index:2;pointer-events:none;
  background:
    linear-gradient(90deg,#0c0d0e 0%,rgba(12,13,14,.94) 12%,rgba(12,13,14,.5) 42%,rgba(12,13,14,0) 76%),
    linear-gradient(180deg,rgba(12,13,14,.72),transparent 24%,transparent 58%,rgba(12,13,14,.82))}
/* occlusion: the plane in front casts onto the one behind */
.hero-media::after{content:"";position:absolute;inset:0;z-index:2;pointer-events:none;
  box-shadow:inset 52px 0 78px -34px rgba(0,0,0,.96),inset 0 0 0 1px rgba(255,255,255,.05)}
.hero .in{grid-area:1/1/2/3;position:relative;z-index:3;width:100%;
  padding-block:clamp(104px,13vw,164px) clamp(44px,6.5vw,96px)}
h1{font-size:clamp(40px,7.2vw,112px);max-width:none;text-shadow:0 2px 44px rgba(0,0,0,.75)}
h1 .l1,h1 .l2{display:block}
h1 .l2{white-space:nowrap}
/* everything under the headline stays inside the black column */
.hero-lede{max-width:min(46ch,50%)}
.hero-lede p{margin:26px 0 0;font-size:clamp(16px,1.35vw,19px);color:#d9dddf}
/* the rating sits with the copy rather than waiting for a section of its own */
.hrate{display:flex;align-items:center;gap:11px;margin:20px 0 0;font-size:14px;color:#d9dddf}
.hrate .stars{display:inline-flex;gap:2px;color:var(--acc)}
.hrate .stars svg{width:15px;height:15px}
.hrate b{font-weight:600;color:var(--fg)}
@supports (animation-timeline:scroll()){
  @media (prefers-reduced-motion:no-preference){
    .hero-media video{animation:drift linear both;animation-timeline:scroll();animation-range:0 92vh}
    @keyframes drift{to{transform:scale(1.04) translateY(5%)}}
  }
}
"""
s = s[:start] + NEW + s[end:]
done.append('hero css')

# --------------------------------------------------------------- markup -----
start = s.index('<section class="hero">')
end = s.index('</section>', start) + len('</section>')
s = s[:start] + """<section class="hero">
  <div class="hero-media">
    <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video>
  </div>
  <div class="in wrap">
    <h1><span class="l1">Crystal clear</span> <span class="l2">views start here.</span></h1>
    <div class="hero-lede">
      <p>Windows, screens, tracks, hard water, tint, solar panels and hauling across the East Valley.</p>
      <p class="hrate"><span class="stars" role="img" aria-label="Rated 5 out of 5"><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg></span><b>5.0</b> from all 4 Google reviews</p>
      <div class="acts">
        <a class="btn" href="tel:+14808069455">Call 480-806-9455</a>
        <a class="tlink" href="sms:+14808069455">Or text a photo of your windows</a>
      </div>
    </div>
  </div>
</section>""" + s[end:]
done.append('hero markup')

# the wide crop of the same job now goes where a wide frame belongs
rep('<div class="frame"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>',
    '<div class="frame"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Two cleaners washing a commercial storefront with water-fed poles"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video></div>',
    'gallery takes the wide crop')

# ---------------------------------------------------------- responsive ------
rep("""  .hero-copy{max-width:100%}
  .glass{width:calc(100% + var(--gp) * 2);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
  h1{max-width:14ch}
  h1 .l1,h1 .l2{display:inline;white-space:normal}
  .vlabel{display:none}""",
"""  .hero{display:flex;align-items:flex-end;min-height:min(88dvh,800px)}
  .hero-media{position:absolute;inset:0;z-index:0}
  .hero-media::before{background:
    linear-gradient(90deg,rgba(12,13,14,.9),rgba(12,13,14,.62) 55%,rgba(12,13,14,.34)),
    linear-gradient(180deg,rgba(12,13,14,.78),rgba(12,13,14,.3) 30%,rgba(12,13,14,.88))}
  .hero-media::after{box-shadow:none}
  .hero .in{padding-block:clamp(110px,22vw,150px) clamp(38px,7vw,70px)}
  .hero-lede{max-width:100%}
  h1{max-width:14ch}
  h1 .l1,h1 .l2{display:inline;white-space:normal}""", 'hero mq')

for dead in ['.plate{margin:0;position:absolute', '.hero-bg{position:absolute']:
    if dead in s:
        print('!! leftover:', dead)

open(p, 'w', encoding='utf-8').write(s)
print('hero split:', len(done), 'edits ->', ', '.join(done))
