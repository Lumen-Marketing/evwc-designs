p = '02-broadsheet.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E"
         "%3Cfilter id='p'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4' "
         "stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23p)' "
         "opacity='.6'/%3E%3C/svg%3E\")")

# 1 -- depth tokens. Shadows are tinted with the deep teal, never neutral black.
rep("""  --d:'Anton',Impact,'Haettenschweiler',sans-serif;
  --b:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
}""",
"""  --d:'Anton',Impact,'Haettenschweiler',sans-serif;
  --b:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;
  --ez:cubic-bezier(.32,.72,0,1);
  --ez-out:cubic-bezier(.16,1,.3,1);
  /* every shadow is tinted with the deep teal so nothing reads as neutral grey */
  --lift-1:0 1px 2px rgba(10,47,58,.06), 0 10px 22px -12px rgba(10,47,58,.22);
  --lift-2:0 2px 6px rgba(10,47,58,.07), 0 26px 52px -22px rgba(10,47,58,.3);
  --lift-3:0 4px 10px rgba(10,47,58,.09), 0 48px 90px -34px rgba(10,47,58,.42);
}
/* paper grain: fixed, pointer-events none */
body::after{content:"";position:fixed;inset:0;z-index:60;pointer-events:none;opacity:.055;mix-blend-mode:multiply;
  background-image:""" + NOISE + "}", 'tokens+grain')

# 2 -- hero: stacked offset planes, a halftone that laps over the type, and a
#      review card that hangs across the section boundary
rep(""".hblock{position:relative;margin-top:clamp(26px,3.5vw,46px);border-radius:var(--r-card);overflow:hidden;background:var(--deep);aspect-ratio:21/9}
.hblock video{width:100%;height:100%;object-fit:cover}
.hblock .dots{position:absolute;inset:0;color:var(--cyan);opacity:.5;mix-blend-mode:screen;pointer-events:none;
  -webkit-mask-image:linear-gradient(105deg,#000 0 26%,transparent 62%);mask-image:linear-gradient(105deg,#000 0 26%,transparent 62%)}
.hblock .cap{position:absolute;left:clamp(18px,2.4vw,34px);bottom:clamp(18px,2.4vw,34px);background:var(--limestone);border-radius:var(--r-pill);padding:9px 20px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}""",
""".slab{position:relative;margin-top:clamp(26px,3.5vw,46px);isolation:isolate}
/* two colour planes stacked behind the media, each offset a little further */
.slab::before,.slab::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.slab::before{background:var(--deep);transform:translate(22px,22px)}
.slab::after{background:var(--cyan);transform:translate(11px,11px)}
.slab-in{position:relative;z-index:1;padding:10px;border-radius:var(--r-card);background:var(--limestone);
  box-shadow:var(--lift-3)}
.hblock{position:relative;border-radius:calc(var(--r-card) - 10px);overflow:hidden;background:var(--deep);aspect-ratio:21/9}
.hblock video{width:100%;height:100%;object-fit:cover}
.hblock .dots{position:absolute;inset:0;color:var(--cyan);opacity:.5;mix-blend-mode:screen;pointer-events:none;
  -webkit-mask-image:linear-gradient(105deg,#000 0 26%,transparent 62%);mask-image:linear-gradient(105deg,#000 0 26%,transparent 62%)}
.hblock .cap{position:absolute;left:clamp(16px,2vw,28px);bottom:clamp(16px,2vw,28px);background:var(--limestone);border-radius:var(--r-pill);padding:9px 20px;font-size:13px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
/* a dot field that laps up over the headline, putting type behind a layer */
.lap{position:absolute;z-index:2;left:clamp(-10px,-1vw,0px);top:clamp(-86px,-7vw,-40px);
  width:clamp(180px,26vw,340px);height:clamp(120px,15vw,210px);color:var(--ink);opacity:.5;pointer-events:none;
  -webkit-mask-image:radial-gradient(72% 82% at 22% 88%,#000,transparent 72%);
  mask-image:radial-gradient(72% 82% at 22% 88%,#000,transparent 72%)}
/* a proof card lifted off the slab and hung across the section edge */
.hcard{position:absolute;z-index:3;right:clamp(16px,3vw,54px);bottom:clamp(-72px,-6vw,-44px);
  background:var(--sun);border-radius:calc(var(--r-card) - 8px);padding:22px 26px;box-shadow:var(--lift-3);
  transform:rotate(-1.6deg);transition:transform .8s var(--ez)}
.hcard:hover{transform:rotate(-.4deg) translateY(-6px)}
.hcard .n{display:flex;align-items:center;gap:9px;font-family:var(--d);font-weight:400;font-size:clamp(30px,3.2vw,46px);line-height:1;letter-spacing:.02em}
.hcard .n svg{width:.6em;height:.6em}
.hcard .l{margin-top:7px;font-size:12.5px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:#5c5426}""",
    'hero slab + lap + card')

rep("""    <div class="hblock">
      <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Crew cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video>
      <div class="dots halftone"></div>
      <span class="cap">Commercial storefront · Mesa</span>
    </div>""",
"""    <div class="slab">
      <span class="lap halftone" aria-hidden="true"></span>
      <div class="slab-in">
        <div class="hblock">
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Crew cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video>
          <div class="dots halftone"></div>
          <span class="cap">Commercial storefront, Mesa</span>
        </div>
      </div>
      <div class="hcard">
        <span class="n"><svg aria-hidden="true"><use href="#i-star"/></svg>5.0</span>
        <span class="l">All 4 Google reviews</span>
      </div>
    </div>""", 'hero markup')

# the stats row now has a card hanging into it
rep('<div class="wrap">\n  <div class="stats">',
    '<div class="wrap" style="padding-top:clamp(56px,7vw,104px)">\n  <div class="stats">', 'stats headroom')

# 3 -- stat cards become nested trays with concentric radii
rep(""".stat{background:var(--cyan);border-radius:var(--r-card);padding:clamp(24px,3vw,40px)}
.stat.alt{background:var(--deep);color:var(--chalk)}""",
""".stat{background:var(--limestone);border-radius:var(--r-card);padding:9px;box-shadow:var(--lift-2);
  transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.stat:hover{transform:translateY(-5px);box-shadow:var(--lift-3)}
.stat>span{display:block}
.stat .core{background:var(--cyan);border-radius:calc(var(--r-card) - 9px);padding:clamp(20px,2.6vw,34px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.5)}
.stat.alt .core{background:var(--deep);color:var(--chalk);box-shadow:inset 0 1px 0 rgba(255,255,255,.14)}
.stat:nth-child(2){transform:translateY(clamp(8px,1.4vw,20px))}
.stat:nth-child(2):hover{transform:translateY(clamp(2px,.6vw,12px))}
.stat:nth-child(4){transform:translateY(clamp(-14px,-1.4vw,0px))}
.stat:nth-child(4):hover{transform:translateY(clamp(-20px,-2vw,-6px))}""", 'stat trays')

for a, b in [
 ('<div class="stat"><span class="l">Google rating</span><span class="n"><svg aria-hidden="true"><use href="#i-star"/></svg>5.0</span></div>',
  '<div class="stat"><div class="core"><span class="l">Google rating</span><span class="n"><svg aria-hidden="true"><use href="#i-star"/></svg>5.0</span></div></div>'),
 ('<div class="stat alt"><span class="l">Google reviews</span><span class="n">4</span></div>',
  '<div class="stat alt"><div class="core"><span class="l">Google reviews</span><span class="n">4</span></div></div>'),
 ('<div class="stat"><span class="l">Services offered</span><span class="n">7</span></div>',
  '<div class="stat"><div class="core"><span class="l">Services offered</span><span class="n">7</span></div></div>'),
 ('<div class="stat"><span class="l">Estimates</span><span class="n">Free</span></div>',
  '<div class="stat"><div class="core"><span class="l">Estimates</span><span class="n">Free</span></div></div>'),
]:
    rep(a, b, 'stat markup')

# 4 -- service cards lift instead of sitting flat
rep(""".svc article{background:var(--limestone);border-radius:var(--r-card);padding:clamp(24px,2.6vw,38px);display:flex;flex-direction:column;transition:transform .2s,background .2s}
.svc article:hover{transform:translateY(-4px);background:#fff}""",
""".svc article{background:var(--limestone);border-radius:var(--r-card);padding:clamp(24px,2.6vw,38px);display:flex;flex-direction:column;
  box-shadow:var(--lift-1);transition:transform .7s var(--ez),background .5s var(--ez),box-shadow .7s var(--ez)}
.svc article:hover{transform:translateY(-6px);background:#fff;box-shadow:var(--lift-3)}
.svc .ic{box-shadow:inset 0 1px 0 rgba(255,255,255,.7),0 1px 2px rgba(10,47,58,.08)}""", 'service lift')

# 5 -- reel bays get trays, a cascade and depth
rep(""".bay{position:relative;border-radius:var(--r-card);overflow:hidden;background:var(--deep);aspect-ratio:9/16}""",
""".bay{position:relative;border-radius:var(--r-card);overflow:hidden;background:var(--deep);aspect-ratio:9/16;
  box-shadow:var(--lift-2);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.bay:hover{transform:translateY(-6px);box-shadow:var(--lift-3)}
.reels .bay:nth-child(2){transform:translateY(clamp(14px,2.4vw,36px))}
.reels .bay:nth-child(2):hover{transform:translateY(clamp(6px,1.4vw,24px))}
.reels .bay:nth-child(3){transform:translateY(clamp(-12px,-1.6vw,0px))}
.reels .bay:nth-child(3):hover{transform:translateY(clamp(-20px,-2.4vw,-8px))}""", 'reel cascade')

# 6 -- proof frames lift
rep(""".proof figure{margin:0;border-radius:var(--r-card);overflow:hidden;position:relative;background:var(--limestone)}""",
""".proof figure{margin:0;border-radius:var(--r-card);overflow:hidden;position:relative;background:var(--limestone);
  box-shadow:var(--lift-2);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.proof figure:hover{transform:translateY(-5px);box-shadow:var(--lift-3)}""", 'proof lift')

# 7 -- review cards lift
rep(""".rev{background:var(--limestone);border-radius:var(--r-card);padding:clamp(24px,2.4vw,34px);display:flex;flex-direction:column}""",
""".rev{background:var(--limestone);border-radius:var(--r-card);padding:clamp(24px,2.4vw,34px);display:flex;flex-direction:column;
  box-shadow:var(--lift-1);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.rev:hover{transform:translateY(-5px);box-shadow:var(--lift-2)}""", 'review lift')

# 8 -- buttons get press physics
rep(""".b1{background:var(--cyan);color:var(--ink)}
.b1:hover{background:var(--cyan-dp);color:#fff;transform:translateY(-2px)}""",
""".b1{background:var(--cyan);color:var(--ink);box-shadow:inset 0 1px 0 rgba(255,255,255,.5),0 8px 20px -8px rgba(11,147,171,.6)}
.b1:hover{background:var(--cyan-dp);color:#fff;transform:translateY(-2px);box-shadow:inset 0 1px 0 rgba(255,255,255,.3),0 16px 32px -10px rgba(11,147,171,.7)}
.b1:active{transform:translateY(0) scale(.985)}""", 'button physics')

# 9 -- mobile collapse for the new hero layers
rep("""@media (max-width:560px){
  .svc,.revs,.stats{grid-template-columns:1fr}""",
"""@media (max-width:860px){
  .lap{display:none}
  .slab::before{transform:translate(12px,12px)}
  .slab::after{transform:translate(6px,6px)}
  .hcard{position:relative;right:auto;bottom:auto;margin:20px 0 0;transform:none;display:inline-block}
  .hcard:hover{transform:translateY(-4px)}
  .stat:nth-child(2),.stat:nth-child(4),
  .reels .bay:nth-child(2),.reels .bay:nth-child(3){transform:none}
}
@media (max-width:560px){
  .svc,.revs,.stats{grid-template-columns:1fr}""", 'mobile collapse')

open(p, 'w', encoding='utf-8').write(s)
print('D2 depth pass:', len(done), 'edits ->', ', '.join(done))
