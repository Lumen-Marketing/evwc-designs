# -*- coding: utf-8 -*-
p = 'index.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep("Same section order in all three: <b>hero &rarr; trust &rarr; services &rarr; reels &rarr; proof &rarr; reviews &rarr; areas &rarr; CTA</b>.",
    "Same section order in all three: <b>hero &rarr; trust &rarr; services &rarr; work gallery &rarr; reviews &rarr; areas &rarr; CTA</b>.",
    'section order')
if 'work gallery' not in s:
    rep("hero → trust → services → reels → proof → reviews → areas → CTA",
        "hero → trust → services → work gallery → reviews → areas → CTA", 'section order plain')

rep("""      <tr><td>Reels</td><td>Two clips as a symmetric pair on a lit table, captions set inside the tray, before and after as one hinged plate below</td><td>Two clips with their colour planes mirrored outward, before and after as a wide plate on the centre line</td><td>Two bolted bays with mirrored hard offsets, before and after in one taped housing</td></tr>
      <tr><td>Proof</td><td>Four unequal frames on a twelve column grid</td><td>Six-column bento, pill captions</td><td>Six-column ruled bento, yellow tab captions</td></tr>""",
"""      <tr><td>Work gallery</td><td>Focused card at full width, neighbours clipped to standing slivers on a lit table, named pills above</td><td>Focused card on its stacked colour planes, neighbours stepped back by scale, house pills above</td><td>Plates on a bench scaling from the foot so the baseline holds, ruled tab strip above</td></tr>
      <tr><td>Gallery controls</td><td>Round outline buttons, count between them</td><td>Round ink buttons, Anton caption above</td><td>One machined block, back and forward bolted either side of the count</td></tr>
      <tr><td>Before and after</td><td>One hinged plate, hairline seam, AFTER in cyan</td><td>Wide plate offset straight down onto sun yellow, pill labels</td><td>One taped housing, steel and hazard-yellow tabs</td></tr>""",
    'matrix rows')

rep("Media sits in lit enclosures with diffused shadows, the two clips stand as a symmetric pair on a lit table, and everything resolves out of a blur as it enters.",
    "Media sits in lit enclosures with diffused shadows, the work gallery stands one card at full width with its neighbours clipped to slivers either side, and everything resolves out of a blur as it enters.",
    'd1 body')

rep("""<h4>The reels are real, and they really auto-play</h4>
    <p>Two clips were pulled from <b>@eastvalleywindowcleaningllc</b> and re-encoded for the web: a commercial storefront job and a rooftop solar-panel rinse. They are self-hosted MP4s, so they start on their own, loop, and stay muted. Instagram's own embed widget cannot do that. It only ever shows a cover frame with a play button.</p>""",
"""<h4>The reels are real, and they really auto-play</h4>
    <p>Two clips were pulled from <b>@eastvalleywindowcleaningllc</b> and re-encoded for the web: a commercial storefront job and a rooftop solar-panel rinse. They are self-hosted MP4s, so they start on their own, loop, and stay muted. Instagram's own embed widget cannot do that. It only ever shows a cover frame with a play button.</p>
    <p>Both clips and every job photograph live in <b>one gallery</b> per page. The card at the front plays; the ones stepped back are paused, so only one video is ever decoding. Click a card, click a name, use the arrows, press left and right, or swipe. On a phone the whole thing becomes a swipeable rail at full size.</p>""",
    'deck note')

open(p, 'w', encoding='utf-8').write(s)
print('gallery:', len(done), 'edits ->', ', '.join(done))
