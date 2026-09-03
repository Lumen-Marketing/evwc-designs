# -*- coding: utf-8 -*-
p = 'README.md'
s = open(p, encoding='utf-8').read()

NEW = """## The work gallery (2026-09-03)

Reference layouts supplied by the client: a centre-stage photo gallery with a
pill index and arrows, and a hero holding one wide image flanked by tall
rounded slivers. Both are the same idea, one card in focus with its neighbours
receding, so all three directions now run that skeleton and none of them share
a line of it.

| | 01 Daylight | 02 Broadsheet | 03 Hazard |
|---|---|---|---|
| Falloff | `clip-path: inset()` narrows neighbours into standing slivers | `scale()` steps neighbours back, centre-origin | `scale()` from `transform-origin: 50% 100%`, so plates keep one baseline on the bench |
| Focus cue | the card is unscrimmed and throws a reflection onto the table | the card sits on its deep and cyan planes, offset straight down | hazard tape and run time appear, cyan hard offset under the plate |
| Index | outline pills | house pills, cyan when live | ruled tab strip, hazard yellow when live |
| Controls | round outline buttons | round ink buttons | one machined block, count bolted between |

Offsets are **accumulated from each step's visible width**, not multiplied by a
constant, which is the only way the gaps stay even once neighbours are narrowed
or scaled. Only `transform`, `opacity` and `clip-path` animate.

`filter: drop-shadow()` rather than `box-shadow` on direction 01: a box-shadow
follows the border box, so a card clipped down to a sliver would still cast a
full-width rectangle behind it. `drop-shadow` follows the clipped silhouette.

**Only the focused card plays.** The section-level `IntersectionObserver` cannot
be left to do this on its own: a parked clip never leaves the viewport, so no
intersection change ever fires and it would sit paused forever. The deck marks
parked clips with `data-off`, calls `play()` itself when a card takes focus, and
the section observer skips anything marked. `shots/reels.mjs` knows about this
and reports parked clips as PARK, then clicks through every index button to
prove each one actually starts.

**Below 760px the deck stops being a deck** and becomes a scroll-snap rail at
full card size. A carousel that has to be driven by arrows is the wrong control
on a touch screen.

### Two things folded in

- **The separate proof bento is gone from all three.** Every photograph it held
  is in the gallery, so it was showing the same work twice. Direction 03's
  section numbering shifted up to match.
- **`junk.jpg` was a promo graphic**, not a photograph: a JUNK REMOVAL banner, a
  CALL NOW pill and the phone number set over the job pictures. Recropped to
  `junk-yard.jpg`, centred on the divider so one portrait frame carries the
  debris on the left and the cleared corner on the right, with every banner
  outside the crop.

## Showcase rebuilt (2026-09-03)"""

old = "## Showcase rebuilt (2026-09-03)"
assert old in s
s = s.replace(old, NEW, 1)

s = s.replace(
    "the reel bays, proof frames and hero plate all got enclosures in the depth pass,",
    "the media blocks all got enclosures in the depth pass,", 1)

open(p, 'w', encoding='utf-8').write(s)
print('README updated,', len(s.splitlines()), 'lines')
