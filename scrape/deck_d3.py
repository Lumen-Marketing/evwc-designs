# -*- coding: utf-8 -*-
p = '03-hazard.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---------------------------------------------------------------- CSS ------
OLD_CSS = """.rstage{--bay:clamp(174px,21.5vw,300px);display:grid;
  grid-template-columns:repeat(2,minmax(0,var(--bay)));justify-content:center;align-items:end;
  gap:clamp(30px,4.6vw,74px);margin-bottom:clamp(66px,8.5vw,124px)}
.bay{border:0;padding:11px;background:var(--plate);position:relative;
  transition:transform .42s var(--ez),box-shadow .42s var(--ez)}
.bay.l{box-shadow:var(--bevel),-10px 10px 0 rgba(18,196,222,.16),var(--cast)}
.bay.r{box-shadow:var(--bevel),10px 10px 0 rgba(18,196,222,.16),var(--cast)}
.bay::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
  background-image:var(--bolts);background-repeat:no-repeat}
@media (hover:hover) and (pointer:fine){
  .bay.l:hover{transform:translate(3px,-3px);box-shadow:var(--bevel),-14px 14px 0 rgba(18,196,222,.2),var(--cast)}
  .bay.r:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),14px 14px 0 rgba(18,196,222,.2),var(--cast)}
}
.bay .vid{position:relative;aspect-ratio:9/16;background:#000;box-shadow:var(--bevel-deep),0 0 0 1px #000}
.bay video,.bay .vid img{width:100%;height:100%;object-fit:cover}
"""

NEW_CSS = """/* the index: a ruled tab strip, not a row of pills */
.rail{display:flex;flex-wrap:wrap;justify-content:center;list-style:none;margin:0 0 clamp(28px,3.6vw,46px);
  padding:0;border-block:1px solid var(--line)}
.rail li{display:flex}
.tab{appearance:none;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.2em;
  text-transform:uppercase;min-height:46px;padding:0 15px;cursor:pointer;
  border:0;border-right:1px solid var(--line);background:transparent;color:var(--grey);
  transition:background .18s var(--ez),color .18s var(--ez)}
.rail li:first-child .tab{border-left:1px solid var(--line)}
.tab:hover{background:var(--steel);color:var(--white)}
.tab[aria-selected="true"]{background:var(--yellow);color:#000}

/* the deck: plates standing on a bench. They scale from the foot, not the
   centre, so however far back a plate steps it keeps the same baseline. */
.deck{--dw:clamp(188px,22vw,312px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 auto clamp(58px,7.2vw,102px);touch-action:pan-y}
.deck::before{content:"";content:"";position:absolute;left:50%;translate:-50% 0;bottom:-1px;height:1px;
  width:min(calc(100% + var(--gut) * 1.2),1320px);background:var(--line2)}
.slide{position:absolute;left:50%;top:0;margin:0;width:var(--dw);height:var(--dh);cursor:pointer;
  -webkit-tap-highlight-color:transparent;transform-origin:50% 100%;
  transform:translate3d(calc(-50% + var(--x,0px)),0,0) scale(var(--s,1));
  transition:transform .55s var(--ez),opacity .4s var(--ez)}
.slide.far{opacity:0;pointer-events:none}
.slide.on{cursor:default}
.plate{position:relative;width:100%;height:100%;padding:10px;background:var(--plate);
  box-shadow:var(--bevel),var(--cast);transition:box-shadow .4s var(--ez)}
.slide.on .plate{box-shadow:var(--bevel),0 14px 0 rgba(18,196,222,.2),var(--cast)}
.plate::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
  background-image:var(--bolts);background-repeat:no-repeat}
.slide .vid{position:relative;width:100%;height:100%;overflow:hidden;background:#000;
  box-shadow:var(--bevel-deep),0 0 0 1px #000}
.slide video,.slide .vid img{width:100%;height:100%;object-fit:cover;filter:saturate(.94) contrast(1.04)}
/* a plate that is not in front is a plate that is not lit */
.slide .vid::after{content:"";position:absolute;inset:0;z-index:3;pointer-events:none;
  background:rgba(6,7,8,.58);transition:opacity .4s var(--ez)}
.slide.on .vid::after{opacity:0}
.slide .tape,.slide .dur{opacity:0;transition:opacity .3s var(--ez)}
.slide.on .tape,.slide.on .dur{opacity:1}

/* one machined control block: back, count, forward, bolted together */
.deck-bar{display:flex;flex-direction:column;align-items:center;gap:clamp(14px,1.8vw,22px);
  margin-top:clamp(30px,3.6vw,50px)}
.dcap{margin:0;text-align:center}
.dcap b{display:block;font-family:var(--d);font-weight:700;text-transform:uppercase;letter-spacing:.01em;
  font-size:clamp(24px,3.1vw,42px);line-height:1}
.dcap span{display:block;margin-top:10px;font-family:var(--m);font-size:9.5px;font-weight:500;
  letter-spacing:.2em;text-transform:uppercase;color:var(--grey)}
.dctl{display:flex;align-items:stretch;border:1px solid var(--line)}
.dnav{appearance:none;width:54px;min-height:48px;border:0;cursor:pointer;background:var(--plate);
  color:var(--white);display:inline-flex;align-items:center;justify-content:center;
  box-shadow:var(--bevel);transition:background .18s var(--ez),color .18s var(--ez)}
.dnav:hover{background:var(--steel2);color:var(--yellow)}
.dnav:active{box-shadow:var(--bevel-deep)}
.dnav svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round}
.dcount{display:flex;align-items:center;justify-content:center;min-width:96px;
  border-inline:1px solid var(--line);font-family:var(--m);font-size:9.5px;font-weight:700;
  letter-spacing:.2em;color:var(--grey);font-variant-numeric:tabular-nums}
"""
rep(OLD_CSS, NEW_CSS, 'deck css')

rep("""/* proof */
.proof{display:grid;grid-template-columns:repeat(6,1fr);grid-auto-rows:150px;gap:12px}
.proof figure{margin:0;position:relative;overflow:hidden;border:1px solid var(--line);
  box-shadow:var(--bevel),0 20px 44px -26px #000;transition:transform .6s var(--ez),box-shadow .6s var(--ez)}
.proof figure:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),10px 10px 0 rgba(252,222,88,.14),0 24px 48px -26px #000}
.proof img{width:100%;height:100%;object-fit:cover;filter:saturate(.92) contrast(1.04)}
.q1{grid-column:span 3;grid-row:span 3}
.q2{grid-column:span 3;grid-row:span 2}
.q3{grid-column:span 2}
.proof figcaption{position:absolute;left:0;bottom:0;background:var(--yellow);color:#000;padding:6px 12px;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}

""", "", 'drop proof css')

# ------------------------------------------------------------- markup ------
OLD_HTML = """    <div class="rstage">
      <figure class="bay l">
        <div class="vid"><div class="tape"></div><span class="dur">0:14</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
        <figcaption class="ft"><b>Storefront</b><span>Mesa</span></figcaption>
      </figure>
      <figure class="bay r">
        <div class="vid"><div class="tape"></div><span class="dur">0:07</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
        <figcaption class="ft"><b>Solar rinse</b><span>Tile roof</span></figcaption>
      </figure>
    </div>
"""

VID = ('<video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/%s" '
       'aria-label="%s"><source src="assets/%s" type="video/mp4"></video>')
IMG = '<img src="assets/%s" alt="%s" loading="lazy" width="%d" height="%d">'

ITEMS = [
    ("Storefront","Mesa / Exterior / 0:14","0:14",
     VID % ("poster-storefront.jpg","Cleaning a commercial storefront with a water-fed pole","reel-storefront.mp4")),
    ("Solar rinse","Tile roof / Panel wash / 0:07","0:07",
     VID % ("poster-solar.jpg","Rinsing dust off rooftop solar panels","reel-solar.mp4")),
    ("Restaurant","Mesa / Interior and exterior",None,
     IMG % ("restaurant.jpg","Looking out through a spotless full-height restaurant window onto an Arizona parking lot",1400,1750)),
    ("Residential","Two storey / Water-fed pole",None,
     IMG % ("hero-pole.jpg","Water-fed pole cleaning a tall arched window on a tile-roofed home",1200,1600)),
    ("Retail entry","Door and window glass",None,
     IMG % ("storefront.jpg","Clean glass shopfront with door and window signage",1200,1200)),
    ("Junk removal","Yard clear-out / Hauled",None,
     IMG % ("junk-yard.jpg","A backyard with a pile of dumped furniture and cardboard on the left and the same corner cleared on the right",820,1094)),
    ("The rig","Owner operated / Ladder racked",None,
     IMG % ("rig.jpg","Work vehicle with a ladder racked on the roof at sunset",1200,1200)),
]
TABS = ["Storefront","Solar","Restaurant","Residential","Retail","Junk","Rig"]

def slide(cap, sub, dur, inner):
    d = '<span class="dur">%s</span>' % dur if dur else ''
    return ('    <figure class="slide" data-cap="%s" data-sub="%s">\n'
            '      <div class="plate"><div class="vid"><div class="tape"></div>%s%s</div></div>\n'
            '    </figure>\n') % (cap, sub, d, inner)

NEW_HTML = ('    <ul class="rail" role="tablist" aria-label="Job record">\n'
    + ''.join('      <li><button class="tab" role="tab" aria-selected="%s">%s</button></li>\n'
              % ('true' if i == 0 else 'false', t) for i, t in enumerate(TABS))
    + '    </ul>\n\n'
    + '    <div class="deck" data-deck aria-roledescription="carousel" aria-label="Job record">\n'
    + ''.join(slide(*it) for it in ITEMS)
    + '    </div>\n\n'
    + '''    <div class="deck-bar">
      <p class="dcap" aria-live="polite"><b>Storefront</b><span>Mesa / Exterior / 0:14</span></p>
      <div class="dctl">
        <button class="dnav" data-dir="-1" aria-label="Previous item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 5.5 8 12l6.5 6.5"/></svg></button>
        <span class="dcount" aria-hidden="true">01 / 07</span>
        <button class="dnav" data-dir="1" aria-label="Next item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 5.5 16 12l-6.5 6.5"/></svg></button>
      </div>
    </div>
''')
rep(OLD_HTML, NEW_HTML, 'deck html')

rep("""      <p>Straight off their Instagram. Both clips play muted on loop, with the before and after bolted in underneath.</p>""",
    """      <p>Their own clips and job photographs, straight off Instagram. The plate in front plays muted on loop.</p>""",
    'sub copy')

rep("""<section>
  <div class="wrap">
    <div class="shead"><div><span class="code">Sec. 03 / Job record</span><h2 style="margin-top:14px">Glass you<br>stop noticing</h2></div></div>
    <div class="proof">
      <figure class="q1"><img src="assets/restaurant.jpg" alt="Looking out through a spotless full-height restaurant window onto an Arizona parking lot" loading="lazy" width="1400" height="1750"><figcaption>Restaurant frontage</figcaption></figure>
      <figure class="q2"><img src="assets/hero-pole.jpg" alt="Water-fed pole cleaning a tall arched window on a tile-roofed home" loading="lazy" width="1200" height="1600"><figcaption>Two-storey residential</figcaption></figure>
      <figure class="q3"><img src="assets/junk.jpg" alt="Before and after of a backyard cleared of debris" loading="lazy" width="1024" height="1024"><figcaption>Junk removal</figcaption></figure>
      <figure class="q3"><img src="assets/storefront.jpg" alt="Clean glass shopfront with door and window signage" loading="lazy" width="1200" height="1200"><figcaption>Retail entry</figcaption></figure>
      <figure class="q3"><img src="assets/rig.jpg" alt="Work vehicle with a ladder racked on the roof at sunset" loading="lazy" width="1200" height="1200"><figcaption>Owner-operated</figcaption></figure>
    </div>
  </div>
</section>

""", "", 'drop proof markup')

# the schedule loses a number when the job record folds into the deck
rep("Sec. 04 / Verified reviews", "Sec. 03 / Verified reviews", 'renum reviews')
rep("Sec. 05 / Coverage zone", "Sec. 04 / Coverage zone", 'renum coverage')
rep("Sec. 06 / Free estimate", "Sec. 05 / Free estimate", 'renum estimate')

rep("  .rstage{grid-template-columns:minmax(0,300px);gap:clamp(38px,9vw,60px);margin-bottom:clamp(56px,11vw,88px)}\n", "", 'drop rstage mq')
rep("  .proof{grid-template-columns:repeat(2,1fr);grid-auto-rows:165px}\n  .q1{grid-column:span 2;grid-row:span 2}.q2{grid-column:span 2;grid-row:span 2}.q3{grid-column:span 1;grid-row:span 1}\n", "", 'drop proof mq')

open(p, 'w', encoding='utf-8').write(s)
print('D3 deck:', len(done), 'edits ->', ', '.join(done))
