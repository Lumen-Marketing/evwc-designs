# -*- coding: utf-8 -*-
# 02 SITE becomes a SPLIT SCREEN page.
#
# The section audit is the reason. Five of nine sections were the same two
# column shape inside the same max width container, and the same was true of the
# other three directions, which is why four different materials still read as
# one page. The answer is not to stop using two columns. It is to make the split
# the page's ARCHETYPE instead of its default: full height, edge to edge, the
# media touching the viewport rather than sitting in a gutter, the side it sits
# on changing down the page, and full width breakers so it never becomes nine
# identical halves.
#
# Stage 1 of 4: the backbone and the hero.
p = '02-site.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ------------------------------------------------------------- backbone -----
rep("""/* ---------- HERO: full bleed photograph, no container over it ---------- */""",
"""/* ---------- THE PAGE IS A SPLIT SCREEN ----------
   One backbone for the whole page. Panes are full height and edge to edge, the
   media pane runs to the viewport rather than stopping at a gutter, and the
   ratio and the side both change section to section. Breakers between runs:
   never more than two splits before something full width. */
.split{display:grid;grid-template-columns:1fr 1fr;align-items:stretch;position:relative}
.split.tall{min-height:min(94dvh,1000px)}
.split.mid{min-height:min(76dvh,800px)}
.split.w58{grid-template-columns:1.16fr .84fr}
.split.w42{grid-template-columns:.84fr 1.16fr}
.sp-copy{display:flex;flex-direction:column;justify-content:center;
  padding:clamp(54px,6.5vw,118px) clamp(24px,5vw,90px)}
.sp-copy > *{max-width:58ch}
.sp-media{position:relative;overflow:hidden;background:#000;min-height:0}
.sp-media > img,.sp-media > video{position:absolute;inset:0;width:100%;height:100%;
  object-fit:cover;display:block}
.sp-media figcaption{position:absolute;left:0;right:0;bottom:0;z-index:2;
  padding:clamp(20px,2.6vw,36px);
  background:linear-gradient(180deg,rgba(7,12,20,0),rgba(7,12,20,.92));
  font-size:14.5px;color:var(--fg-2)}
.sp-media figcaption b{display:block;font-family:'Big Shoulders Display',sans-serif;
  font-size:clamp(20px,2.2vw,30px);font-weight:800;text-transform:uppercase;
  letter-spacing:.03em;color:#fff;margin-bottom:4px}
/* the white pane: a second material meeting the first at the seam, rather than
   a white card floating on a dark ground */
.sp-copy.paper{background:var(--card);color:var(--card-ink)}
.sp-copy.paper .lede,.sp-copy.paper p{color:var(--card-muted)}
@media (max-width:900px){
  /* a split screen on a phone is one column. The media leads where the picture
     is the point, and follows where the words are. */
  .split,.split.w58,.split.w42{grid-template-columns:1fr}
  .split.tall,.split.mid{min-height:0}
  .sp-media{height:clamp(280px,64vw,440px)}
  .split.flip .sp-media{order:-1}
  .sp-copy{padding:clamp(40px,9vw,64px) var(--pad)}
}

/* ---------- HERO: the first split ---------- */""", 'backbone')

# ----------------------------------------------------------------- hero -----
rep(""".hero{position:relative;min-height:100dvh;display:flex;align-items:flex-end;overflow:hidden}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:48% 52%;z-index:0}
/* headroom for the camera push. The plate drifts inside this margin, so the
   frame edge is never exposed at either end of the travel. */
.hero>img{top:-9%;height:118%}
/* plane two: graded scrim, dark at the bottom where type sits */
.hero::after{
  content:"";position:absolute;inset:0;z-index:1;
  background:linear-gradient(178deg,rgba(7,12,20,.82) 0%,rgba(7,12,20,.18) 34%,rgba(7,12,20,.72) 74%,rgba(7,12,20,.97) 100%);
}
.hero-in{position:relative;z-index:2;width:100%;
  padding-top:calc(76px + clamp(18px,4vh,52px));   /* the nav is fixed: never let a tall headline slide under it */
  padding-bottom:var(--hero-foot)}
.hero h1{font-size:clamp(52px,10.6vw,152px);font-weight:900;letter-spacing:.002em;line-height:.84;max-width:21ch}""",
""".hero{position:relative;overflow:hidden;min-height:min(96dvh,1020px);
  display:grid;grid-template-columns:1.06fr .94fr;align-items:stretch}
.hero .sp-copy{position:relative;z-index:3;justify-content:flex-end;
  /* the nav is fixed, and the plate below hangs up into this pane, so the copy
     has to clear both ends */
  padding-top:calc(76px + clamp(26px,4vw,62px));
  padding-bottom:calc(var(--hang-climb) + clamp(46px,5vw,88px))}
.hero .sp-media > img{top:-6%;height:112%;object-position:48% 52%}
/* the scrim only has to work over the media pane now, so it can be lighter and
   the photograph survives it */
.hero .sp-media::after{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(96deg,rgba(7,12,20,.72),rgba(7,12,20,.12) 42%,rgba(7,12,20,0) 70%),
             linear-gradient(180deg,rgba(7,12,20,.42),transparent 26%,transparent 62%,rgba(7,12,20,.72))}
.hero h1{font-size:clamp(46px,5.6vw,92px);font-weight:900;letter-spacing:.002em;line-height:.86;max-width:none}""",
    'hero css')

rep(""".hero-act{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}""",
""".hero-act{display:flex;flex-wrap:wrap;gap:14px;margin-top:34px}
/* the figures run OUT of the copy pane and across the seam onto the
   photograph. Occlusion, not a shadow: one plane in front of the other is what
   makes a split read as two surfaces rather than two boxes. */
.hero .hcard{position:relative;z-index:4;margin:clamp(30px,3.6vw,50px) 0 0;
  width:calc(100% + clamp(40px,9vw,180px));max-width:none;right:auto;bottom:auto}
@media (max-width:900px){
  .hero{grid-template-columns:1fr;min-height:0}
  .hero .sp-media{height:clamp(320px,70vw,520px)}
  .hero .sp-copy{padding-top:calc(76px + clamp(26px,7vw,44px));
    padding-bottom:calc(var(--hang-climb) + clamp(34px,7vw,56px))}
  .hero .hcard{width:100%}
}""", 'hcard occlusion')

# ---------------------------------------------------------------- markup -----
rep("""<section class="hero" id="top">
  <img src="assets/restaurant.jpg" width="1400" height="1750"
       alt="A restaurant frontage looking out through a wall of cleaned glass" fetchpriority="high">
  <div class="wrap hero-in">""",
"""<section class="hero split" id="top">
  <div class="sp-copy">""", 'hero open')

rep("""      <a class="btn wire" href="sms:+14808069455"><span>Text for a quote</span></a>
    </div>
  </div>

</section>""",
"""      <a class="btn wire" href="sms:+14808069455"><span>Text for a quote</span></a>
    </div>
  </div>
  <figure class="sp-media" style="margin:0">
    <img src="assets/restaurant.jpg" width="1400" height="1750"
         alt="A restaurant frontage looking out through a wall of cleaned glass" fetchpriority="high">
  </figure>
</section>""", 'hero close')

# the hero's stat card moves into the copy pane, so it goes above the headline
# in source order only if we say so. Keep it after the buttons, where it reads.
rep("""    <!-- smoked glass card, draggable, sitting over the photograph beside the buttons -->
    <aside class="hcard smoke" id="hcard">
      <div class="k">On the route</div>
      <ul>
        <li><b>5.0</b><span>Google rating</span></li>
        <li><b>4</b><span>Google reviews</span></li>
        <li><b>7</b><span>Services offered</span></li>
        <li><b>8</b><span>East Valley towns</span></li>
      </ul>
    </aside>
    <h1>""", """    <h1>""", 'hcard out of the top')

rep("""      <a class="btn wire" href="sms:+14808069455"><span>Text for a quote</span></a>
    </div>
  </div>
  <figure class="sp-media" style="margin:0">""",
"""      <a class="btn wire" href="sms:+14808069455"><span>Text for a quote</span></a>
    </div>
    <!-- smoked glass, draggable, running out of the pane and over the photograph -->
    <aside class="hcard smoke" id="hcard">
      <div class="k">On the route</div>
      <ul>
        <li><b>5.0</b><span>Google rating</span></li>
        <li><b>4</b><span>Google reviews</span></li>
        <li><b>7</b><span>Services offered</span></li>
        <li><b>8</b><span>East Valley towns</span></li>
      </ul>
    </aside>
  </div>
  <figure class="sp-media" style="margin:0">""", 'hcard into the pane')

# the camera push now drives the pane's plate, not a full bleed background
rep("""  gsap.fromTo('.hero>img', {yPercent:-3.2, scale:1.02}, {""",
    """  gsap.fromTo('.hero .sp-media > img', {yPercent:-3.2, scale:1.02}, {""", 'motion target')

open(p, 'w', encoding='utf-8').write(s)
print('split stage 1:', len(done), 'edits ->', ', '.join(done))
