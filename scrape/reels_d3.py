# -*- coding: utf-8 -*-
p = '03-hazard.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

OLD_CSS = """/* reels */
.reels{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.bay{border:0;padding:11px;background:var(--plate);position:relative;
  box-shadow:var(--bevel),var(--hard-c),var(--cast);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.bay::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
  background-image:var(--bolts);background-repeat:no-repeat}
.bay:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),14px 14px 0 rgba(18,196,222,.2),var(--cast)}
.bay .vid{position:relative;aspect-ratio:9/16;background:#000;box-shadow:var(--bevel-deep),0 0 0 1px #000}
.bay video,.bay .vid img{width:100%;height:100%;object-fit:cover}
.stillpill{position:absolute;top:20px;right:14px;z-index:2;background:var(--yellow);color:#000;padding:5px 10px;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase}
.bay .tape{position:absolute;top:0;left:0;right:0;height:7px;background:repeating-linear-gradient(-45deg,var(--yellow) 0 9px,#0b0b0c 9px 18px);z-index:2}
.bay .ft{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px 4px 2px}
.bay .ft b{font-family:var(--d);font-weight:700;font-size:19px;text-transform:uppercase;letter-spacing:.01em}
.bay .ft span{font-family:var(--m);font-size:9.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--grey)}"""

NEW_CSS = """/* reels: the bench.
   Two machined bays of equal size on one baseline, their hard offsets mirrored
   outward so the pair reads as one symmetric assembly, then the before and
   after bolted into a single wide plate on the same centre line. */
.rstage{--bay:clamp(174px,21.5vw,300px);display:grid;
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
/* a run time, which is true of the clip, rather than a decorative status light */
.dur{position:absolute;top:20px;right:14px;z-index:2;background:rgba(11,11,12,.82);color:var(--white);
  padding:5px 10px;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.2em;
  font-variant-numeric:tabular-nums}
.tape{position:absolute;top:0;left:0;right:0;height:7px;z-index:2;
  background:repeating-linear-gradient(-45deg,var(--yellow) 0 9px,#0b0b0c 9px 18px)}
.ft{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px 4px 2px}
.ft b{font-family:var(--d);font-weight:700;font-size:19px;text-transform:uppercase;letter-spacing:.01em}
.ft span{font-family:var(--m);font-size:9.5px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--grey)}

/* the record plate: two panes bolted into one housing, split by a steel gap */
.ba{position:relative;margin:0 auto;max-width:clamp(292px,53vw,648px);padding:11px;padding-top:18px;
  background:var(--plate);box-shadow:var(--bevel),var(--hard-y),var(--cast)}
.ba::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
  background-image:var(--bolts);background-repeat:no-repeat}
.ba-g{display:grid;grid-template-columns:1fr 1fr;gap:11px}
.ba-g figure{margin:0;position:relative;aspect-ratio:4/5;background:#000;overflow:hidden;
  box-shadow:var(--bevel-deep),0 0 0 1px #000}
.ba-g img{width:100%;height:100%;object-fit:cover;filter:saturate(.94) contrast(1.05)}
.ba-g figcaption{position:absolute;left:0;bottom:0;z-index:3;background:var(--steel2);color:var(--white);
  padding:8px 14px;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.22em;
  text-transform:uppercase;box-shadow:var(--bevel)}
.ba-g figure+figure figcaption{left:auto;right:0;background:var(--yellow);color:#000}"""

rep(OLD_CSS, NEW_CSS, 'reels css')

# the blinking red dot claimed a live recording that is not happening
rep(""".rec{position:absolute;top:20px;right:14px;display:inline-flex;align-items:center;gap:7px;background:rgba(11,11,12,.8);padding:5px 10px;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase}
.rec i{width:7px;height:7px;background:#ff3b3b;border-radius:50%;animation:bl 1.6s steps(1,end) infinite}
""", "", 'drop rec badge')

OLD_HTML = """    <div class="reels">
      <div class="bay">
        <div class="vid"><div class="tape"></div><span class="rec"><i></i>Rec</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
        <div class="ft"><b>Storefront</b><span>Mesa / Exterior</span></div>
      </div>
      <div class="bay">
        <div class="vid"><div class="tape"></div><span class="rec"><i></i>Rec</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
        <div class="ft"><b>Solar rinse</b><span>Tile roof</span></div>
      </div>
      <div class="bay">
        <div class="vid"><div class="tape"></div><span class="stillpill">Still</span>
          <img src="assets/beforeafter.jpg" alt="Before and after of a commercial glass frontage, dull filmed glass above and clear glass below" loading="lazy" width="608" height="1080"></div>
        <div class="ft"><b>Before / after</b><span>Glazing</span></div>
      </div>
    </div>"""

NEW_HTML = """    <div class="rstage">
      <figure class="bay l">
        <div class="vid"><div class="tape"></div><span class="dur">0:14</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
        <figcaption class="ft"><b>Storefront</b><span>Mesa / Exterior</span></figcaption>
      </figure>
      <figure class="bay r">
        <div class="vid"><div class="tape"></div><span class="dur">0:07</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
        <figcaption class="ft"><b>Solar rinse</b><span>Tile roof</span></figcaption>
      </figure>
    </div>
    <figure class="ba">
      <div class="tape"></div>
      <div class="ba-g">
        <figure><img src="assets/ba-before.jpg" alt="A commercial glass frontage before cleaning, the panes hazy with dust and hard water film" loading="lazy" width="390" height="488"><figcaption>Before</figcaption></figure>
        <figure><img src="assets/ba-after.jpg" alt="The same frontage after cleaning, the panes clear and reflecting the sky" loading="lazy" width="390" height="488"><figcaption>After</figcaption></figure>
      </div>
      <figcaption class="ft"><b>Same glazing, one visit</b><span>Mesa / Commercial</span></figcaption>
    </figure>"""

rep(OLD_HTML, NEW_HTML, 'reels html')

rep("""      <p>Straight off their Instagram. Two clips playing muted on loop, plus a before and after.</p>""",
    """      <p>Straight off their Instagram. Both clips play muted on loop, with the before and after bolted in underneath.</p>""",
    'sub copy')

rep("  .reels{grid-template-columns:1fr;max-width:390px;margin-inline:auto}",
    "  .rstage{grid-template-columns:minmax(0,300px);gap:clamp(38px,9vw,60px);margin-bottom:clamp(56px,11vw,88px)}",
    'stage mq')

open(p, 'w', encoding='utf-8').write(s)
print('D3 reels:', len(done), 'edits ->', ', '.join(done))
