# -*- coding: utf-8 -*-
p = 'README.md'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep("""| `beforeafter.jpg` | `/reel/C3j11U1Ot1i/` | **Still, not video** — see below |

Their third reel is a **static image posted as a reel**: 0.03% of pixels change
between t=1s and t=13s and every scene score is ~0. Shipping it as a looping
video with a REC badge would have implied footage that does not exist, so it runs
as a still in the third bay, badged accordingly. Check motion before assuming a
reel moves:""",
"""| `ba-before.jpg` / `ba-after.jpg` | `/reel/C3j11U1Ot1i/` | **Stills, not video** — see below |

Their third reel is a **static image posted as a reel**: 0.03% of pixels change
between t=1s and t=13s and every scene score is ~0. Shipping it as a looping
video would have implied footage that does not exist. It is a single frame
holding two photographs of one storefront, so both halves were cut out of the
720x1280 master and are shown as a matched 390x488 pair. Check motion before
assuming a reel moves:""", 'reel table')

rep("""**There is no offer running** (confirmed by the client, 2026-09-03), and nothing
on any page states one. Their before/after reel had **"20% off new customers"**
burned into the footage; it is masked out in `assets/beforeafter.jpg` with two
`drawbox` fills colour-matched to the backing wall, which leaves both photos and
the Before/After labels untouched. Their **$50 off** promo graphic is not used at
all. If an offer ever starts, add it as copy — do not un-mask the reel, the
discount in it is stale.""",
"""**There is no offer running** (confirmed by the client, 2026-09-03), and nothing
on any page states one. Their before/after reel had **"20% off new customers"**
burned into the footage, along with **"Before"** and **"After"** in a heavy sans.
All three sit outside the two crops now used (`ba-before.jpg`, `ba-after.jpg`),
so the promotion is gone rather than painted over, and the labels are set in each
direction's own type instead. Their **$50 off** promo graphic is not used at all.
If an offer ever starts, add it as copy — the discount in that post is stale.""",
    'offer note')

NEW_SECTION = """## Showcase rebuilt (2026-09-03)

The reel row in all three directions was a **three-up grid with two of the tiles
nudged out of line on the y-axis**, and the third tile held a composite image
whose baked-in Before/After labels clipped against the frame. Feedback: *"this
section like the showcase or gallery its horrible ... use other components and
style and most importantly symmetry"*. Fair. An offset that is not anchored to
anything reads as a rendering fault, not as composition.

**Registration was tried first and rejected.** A drag comparison slider is the
obvious component for a before and after, so the two photographs were tested for
alignment with a scale sweep plus phase cross-correlation on their Sobel edges
(`skimage`). Best normalised cross-correlation across the whole search was
**-0.04** — the camera moved between the two shots, so a wipe seam would have
torn the window frame in half. The pair is shown side by side instead.

Every direction now runs the same structure and none of them share a component:

| | 01 Daylight | 02 Broadsheet | 03 Hazard |
|---|---|---|---|
| Clip pair | Trays on a lit table, a ground rule fading out equally at both ends, each screen throwing a reflection onto the surface | Trays with their deep and cyan planes **mirrored outward**, left stack leaning left, right stack leaning right | Bolted plates with their hard offsets **mirrored outward**, hazard tape across each |
| Caption | Inside the tray, name left and place right | Inside the paper tray, sun-yellow pill | Ruled foot strip, condensed name and mono locator |
| Before / after | One hinged plate, two halves split by a hairline seam, labels at opposite corners with AFTER in cyan | One wide plate offset **straight down** onto sun yellow, pill labels, limestone and cyan | One taped housing, steel BEFORE tab and hazard-yellow AFTER tab |

Everything sits on one centre line. Nothing is offset on a diagonal any more:
where an offset survives it is either mirrored about that line or straight down,
so it reads as intent rather than drift.

Two things went out with it:

- The **"REC" badge with a blinking red dot** on the D3 bays and hero. Nothing
  was recording. Replaced with the clip's actual run time (`0:14`, `0:07`).
- `assets/beforeafter.jpg`, the masked composite. Deleted.

## The reels genuinely auto-play"""

rep("## The reels genuinely auto-play", NEW_SECTION, 'new section')

open(p, 'w', encoding='utf-8').write(s)
print('README:', len(done), 'edits ->', ', '.join(done))
