p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# --- 1. the plate: real photograph, thinner bezel so it stops reading as a phone,
#        3:4 to match the source rather than a hard 9:16 crop. Emil's ease-out
#        curve, a duration that is not sluggish, and hover gated off touch.
rep(""".plate{margin:0;position:absolute;z-index:4;right:var(--gut);bottom:clamp(-108px,-9vw,-64px);
  width:clamp(168px,20vw,286px);transform:rotate(-2.6deg);transition:transform .9s var(--ez)}
.plate-in{padding:9px;border-radius:22px;background:linear-gradient(168deg,#26292b,#141618);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.09),var(--rim)}
.plate-in img{width:100%;height:auto;aspect-ratio:9/16;object-fit:cover;border-radius:13px;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.5)}
.plate figcaption{margin-top:15px;text-align:right;font-size:12.5px;line-height:1.45;color:var(--fg-2);
  text-shadow:0 1px 10px rgba(0,0,0,.8)}
.plate:hover{transform:rotate(-1.4deg) translateY(-7px)}""",
""".plate{margin:0;position:absolute;z-index:4;right:var(--gut);bottom:clamp(-96px,-8vw,-56px);
  width:clamp(186px,23vw,320px);transform:rotate(-2.4deg);
  transition:transform 420ms var(--ez-out),filter 420ms var(--ez-out)}
.plate-in{padding:6px;border-radius:16px;background:linear-gradient(168deg,#2b2f31,#131517);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.11),var(--rim)}
.plate-in img{display:block;width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;
  object-position:center 34%;border-radius:10px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.55)}
.plate figcaption{margin-top:14px;text-align:right;font-size:12.5px;line-height:1.45;color:var(--fg-2);
  text-shadow:0 1px 10px rgba(0,0,0,.85)}
@media (hover:hover) and (pointer:fine){
  .plate:hover{transform:rotate(-1.2deg) translateY(-6px)}
}""", 'plate material')

rep("""    <figure class="plate">
      <div class="plate-in"><img src="assets/beforeafter.jpg" alt="Before and after of a commercial glass frontage, dull filmed glass above and clear glass below" width="608" height="1080"></div>
      <figcaption>The same frontage,<br>before and after</figcaption>
    </figure>""",
"""    <figure class="plate">
      <div class="plate-in"><img src="assets/hero-pole.jpg" alt="A water-fed pole reaching a tall arched window on a tile-roofed Arizona home against a blue sky" width="1200" height="1600"></div>
      <figcaption>Two storey residential,<br>water-fed pole</figcaption>
    </figure>""", 'plate image')

# --- 2. emil's exact strong ease-out
rep("--ez-out:cubic-bezier(.16,1,.3,1);", "--ez-out:cubic-bezier(.23,1,.32,1);", 'ease-out curve')

# --- 3. reshuffle the image slots so the pole is not used twice and nothing
#        prominent repeats. Every asset now has one clear home.
rep("""  <img src="assets/hero-pole.jpg" alt="A water-fed pole reaching a tall arched window on a tile-roofed Arizona home against a blue sky" loading="lazy" width="1200" height="1600">
  <figcaption>Two storey residential, water-fed pole</figcaption>""",
"""  <img src="assets/restaurant.jpg" alt="Looking out through a spotless full height restaurant window onto an Arizona parking lot" loading="lazy" width="1400" height="1750">
  <figcaption>Restaurant frontage, interior and exterior glass</figcaption>""", 'band image')

rep("""      <figure class="pa rv"><img src="assets/restaurant.jpg" alt="Looking out through a spotless full height restaurant window onto an Arizona parking lot" loading="lazy" width="1400" height="1750"></figure>
      <figure class="pb rv"><img src="assets/storefront.jpg" alt="A clean glass shopfront with door and window signage" loading="lazy" width="1200" height="1200"></figure>
      <figure class="pc rv"><img src="assets/junk.jpg" alt="A backyard before and after being cleared of debris" loading="lazy" width="1024" height="1024"></figure>
      <figure class="pd rv"><img src="assets/rig.jpg" alt="The work vehicle with a ladder racked on the roof at sunset" loading="lazy" width="1200" height="1200"></figure>""",
"""      <figure class="pa rv"><img src="assets/storefront.jpg" alt="A clean glass shopfront with door and window signage" loading="lazy" width="1200" height="1200"></figure>
      <figure class="pb rv"><img src="assets/junk.jpg" alt="A backyard before and after being cleared of debris" loading="lazy" width="1024" height="1024"></figure>
      <figure class="pc rv"><img src="assets/rig.jpg" alt="The work vehicle with a ladder racked on the roof at sunset" loading="lazy" width="1200" height="1200"></figure>
      <figure class="pd rv"><img src="assets/beforeafter.jpg" alt="Before and after of a commercial glass frontage, dull filmed glass above and clear glass below" loading="lazy" width="608" height="1080"></figure>""",
    'proof images')

# the before/after is 9:16, so give its frame a ratio that does not crop it apart
rep(".pd{grid-column:span 7;aspect-ratio:16/10}",
    ".pd{grid-column:span 7;aspect-ratio:16/10}\n.pd img{object-position:center 42%}", 'pd crop')

# reviews backdrop: no third-party signage legible once blurred, and it frees the pole
rep("  background:url(assets/hero-pole.jpg) center 30%/cover no-repeat;opacity:.2;filter:grayscale(.3) blur(3px);",
    "  background:url(assets/storefront.jpg) center 40%/cover no-repeat;opacity:.17;filter:grayscale(.45) blur(5px);",
    'reviews backdrop')

open(p, 'w', encoding='utf-8').write(s)
print('plate swap:', len(done), 'edits ->', ', '.join(done))
