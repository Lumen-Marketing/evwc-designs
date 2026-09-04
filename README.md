# East Valley Window Cleaning - four homepage directions

Four complete homepage designs for **East Valley Window Cleaning LLC** (Mesa and San Tan
Valley, AZ). Owner **Jose Sandoval**, **480-806-9455**,
[@eastvalleywindowcleaningllc](https://www.instagram.com/eastvalleywindowcleaningllc/).

**Live gallery:** https://lumen-marketing.github.io/evwc-designs/

---

## Where these came from

These four are a port of the **Set Right Homes** design set
([lumen-marketing.github.io/setrighthomes-designs](https://lumen-marketing.github.io/setrighthomes-designs/)),
rebuilt around East Valley's content and recoloured to their logo turquoise. The layouts,
components, materials and type pairings are Set Right's. Every word, photograph, clip,
review, town and phone number is East Valley's.

The three earlier directions, Daylight, Broadsheet and Hazard, were replaced. They are
still in the git history if you want them back.

| # | Name | Material | Type | Ground |
|---|------|----------|------|--------|
| 01 | **Mesic** | Drafting linen: 24px minor and 144px major rules painted on the page, survey contours, aggregate speckle | Bricolage Grotesque + Hanken Grotesk | Light, bluish white |
| 02 | **Site** | Film stock: grain on a shuffling four step gate, scanline, vignette, raked light shafts | Big Shoulders Display + Sora | Near black |
| 03 | **Plate** | Brushed steel with a specular sweep, knurled teal field, tread plate on the sheared seams | Saira Condensed + Saira | Dark steel |
| 04 | **Burst** | Screen print: 45 degree halftone with a second screen pulled two pixels off register, paper grain | Archivo Black + Archivo | Light paper |

---

## The furniture matrix

All four run **the same section set in the same order with the same words**. No section is
laid out the same way twice, so the client is comparing designs rather than colourways.

| Section | 01 Mesic | 02 Site | 03 Plate | 04 Burst |
|---|---|---|---|---|
| Hero | Full bleed photo, glass jump menu and glass stat bar floating on it | Photo, draggable smoked glass card, 152px headline underneath | Photo, bolted spec panel, sheared teal field cutting in below | Sunburst rays, photo in a keylined plate, acetate card pinned over it |
| Figures | Four cells inside the hero glass bar | Four counters on a ruled row | Four bolted steel boxes | Four acetate plates with offset colour blocks |
| Owner statement | Blurred photo ground, two columns, six ruled promise rows | Statement at 64px, three ruled notes | Numbered bolted nodes on the teal field beside a checklist | Teal plane, white ink screened over rays, three ruled notes |
| Services, three groups | One large photo card beside two stacked | Three alternating plates, left and right, with recessed job lists | Three milled cards, picture over a recessed list | Three keylined modules, mirrored plates, offset blocks |
| Seven services | Accordion strip, the panel under the pointer takes a third | Job lists inside each alternating chapter | Recessed lists inside the milled cards | Lists inside the keylined modules |
| Photographic band | Full bleed photo with a glass figure card | (not used) | (not used) | Full bleed photo with an acetate figure card |
| Before and after | Two plates on a teal field inside one white panel | Two plates on the lit band | Two bolted plates | Two keylined prints, second one mirrored |
| Recent work, 7 items | Drag filmstrip, mixed slide widths, runs off the right edge | Seven plate composition, pair then full width then pair | Seven bolted plates on a twelve column grid | Seven prints on a twelve column grid, each pulled at a different size |
| Reviews, all four | Glass cards on the teal band with quote marks | Hairline entries, accent rule on top | Bolted frames around white cores | Keylined cards with offset blocks |
| Service area | Town columns on survey contours beside a map card | Ruled town grid on the lit band | Ruled town columns on a milled ground | Ruled town grid on a screened white ground |
| Contact | Teal panel, details list beside the call block | Photo ground, details beside a white call plate | Teal bar, details beside a bolted call plate | Screened near black, details beside an acetate call plate |

---

## Colour

Set Right's four directions were all built around blue. Every blue here became the East
Valley logo turquoise, but **not as a single swap**, because `#12C4DE` measures 2.10:1 on
white and cannot legally carry text on a light ground. The ramp splits by job, and every
value was measured rather than eyeballed:

| Token | Value | Used for | Measured |
|---|---|---|---|
| Logo turquoise | `#12C4DE` | Fills, buttons, and text on dark grounds only | 9.31:1 on near black, 7.19:1 on deep teal |
| Text teal | `#0B6E7E` | Links and text on light grounds | 5.92:1 on white, 5.05:1 on ice |
| Deep panel | `#062A33` | The navy panels and dark fields | 15.14:1 against white text |
| Field | `#0A4E5C` | 03's knurled field | 9.30:1 against white text |
| Bright | `#48D8EC` | 03's accent on steel | 10.25:1 on steel |
| Ice | `#DFF0F4` | Light washes | ground only |

---

## What is NOT on these pages, and why

**Set Right had an FAQ section and a five step process rail. Both are gone.** East Valley
has no FAQ content and no published process anywhere in their existing pages, and filling
those sections would have meant inventing facts about how Jose runs a job. The other
sections carry the page.

**Set Right had an estimate form. It became the call and text block.** East Valley's own
copy says most homes are priced off a photo and an address with no visit, so a form would
have contradicted the sentence next to it. The form's slot, shape and material are kept in
all four; the content inside it is the phone number.

If you want the FAQ and the process back, say so and they will be written as `SWAP:`
placeholders for Jose to correct rather than invented.

---

## Before this goes live

**1. Everything on these pages is real except one thing.** Phone, owner, towns, services,
reviews and photographs all came from the business. The single placeholder:

| Placeholder | Where | Currently |
|---|---|---|
| `SWAP:` map embed | 01 Mesic, service area | A photograph standing in for a Google Maps embed of the service area |

There are no invented statistics on any of the four. The only numbers are 5.0 (the Google
rating), 4 (the review count, stated alongside it every time), 7 (the services listed) and
8 (the towns listed).

**2. The before and after photographs are 390x488.** They are the smallest assets in the
set and they render at roughly 500px wide, so they are visibly soft. Everything else is
between 820px and 1400px on the long edge. A fresh pair shot on a phone would fix the one
piece of proof that matters most on a window cleaning page.

**3. There is no logo file.** All four use an `EV` lockup or a wordmark. A real logo at
1000px or better would replace it.

---

## Photography

Every picture and both clips are **East Valley's own**, pulled from their Instagram and
self hosted in `/assets`. Nothing is stock, nothing is hotlinked, nothing is drawn. There
are no licence obligations and no credits to carry.

The two reels play muted on a loop and **pause when they scroll out of view**, so a clip
running off screen is never decoding frames nobody is looking at.

---

## Measured before shipping

Not eyeballed. The harness is in `shots/` and every number below is reproducible.

| Check | Result |
|---|---|
| Horizontal overflow at 505, 780, 880, 1024, 1280, 1440 | zero on all four |
| Text contrast on photographs, glass and gradients | every node clears 4.5:1, measured on rendered pixels |
| Section heading fill | 86 to 100 percent of its own box on all four |
| Photographic grounds | 2, 2, 1, 1 against a cap of 2 |
| Eyebrows | 2, 2, 2, 3 against a cap of `ceil(sections / 3)` |
| Em dashes | zero |
| Middle dot chains | zero |
| Decorative dots | zero. 03's bolt heads carry the direction's concept, not decoration |

```
node shots/shot.mjs           screenshots, viewport slices, per direction
node shots/audit.mjs *.html   overflow, heading fill, dead space, ground and eyebrow counts
node shots/contrast.mjs       contrast where CSS can resolve the background
node shots/pixcontrast.mjs    contrast on the rendered pixels, for text over photos and glass
node shots/headfit.mjs        natural string width per heading, in its real typeface
node shots/click.mjs          every interactive piece driven by a real click
```

`click.mjs` output on the current build, all passing:

```
chooser toggle   desktop/mobile 4/0 -> 0/4  aria-pressed=true  iframe width=390px
chooser veil     live stages 0 -> 1
01 accordion     open panel index 0 -> 3
01 filmstrip     scrollLeft 0 -> 636
01, 02, 03, 04   drawer "drawer" -> "drawer open"
```

The hero on each direction was measured against the fold at 1440x900, 1920x1080,
1440x760, 1366x720 and 1600x820. All four now end at or just past it, so the next
section never peeks in on load.

Three traps are documented in those files because each one cost real time:

- A **clipped** CDP screenshot over a `backdrop-filter` pane comes back blank white, so
  every glass element scored a clean 1:1 and looked like a pass. Capture the whole
  viewport and crop in Node.
- Measuring the **widest rect** instead of the widest line measures the widest inline
  fragment, so a full width heading holding a `<b>` reports as filling 60 percent of its
  row.
- Reveal animations have to be frozen with `--force-prefers-reduced-motion`, or a `.rv`
  block mid transition reports a box that overlaps the section above.

---

## Files

```
index.html          the chooser: four live scaled iframes, desktop and mobile toggle
01-mesic.html       drafting linen, light
02-site.html        film stock, near black
03-plate.html       brushed steel, dark
04-burst.html       screen print, light
assets/             their photographs and re-encoded reels
scrape/             the Instagram extraction scripts
shots/              the headless Chrome verification harness
```
