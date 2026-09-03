# -*- coding: utf-8 -*-
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

OLD_CSS = """/* ---------- reels ---------- */
.reels{padding-block:clamp(72px,10vw,148px);position:relative}
.reels::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:-1;
  background:radial-gradient(74% 52% at 50% 42%,rgba(18,196,222,.075),transparent 72%)}
.reels h2{font-size:clamp(30px,4.6vw,66px);max-width:14ch}
.reels .sub{margin:18px 0 clamp(36px,4.5vw,64px);max-width:50ch;color:var(--fg-2)}
.rgrid{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(12px,1.6vw,22px)}
.rgrid figure{margin:0}
.rgrid .m{position:relative;aspect-ratio:9/16;overflow:hidden;background:var(--bg-2);border-radius:16px;
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.07),var(--rim)}
.rgrid figure:nth-child(2){transform:translateY(clamp(12px,2.2vw,34px))}
.rgrid figure:nth-child(3){transform:translateY(clamp(-10px,-1.4vw,0px))}
.rgrid video,.rgrid img{width:100%;height:100%;object-fit:cover}
.rgrid figcaption{margin-top:14px;font-size:14.5px;color:var(--fg-2)}
.rgrid figcaption b{display:block;color:var(--fg);font-weight:500;font-size:16px;margin-bottom:3px}"""

NEW_CSS = """/* ---------- reels: a light table ----------
   Two clips of equal size standing on one shared surface, mirrored about the
   centre line, then the before and after as a single hinged plate below. The
   depth device stays the one this direction owns: thrown light and diffusion,
   never a hard edge. */
.reels{padding-block:clamp(72px,10vw,148px);position:relative}
.reels::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:-1;
  background:radial-gradient(74% 52% at 50% 42%,rgba(18,196,222,.075),transparent 72%)}
.reels h2{font-size:clamp(30px,4.6vw,66px)}
.reels .sub{color:var(--fg-2)}
.rhead{max-width:54ch;margin:0 auto clamp(56px,6.5vw,96px);text-align:center}
.rhead .sub{margin:18px auto 0;max-width:48ch}

/* the stage: two equal bays, one baseline, symmetric about the centre */
.stage{--bay:clamp(184px,24vw,330px);
  position:relative;display:grid;grid-template-columns:repeat(2,minmax(0,var(--bay)));
  justify-content:center;align-items:end;gap:clamp(20px,3.6vw,58px);
  margin-bottom:clamp(104px,13vw,178px)}
/* the surface they stand on, fading out equally at both ends */
.stage::before{content:"";position:absolute;left:50%;translate:-50% 0;bottom:0;height:1px;
  width:min(126%,1160px);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.17) 24%,rgba(255,255,255,.17) 76%,transparent)}

.bay{margin:0;position:relative}
/* tray and core, concentric: the core radius is the tray radius less its padding */
.bay-in{padding:7px;border-radius:20px;background:linear-gradient(168deg,#2a2e30,#131517);
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.1),var(--rim);
  transition:transform 420ms var(--ez-out),box-shadow 420ms var(--ez-out)}
.bay .m{position:relative;aspect-ratio:9/16;overflow:hidden;border-radius:13px;background:var(--bg-2);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.62)}
.bay video,.bay img{width:100%;height:100%;object-fit:cover}
/* the caption lives inside the tray, so a bay is one object rather than a
   card with loose text floating under it */
.bay figcaption{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  padding:11px 6px 3px;font-size:14px;color:var(--fg)}
.bay figcaption span{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:#767d80;
  white-space:nowrap}
/* the light each lit screen throws down onto the table */
.bay::after{content:"";position:absolute;left:6%;right:6%;top:100%;height:clamp(56px,8vw,104px);
  pointer-events:none;background-image:var(--pv);background-size:cover;background-position:center;
  transform:scaleY(-1);filter:blur(13px) saturate(.62);opacity:.28;
  -webkit-mask-image:linear-gradient(to bottom,transparent,#000);
  mask-image:linear-gradient(to bottom,transparent,#000)}
@media (hover:hover) and (pointer:fine){
  .bay:hover .bay-in{transform:translateY(-6px);box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.15),var(--rim)}
}

/* the hinge: a centred rule that names the pair below it */
.hinge{display:flex;align-items:center;gap:20px;max-width:min(88%,660px);
  margin:0 auto clamp(26px,3.2vw,40px)}
.hinge::before,.hinge::after{content:"";flex:1;height:1px}
.hinge::before{background:linear-gradient(90deg,transparent,rgba(255,255,255,.2))}
.hinge::after{background:linear-gradient(90deg,rgba(255,255,255,.2),transparent)}
.hinge span{font-size:14.5px;color:var(--fg-2);white-space:nowrap}

/* the plate: two halves of one object, split by a seam, labelled at opposite corners */
.dip{margin:0 auto;max-width:clamp(292px,50vw,600px)}
.dip-in{padding:7px;border-radius:20px;background:linear-gradient(168deg,#2a2e30,#131517);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.1),var(--rim)}
.dip-g{display:grid;grid-template-columns:1fr 1fr;gap:2px;border-radius:13px;overflow:hidden;
  background:rgba(255,255,255,.16)}
.dip-g figure{margin:0;position:relative;aspect-ratio:4/5;overflow:hidden;background:var(--bg-2)}
.dip-g img{width:100%;height:100%;object-fit:cover}
.dip-g figcaption{position:absolute;inset:auto 0 0 0;padding:30px 13px 11px;font-size:12px;
  letter-spacing:.15em;text-transform:uppercase;color:#e9edee;
  background:linear-gradient(180deg,transparent,rgba(7,8,9,.88))}
.dip-g figure+figure figcaption{text-align:right;color:var(--acc)}
.dcap{margin:15px 0 0;text-align:center;font-size:13.5px;color:#777e81}"""

rep(OLD_CSS, NEW_CSS, 'reels css')

OLD_HTML = """<section class="reels wrap" id="reels">
  <h2 class="rv">Straight from the van.</h2>
  <p class="sub rv">Filmed on their own jobs and posted to Instagram. Two clips play here with the sound off, alongside a before and after.</p>
  <div class="rgrid">
    <figure class="rv">
      <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
      <figcaption><b>Commercial storefront</b>Mesa, exterior glass</figcaption>
    </figure>
    <figure class="rv">
      <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
      <figcaption><b>Solar array rinse</b>Tile roof, panel wash</figcaption>
    </figure>
    <figure class="rv">
      <div class="m"><img src="assets/beforeafter.jpg" alt="Before and after of a commercial glass frontage, dull filmed glass above and clear glass below" loading="lazy" width="608" height="1080"></div>
      <figcaption><b>Before and after</b>Storefront glazing</figcaption>
    </figure>
  </div>
</section>"""

NEW_HTML = """<section class="reels wrap" id="reels">
  <div class="rhead rv">
    <h2>Straight from the van.</h2>
    <p class="sub">Filmed on their own jobs and posted to Instagram. Both clips play here with the sound off.</p>
  </div>

  <div class="stage">
    <figure class="bay rv" style="--pv:url(assets/poster-storefront.jpg)">
      <div class="bay-in">
        <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
        <figcaption>Commercial storefront <span>Mesa</span></figcaption>
      </div>
    </figure>
    <figure class="bay rv" style="--pv:url(assets/poster-solar.jpg)">
      <div class="bay-in">
        <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
        <figcaption>Solar array rinse <span>Tile roof</span></figcaption>
      </div>
    </figure>
  </div>

  <div class="hinge rv"><span>The same glass, one visit</span></div>
  <figure class="dip rv">
    <div class="dip-in">
      <div class="dip-g">
        <figure><img src="assets/ba-before.jpg" alt="A commercial glass frontage before cleaning, the panes hazy with dust and hard water film" loading="lazy" width="390" height="488"><figcaption>Before</figcaption></figure>
        <figure><img src="assets/ba-after.jpg" alt="The same frontage after cleaning, the panes clear and reflecting the sky" loading="lazy" width="390" height="488"><figcaption>After</figcaption></figure>
      </div>
    </div>
    <figcaption class="dcap">Storefront glazing, Mesa</figcaption>
  </figure>
</section>"""

rep(OLD_HTML, NEW_HTML, 'reels html')

# responsive: the stage collapses to one column, the plate keeps both halves
# side by side because the comparison is the entire point of it
rep("  .rgrid{grid-template-columns:1fr;max-width:400px;margin-inline:auto}",
    "  .stage{grid-template-columns:minmax(0,330px);margin-bottom:clamp(88px,17vw,120px)}", 'stage mq960')
rep("  .rgrid figure:nth-child(2),.rgrid figure:nth-child(3){transform:none}\n", "", 'drop stagger mq820')

open(p, 'w', encoding='utf-8').write(s)
print('D1 reels:', len(done), 'edits ->', ', '.join(done))
