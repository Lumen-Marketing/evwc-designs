import re

def load(p):  return open(p, encoding='utf-8').read()
def save(p,s): open(p,'w',encoding='utf-8').write(s)

STAR = '<svg><use href="#i-star"/></svg>'
STARS5 = STAR*5

# =====================================================================
# D1 -- reviews as panes of glass: a photographic plane behind, lit
#       enclosures with an edge highlight, and a rating plate that
#       overlaps the quote pane the way the hero plate does.
# =====================================================================
p = '01-daylight.html'
s = load(p); n1 = 0

old_css = """/* ---------- reviews: one large, three quiet ---------- */
.rev{padding-bottom:clamp(72px,10vw,148px)}
.pull{font-family:var(--d);font-weight:600;font-size:clamp(24px,3.6vw,50px);line-height:1.14;letter-spacing:-.03em;max-width:20ch;margin:0}
.pull-by{margin-top:24px;padding:0;border:0;color:var(--fg-2);font-size:15px;font-family:var(--b);font-weight:400;letter-spacing:0}
.rmore{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(22px,3vw,52px);margin-top:clamp(48px,6vw,88px);
  padding-top:clamp(34px,4vw,52px);border-top:1px solid var(--line)}
.rmore p{margin:0;font-size:15.5px;line-height:1.62;color:#d3d7d9}
.rmore .by{margin-top:16px;color:var(--fg-2);font-size:13.5px}"""
new_css = """/* ---------- reviews: panes of glass, lit at the top edge ---------- */
.rev{position:relative;padding-bottom:clamp(72px,10vw,148px);overflow:hidden}
/* a photographic plane behind the panes so the section is never bare */
.rev::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;
  background:url(assets/storefront.jpg) center/cover no-repeat;opacity:.16;filter:grayscale(.45) contrast(1.05);
  -webkit-mask-image:radial-gradient(58% 62% at 86% 26%,#000,transparent 74%);
  mask-image:radial-gradient(58% 62% at 86% 26%,#000,transparent 74%)}
.rev>.wrap{position:relative;z-index:1}

/* the shared pane material: a lifted sheet with light catching its top edge */
.pane{position:relative;border-radius:20px;
  background:linear-gradient(166deg,rgba(255,255,255,.062),rgba(255,255,255,.014) 64%);
  box-shadow:var(--lift-2),inset 0 1px 0 rgba(255,255,255,.17),inset 0 0 0 1px rgba(255,255,255,.045);
  transition:transform .45s var(--ez-out),box-shadow .45s var(--ez-out)}
/* a single reflection sweeping across the sheet */
.pane::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:linear-gradient(112deg,transparent 26%,rgba(255,255,255,.05) 44%,transparent 58%)}
@media (hover:hover) and (pointer:fine){
  .pane:hover{transform:translateY(-4px);box-shadow:var(--lift-3),inset 0 1px 0 rgba(255,255,255,.24),inset 0 0 0 1px rgba(255,255,255,.08)}
}

.pull-wrap{position:relative;max-width:min(100%,860px)}
.pull{margin:0;padding:clamp(30px,3.6vw,56px) clamp(28px,3.4vw,52px) clamp(34px,4vw,58px);border-radius:24px}
.pull q,.pull .q{display:block;font-family:var(--d);font-weight:600;font-size:clamp(23px,3.3vw,46px);
  line-height:1.14;letter-spacing:-.03em;max-width:19ch}
.pull-by{margin-top:26px;padding:0;border:0;color:var(--fg-2);font-size:15px;font-family:var(--b);font-weight:400;letter-spacing:0}
/* the rating lifted clear of the pane, overlapping its edge */
.rating-plate{position:absolute;z-index:3;right:clamp(-4px,-.6vw,0px);bottom:clamp(-34px,-3vw,-24px);
  padding:15px 22px;border-radius:16px;background:linear-gradient(168deg,#26292b,#141618);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.1),var(--rim);
  transform:rotate(-1.8deg);transition:transform .45s var(--ez-out)}
@media (hover:hover) and (pointer:fine){.rating-plate:hover{transform:rotate(-.5deg) translateY(-4px)}}
.rating-plate .stars{margin-bottom:8px}
.rating-plate b{font-family:var(--d);font-weight:800;font-size:26px;letter-spacing:-.03em;line-height:1}
.rating-plate span{display:block;margin-top:4px;font-size:12.5px;color:var(--fg-2)}

.rmore{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(16px,1.8vw,26px);margin-top:clamp(58px,7vw,104px)}
.rmore .pane{padding:clamp(24px,2.4vw,34px)}
.rmore .pane:nth-child(2){transform:translateY(clamp(10px,1.6vw,24px))}
.rmore .pane:nth-child(3){transform:translateY(clamp(-8px,-1vw,0px))}
@media (hover:hover) and (pointer:fine){
  .rmore .pane:nth-child(2):hover{transform:translateY(clamp(4px,.8vw,16px))}
  .rmore .pane:nth-child(3):hover{transform:translateY(clamp(-14px,-1.8vw,-6px))}
}
.rmore p{margin:0;font-size:15.5px;line-height:1.62;color:#d8dcde;position:relative}
.rmore .by{margin-top:18px;color:var(--fg-2);font-size:13.5px}"""
if old_css in s: s = s.replace(old_css, new_css, 1); n1 += 1
else: print('!! D1 css MISS')

old_html = """<section class="rev wrap" id="reviews">
  <blockquote class="pull rv">“They left every window spotless, even cleaning the frames and screens to perfection.”
    <footer class="pull-by">Lacey Shultz, Google review</footer>
  </blockquote>
  <div class="rmore">
    <div class="rv"><p>“Jose from East Valley Window Cleaning is a true professional. They are polite, easy to communicate with, and make you feel confident in their honesty and reliability.”</p><p class="by">Nina Hanopol, Google</p></div>
    <div class="rv"><p>“Great job done! On time, on schedule. Windows and sliding doors look great.”</p><p class="by">Kirkland Sanders, Google</p></div>
    <div class="rv"><p>“Really great service!”</p><p class="by">Maria Sandoval, Google</p></div>
  </div>
</section>"""
new_html = """<section class="rev" id="reviews">
  <div class="wrap">
    <div class="pull-wrap rv">
      <blockquote class="pull pane">
        <span class="q">“They left every window spotless, even cleaning the frames and screens to perfection.”</span>
        <footer class="pull-by">Lacey Shultz, Google review</footer>
      </blockquote>
      <div class="rating-plate">
        <span class="stars" role="img" aria-label="Rated 5 out of 5">""" + STARS5 + """</span>
        <b>5.0</b><span>from all 4 reviews</span>
      </div>
    </div>
    <div class="rmore">
      <figure class="pane rv"><p>“Jose from East Valley Window Cleaning is a true professional. They are polite, easy to communicate with, and make you feel confident in their honesty and reliability.”</p><figcaption class="by">Nina Hanopol, Google</figcaption></figure>
      <figure class="pane rv"><p>“Great job done! On time, on schedule. Windows and sliding doors look great.”</p><figcaption class="by">Kirkland Sanders, Google</figcaption></figure>
      <figure class="pane rv"><p>“Really great service!”</p><figcaption class="by">Maria Sandoval, Google</figcaption></figure>
    </div>
  </div>
</section>"""
if old_html in s: s = s.replace(old_html, new_html, 1); n1 += 1
else: print('!! D1 html MISS')

# mobile: flatten the cascade and bring the rating plate into flow
s = s.replace("""  .rgrid figure:nth-child(2),.rgrid figure:nth-child(3){transform:none}
  .shaft{display:none}""",
"""  .rgrid figure:nth-child(2),.rgrid figure:nth-child(3){transform:none}
  .shaft{display:none}
  .rmore{grid-template-columns:1fr}
  .rmore .pane:nth-child(2),.rmore .pane:nth-child(3){transform:none}
  .rating-plate{position:relative;right:auto;bottom:auto;margin-top:18px;transform:none;display:inline-block}
  .rev::before{opacity:.1}""", 1); n1 += 1
save(p, s); print('D1 reviews:', n1, 'edits')

# =====================================================================
# D2 -- tray and core at concentric radii, matching the stat row, with
#       the featured review raised highest in sun yellow.
# =====================================================================
p = '02-broadsheet.html'
s = load(p); n2 = 0

old = """.rev{background:var(--limestone);border-radius:var(--r-card);padding:clamp(24px,2.4vw,34px);display:flex;flex-direction:column;
  box-shadow:var(--lift-1);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.rev:hover{transform:translateY(-5px);box-shadow:var(--lift-2)}
.rev.hi{background:var(--sun)}"""
new = """.rev{background:var(--pumice);border-radius:var(--r-card);padding:9px;display:flex;flex-direction:column;
  box-shadow:var(--lift-2);transition:transform .55s var(--ez),box-shadow .55s var(--ez)}
.rev .core{background:var(--limestone);border-radius:calc(var(--r-card) - 9px);padding:clamp(22px,2.2vw,30px);
  display:flex;flex-direction:column;flex:1;box-shadow:inset 0 1px 0 rgba(255,255,255,.85)}
.rev.hi{background:#e8d976}
.rev.hi .core{background:var(--sun)}
.rev:nth-child(2){transform:translateY(clamp(10px,1.5vw,22px))}
.rev:nth-child(4){transform:translateY(clamp(-12px,-1.2vw,0px))}
@media (hover:hover) and (pointer:fine){
  .rev:hover{transform:translateY(-6px);box-shadow:var(--lift-3)}
  .rev:nth-child(2):hover{transform:translateY(clamp(3px,.7vw,14px))}
  .rev:nth-child(4):hover{transform:translateY(clamp(-19px,-2vw,-7px))}
}"""
if old in s: s = s.replace(old, new, 1); n2 += 1
else: print('!! D2 css MISS')

# wrap each review body in a core
def d2_core(m):
    return ('<article class="rev%s">\n        <div class="core">%s</div></article>'
            % (m.group(1), m.group(2)))
s2, cnt = re.subn(r'<article class="rev( hi)?">\s*(<div class="stars".*?</div>)</article>',
                  lambda m: '<article class="rev%s">\n        <div class="core">%s</div></article>'
                            % (m.group(1) or '', m.group(2)),
                  s, flags=re.S)
if cnt == 4: s = s2; n2 += cnt
else: print('!! D2 markup wrapped', cnt, 'of 4')

s = s.replace("""  .stat:nth-child(2),.stat:nth-child(4),
  .reels .bay:nth-child(2),.reels .bay:nth-child(3){transform:none}""",
"""  .stat:nth-child(2),.stat:nth-child(4),
  .rev:nth-child(2),.rev:nth-child(4),
  .reels .bay:nth-child(2),.reels .bay:nth-child(3){transform:none}""", 1); n2 += 1
save(p, s); print('D2 reviews:', n2, 'edits')

# =====================================================================
# D3 -- ruled cells become bolted plates, consistent with the reel bays.
# =====================================================================
p = '03-hazard.html'
s = load(p); n3 = 0

old = """.revs{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-left:1px solid var(--line)}
.rev{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:clamp(22px,2.3vw,32px);display:flex;flex-direction:column}"""
new = """.revs{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.rev{position:relative;padding:11px;background:var(--plate);display:flex;flex-direction:column;
  box-shadow:var(--bevel),var(--hard-y),var(--cast);transition:transform .5s var(--ez),box-shadow .5s var(--ez)}
.rev::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:3;
  background-image:var(--bolts);background-repeat:no-repeat}
.rev .core{background:#0e1011;padding:clamp(20px,2.1vw,28px);display:flex;flex-direction:column;flex:1;
  box-shadow:var(--bevel-deep)}
@media (hover:hover) and (pointer:fine){
  .rev:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),18px 18px 0 rgba(252,222,88,.18),var(--cast)}
}"""
if old in s: s = s.replace(old, new, 1); n3 += 1
else: print('!! D3 css MISS')

s3, cnt = re.subn(r'<article class="rev">\s*(<div class="stars".*?</div>)</article>',
                  lambda m: '<article class="rev">\n        <div class="core">%s</div></article>' % m.group(1),
                  s, flags=re.S)
if cnt == 4: s = s3; n3 += cnt
else: print('!! D3 markup wrapped', cnt, 'of 4')
save(p, s); print('D3 reviews:', n3, 'edits')
