# -*- coding: utf-8 -*-
# 01 MESIC, the services row: "On The Job" was plain, and it was plain by a
# number rather than by opinion.
#
#   heading fill    194 / 1240 = 16%. The lowest on the page by a factor of
#                   1.5, so the top of the section was a thousand pixels of
#                   empty sheet beside four words.
#   structure       all three items were div>h3>p. An asymmetric grid holding
#                   a card grid.
#   information     7, 4 and 6 words of copy. 1088px of section carrying
#                   seventeen words, while 02 and 03 both hang a job list off
#                   every one of the three groups.
#   photograph      627x655 and two at 493x246. On a trades page the
#                   photography is the product.
#   depth           none. Three pictures sitting in their own grid tracks,
#                   nothing crossing anything.
#
# It is now the KEY to the page: three groups, the seven services named under
# the group they belong to, and the pictures at a size that sells the work.
# The furniture is drafting, because that is this direction's material. A
# detail on a sheet is bounded by a rule drawn OUTSIDE the picture, and its
# title sits on a plate. The plate on the primary detail is hung into the
# corner of the photograph and half onto the sheet below, and THAT is the
# depth: an overlap, not a shadow under a card.
#
# Tier discipline: no scroll driven anything. The entry reveal this page
# already has, and a hover that belongs to the picture. That is Basic.

p = '01-mesic.html'
s = open(p, encoding='utf-8').read()
done = []


def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label)
        return
    s = s.replace(old, new, 1)
    done.append(label)


# ---------------------------------------------------------------- CSS ------
CSS = """/* ---------- ON THE JOB: three details on one sheet ----------
   The section is the key to the page. Three groups, the seven services named
   under the one they belong to, and the photographs at the size the work
   deserves rather than in a grid of thumbnails.

   Drafting furniture, since that is this direction's material: a detail on a
   sheet is bounded by a rule drawn OUTSIDE the picture, not by a frame around
   it, and its title sits on a plate. The plate on the primary detail is hung
   into the corner of the photograph and half onto the sheet below. That
   overlap is the depth device here. There is no shadow under a flat card
   anywhere in this section. */
.jobs-hd{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.8fr);
  gap:clamp(16px,4vw,72px);align-items:end}
.jobs-hd .sh{margin:0}
.jobs-hd p{margin:0 0 7px;color:var(--muted);font-size:16px;line-height:1.62;max-width:46ch}

.det{position:relative}
/* the drawn detail boundary. It is a mark on the sheet, so it sits outside
   the picture; the picture itself carries no border at all. */
.det .vp{position:relative;background:var(--ice)}
.det .vp::after{content:"";position:absolute;inset:-9px;
  border:1px solid var(--line);pointer-events:none}
.det .vp img{display:block;width:100%;height:100%;object-fit:cover;
  transition:transform 1s cubic-bezier(.16,1,.3,1)}
.det:hover .vp img{transform:scale(1.035)}

.det .cap h3{font-size:clamp(21px,2.2vw,27px);letter-spacing:-.022em;margin:0}
/* the job list: ruled rows, no box. The same seven services 02 and 03 hang
   off their three groups, so the whole set carries one set of facts. */
.det .cap ul{list-style:none;margin:13px 0 0;padding:0}
.det .cap li{border-top:1px solid var(--line);padding:9px 0;
  font-size:14.5px;line-height:1.45;color:var(--ink-2)}

/* the primary detail runs the full measure */
.det.lead{margin-top:clamp(30px,3.8vw,52px);margin-bottom:clamp(92px,8.5vw,132px)}
.det.lead .vp{aspect-ratio:2.15/1}
.det.lead .cap{position:absolute;z-index:2;right:0;bottom:0;
  width:min(400px,44%);transform:translateY(36%);
  background:var(--white);
  padding:clamp(20px,2.1vw,27px) clamp(20px,2.1vw,27px) clamp(13px,1.4vw,18px);
  box-shadow:0 0 0 1px var(--line),0 28px 58px -30px rgba(6,42,51,.52)}

/* the two secondary details share one baseline. No plate on these: the
   contrast between a title hung ON the picture and a title set on the sheet
   is what says which of the three groups is the business. */
.detpair{display:grid;grid-template-columns:1fr 1fr;gap:clamp(22px,3.6vw,60px)}
.detpair .vp{aspect-ratio:4/3}
.detpair .cap{margin-top:27px}

@media (max-width:980px){
  .jobs-hd{grid-template-columns:1fr;gap:18px;align-items:start}
  .jobs-hd p{margin-bottom:0}
  /* the hang comes off below 980. An element overlapping another one is a
     touch target sitting on top of a touch target. */
  .det.lead{margin-bottom:clamp(38px,5vw,56px)}
  .det.lead .vp{aspect-ratio:16/9}
  .det.lead .cap{position:static;width:auto;transform:none;margin-top:27px;
    padding:0;background:none;box-shadow:none}
}
@media (max-width:700px){
  .detpair{grid-template-columns:1fr;gap:clamp(34px,7vw,48px)}
  .det.lead .vp,.detpair .vp{aspect-ratio:3/2}
}

"""
rep('/* ---------- BEFORE AND AFTER: a wipe ----------',
    CSS + '/* ---------- BEFORE AND AFTER: a wipe ----------', 'css block')

# ---- the furniture this replaces, removed rather than left as dead rules ---
rep(""".cards{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(14px,2vw,22px);margin-top:26px}
.pcard{""", """.pcard{""", 'drop .cards base')

rep(""".cards{gap:40px 40px;margin-top:40px}
  .cards.feature{grid-template-columns:1.12fr .88fr}
  .cards.feature>.pcard:first-child{grid-row:1/3;display:flex;flex-direction:column}
  .cards.feature>.pcard:first-child .shot{aspect-ratio:auto;flex:1;min-height:320px}
  .cards.feature>.pcard:first-child h3{font-size:28px}
  .cards.feature>.pcard:first-child p{font-size:16px;max-width:38ch}
  .cards.feature>.pcard{border-bottom:0}
  .cards.feature>.pcard:not(:first-child) .shot{aspect-ratio:16/8}
""", "", 'drop .cards.feature')

rep("""  .cards.feature{grid-template-columns:1fr}
  .cards.feature>.pcard:first-child{grid-row:auto}
""", "", 'drop .cards.feature mq')

rep(""".ba,.cards,.revs,.trio,.towns{grid-template-columns:1fr}""",
    """.ba,.revs,.trio,.towns{grid-template-columns:1fr}""", 'drop .cards from stack mq')

# ------------------------------------------------------------- MARKUP ------
OLD = """    <h2 class="sh rv">On The Job</h2>
    <div class="cards feature">
      <article class="pcard rv">
        <div class="shot"><img src="assets/storefront.jpg" width="1200" height="1200" loading="lazy" alt="Clean commercial storefront glazing at street level"></div>
        <h3>Glass</h3>
        <p>Windows in and out, screens, tracks and hard water stains.</p>
      </article>
      <article class="pcard rv">
        <div class="shot"><img src="assets/job-solar-sky.jpg" width="540" height="960" loading="lazy" alt="A rooftop solar array under open sky, washed clear of dust"></div>
        <h3>Film &amp; Panels</h3>
        <p>UV and privacy film, and solar arrays washed back to output.</p>
      </article>
      <article class="pcard rv">
        <div class="shot"><img src="assets/job-haul.jpg" width="820" height="1094" loading="lazy" alt="Monsoon debris and a cleared-out load stacked in a yard ready to haul"></div>
        <h3>Property</h3>
        <p>Pressure washing, plus junk and monsoon debris hauled away.</p>
      </article>
    </div>"""

NEW = """    <div class="jobs-hd rv">
      <h2 class="sh">Three Groups, One Operator</h2>
      <p>Seven services, split three ways. All of it goes on one visit and one invoice, because the same person does the lot.</p>
    </div>

    <!-- the primary detail: glass is the business, so it gets the measure -->
    <article class="det lead rv">
      <div class="vp"><img src="assets/storefront.jpg" width="1200" height="1200" loading="lazy" alt="Clean commercial storefront glazing at street level"></div>
      <div class="cap">
        <h3>Glass</h3>
        <ul>
          <li>Interior and exterior windows, homes and businesses</li>
          <li>Screens pulled, washed and re-set</li>
          <li>Sills and sliding tracks scrubbed out</li>
          <li>Hard water and mineral etching cut back</li>
        </ul>
      </div>
    </article>

    <div class="detpair">
      <article class="det rv">
        <div class="vp"><img src="assets/job-solar-sky.jpg" width="540" height="960" loading="lazy" alt="A rooftop solar array under open sky, washed clear of dust"></div>
        <div class="cap">
          <h3>Film &amp; Panels</h3>
          <ul>
            <li>UV and heat film to protect furnishings</li>
            <li>Reflective film for privacy</li>
            <li>Solar arrays washed back to output</li>
          </ul>
        </div>
      </article>
      <article class="det rv">
        <div class="vp"><img src="assets/job-haul.jpg" width="820" height="1094" loading="lazy" alt="Monsoon debris and a cleared-out load stacked in a yard ready to haul"></div>
        <div class="cap">
          <h3>Property</h3>
          <ul>
            <li>Driveways, walkways and patios back to colour</li>
            <li>Building exteriors and elevations washed down</li>
            <li>Monsoon debris and clear-outs hauled away</li>
          </ul>
        </div>
      </article>
    </div>"""

rep(OLD, NEW, 'services markup')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
