# -*- coding: utf-8 -*-
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---------------------------------------------------------- hero CSS -------
rep(""".hero .in{position:relative;z-index:3;width:100%;padding-block:clamp(56px,8vw,116px)}
.hero-copy{position:relative;z-index:3;max-width:min(64ch,66%)}
h1{font-size:clamp(42px,7.6vw,116px);max-width:14ch;text-shadow:0 2px 40px rgba(0,0,0,.5)}
.hero p{margin:24px 0 0;max-width:44ch;font-size:clamp(16px,1.35vw,19px);color:#d9dddf}""",
""".hero .in{position:relative;z-index:3;width:100%;padding-block:clamp(56px,8vw,116px)}
.hero-copy{position:relative;z-index:3;max-width:min(64ch,66%)}
/* a pane of frosted glass under the copy. The headline is wider than the pane
   on purpose: its second line crosses the edge and lands on the sharp footage,
   which is what makes the boundary read as a real surface. */
.glass{--gp:clamp(22px,3vw,50px);
  position:absolute;z-index:-1;pointer-events:none;
  top:calc(var(--gp) * -1);bottom:calc(var(--gp) * -1);left:calc(var(--gp) * -1);
  width:calc(84% + var(--gp) * 2);border-radius:clamp(18px,2vw,30px);
  background:linear-gradient(158deg,rgba(22,25,27,.5),rgba(12,13,14,.32));
  -webkit-backdrop-filter:blur(22px) saturate(1.18);backdrop-filter:blur(22px) saturate(1.18);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),inset 0 0 0 1px rgba(255,255,255,.06),
    0 44px 96px -46px rgba(0,0,0,.95)}
h1{font-size:clamp(42px,7.6vw,116px);max-width:none;text-shadow:0 2px 40px rgba(0,0,0,.5)}
h1 .l1,h1 .l2{display:block}
h1 .l2{white-space:nowrap}
.hero p{margin:24px 0 0;max-width:40ch;font-size:clamp(16px,1.35vw,19px);color:#d9dddf}
/* the rating sits with the copy rather than waiting for a section of its own */
.hrate{display:flex;align-items:center;gap:11px;margin:22px 0 0;font-size:14px;color:#d9dddf}
.hrate .stars{display:inline-flex;gap:2px;color:var(--acc)}
.hrate .stars svg{width:15px;height:15px}
.hrate b{font-weight:600;color:var(--fg)}
/* the town name set on its side down the edge of the frame */
.vlabel{position:absolute;z-index:3;right:calc(var(--gut) * .4);top:clamp(96px,15vh,190px);
  writing-mode:vertical-rl;font-size:12px;letter-spacing:.44em;text-transform:uppercase;
  color:rgba(242,243,243,.4);text-shadow:0 1px 14px rgba(0,0,0,.85)}""",
    'hero css')

rep("""    <div class="hero-copy">
      <h1>Crystal clear views start here.</h1>
      <p>Windows, screens, tracks, hard water, tint, solar panels and hauling across the East Valley.</p>
      <div class="acts">""",
"""    <div class="hero-copy">
      <span class="glass" aria-hidden="true"></span>
      <h1><span class="l1">Crystal clear</span><span class="l2">views start here.</span></h1>
      <p>Windows, screens, tracks, hard water, tint, solar panels and hauling across the East Valley.</p>
      <p class="hrate"><span class="stars" role="img" aria-label="Rated 5 out of 5"><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg></span><b>5.0</b> from all 4 Google reviews</p>
      <div class="acts">""", 'hero markup')

rep("""  <span class="shaft" aria-hidden="true"></span>""",
    """  <span class="shaft" aria-hidden="true"></span>
  <span class="vlabel" aria-hidden="true">East Valley Arizona</span>""", 'vlabel')

# ------------------------------------------------------- verified stats ----
rep(""".statement .lead b{font-weight:800;color:var(--acc)}""",
""".statement .lead b{font-weight:800;color:var(--acc)}
/* four figures, every one of them checkable: the Google rating and its count,
   the number of services, the towns covered, and what an estimate costs */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(10px,1.3vw,18px);
  margin-top:clamp(44px,5.4vw,78px)}
.stat{padding:7px;border-radius:20px;background:linear-gradient(168deg,#262a2c,#131517);
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.08),var(--rim);
  transition:transform .45s var(--ez-out),box-shadow .45s var(--ez-out)}
.stat .core{border-radius:13px;padding:clamp(18px,2.1vw,30px);background:var(--bg-2);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.55)}
.stat b{display:block;font-family:var(--d);font-weight:800;letter-spacing:-.045em;line-height:1;
  font-size:clamp(30px,4vw,58px)}
.stat span{display:block;margin-top:11px;font-size:13.5px;line-height:1.45;color:var(--fg-2)}
.stat .stars{display:inline-flex;gap:2px;color:var(--acc);vertical-align:middle;margin-left:4px}
.stat .stars svg{width:14px;height:14px}
@media (hover:hover) and (pointer:fine){
  .stat:hover{transform:translateY(-5px);box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.13),var(--rim)}
}""", 'stats css')

rep("""  <p class="rating">
    <span class="stars" role="img" aria-label="Rated 5 out of 5"><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg><svg><use href="#star"/></svg></span>
    5.0 on Google from all 4 reviews. Free estimates, no visit needed for most homes.
  </p>
</section>""",
"""  <div class="stats">
    <div class="stat"><div class="core"><b>5.0</b><span>On Google, from all four reviews</span></div></div>
    <div class="stat"><div class="core"><b>7</b><span>Services on one phone number</span></div></div>
    <div class="stat"><div class="core"><b>8</b><span>East Valley towns covered</span></div></div>
    <div class="stat"><div class="core"><b>Free</b><span>Estimates, most without a visit</span></div></div>
  </div>
</section>""", 'stats markup')

# ---------------------------------------------------------- responsive -----
rep("""  .hero-copy{max-width:100%}""",
"""  .hero-copy{max-width:100%}
  .glass{width:calc(100% + var(--gp) * 2);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px)}
  h1{max-width:14ch}
  h1 .l1,h1 .l2{display:inline;white-space:normal}
  .vlabel{display:none}""", 'hero mq')

rep("""  .cluster{grid-template-columns:1fr;gap:16px}""",
"""  .stats{grid-template-columns:repeat(2,1fr)}
  .cluster{grid-template-columns:1fr;gap:16px}""", 'stats mq')

open(p, 'w', encoding='utf-8').write(s)
print('premium hero:', len(done), 'edits ->', ', '.join(done))
