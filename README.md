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
order, zero shared components. The furniture matrix in `index.html` records what
differs; keep it updated if a direction changes.

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

## The reels genuinely auto-play

Self-hosted, muted, looping MP4s taken from their Instagram:

| File | Source post | Content |
|---|---|---|
| `reel-storefront.mp4` / `-wide.mp4` | `/reel/C0joTZTuT9r/` | Commercial storefront, water-fed pole (60s source, cut to 14s) |
| `reel-solar.mp4` | `/reel/DG8Opp4R9e6/` | Rooftop solar-panel rinse (trimmed to the 6.7s of clean footage) |
| `beforeafter.jpg` | `/reel/C3j11U1Ot1i/` | **Still, not video** — see below |

Their third reel is a **static image posted as a reel**: 0.03% of pixels change
between t=1s and t=13s and every scene score is ~0. Shipping it as a looping
video with a REC badge would have implied footage that does not exist, so it runs
as a still in the third bay, badged accordingly. Check motion before assuming a
reel moves:

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
burned into the footage; it is masked out in `assets/beforeafter.jpg` with two
`drawbox` fills colour-matched to the backing wall, which leaves both photos and
the Before/After labels untouched. Their **$50 off** promo graphic is not used at
all. If an offer ever starts, add it as copy — do not un-mask the reel, the
discount in it is stale.

They already advertise **www.eastvalleywindowcleaning.com** on printed door
hangers — check who controls that domain before choosing a deploy target.

## Still open

- **High-resolution logo file — still outstanding.** Only a 150px Instagram avatar is available, so
  the Arizona mark here (`assets/az-mark.svg`, inlined per direction so it
  recolours with `currentColor`) is a clean vector rebuild of the real one.
- No contact form — every CTA is `tel:` or `sms:`.
