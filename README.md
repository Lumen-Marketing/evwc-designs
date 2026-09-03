# East Valley Window Cleaning — homepage directions

Three industrial homepage directions for **East Valley Window Cleaning LLC**
(Mesa / San Tan Valley, AZ). Owner **Jose Sandoval**, **480-806-9455**,
[@eastvalleywindowcleaningllc](https://www.instagram.com/eastvalleywindowcleaningllc/).

**Live:** https://lumen-marketing.github.io/evwc-designs/

| | |
|---|---|
| `index.html` | Gallery chooser — live scaled iframe previews, Desktop/Mobile toggle |
| `01-daylight.html` | **Daylight** - container-less, full-bleed photography |
| `02-broadsheet.html` | **Broadsheet** — light limestone poster, architectural type |
| `03-hazard.html` | **Hazard** — black + hazard yellow site signage |
| `assets/` | Their real photos and re-encoded reels |
| `scrape/` | The Instagram extraction scripts (see below) |
| `shots/` | Headless-Chrome verification harness |

Homepages only, as asked. Each direction is a **standalone file** — same section
order, zero shared components. `index.html` is the chooser and nothing else: three
live previews with a tier chip and a short note each, then the footer. The
build-notes column and the section-by-section comparison table that used to sit
under them were cut on 2026-09-03 — the client is choosing a homepage, not
reading a spec.

---

## Direction 01 was rebuilt (2026-09-03)

The first version of direction 01 ("Control Room") was rejected by the client as
generic AI output, correctly. It was audited against the `design-taste-frontend`
anti-slop rules and failed on ten counts:

- dark navy plus cyan **outer glows** on buttons and the CTA panel
- **seven identical icon-in-a-rounded-square cards** in an equal 4-column grid
- **six numbered eyebrows** (`01 - Capabilities`, `02 - On the job`, ...) against
  a cap of `ceil(sections / 3)`
- **div-built fake monitor chrome** (three dots, `CAM 01`, a telemetry strip),
  which is the single most recognisable AI tell
- **"LIVE FEED" badges with pulsing red dots** on pre-recorded clips, which was
  also simply untrue
- middle-dot chains, em-dashes throughout, Manrope as the safe default grotesk,
  a centered glowing CTA, and photos shrunk into small rounded cards

Underneath all of it, "control room" was a crypto-dashboard concept bolted onto a
window cleaner. It described nothing about the business.

**`01-daylight.html`** replaces it. The concept is the only thing this business
actually sells: glass, at scale. There are no cards, no borders, no badges and no
fake UI anywhere on the page. Footage runs edge to edge behind the headline, the
services are three named groups of large type instead of an icon grid, and a
neutral off-black lets the photography carry the colour. The logo turquoise is
the single locked accent, used for actions only.

Type is Bricolage Grotesque 800 with Instrument Sans. Dials: variance 8, motion 5,
density 2, deliberately the inverse of direction 03 so that two dark pages read as
completely different things (03 is a dense ruled document, 01 is sparse and
cinematic).

The em-dash sweep was applied to all three directions and the gallery, not just 01.

## Depth pass (2026-09-03)

The client's second note was that all three read flat and the heroes were boring.
Fair: every hero was the same structural idea (type on one plane, media on
another, nothing overlapping), and direction 02 was flat because the Caldera
reference it derives from is explicitly shadowless.

Each direction now has its **own** depth device rather than the same trick three
times:

| | Depth language | Hero device |
|---|---|---|
| 01 Daylight | Layered planes, occlusion, diffused ambient lift | Footage, a shaft of light, and a before-and-after plate lifted above both and hung across the section edge |
| 02 Broadsheet | Offset colour planes, concentric tray-and-core radii | Halftone lapping over the headline, media slab on two offset planes, review card hung across the boundary |
| 03 Hazard | Machined bevels, corner bolts, hard accent offsets | Footage bolted on as a steel plate, extruded headline, two-scale construction grid |

Shared rules kept from `high-end-visual-design`, adapted rather than copied (its
glassmorphic SaaS look would have walked straight back into slop):

- shadows are always **tinted to the page**, never neutral black, and always
  large-radius diffused rather than tight and harsh
- containers are **nested** (outer tray, inner core, mathematically smaller radius)
- scroll entry resolves out of `blur()` on a custom cubic-bezier, driven by
  IntersectionObserver, never a scroll listener
- grain lives on a single `position:fixed; pointer-events:none` layer
- everything animates `transform` and `opacity` only

**Gotcha worth remembering:** an `<img>` with an HTML `height` attribute ignores
`aspect-ratio`, because the attribute is a presentational hint and `aspect-ratio`
only applies when height is `auto`. The hero plate rendered 1080px tall until
`height:auto` was added. Anywhere else on these pages the images carry an explicit
`height:100%`, which is why it only bit once.

## Hero plate replaced (2026-09-03)

The client rejected the before/after image in direction 01's hero plate. The
cause was self-inflicted: masking the stale "20% off" out of that reel left
roughly a third of the frame as flat dead brown, and its baked-in Before/After
labels are set in a heavy sans that clashes with Bricolage Grotesque. It survives
at thumbnail size in the reel wall but not enlarged in the hero, where it reads as
a pasted screenshot.

Replaced with `assets/plate-pole.jpg`, a **dedicated tight crop** cut from the
original 1440x1920 source: the brush head on the glass with water running down,
the yellow pole, blue sky. Bright and saturated against the dark orange interior
footage behind it, so the plate now pops instead of muddying. The bezel was
thinned from 9px to 6px with a smaller inner radius so it reads as a photographic
print rather than a phone mockup, and the hover was cut from 900ms to 420ms on
Emil's strong ease-out curve and gated behind `(hover:hover) and (pointer:fine)`.

Cutting a fresh crop rather than reusing `hero-pole.jpg` directly matters: the
band below it used that file as a wide architectural shot. The plate is a
tight detail of the same job, which reads as detail-then-context rather than as a
duplicate.

**Lesson:** an image that works at 300px does not necessarily work at 900px.
Anything with baked-in text or masked-out regions should stay small.

## Reviews depth pass (2026-09-03)

He then pointed at the reviews block: it still read flat. He was right, and the
cause was an inconsistency inside each page rather than a missing effect. On 01
the media blocks all got enclosures in the depth pass,
and the reviews got nothing at all, so it was the only block on the page with no
material. Same on 03, where reviews were still plain ruled cells while the reel
bays had become plates.

Fixed in each direction's own language rather than by adding testimonial cards:

- **01 Daylight** - reviews are now panes of glass, which is the product. A lifted
  sheet with light catching the top edge, one reflection sweeping across it, an
  out-of-focus photographic plane behind the section, and the 5.0 rating on a
  small plate that overlaps the quote pane the way the hero plate overlaps the
  fold. Three smaller panes stagger below.
- **02 Broadsheet** - trays holding cores at concentric radii, matching the stat
  row so the page reads as one system, cascaded on the z-axis with the featured
  review raised highest in sun yellow.
- **03 Hazard** - the ruled cells became bolted plates with recessed cores,
  bevels, corner bolts and a hard yellow offset, consistent with the reel bays.

Craft rules applied from `emil-design-eng`: no `transition: all`, exact properties
only, custom cubic-bezier curves rather than the built-ins, hover effects gated
behind `@media (hover:hover) and (pointer:fine)` so touch devices do not fire them
on tap, and a short stagger between panes.

**Gotcha:** direction 01 defines its star sprite as `#star` while 02 and 03 use
`#i-star`. The shared patch script emitted `#i-star` everywhere, so 01's new
rating plate rendered five invisible SVGs. Check the sprite id per file. A second
one right after it: `.rating-plate span` beat `.stars` on specificity and turned
the stars grey, so the accent colour needed restating at the more specific
selector.

## Three tiers: basic, standard, premium (2026-09-03)

The chooser now presents the three as a ladder rather than three flavours. The
ladder is **how much bespoke work is in the build**, not how much content the
page holds, because that is what actually costs money:

| Tier | Direction | Why it sits there |
|---|---|---|
| **Basic** | 02 Broadsheet | Conventional patterns done well: a card grid, a poster hero, a stat row. Quickest to build, easiest for anyone to extend later. |
| **Standard** | 03 Hazard | A designed system rather than a set of cards: a ruled construction grid, bolted plates, a picture strip and a machined control block, all from one rule set. |
| **Premium** | 01 Daylight | Full-bleed footage, a pane of frosted glass the headline crosses, a bespoke gallery engine, service rows that text a quote. The most custom engineering. |

Filenames did not change, so any link already sent still works. The chooser is
re-ordered and the comparison table's columns follow it. The tier chip itself
is the ladder: outline, cyan outline, cyan filled.

### What each tier gained from the reference layouts

**Premium.** The hero copy now sits on a **pane of frosted glass**, and the
headline is deliberately wider than the pane so its second line crosses the edge
onto the sharp footage. That crossing is the whole effect, and it needs no text
masks: the pane is a decorative element sized to about 84% of the copy block, so
the long line simply overhangs it. `backdrop-filter` works here because `.hero`
carries `isolation: isolate`, which makes the hero its own backdrop root, so the
pane samples the footage and nothing above it. The town runs vertically down the
right edge.

Services were rebuilt as **one ruled run of rows**: name, kicker, a stadium of
the job, the detail, and an arrow. The whole row is an `sms:` link with the body
pre-filled for that service, so the arrow is a real control rather than
decoration. Seven services, seven pictures, where the old three-group layout
carried three.

The stadium runs **about two thirds larger** than it started at, roughly 306px
across at full width and 2:1 rather than 2.5:1. There was a version in between
where the photograph filled the whole row as a background band, and it was
dropped: every source here is a portrait phone frame, and cropping one to a band
seven times wider than it is tall reads as *stretched* however carefully it is
scrimmed and desaturated. A 2:1 stadium is a crop this source can actually
carry, and the type gets a clean field instead of fighting for one. Each picture
keeps a hand-set `object-position` so a portrait frame crops to the work rather
than to somebody's knees, and the stadium lifts three pixels and takes a cyan
ring on hover.

Two photographs were swapped along the way. *Screens and tracks* was a wall of
shop lettering — NOTARY SERVICES, SHREDDING, COPIES — running straight through
the headline; type over type is not a treatment problem, it is the wrong
photograph, so it became the squeegee arc. *Pressure washing* was a second
frame of the same storefront as the first row, near enough identical once the
pictures got big, so it became the crew shot. The trust line became four figures in trays and cores, every one
of them checkable: the Google rating and its count, the number of services, the
towns covered, and what an estimate costs. **No invented statistics.**

**Basic.** The single wide plate between services and the gallery became
**three tall photo cards** with an icon and a label overlaid at the foot, each a
link into the schedule. The deep and cyan planes step down behind the row rather
than behind each card, so the trio reads as one object rather than three.

**Standard.** The frosted pane has a machined equivalent: the hero copy sits in
a **recess milled into the plate**, with `--bevel-deep`, corner bolts and a
hazard-yellow stripe down its leading edge. Same idea as the premium hero, drawn
entirely in this direction's own vocabulary.

## More photography, all of it theirs (2026-09-03)

The services sections were type only, so the whole right of the column ran
empty. Every section that needed a picture has one now: **eleven added across
the three pages**, plus a photograph in each closing band.

The account has **thirteen posts**, twelve of which are in the grid, eleven
scraped, and the twelfth belongs to another account. Nothing usable was left, so
rather than reach for a stock library the new images were **cut from their own
footage**:

| Asset | Source |
|---|---|
| `job-squeegee.jpg` | `reel-storefront-wide.mp4` at 9.6s, cropped to portrait |
| `job-glass-wide.jpg` | same clip at 3.2s |
| `job-pole-wide.jpg` | same clip at 0.4s, the pole at full reach |
| `job-crew.jpg` | `reel-storefront.mp4` at 6.4s, portrait |
| `job-solar-sky.jpg` | `reel-solar.mp4` at 0.15s, panels under cloud |
| `job-solar-roof.jpg` | same clip at 5.6s |
| `job-haul.jpg` | the debris half of the junk post, cropped away from its banners |

Pull frames with `ffmpeg -ss N -i in.mp4 -frames:v 1 -q:v 2 out.jpg`, and pick
the timestamps off a contact sheet first
(`-vf "fps=1,scale=200:-1,tile=7x2"`) rather than guessing. The wide clip is
1280x722, so its frames stand up at full width; the portrait clips are 608x1080
and 540x960 and stay in column-sized slots.

Where they went:

- **01** a photograph takes the third column of each services group and
  stretches to whatever height that group runs to, so the column that was empty
  now carries the picture.
- **02** the deep-teal feature card gets a band across its foot, a photo card
  squares off the grid, a wide plate of the work sits between services and the
  gallery, and a limestone tray fills the empty half of the closing band.
- **03** a recessed photo sits beside the copy in the lead cell, a four-wide
  picture strip continues the ruled table underneath it, and the closing band
  takes the job behind it under the plate gradient.

## The work gallery (2026-09-03)

**It runs the full width of the viewport, inside a gutter.** The header, the
index and the controls stay in the centred column; only the deck breaks out, so
it is a sibling of the `.wrap` rather than a child of it. No `100vw` anywhere:
`vw` includes the scrollbar and would push the document sideways.

The step between cards is **solved from the width actually available** rather
than fixed. Given the visible width of each rank, the gap that makes the row
span exactly the space inside the gutter is
`g = (A - 2*B[D] - w[D]) / (2*D)`, and the deck drops a rank if that gap would
crowd the cards. A fixed step cannot do this: it leaves a band of dead space on
a wide screen and overflows on a narrow one.

`overflow-x: clip` on the deck, with `overflow-y: visible` so the reflection
below it survives. A card narrowed by `clip-path` still occupies its full box,
so the outermost pair was pushing the document sideways even though nothing was
painted out there.

Direction 01's full-bleed photo band is gone. It held the one job photograph the
gallery was missing, and a full-bleed strip immediately above a full-bleed
gallery was the same move twice. All three decks now carry seven items, which is
what a symmetric three-deep row needs.

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

## Showcase rebuilt (2026-09-03)

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

## The reels genuinely auto-play

Self-hosted, muted, looping MP4s taken from their Instagram:

| File | Source post | Content |
|---|---|---|
| `reel-storefront.mp4` / `-wide.mp4` | `/reel/C0joTZTuT9r/` | Commercial storefront, water-fed pole (60s source, cut to 14s) |
| `reel-solar.mp4` | `/reel/DG8Opp4R9e6/` | Rooftop solar-panel rinse (trimmed to the 6.7s of clean footage) |
| `ba-before.jpg` / `ba-after.jpg` | `/reel/C3j11U1Ot1i/` | **Stills, not video** — see below |

Their third reel is a **static image posted as a reel**: 0.03% of pixels change
between t=1s and t=13s and every scene score is ~0. Shipping it as a looping
video would have implied footage that does not exist. It is a single frame
holding two photographs of one storefront, so both halves were cut out of the
720x1280 master and are shown as a matched 390x488 pair. Check motion before
assuming a reel moves:

```
ffmpeg -i in.mp4 -vf "select='gt(scene,0)',metadata=print:file=-" -f null -
```

Each `<video>` is `autoplay muted loop playsinline` with a poster frame, and an
IntersectionObserver plays it only while it is on screen. `prefers-reduced-motion`
and `saveData` both fall back to a paused video with controls.

**This is a change from the [Pane Solutions](https://github.com/Lumen-Marketing/pane-solutions-designs)
build.** That account's reels exposed no `<video>` element and issued zero video
network requests, so only Instagram's non-auto-playing embed widget was possible.
This account's reels *do* serve video — see the recipe below.

---

## Instagram extraction — updated recipe

Instagram has no usable API and `curl` gets a login shell. Render in **headless
Chrome over CDP** and read signed CDN URLs out of the live DOM. Scripts in
`scrape/` (`cdp.mjs`, `grid.mjs`, `posts.mjs`, `dlimg.mjs`, `dlvid.mjs`).

- The profile grid only serves **640px** thumbnails. Rendering each **post
  permalink** individually yields the **1440px** original.
- Signed CDN URLs **403 if you rebuild them** — `oh=`/`oe=`/`_nc_ohc` are a
  signature. Take the URL verbatim from the DOM.
- The profile picture only ever returns **150px** (`s640x640`/`s1080x1080`
  substitution 403s on this account). Ask the client for the real logo.

### Reel MP4s — the part that changed

The reel page's `<video>` has a `blob:` src, so it is useless. **Enable
`Network` domain and collect the request URLs instead.** They look like:

```
https://instagram.f???.fna.fbcdn.net/o1/v/t2/f2/m82/AQ....mp4?...&bytestart=866&byteend=1053
```

Every captured URL is a **DASH byte-range segment**. Strip `bytestart` and
`byteend` from the query and refetch — you get the whole track:

```js
const u = new URL(capturedUrl);
u.searchParams.delete('bytestart');
u.searchParams.delete('byteend');
```

- The `/t2/.../m82|m86/` base is the **video** track (720x1280 here).
- The `/t16/.../m69/` base is **audio-only** — `videoWidth` comes back `0`.
  Harmless for muted background loops; do not ship it as the visual.
- Confirm by loading each file in Chrome and reading `videoWidth`/`duration`
  (`scrape/testvid.mjs`). File size alone will not tell you.
- Decode `efg=` (base64 JSON) for `duration_s` and `bitrate` before downloading.

**CDP `Page.captureScreenshot` does not composite video frames** — poster frames
came back pure white. Use `ffmpeg -ss N -i file -frames:v 1` for stills and
contact sheets.

Reels carry baked-in caption cards and letterboxed lead-ins. Build a contact
sheet (`ffmpeg -vf "fps=2,scale=140:-1,tile=8x3"`) and trim to the clean run
before encoding.

---

## Verification harness

`shots/shot.mjs` (viewport slices + overflow probe), `shots/reels.mjs` (asserts
every video loaded, is muted, looping and has advanced past t=0),
`shots/mobnav.mjs` (burger reachable at 390px, all menu links visible when open,
no tap target under 44px), `shots/measure.mjs` (headline vs. its column).

- **Viewport slices, never one tall capture** — a full-page shot of a page with
  `position:fixed` blend layers hangs Chrome indefinitely.
- Random port **and** its own `--user-data-dir` per run, or Chrome reattaches to
  a leftover and shoots the old page. Kill the process **tree** (`taskkill /T /F`).
- `documentElement.scrollWidth` will not catch a burger pushed off-screen or a
  short tap target — `mobnav.mjs` probes elements directly. It caught D2 hiding
  its phone CTA in the open mobile menu and D3's burger collapsing to 24px tall.
- **Size an `h1` for its column, not the viewport.** `measure.mjs` measures the
  longest line at the computed font size; D2's headline needed 156px, not 178px.

---

## Content rules used here

Every claim is traceable. Services and the tagline come from their own door
hanger (`assets/doorhanger.jpg`) and Instagram captions; the **5.0 rating from 4
Google reviews** is the real count and all four reviews are quoted in full. No
invented statistics.

**There is no offer running** (confirmed by the client, 2026-09-03), and nothing
on any page states one. Their before/after reel had **"20% off new customers"**
burned into the footage, along with **"Before"** and **"After"** in a heavy sans.
All three sit outside the two crops now used (`ba-before.jpg`, `ba-after.jpg`),
so the promotion is gone rather than painted over, and the labels are set in each
direction's own type instead. Their **$50 off** promo graphic is not used at all.
If an offer ever starts, add it as copy — the discount in that post is stale.

They already advertise **www.eastvalleywindowcleaning.com** on printed door
hangers — check who controls that domain before choosing a deploy target.

## Still open

- **High-resolution logo file — still outstanding.** Only a 150px Instagram avatar is available, so
  the Arizona mark here (`assets/az-mark.svg`, inlined per direction so it
  recolours with `currentColor`) is a clean vector rebuild of the real one.
- No contact form — every CTA is `tel:` or `sms:`.
