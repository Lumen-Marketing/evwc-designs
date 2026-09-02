p = '03-hazard.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

NOISE = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='170' height='170'%3E"
         "%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4' "
         "stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='170' height='170' filter='url(%23g)' "
         "opacity='.55'/%3E%3C/svg%3E\")")

BOLT = ("radial-gradient(circle 3.6px at 12px 12px,#7c8288 0 52%,#0a0b0c 58%,transparent 62%),"
        "radial-gradient(circle 3.6px at calc(100% - 12px) 12px,#7c8288 0 52%,#0a0b0c 58%,transparent 62%),"
        "radial-gradient(circle 3.6px at 12px calc(100% - 12px),#7c8288 0 52%,#0a0b0c 58%,transparent 62%),"
        "radial-gradient(circle 3.6px at calc(100% - 12px) calc(100% - 12px),#7c8288 0 52%,#0a0b0c 58%,transparent 62%)")

# 1 -- machined tokens. Industrial depth is bevels and hard offsets, not soft blur.
rep("""  --d:'Saira Condensed',"Arial Narrow",sans-serif;
  --m:'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
}""",
"""  --d:'Saira Condensed',"Arial Narrow",sans-serif;
  --m:'JetBrains Mono',ui-monospace,'SFMono-Regular',Menlo,monospace;
  --ez:cubic-bezier(.32,.72,0,1);
  /* machined surfaces: a light top edge and a dark bottom edge read as bevel */
  --bevel:inset 0 1px 0 rgba(255,255,255,.13), inset 0 -1px 0 rgba(0,0,0,.85);
  --bevel-deep:inset 0 2px 3px rgba(0,0,0,.75), inset 0 -1px 0 rgba(255,255,255,.06);
  --plate:linear-gradient(180deg,#202326 0%,#17191b 42%,#121416 100%);
  --hard-y:14px 14px 0 rgba(252,222,88,.14);
  --hard-c:10px 10px 0 rgba(18,196,222,.16);
  --cast:0 26px 54px -26px #000;
  --bolts:""" + BOLT + """;
}
/* grain: fixed, pointer-events none */
body::after{content:"";position:fixed;inset:0;z-index:70;pointer-events:none;opacity:.06;
  background-image:""" + NOISE + "}", 'machined tokens')

# 2 -- hero: deeper grid, light falloff, extruded headline
rep(""".hmain::before{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:64px 64px;opacity:.34}""",
""".hmain::before{content:"";position:absolute;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px),
    linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:16px 16px,16px 16px,64px 64px,64px 64px;opacity:.5;
  -webkit-mask-image:radial-gradient(88% 74% at 26% 34%,#000 12%,transparent 78%);
  mask-image:radial-gradient(88% 74% at 26% 34%,#000 12%,transparent 78%)}
.hmain::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:radial-gradient(58% 46% at 22% 26%,rgba(252,222,88,.05),transparent 70%)}""", 'hero grid depth')

rep("""h1{font-size:clamp(46px,7.2vw,104px);letter-spacing:-.015em}""",
"""h1{font-size:clamp(46px,7.2vw,104px);letter-spacing:-.015em;
  text-shadow:3px 3px 0 rgba(18,196,222,.2),7px 7px 0 rgba(18,196,222,.08),0 18px 40px rgba(0,0,0,.6)}""", 'headline extrusion')

# 3 -- the hero video becomes a plate bolted to the page
rep(""".hvid{position:relative;border:1px solid var(--line);background:#000}
.hvid video{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.hvid .tape{position:absolute;top:0;left:0;right:0;height:8px;background:repeating-linear-gradient(-45deg,var(--yellow) 0 10px,#0b0b0c 10px 20px)}
.hvid .cap{display:flex;justify-content:space-between;gap:12px;padding:11px 14px;border-top:1px solid var(--line);font-family:var(--m);font-size:10.5px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--grey)}""",
""".hvid{position:relative;padding:13px;background:var(--plate);
  box-shadow:var(--bevel),var(--hard-y),var(--cast);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.hvid::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
  background-image:var(--bolts);background-repeat:no-repeat}
.hvid:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),18px 18px 0 rgba(252,222,88,.18),var(--cast)}
.hvid-core{position:relative;background:#000;box-shadow:var(--bevel-deep),0 0 0 1px #000}
.hvid video{width:100%;aspect-ratio:16/10;object-fit:cover;display:block}
.hvid .tape{position:absolute;top:0;left:0;right:0;height:8px;z-index:3;background:repeating-linear-gradient(-45deg,var(--yellow) 0 10px,#0b0b0c 10px 20px);box-shadow:0 2px 5px rgba(0,0,0,.85)}
.hvid .cap{display:flex;justify-content:space-between;gap:12px;padding:12px 4px 2px;font-family:var(--m);font-size:10.5px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:var(--grey)}""",
    'hero plate')

rep("""      <div class="hvid">
        <div class="tape"></div>
        <span class="rec"><i></i>Rec</span>
        <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Crew cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video>
        <div class="cap"><span>Commercial storefront · Mesa</span><b>Water-fed pole</b></div>
      </div>""",
"""      <div class="hvid">
        <div class="hvid-core">
          <div class="tape"></div>
          <span class="rec"><i></i>Rec</span>
          <video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront-wide.jpg" aria-label="Crew cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront-wide.mp4" type="video/mp4"></video>
        </div>
        <div class="cap"><span>Commercial storefront, Mesa</span><b>Water-fed pole</b></div>
      </div>""", 'hero plate markup')

# 4 -- spec table reads as a machined strip
rep(""".hspecs{display:flex;flex-wrap:wrap;gap:0;margin-top:34px;border:1px solid var(--line)}""",
""".hspecs{display:flex;flex-wrap:wrap;gap:0;margin-top:34px;border:1px solid var(--line);
  background:var(--plate);box-shadow:var(--bevel),0 14px 30px -18px #000}""", 'spec strip')

# 5 -- trust strip plated
rep(""".strip{display:grid;grid-template-columns:repeat(5,1fr);border-bottom:1px solid var(--line)}""",
""".strip{display:grid;grid-template-columns:repeat(5,1fr);border-bottom:1px solid var(--line);
  background:var(--plate);box-shadow:var(--bevel)}""", 'strip plated')

# 6 -- service cells recessed, raising on hover
rep(""".svc article{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:clamp(22px,2.4vw,34px);position:relative;transition:background .18s}
.svc article:hover{background:var(--steel)}""",
""".svc article{border-right:1px solid var(--line);border-bottom:1px solid var(--line);padding:clamp(22px,2.4vw,34px);position:relative;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.035);transition:background .4s var(--ez),transform .5s var(--ez),box-shadow .5s var(--ez);z-index:1}
.svc article:hover{background:var(--steel);transform:translate(-2px,-2px);z-index:2;
  box-shadow:var(--bevel),8px 8px 0 rgba(252,222,88,.13),0 18px 34px -20px #000}
.svc .ic{box-shadow:var(--bevel-deep)}""", 'service recess')
rep(""".svc .wide{grid-column:span 2;background:var(--steel)}""",
""".svc .wide{grid-column:span 2;background:var(--plate);box-shadow:var(--bevel)}""", 'wide cell plate')

# 7 -- reel bays become bolted plates
rep(""".bay{border:1px solid var(--line);background:var(--steel);position:relative}
.bay .vid{position:relative;aspect-ratio:9/16;background:#000;border-bottom:1px solid var(--line)}""",
""".bay{border:0;padding:11px;background:var(--plate);position:relative;
  box-shadow:var(--bevel),var(--hard-c),var(--cast);transition:transform .7s var(--ez),box-shadow .7s var(--ez)}
.bay::before{content:"";position:absolute;inset:0;pointer-events:none;z-index:4;
  background-image:var(--bolts);background-repeat:no-repeat}
.bay:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),14px 14px 0 rgba(18,196,222,.2),var(--cast)}
.bay .vid{position:relative;aspect-ratio:9/16;background:#000;box-shadow:var(--bevel-deep),0 0 0 1px #000}""",
    'reel plates')
rep(""".bay .ft{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px 15px}""",
""".bay .ft{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:13px 4px 2px}""", 'bay footer')

# 8 -- proof frames become plates too
rep(""".proof figure{margin:0;position:relative;overflow:hidden;border:1px solid var(--line)}""",
""".proof figure{margin:0;position:relative;overflow:hidden;border:1px solid var(--line);
  box-shadow:var(--bevel),0 20px 44px -26px #000;transition:transform .6s var(--ez),box-shadow .6s var(--ez)}
.proof figure:hover{transform:translate(-3px,-3px);box-shadow:var(--bevel),10px 10px 0 rgba(252,222,88,.14),0 24px 48px -26px #000}""",
    'proof plates')

# 9 -- area panel and CTA band plated
rep(""".azwrap{border:1px solid var(--line);padding:clamp(26px,3.4vw,50px);display:grid;place-items:center;background:var(--steel)}""",
""".azwrap{border:1px solid var(--line);padding:clamp(26px,3.4vw,50px);display:grid;place-items:center;
  background:var(--plate);box-shadow:var(--bevel),var(--hard-y),var(--cast)}""", 'area plate')
rep(""".ctaband{border:1px solid var(--line);background:var(--steel);position:relative}""",
""".ctaband{border:1px solid var(--line);background:var(--plate);position:relative;
  box-shadow:var(--bevel),0 30px 64px -34px #000}""", 'cta plate')

# 10 -- button press physics
rep(""".b1{background:var(--yellow);color:#000}
.b1:hover{background:var(--cyan);transform:translate(-2px,-2px);box-shadow:4px 4px 0 var(--yellow)}""",
""".b1{background:var(--yellow);color:#000;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),4px 4px 0 rgba(0,0,0,.55)}
.b1:hover{background:var(--cyan);transform:translate(-3px,-3px);box-shadow:inset 0 1px 0 rgba(255,255,255,.55),7px 7px 0 var(--yellow)}
.b1:active{transform:translate(0,0);box-shadow:inset 0 2px 4px rgba(0,0,0,.4),2px 2px 0 rgba(0,0,0,.5)}""",
    'button physics')

# 11 -- mobile: hard offsets shrink so nothing spills
rep("""@media (max-width:560px){
  .svc,.revs{grid-template-columns:1fr}""",
"""@media (max-width:860px){
  :root{--hard-y:7px 7px 0 rgba(252,222,88,.14);--hard-c:6px 6px 0 rgba(18,196,222,.16)}
}
@media (max-width:560px){
  .svc,.revs{grid-template-columns:1fr}""", 'mobile offsets')

open(p, 'w', encoding='utf-8').write(s)
print('D3 depth pass:', len(done), 'edits ->', ', '.join(done))
