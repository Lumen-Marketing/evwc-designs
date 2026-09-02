import io, sys
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
edits = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); edits.append(label)

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180'%3E"
         "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.82' numOctaves='4' "
         "stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' "
         "opacity='.5'/%3E%3C/svg%3E\")")

# 1 -- depth tokens, richer easing, fixed grain layer
rep("""  --ez:cubic-bezier(.16,1,.3,1);
}""",
"""  --ez:cubic-bezier(.32,.72,0,1);
  --ez-out:cubic-bezier(.16,1,.3,1);
  /* diffused ambient shadows tinted to the page, never harsh */
  --lift-1:0 2px 4px -2px rgba(0,0,0,.6), 0 12px 28px -12px rgba(0,0,0,.75);
  --lift-2:0 8px 18px -8px rgba(0,0,0,.7), 0 40px 80px -28px rgba(0,0,0,.9);
  --lift-3:0 12px 26px -10px rgba(0,0,0,.75), 0 60px 120px -34px rgba(0,0,0,.95);
  --rim:inset 0 1px 0 rgba(255,255,255,.14);
}
/* grain: fixed, pointer-events none, never on a scrolling container */
body::after{content:"";position:fixed;inset:0;z-index:60;pointer-events:none;opacity:.05;
  background-image:""" + NOISE + "}", 'tokens+grain')

# 2 -- hero becomes three physical planes
rep("""/* ---------- hero: full-bleed media, type on top, no chrome ---------- */
.hero{position:relative;min-height:min(88dvh,860px);display:flex;align-items:flex-end;overflow:hidden;padding-top:68px}
.hero video,.hero .fallback{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}
.hero::after{content:"";position:absolute;inset:0;z-index:1;
  background:linear-gradient(78deg,rgba(12,13,14,.92) 0%,rgba(12,13,14,.62) 32%,rgba(12,13,14,.06) 64%,rgba(12,13,14,.42) 100%),
             linear-gradient(180deg,rgba(12,13,14,.42) 0%,transparent 18%,transparent 46%,rgba(12,13,14,.82) 100%)}
.hero .in{position:relative;z-index:2;width:100%;padding-block:clamp(40px,7vw,88px)}
h1{font-size:clamp(40px,7.1vw,104px);max-width:15ch}
.hero p{margin:22px 0 0;max-width:44ch;font-size:clamp(16px,1.35vw,19px);color:#d6dadb}""",
"""/* ---------- hero: three physical planes, back / mid / front ---------- */
.hero{position:relative;min-height:min(94dvh,950px);display:flex;align-items:flex-end;padding-top:68px;isolation:isolate}
.hero-bg{position:absolute;inset:0;overflow:hidden;z-index:0}
.hero-bg video{width:100%;height:100%;object-fit:cover;transform:scale(1.08);will-change:transform}
/* back plane depth: vignette plus falloff */
.hero::before{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:radial-gradient(128% 84% at 62% 30%,transparent 30%,rgba(12,13,14,.55) 76%,rgba(12,13,14,.9) 100%)}
.hero::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(78deg,rgba(12,13,14,.95) 0%,rgba(12,13,14,.66) 34%,rgba(12,13,14,.02) 66%,rgba(12,13,14,.3) 100%),
             linear-gradient(180deg,rgba(12,13,14,.5) 0%,transparent 20%,transparent 44%,rgba(12,13,14,.88) 100%)}
/* a shaft of light coming off the glass, sits between the footage and the type */
.shaft{position:absolute;z-index:1;pointer-events:none;inset:-14% 0 auto 34%;height:128%;width:44%;
  background:linear-gradient(102deg,transparent,rgba(120,208,226,.11) 42%,rgba(255,255,255,.05) 58%,transparent);
  transform:rotate(9deg);filter:blur(22px);mix-blend-mode:screen}
.hero .in{position:relative;z-index:3;width:100%;padding-block:clamp(56px,8vw,116px)}
.hero-copy{position:relative;z-index:3;max-width:min(64ch,66%)}
h1{font-size:clamp(42px,7.6vw,116px);max-width:14ch;text-shadow:0 2px 40px rgba(0,0,0,.5)}
.hero p{margin:24px 0 0;max-width:44ch;font-size:clamp(16px,1.35vw,19px);color:#d9dddf}

/* front plane: a plate of proof lifted off the footage, hung over the section edge */
.plate{margin:0;position:absolute;z-index:4;right:var(--gut);bottom:clamp(-108px,-9vw,-64px);
  width:clamp(168px,20vw,286px);transform:rotate(-2.6deg);transition:transform .9s var(--ez)}
.plate-in{padding:9px;border-radius:22px;background:linear-gradient(168deg,#26292b,#141618);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.09),var(--rim)}
.plate-in img{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:13px;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.5)}
.plate figcaption{margin-top:15px;text-align:right;font-size:12.5px;line-height:1.45;color:var(--fg-2);
  text-shadow:0 1px 10px rgba(0,0,0,.8)}
.plate:hover{transform:rotate(-1.4deg) translateY(-7px)}
@supports (animation-timeline:scroll()){
  @media (prefers-reduced-motion:no-preference){
    .hero-bg video{animation:drift linear both;animation-timeline:scroll();animation-range:0 92vh}
    @keyframes drift{to{transform:scale(1.08) translateY(7%)}}
  }
}""", 'hero planes')

# 3 -- hero markup
rep("""<section class="hero">
  <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Two cleaners washing a commercial storefront with water-fed poles"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video>
  <div class="in wrap">
    <h1>Crystal clear views start here.</h1>
    <p>Windows, screens, tracks, hard water, tint, solar panels and hauling across the East Valley.</p>
    <div class="acts">
      <a class="btn" href="tel:+14808069455">Call 480-806-9455</a>
      <a class="tlink" href="sms:+14808069455">Or text a photo of your windows</a>
    </div>
  </div>
</section>""",
"""<section class="hero">
  <div class="hero-bg">
    <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Two cleaners washing a commercial storefront with water-fed poles"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video>
  </div>
  <span class="shaft" aria-hidden="true"></span>
  <div class="in wrap">
    <div class="hero-copy">
      <h1>Crystal clear views start here.</h1>
      <p>Windows, screens, tracks, hard water, tint, solar panels and hauling across the East Valley.</p>
      <div class="acts">
        <a class="btn" href="tel:+14808069455">Call 480-806-9455</a>
        <a class="tlink" href="sms:+14808069455">Or text a photo of your windows</a>
      </div>
    </div>
    <figure class="plate">
      <div class="plate-in"><img src="assets/beforeafter.jpg" alt="Before and after of a commercial glass frontage, dull filmed glass above and clear glass below" width="608" height="1080"></div>
      <figcaption>The same frontage,<br>before and after</figcaption>
    </figure>
  </div>
</section>""", 'hero markup')

# statement needs headroom for the plate hanging into it
rep(".statement{padding-block:clamp(72px,11vw,164px)}",
    ".statement{padding-block:clamp(112px,14vw,208px) clamp(72px,11vw,164px);position:relative}", 'statement headroom')

# 4 -- button haptics
rep(""".btn:hover{background:#3ad6ec;transform:translateY(-2px)}
.btn:active{transform:translateY(0) scale(.985)}""",
""".btn{box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 10px 24px -10px rgba(18,196,222,.7)}
.btn:hover{background:#3ad6ec;transform:translateY(-2px);box-shadow:inset 0 1px 0 rgba(255,255,255,.36),0 18px 38px -12px rgba(18,196,222,.85)}
.btn:active{transform:translateY(0) scale(.985)}""", 'button haptics')

# 5 -- media get real enclosures and a z-axis cascade
rep(".rgrid .m{position:relative;aspect-ratio:9/16;overflow:hidden;background:var(--bg-2)}",
""".rgrid .m{position:relative;aspect-ratio:9/16;overflow:hidden;background:var(--bg-2);border-radius:16px;
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.07),var(--rim)}
.rgrid figure:nth-child(2){transform:translateY(clamp(12px,2.2vw,34px))}
.rgrid figure:nth-child(3){transform:translateY(clamp(-10px,-1.4vw,0px))}""", 'reel enclosures')

rep(".proof figure{margin:0;position:relative;overflow:hidden;background:var(--bg-2)}",
""".proof figure{margin:0;position:relative;overflow:hidden;background:var(--bg-2);border-radius:16px;
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.06);transition:box-shadow .7s var(--ez),transform .7s var(--ez)}
.proof figure:hover{box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.12);transform:translateY(-5px)}
.pb{margin-top:clamp(18px,3vw,52px)}""", 'proof enclosures')

# 6 -- atmospheric glow behind the reels band
rep(".reels{padding-block:clamp(72px,10vw,148px)}",
""".reels{padding-block:clamp(72px,10vw,148px);position:relative}
.reels::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:-1;
  background:radial-gradient(74% 52% at 50% 42%,rgba(18,196,222,.075),transparent 72%)}""", 'reels glow')

# 7 -- scroll interpolation resolves out of blur
rep(""".rv{opacity:0;transform:translateY(22px);transition:opacity .85s var(--ez),transform .85s var(--ez)}
.rv.in{opacity:1;transform:none}""",
""".rv{opacity:0;transform:translateY(30px);filter:blur(9px);
  transition:opacity .95s var(--ez-out),transform .95s var(--ez-out),filter .95s var(--ez-out)}
.rv.in{opacity:1;transform:none;filter:blur(0)}""", 'scroll interpolation')

# 8 -- mobile: unstack the plate, drop the shaft
rep("""  .hero{min-height:auto;padding-top:68px}
  .hero .in{padding-block:clamp(120px,34vw,220px) clamp(40px,10vw,72px)}""",
"""  .hero{min-height:auto;padding-top:68px}
  .hero .in{padding-block:clamp(120px,34vw,220px) clamp(40px,10vw,72px)}
  .hero-copy{max-width:100%}
  .plate{position:relative;right:auto;bottom:auto;width:min(58%,220px);margin:36px 0 0;transform:none}
  .plate:hover{transform:translateY(-5px)}
  .plate figcaption{text-align:left}
  .statement{padding-block:clamp(64px,12vw,120px)}
  .rgrid figure:nth-child(2),.rgrid figure:nth-child(3){transform:none}
  .shaft{display:none}""", 'mobile collapse')

open(p, 'w', encoding='utf-8').write(s)
print('D1 depth pass applied:', len(edits), 'edits ->', ', '.join(edits))
