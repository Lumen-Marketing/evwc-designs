# -*- coding: utf-8 -*-
# Stage 2 of 4: the three service chapters.
#
# Two of them become full height splits on opposite sides of the seam. The
# third does NOT: three image-and-text splits in a row is the zigzag every
# templated page ships, so Property becomes a full bleed band with the copy
# standing on the photograph. Two splits, then a breaker.
p = '02-site.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------------ CSS -----
rep(""".chap{position:relative;padding-block:clamp(40px,4.8vw,72px);overflow:hidden}""",
"""/* ---------- SERVICE CHAPTERS ----------
   Two splits on opposite sides, then a full bleed band. The band is not a
   stylistic whim: three image-and-text splits in a row is the zigzag that every
   templated page ships, and the third one is where a reader stops seeing the
   composition and starts seeing the pattern. */
.chap{position:relative;overflow:hidden}
.chap h3{font-size:clamp(38px,4.4vw,72px);letter-spacing:.002em;line-height:.92}
.chap .lede{margin-top:18px}
/* the band: the picture is the ground, the copy stands on it */
.band-chap{position:relative;overflow:hidden;min-height:min(80dvh,860px);
  display:flex;align-items:flex-end}
.band-chap > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  object-position:50% 46%;z-index:0}
.band-chap::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(180deg,rgba(7,12,20,.72),rgba(7,12,20,.24) 30%,rgba(7,12,20,.5) 62%,rgba(7,12,20,.96)),
             linear-gradient(90deg,rgba(7,12,20,.78),rgba(7,12,20,.1) 52%,transparent)}
.band-in{position:relative;z-index:2;width:100%;
  padding:clamp(60px,8vw,130px) 0 clamp(48px,6vw,96px)}
.band-in .chap-txt{max-width:52ch}
@media (max-width:900px){
  .band-chap{min-height:0}
  .band-in{padding:clamp(280px,58vw,380px) 0 clamp(40px,8vw,60px)}
}""", 'chap css')

# the old chapter grid is gone; keep only what the copy blocks still need
for dead, label in [
 (""".chap-in{position:relative;z-index:2;width:100%;display:grid;""", 'chap-in'),
 (""".chap.r .chap-in{grid-template-columns:minmax(0,1.02fr) minmax(0,1fr)}""", 'chap.r'),
 (""".chap.l .chapshot{order:2}""", 'order l'),
 (""".chap.r .chap-txt{order:2}""", 'order r'),
 (""".chap.r .lede{margin-left:auto}""", 'lede r'),
 (""".chap.r .jobs{text-align:right}""", 'jobs r'),
]:
    if dead in s:
        # drop the whole declaration line, wherever it wraps to
        i = s.index(dead)
        j = s.index('}\n', i) + 2
        s = s[:i] + s[j:]
        done.append('dropped ' + label)

rep(""".chap h3{font-size:clamp(40px,6.4vw,88px);letter-spacing:.002em}
.chap .lede{margin-top:18px}
""", "", 'old chap type')

# ---------------------------------------------------------------- markup -----
start = s.index('<section id="services">')
end = s.index('<!-- ============ STATEMENT ============ -->')
NEW = """<section id="services">
  <!-- copy left, glass right -->
  <div class="chap split w58 mid">
    <div class="sp-copy">
      <div class="chap-txt rv">
        <h3>Glass</h3>
        <p class="lede">Windows in and out, screens, tracks and hard water stains. Streak-free on homes and businesses, single storey to multi-storey.</p>
        <div class="jobs">
          <div>Interior and exterior windows, homes and businesses</div>
          <div>Purified water and a water-fed pole where the height calls for it</div>
          <div>Screens pulled, washed and re-set</div>
          <div>Sills and sliding tracks vacuumed and scrubbed out</div>
          <div>Mineral etching from sprinkler overspray cut back off the glass</div>
        </div>
      </div>
    </div>
    <figure class="sp-media rv" style="margin:0">
      <img src="assets/storefront.jpg" width="1200" height="1200" loading="lazy"
           alt="Clean commercial storefront glazing at street level">
    </figure>
  </div>

  <!-- the seam changes sides: panels left, copy right -->
  <div class="chap split w42 mid flip">
    <figure class="sp-media rv" style="margin:0">
      <img src="assets/job-solar-sky.jpg" width="540" height="960" loading="lazy"
           alt="A rooftop solar array under open sky after cleaning">
    </figure>
    <div class="sp-copy">
      <div class="chap-txt rv">
        <h3>Film<br>and panels</h3>
        <p class="lede">UV and privacy film, and solar arrays washed back to output. Two jobs the same van already carries the water for.</p>
        <div class="jobs">
          <div>UV and heat film to protect furnishings and hold the AC in</div>
          <div>Reflective film for privacy</div>
          <div>Dust and hard water film lifted off panels</div>
          <div>The array stops losing output to grime</div>
        </div>
      </div>
    </div>
  </div>

  <!-- the breaker. No seam at all: the picture is the whole ground. -->
  <div class="chap band-chap">
    <img src="assets/job-haul.jpg" width="820" height="1094" loading="lazy"
         alt="Monsoon debris and a cleared-out load stacked in a yard ready to haul">
    <div class="band-in wrap">
      <div class="chap-txt rv">
        <h3>Property</h3>
        <p class="lede">Pressure washing, plus junk and monsoon debris hauled away. The rest of the exterior, while the van is already at the kerb.</p>
        <div class="jobs">
          <div>Driveways, walkways and patios brought back to colour</div>
          <div>Building exteriors and elevations washed down</div>
          <div>Monsoon debris cleared</div>
          <div>Rental clear-outs and listing prep loaded and taken away</div>
        </div>
      </div>
    </div>
  </div>
</section>

"""
s = s[:start] + NEW + s[end:]
done.append('chapters markup')

# the shutter animation pointed at .chapshot, which no longer exists
rep("""  gsap.utils.toArray('.chapshot').forEach(function(f){""",
    """  gsap.utils.toArray('.chap .sp-media').forEach(function(f){""", 'shutter target')

open(p, 'w', encoding='utf-8').write(s)
print('split stage 2:', len(done), 'edits ->', ', '.join(done))
