# -*- coding: utf-8 -*-
# Drops the wipe into all four, each in its own material.
import sys
sys.path.insert(0, 'scrape')
from wipe import BASE, JS, wipe_markup, BEFORE_ALT, AFTER_ALT, LABEL

def patch(path, css, css_anchor, old_markup, new_markup, js_anchor, label):
    s = open(path, encoding='utf-8').read()
    ok = []
    if css_anchor in s:
        s = s.replace(css_anchor, css + css_anchor, 1); ok.append('css')
    else:
        print('!! MISS css', path)
    if old_markup in s:
        s = s.replace(old_markup, new_markup, 1); ok.append('markup')
    else:
        print('!! MISS markup', path)
    if js_anchor in s:
        s = s.replace(js_anchor, JS + '\n' + js_anchor, 1); ok.append('js')
    else:
        print('!! MISS js', path)
    open(path, 'w', encoding='utf-8').write(s)
    print('%-14s %s  (%s)' % (path, ', '.join(ok), label))

# ============================================================== 01 MESIC ====
# drafting linen: a ruled divider and a keylined tab, like a section mark on a
# drawing. The handle is a square, because nothing on this sheet is round.
CSS_01 = BASE % dict(
    lw='2px', line='var(--blue)',
    grip='background:#fff;color:var(--blue);box-shadow:0 0 0 1px var(--blue),0 10px 26px -12px rgba(7,34,42,.5)',
    tagtop='clamp(12px,1.6vw,20px)',
    tag=("font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:12px;"
         "letter-spacing:.16em;text-transform:uppercase;padding:8px 12px;"
         "background:#fff;color:var(--ink);box-shadow:0 0 0 1px var(--line)"),
)
patch('01-mesic.html', CSS_01, '/* ---------- FOOTER',
"""      <div class="ba">
        <figure>
          <div class="shot"><span class="tag">Before</span>
            <img src="assets/ba-before.jpg" width="390" height="488" loading="lazy" alt="Commercial storefront glazing in Mesa before cleaning, hazed with dust and hard water">
          </div>
          <figcaption><b>Before</b><span>Storefront glazing in Mesa, carrying monsoon dust and sprinkler overspray.</span></figcaption>
        </figure>
        <figure>
          <div class="shot"><span class="tag a">After</span>
            <img src="assets/ba-after.jpg" width="390" height="488" loading="lazy" alt="The same Mesa storefront glazing after cleaning, clear and streak free">
          </div>
          <figcaption><b>After</b><span>The same glass after one visit. Frames and screens done at the same time.</span></figcaption>""",
"""      <div class="ba">
        <figure style="margin:0;grid-column:1/-1">
%s
          <figcaption><b>Drag the handle</b><span>The same storefront glazing in Mesa, one visit apart. Frames and screens done at the same time.</span></figcaption>
        </figure>
        <figure hidden>
          <div class="shot"><span class="tag a">After</span>
            <img src="assets/ba-after.jpg" width="390" height="488" loading="lazy" alt="The same Mesa storefront glazing after cleaning, clear and streak free">
          </div>
          <figcaption><b>After</b><span>The same glass after one visit. Frames and screens done at the same time.</span></figcaption>""" % wipe_markup(10, BEFORE_ALT, AFTER_ALT, 'Before', 'After', LABEL),
 '</script>', 'ruled divider, keylined tabs')

# =============================================================== 02 SITE ====
# film stock: a bright hairline and a smoked gate handle, and the box runs edge
# to edge because this page is a split screen and this is its one true split.
CSS_02 = (BASE % dict(
    lw='2px', line='var(--blue)',
    grip=('background:rgba(7,12,20,.62);color:#fff;'
          'box-shadow:inset 0 0 0 1px rgba(255,255,255,.5),0 18px 40px -16px rgba(0,0,0,.9);'
          '-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)'),
    tagtop='clamp(14px,2vw,26px)',
    tag=("font-family:'Big Shoulders Display',sans-serif;font-weight:800;font-size:13px;"
         "letter-spacing:.2em;text-transform:uppercase;padding:8px 13px;color:#fff;"
         "background:rgba(7,12,20,.66);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px)"),
) + """/* full bleed, because this page is a split screen and the wipe is the one
   piece of content that IS one */
#proof-wipe{aspect-ratio:auto;height:min(82dvh,860px);margin-top:clamp(28px,3.6vw,48px)}
@media (max-width:760px){#proof-wipe{height:clamp(320px,72vw,470px)}}
""")
patch('02-site.html', CSS_02, '/* ---------- REVIEWS: a ruled run, full width ----------',
"""  <div class="basplit rv">
    <figure>
      <img src="assets/ba-before.jpg" width="390" height="488" loading="lazy"
           alt="Commercial storefront glazing in Mesa before cleaning">
      <figcaption><b>Before</b>Monsoon dust and sprinkler overspray on the glass.</figcaption>
    </figure>
    <figure>
      <img src="assets/ba-after.jpg" width="390" height="488" loading="lazy"
           alt="The same Mesa storefront glazing after cleaning">
      <figcaption><b>After</b>One visit. Frames and screens done at the same time.</figcaption>
    </figure>
  </div>""",
"""  <div class="rv" id="proof-wipe-wrap">
%s
  </div>""" % wipe_markup(4, BEFORE_ALT, AFTER_ALT, 'Before', 'After', LABEL).replace(
      '<div class="wipe">', '<div class="wipe" id="proof-wipe">', 1),
 '</script>', 'full bleed, smoked gate handle')

# ============================================================== 03 PLATE ====
# milled metal: the divider is a machined seam and the handle is a knurled boss
# bolted through it, like every other control on this page.
CSS_03 = BASE % dict(
    lw='3px', line='var(--bright)',
    grip=('background:linear-gradient(180deg,#2a333f,#161d26);color:#fff;'
          'box-shadow:inset 0 1px 0 rgba(255,255,255,.22),inset 0 -1px 0 rgba(0,0,0,.7),'
          '0 14px 30px -14px rgba(0,0,0,.95),0 0 0 1px rgba(0,0,0,.8);'
          'background-image:repeating-linear-gradient(45deg,rgba(255,255,255,.07) 0 1px,transparent 1px 5px),'
          'linear-gradient(180deg,#2a333f,#161d26)'),
    tagtop='clamp(12px,1.6vw,20px)',
    tag=("font-family:'Saira Condensed',sans-serif;font-weight:700;font-size:14px;"
         "letter-spacing:.18em;text-transform:uppercase;padding:7px 12px;color:#fff;"
         "background:var(--steel-2);box-shadow:var(--bevel)"),
)
patch('03-plate.html', CSS_03, '/* ---------- RECENT WORK: the indexing rail ----------',
"""    <div class="ba">
      <figure class="rv" style="margin:0">
        <div class="plate bolts"><span class="b2"></span><span class="b3"></span>
          <div><img src="assets/ba-before.jpg" width="390" height="488" loading="lazy" alt="Commercial storefront glazing in Mesa before cleaning"></div>
          <figcaption><b>Before</b>Monsoon dust and sprinkler overspray on the glass.</figcaption>
        </div>
      </figure>
      <figure class="rv" style="margin:0">
        <div class="plate bolts"><span class="b2"></span><span class="b3"></span>
          <div><img src="assets/ba-after.jpg" width="390" height="488" loading="lazy" alt="The same Mesa storefront glazing after cleaning"></div>
          <figcaption><b>After</b>One visit. Frames and screens done at the same time.</figcaption>
        </div>
      </figure>""",
"""    <div class="ba" style="grid-template-columns:1fr">
      <figure class="rv" style="margin:0">
        <div class="plate bolts"><span class="b2"></span><span class="b3"></span>
%s
          <figcaption><b>Drag the handle</b>The same storefront glazing, one visit apart. Frames and screens done at the same time.</figcaption>
        </div>
      </figure>""" % wipe_markup(10, BEFORE_ALT, AFTER_ALT, 'Before', 'After', LABEL),
 '</script>', 'machined seam, knurled boss')

# ============================================================== 04 BURST ====
# screen print: a hard ink rule and a handle with the accent block pulled two
# pixels off register behind it, the way every plate on this page is printed.
CSS_04 = BASE % dict(
    lw='3px', line='var(--ink)',
    grip=('background:var(--white);color:var(--ink);'
          'box-shadow:2px 2px 0 0 var(--sky),0 0 0 2px var(--ink)'),
    tagtop='clamp(12px,1.6vw,20px)',
    tag=("font-family:'Archivo Black',sans-serif;font-size:12px;letter-spacing:.12em;"
         "text-transform:uppercase;padding:8px 12px;color:var(--white);background:var(--ink)"),
)
patch('04-burst.html', CSS_04, '/* ---------- FOOTER',
"""    <div class="ba">
      <figure class="rv" style="margin:0">
        <div class="plate"><img src="assets/ba-before.jpg" width="390" height="488" loading="lazy" alt="Commercial storefront glazing in Mesa before cleaning"></div>
        <figcaption><b>Before</b>Monsoon dust and sprinkler overspray on the glass.</figcaption>
      </figure>
      <figure class="rv" style="margin:0">
        <div class="plate mirror"><img src="assets/ba-after.jpg" width="390" height="488" loading="lazy" alt="The same Mesa storefront glazing after cleaning"></div>
        <figcaption><b>After</b>One visit. Frames and screens done at the same time.</figcaption>
      </figure>
    </div>""",
"""    <div class="ba" style="grid-template-columns:1fr">
      <figure class="rv" style="margin:0">
        <div class="plate">
%s
        </div>
        <figcaption><b>Drag the handle</b>The same storefront glazing, one visit apart. Frames and screens done at the same time.</figcaption>
      </figure>
    </div>""" % wipe_markup(10, BEFORE_ALT, AFTER_ALT, 'Before', 'After', LABEL),
 '</script>', 'ink rule, off register handle')
