# -*- coding: utf-8 -*-
p = '02-broadsheet.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

OLD_CSS = """/* reels */
.reels{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.bay{position:relative;border-radius:var(--r-card);overflow:hidden;background:var(--deep);aspect-ratio:9/16;
  box-shadow:var(--lift-2);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.bay:hover{transform:translateY(-6px);box-shadow:var(--lift-3)}
.reels .bay:nth-child(2){transform:translateY(clamp(14px,2.4vw,36px))}
.reels .bay:nth-child(2):hover{transform:translateY(clamp(6px,1.4vw,24px))}
.reels .bay:nth-child(3){transform:translateY(clamp(-12px,-1.6vw,0px))}
.reels .bay:nth-child(3):hover{transform:translateY(clamp(-20px,-2.4vw,-8px))}
.bay video,.bay img{width:100%;height:100%;object-fit:cover}
.bay .lab{position:absolute;left:16px;bottom:16px;right:16px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.bay .lab b{background:var(--limestone);border-radius:var(--r-pill);padding:9px 17px;font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.bay .lab i{background:var(--cyan);color:var(--ink);border-radius:var(--r-pill);padding:9px 15px;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-style:normal}"""

NEW_CSS = """/* reels: a symmetric spread.
   Two clips of equal size on one baseline with their colour planes mirrored
   outward, then the before and after as a single wide plate on the centre
   line. Depth here is still stacking, never blur: planes offset behind the
   paper, trays and cores at concentric radii. */
.rstage{--bay:clamp(176px,22.5vw,312px);
  display:grid;grid-template-columns:repeat(2,minmax(0,var(--bay)));justify-content:center;
  align-items:end;gap:clamp(34px,5vw,80px);margin-bottom:clamp(78px,9.5vw,136px)}
.rbay{position:relative;margin:0;isolation:isolate;
  transition:transform .5s var(--ez-out)}
.rbay::before,.rbay::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.rbay::before{background:var(--deep)}
.rbay::after{background:var(--cyan)}
/* mirrored about the centre: the left stack leans left, the right stack right */
.rbay.l::before{transform:translate(-20px,20px)}
.rbay.l::after{transform:translate(-10px,10px)}
.rbay.r::before{transform:translate(20px,20px)}
.rbay.r::after{transform:translate(10px,10px)}
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

/* the payoff plate: one object, two halves, offset straight down so it stays
   on the centre line the clips above it share */
.ba{position:relative;margin:0 auto;max-width:clamp(292px,56vw,680px);isolation:isolate}
.ba::before,.ba::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.ba::before{background:var(--deep);transform:translate(0,22px)}
.ba::after{background:var(--sun);transform:translate(0,11px)}
.ba-in{position:relative;z-index:1;padding:9px;border-radius:var(--r-card);background:var(--limestone);
  box-shadow:var(--lift-3)}
.ba-g{display:grid;grid-template-columns:1fr 1fr;gap:9px}
.ba-g figure{margin:0;position:relative;border-radius:calc(var(--r-card) - 9px);overflow:hidden;
  background:var(--deep);aspect-ratio:4/5}
.ba-g img{width:100%;height:100%;object-fit:cover}
.ba-g figcaption{position:absolute;left:14px;bottom:14px;background:var(--limestone);border-radius:var(--r-pill);
  padding:8px 17px;font-size:11.5px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
.ba-g figure+figure figcaption{left:auto;right:14px;background:var(--cyan)}
.bacap{margin:26px 0 0;text-align:center;font-size:14px;color:#4c5a5f}"""

rep(OLD_CSS, NEW_CSS, 'reels css')

OLD_HTML = """    <div class="reels">
      <div class="bay">
        <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video>
        <span class="lab"><b>Commercial storefront</b><i>Mesa</i></span>
      </div>
      <div class="bay">
        <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video>
        <span class="lab"><b>Solar array rinse</b><i>Tile roof</i></span>
      </div>
      <div class="bay">
        <img src="assets/beforeafter.jpg" alt="Before and after of a commercial glass frontage, dull filmed glass above and clear glass below" loading="lazy" width="608" height="1080">
        <span class="lab"><b>Before / after</b><i>Glazing</i></span>
      </div>
    </div>"""

NEW_HTML = """    <div class="rstage">
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
    <figure class="ba">
      <div class="ba-in">
        <div class="ba-g">
          <figure><img src="assets/ba-before.jpg" alt="A commercial glass frontage before cleaning, the panes hazy with dust and hard water film" loading="lazy" width="390" height="488"><figcaption>Before</figcaption></figure>
          <figure><img src="assets/ba-after.jpg" alt="The same frontage after cleaning, the panes clear and reflecting the sky" loading="lazy" width="390" height="488"><figcaption>After</figcaption></figure>
        </div>
      </div>
      <figcaption class="bacap">The same storefront glazing in Mesa, photographed either side of one visit.</figcaption>
    </figure>"""

rep(OLD_HTML, NEW_HTML, 'reels html')

rep("""      <p>Straight off their Instagram. Two clips playing muted on loop, plus a before and after.</p>""",
    """      <p>Straight off their Instagram. Both clips play muted on loop, with the before and after underneath.</p>""",
    'sub copy')

# responsive
rep("  .reels{grid-template-columns:1fr;max-width:400px;margin-inline:auto}",
    "  .rstage{grid-template-columns:minmax(0,312px);gap:clamp(40px,9vw,64px);margin-bottom:clamp(64px,12vw,96px)}",
    'stage mq')
rep("  .reels .bay:nth-child(2),.reels .bay:nth-child(3){transform:none}\n", "", 'drop stagger mq')

open(p, 'w', encoding='utf-8').write(s)
print('D2 reels:', len(done), 'edits ->', ', '.join(done))
