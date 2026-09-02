# East Valley Window Cleaning — homepage directions

Three industrial homepage directions for **East Valley Window Cleaning LLC**
(Mesa / San Tan Valley, AZ). Owner **Jose Sandoval**, **480-806-9455**,
[@eastvalleywindowcleaningllc](https://www.instagram.com/eastvalleywindowcleaningllc/).

**Live:** https://lumen-marketing.github.io/evwc-designs/

| | |
|---|---|
| `index.html` | Gallery chooser — live scaled iframe previews, Desktop/Mobile toggle |
| `01-control.html` | **Control Room** — dark midnight-teal instrument panel |
| `02-broadsheet.html` | **Broadsheet** — light limestone poster, architectural type |
| `03-hazard.html` | **Hazard** — black + hazard yellow site signage |
| `assets/` | Their real photos and re-encoded reels |
| `scrape/` | The Instagram extraction scripts (see below) |
| `shots/` | Headless-Chrome verification harness |

Homepages only, as asked. Each direction is a **standalone file** — same section
order, zero shared components. The furniture matrix in `index.html` records what
differs; keep it updated if a direction changes.

---

## The reels genuinely auto-play

Three clips from their Instagram, self-hosted as muted looping MP4s:

| File | Source post | Content |
|---|---|---|
| `reel-storefront.mp4` / `-wide.mp4` | `/reel/C0joTZTuT9r/` | Commercial storefront, water-fed pole (60s source, cut to 14s) |
| `reel-solar.mp4` | `/reel/DG8Opp4R9e6/` | Rooftop solar-panel rinse (trimmed to the 6.7s of clean footage) |
| `reel-beforeafter.mp4` | `/reel/C3j11U1Ot1i/` | Before/after on a glass frontage |

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

Two things to check with the client:

- The before/after reel has **"20% off new customers"** burned into the footage,
  and a 2026 promo graphic offers **$50 off**. Neither is stated as current
  anywhere in the copy, but confirm what offer (if any) should run.
- They already advertise **www.eastvalleywindowcleaning.com** on printed door
  hangers — check who controls that domain before choosing a deploy target.

## Still open

- **High-resolution logo file.** Only a 150px Instagram avatar is available, so
  the Arizona mark here (`assets/az-mark.svg`, inlined per direction so it
  recolours with `currentColor`) is a clean vector rebuild of the real one.
- No contact form — every CTA is `tel:` or `sms:`.
