# -*- coding: utf-8 -*-
p = '02-broadsheet.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

OLD_CSS = """.rstage{--bay:clamp(176px,22.5vw,312px);
  display:grid;grid-template-columns:repeat(2,minmax(0,var(--bay)));justify-content:center;
  align-items:end;gap:clamp(34px,5vw,80px);margin-bottom:clamp(78px,9.5vw,136px)}
.rbay{position:relative;margin:0;isolation:isolate;
  transition:transform .5s var(--ez-out)}
.rbay::before,.rbay::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.rbay::before{background:var(--deep)}
.rbay::after{background:var(--cyan)}
/* mirrored about the centre: the left stack leans left, the right stack right */
.rbay.l::before{transform:translate(-24px,24px)}
.rbay.l::after{transform:translate(-12px,12px)}
.rbay.r::before{transform:translate(24px,24px)}
.rbay.r::after{transform:translate(12px,12px)}
.rbay-in{position:relative;z-index:1;padding:9px;border-radius:var(--r-card);background:var(--limestone);
  box-shadow:var(--lift-3)}
.rbay .m{position:relative;border-radius:calc(var(--r-card) - 9px);overflow:hidden;background:var(--deep);
  aspect-ratio:9/16}
.rbay video,.rbay img{width:100%;height:100%;object-fit:cover}
/* the label is set into the paper tray, not floated over the footage */
.rbay figcaption{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 10px 4px}
.rbay figcaption b{font-size:13.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.rbay figcaption i{font-style:normal;background:var(--sun);border-radius:var(--r-pill);padding:5px 12px;
  font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap}
@media (hover:hover) and (pointer:fine){.rbay:hover{transform:translateY(-6px)}}
"""

NEW_CSS = """/* the index: every card in the deck, named, in the house pill */
.pills{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;list-style:none;
  margin:0 0 clamp(32px,4.2vw,56px);padding:0}
.pill{appearance:none;font:inherit;font-size:12.5px;font-weight:700;letter-spacing:.07em;
  text-transform:uppercase;cursor:pointer;min-height:44px;padding:0 19px;border-radius:var(--r-pill);
  border:1.5px solid var(--ink);background:transparent;color:var(--ink);
  transition:background .2s var(--ez-out),color .2s var(--ez-out),border-color .2s var(--ez-out)}
.pill:hover{background:var(--limestone)}
.pill[aria-selected="true"]{background:var(--cyan);border-color:var(--cyan)}

/* the deck: one card at full size on the centre line with its colour planes
   stacked straight down behind it, its neighbours stepped back either side.
   Depth stays stacking, never blur, so the falloff is scale and not focus. */
.deck{--dw:clamp(198px,23.5vw,332px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 auto clamp(72px,9vw,126px);touch-action:pan-y}
.deck::before,.deck::after{content:"";position:absolute;left:50%;top:0;z-index:0;
  width:var(--dw);height:var(--dh);border-radius:var(--r-card);pointer-events:none}
.deck::before{background:var(--deep);transform:translate(-50%,0) translate(0,26px)}
.deck::after{background:var(--cyan);transform:translate(-50%,0) translate(0,13px)}

.slide{position:absolute;left:50%;top:0;margin:0;width:var(--dw);height:var(--dh);cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  transform:translate3d(calc(-50% + var(--x,0px)),0,0) scale(var(--s,1));
  transition:transform .62s var(--ez-out),opacity .45s var(--ez-out)}
.slide.far{opacity:0;pointer-events:none}
.slide.on{cursor:default}
/* tray and core at concentric radii, the same construction as the stat row */
.frame{position:relative;width:100%;height:100%;padding:9px;border-radius:var(--r-card);
  background:var(--limestone);box-shadow:var(--lift-3)}
.frame>.core{position:relative;width:100%;height:100%;overflow:hidden;background:var(--deep);
  border-radius:calc(var(--r-card) - 9px)}
.frame img,.frame video{width:100%;height:100%;object-fit:cover}
.frame .core::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:rgba(10,47,58,.34);transition:opacity .45s var(--ez-out)}
.slide.on .frame .core::after{opacity:0}

.deck-bar{display:flex;flex-direction:column;align-items:center;gap:clamp(14px,1.8vw,22px);
  margin-top:clamp(52px,6vw,86px)}
.dcap{margin:0;text-align:center}
.dcap b{display:block;font-family:var(--d);font-weight:400;text-transform:uppercase;letter-spacing:.02em;
  font-size:clamp(24px,3vw,40px);line-height:1}
.dcap span{display:block;margin-top:9px;font-size:14px;color:#4c5a5f}
.dctl{display:flex;align-items:center;gap:14px}
.dnav{appearance:none;width:48px;height:48px;border-radius:var(--r-pill);cursor:pointer;
  background:transparent;color:var(--ink);border:1.5px solid var(--ink);
  display:inline-flex;align-items:center;justify-content:center;
  transition:background .2s var(--ez-out),color .2s var(--ez-out),transform .16s var(--ez-out)}
.dnav:hover{background:var(--ink);color:var(--limestone)}
.dnav:active{transform:scale(.94)}
.dnav svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}
.dcount{min-width:76px;text-align:center;font-size:12px;font-weight:700;letter-spacing:.16em;
  color:#4c5a5f;font-variant-numeric:tabular-nums}
"""
rep(OLD_CSS, NEW_CSS, 'deck css')

rep("""/* proof */
.proof{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;grid-auto-rows:150px}
.proof figure{margin:0;border-radius:var(--r-card);overflow:hidden;position:relative;background:var(--limestone);
  box-shadow:var(--lift-2);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.proof figure:hover{transform:translateY(-5px);box-shadow:var(--lift-3)}
.proof img{width:100%;height:100%;object-fit:cover}
.p1{grid-column:span 3;grid-row:span 3}
.p2{grid-column:span 3;grid-row:span 2}
.p3{grid-column:span 2;grid-row:span 1}
.proof figcaption{position:absolute;left:14px;bottom:14px;background:var(--limestone);border-radius:var(--r-pill);padding:7px 15px;font-size:11.5px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}

""", "", 'drop proof css')

OLD_HTML = """    <div class="rstage">
      <figure class="rbay l">
        <div class="rbay-in">
          <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
          <figcaption><b>Commercial storefront</b><i>Mesa</i></figcaption>
        </div>
      </figure>
      <figure class="rbay r">
        <div class="rbay-in">
          <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
          <figcaption><b>Solar array rinse</b><i>Tile roof</i></figcaption>
        </div>
      </figure>
    </div>
"""

def slide(cap, sub, pv, inner):
    return ('    <figure class="slide" data-cap="%s" data-sub="%s" data-pv="%s">\n'
            '      <div class="frame"><div class="core">%s</div></div>\n'
            '    </figure>\n') % (cap, sub, pv, inner)

VID = ('<video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/%s" '
       'aria-label="%s"><source src="assets/%s" type="video/mp4"></video>')
IMG = '<img src="assets/%s" alt="%s" loading="lazy" width="%d" height="%d">'

ITEMS = [
    ("Commercial storefront","Mesa, exterior glass","poster-storefront.jpg",
     VID % ("poster-storefront.jpg","Cleaning a commercial storefront with a water-fed pole","reel-storefront.mp4")),
    ("Solar array rinse","Tile roof, panel wash","poster-solar.jpg",
     VID % ("poster-solar.jpg","Rinsing dust off rooftop solar panels","reel-solar.mp4")),
    ("Restaurant frontage","Interior and exterior glass","restaurant.jpg",
     IMG % ("restaurant.jpg","Looking out through a spotless full-height restaurant window onto an Arizona parking lot",1400,1750)),
    ("Two storey residential","Water-fed pole, arched glass","hero-pole.jpg",
     IMG % ("hero-pole.jpg","Water-fed pole cleaning a tall arched window on a tile-roofed home",1200,1600)),
    ("Retail entry","Door and window glass","storefront.jpg",
     IMG % ("storefront.jpg","Clean glass shopfront with door and window signage",1200,1200)),
    ("Junk removal","Yard cleared and hauled away","junk-yard.jpg",
     IMG % ("junk-yard.jpg","A backyard with a pile of dumped furniture and cardboard on the left and the same corner cleared on the right",820,1094)),
    ("Owner operated","The rig, ladder racked","rig.jpg",
     IMG % ("rig.jpg","Work vehicle with a ladder racked on the roof at sunset",1200,1200)),
]
PILLS = ["Storefront","Solar","Restaurant","Residential","Retail entry","Junk removal","The rig"]

NEW_HTML = ('    <ul class="pills" role="tablist" aria-label="Recent work">\n'
    + ''.join('      <li><button class="pill" role="tab" aria-selected="%s">%s</button></li>\n'
              % ('true' if i == 0 else 'false', t) for i, t in enumerate(PILLS))
    + '    </ul>\n\n'
    + '    <div class="deck" data-deck aria-roledescription="carousel" aria-label="Recent work">\n'
    + ''.join(slide(*it) for it in ITEMS)
    + '    </div>\n\n'
    + '''    <div class="deck-bar">
      <p class="dcap" aria-live="polite"><b>Commercial storefront</b><span>Mesa, exterior glass</span></p>
      <div class="dctl">
        <button class="dnav" data-dir="-1" aria-label="Previous item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 5.5 8 12l6.5 6.5"/></svg></button>
        <span class="dcount" aria-hidden="true">01 / 07</span>
        <button class="dnav" data-dir="1" aria-label="Next item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 5.5 16 12l-6.5 6.5"/></svg></button>
      </div>
    </div>
''')
rep(OLD_HTML, NEW_HTML, 'deck html')

rep("""      <p>Straight off their Instagram. Both clips play muted on loop, with the before and after underneath.</p>""",
    """      <p>Their own clips and job photographs, straight off Instagram. The card in front plays muted on loop.</p>""",
    'sub copy')

# the deck carries all of this work now, so the bento below it was a repeat
rep("""<section>
  <div class="wrap">
    <div class="shead"><div><span class="eyebrow">Evidence</span><h2 style="margin-top:12px">Glass you stop noticing</h2></div></div>
    <div class="proof">
      <figure class="p1"><img src="assets/restaurant.jpg" alt="Looking out through a spotless full-height restaurant window onto an Arizona parking lot" loading="lazy" width="1400" height="1750"><figcaption>Restaurant frontage</figcaption></figure>
      <figure class="p2"><img src="assets/hero-pole.jpg" alt="Water-fed pole cleaning a tall arched window on a tile-roofed home" loading="lazy" width="1200" height="1600"><figcaption>Two-storey residential</figcaption></figure>
      <figure class="p3"><img src="assets/junk.jpg" alt="Before and after of a backyard cleared of debris" loading="lazy" width="1024" height="1024"><figcaption>Junk removal</figcaption></figure>
      <figure class="p3"><img src="assets/storefront.jpg" alt="Clean glass shopfront with door and window signage" loading="lazy" width="1200" height="1200"><figcaption>Retail entry</figcaption></figure>
      <figure class="p3"><img src="assets/rig.jpg" alt="Work vehicle with a ladder racked on the roof at sunset" loading="lazy" width="1200" height="1200"><figcaption>Owner-operated</figcaption></figure>
    </div>
  </div>
</section>

""", "", 'drop proof markup')

rep("  .rstage{grid-template-columns:minmax(0,312px);gap:clamp(40px,9vw,64px);margin-bottom:clamp(64px,12vw,96px)}\n", "", 'drop rstage mq')
rep("  .proof{grid-template-columns:repeat(2,1fr);grid-auto-rows:170px}\n  .p1{grid-column:span 2;grid-row:span 2}.p2{grid-column:span 2;grid-row:span 2}.p3{grid-column:span 1;grid-row:span 1}\n", "", 'drop proof mq')

open(p, 'w', encoding='utf-8').write(s)
print('D2 deck:', len(done), 'edits ->', ', '.join(done))
