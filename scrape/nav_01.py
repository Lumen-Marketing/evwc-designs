# -*- coding: utf-8 -*-
# 01 MESIC, the nav: from a bar to a TITLE BLOCK.
#
# What was wrong, countably:
#
#   one component, three times   02 and 03 share their nav markup BYTE FOR
#                                BYTE, and 01 is the same skeleton with a
#                                logo box bolted on: wordmark, links, phone,
#                                filled button, burger, left to right.
#   glass over nothing           .nav wrapped its contents in .glass, whose
#                                tint is rgba(5,28,34,.46 to .62). Over the
#                                white body that is a dark rectangle, which
#                                is the exact failure the house rules name:
#                                a tint only reads as glass if what is behind
#                                it is bright enough to survive being tinted.
#                                Nothing was behind it.
#   the brand mark               "EV" in a 36px filled square. An icon in a
#                                square is the most templated mark there is.
#   duplicate links              the utility strip carried Services, Owner
#                                operated, Recent work and Contact, and the
#                                nav 14px below it carried four of the same
#                                five. Two rows of the same links.
#
# A drawing sheet identifies itself in a TITLE BLOCK: named fields in ruled
# cells, divided by drawn rules rather than by gaps, with the action field
# filled. That is this direction's own material doing the job the generic bar
# was doing, and it is a shape no other direction in the set can use.
#
# Depth, and it is occlusion rather than a shadow: the estimate cell runs
# proud of the block's bottom rule and crosses into the hero.
#
# Basic tier, so nothing here is driven by the scroll.
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
OLD_CSS = """.nav{position:sticky;top:0;z-index:60;transition:background .35s,box-shadow .35s,border-color .35s;
  border-bottom:1px solid transparent;background:transparent}
.nav .glass{border-radius:0;border:0;border-bottom:1px solid rgba(255,255,255,.13)}
.nav .glass::after{display:none}
.nav.stuck{background:var(--white);border-bottom-color:var(--line);box-shadow:0 6px 22px -16px rgba(6,42,51,.5)}
.nav.stuck .glass{background:transparent;backdrop-filter:none;-webkit-backdrop-filter:none;border-color:transparent;box-shadow:none}
.nav.stuck .glass::before,.nav.stuck .glass::after{display:none}
.nav-in{height:70px;display:flex;align-items:center;gap:22px;position:relative;z-index:2}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;flex:none}
.brand .mk{width:36px;height:36px;border-radius:0;background:var(--blue);color:#fff;display:grid;place-items:center;
  font-weight:800;font-size:14px;letter-spacing:-.02em}
.brand b{font-size:16.5px;font-weight:800;letter-spacing:-.035em;line-height:1.05;color:#fff;transition:color .3s}
.brand small{display:block;font-size:9.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.66);font-weight:700;transition:color .3s}
.nav.stuck .brand b{color:var(--ink)}
.nav.stuck .brand small{color:var(--muted)}
.nav-links{display:flex;gap:4px;margin-left:14px}
.nav-links a{text-decoration:none;font-size:13.5px;font-weight:700;color:rgba(255,255,255,.86);padding:8px 11px;border-radius:4px;transition:background .22s,color .22s}
.nav-links a:hover{background:rgba(255,255,255,.16);color:#fff}
.nav.stuck .nav-links a{color:var(--ink-2)}
.nav.stuck .nav-links a:hover{background:var(--ice);color:var(--navy)}
.nav-cta{margin-left:auto;display:flex;gap:9px;align-items:center}
.tel{display:inline-flex;align-items:center;gap:8px;padding:14px 20px;border-radius:4px;background:var(--navy);color:#fff;
  text-decoration:none;font-weight:800;font-size:14px;white-space:nowrap;transition:background .25s,transform .18s}
.tel:hover{background:var(--navy-2);transform:translateY(-2px)}
.burger{display:none;width:42px;height:42px;border:1px solid rgba(255,255,255,.4);background:rgba(255,255,255,.14);
  border-radius:4px;margin-left:auto;cursor:pointer}
.nav.stuck .burger{border-color:var(--line);background:var(--white)}
.burger i{display:block;width:17px;height:2px;background:#fff;margin:0 auto;position:relative;transition:background .3s}
.burger i::before,.burger i::after{content:"";position:absolute;left:0;width:17px;height:2px;background:#fff;transition:transform .3s}
.burger i::before{top:-5.5px}.burger i::after{top:5.5px}
.nav.stuck .burger i,.nav.stuck .burger i::before,.nav.stuck .burger i::after{background:var(--ink)}
.burger[aria-expanded="true"] i{background:transparent}
.burger[aria-expanded="true"] i::before{transform:translateY(5.5px) rotate(45deg)}
.burger[aria-expanded="true"] i::after{transform:translateY(-5.5px) rotate(-45deg)}"""

NEW_CSS = """/* ---------- NAV: the title block ----------
   A drawing sheet identifies itself in a title block: named fields in ruled
   cells, divided by drawn rules rather than by gaps, with the action field
   filled. Every rule in here is a rule DRAWN on the sheet, which is why the
   cells touch: a gap would make them four objects instead of one block.

   What this replaces: the contents used to sit in a .glass pane, and the
   only thing behind that pane was the white body, so its rgba(5,28,34,.46)
   tint read as a dark rectangle rather than as a material. Glass needs a
   photograph behind it or it should not be there. */
.nav{position:sticky;top:0;z-index:60;background:var(--white);
  transition:box-shadow .35s}
.nav.stuck{box-shadow:0 10px 26px -20px rgba(6,42,51,.6)}
.tblock{display:grid;grid-template-columns:auto minmax(0,1fr) auto auto;
  align-items:stretch;border-bottom:1px solid var(--line);
  /* the block is laid ON the sheet, so it casts onto the drawing below */
  box-shadow:0 15px 30px -26px rgba(6,42,51,.5)}
.tb-cell{display:flex;flex-direction:column;justify-content:center;
  padding:13px clamp(15px,1.7vw,23px);text-decoration:none;position:relative;
  border-left:1px solid var(--line);min-width:0}
.tb-cell:first-child{border-left:0;padding-left:0}

.brand b{font-family:'Bricolage Grotesque',sans-serif;font-size:15.5px;font-weight:800;
  letter-spacing:-.032em;line-height:1.1;color:var(--ink);white-space:nowrap}
.brand small{margin-top:4px;font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--muted);font-weight:700}
.brand:hover b{color:var(--blue)}

/* the links are cells of the block too, so the hover fills floor to ceiling
   the way a cell in a table does, not a pill floating inside one */
.nav-links{flex-direction:row;align-items:stretch;padding:0;gap:0}
.nav-links a{display:flex;align-items:center;text-decoration:none;
  padding:0 clamp(11px,1.25vw,18px);font-size:13.5px;font-weight:600;
  color:var(--ink-2);white-space:nowrap;transition:background .2s,color .2s}
.nav-links a:hover{background:var(--ice);color:var(--navy)}

/* the one named field. It is named because the number takes a text as well
   as a call, and that is worth saying. */
.tb-tel small{font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--muted);font-weight:700}
.tb-tel b{margin-top:3px;font-family:'Bricolage Grotesque',sans-serif;font-size:19px;
  font-weight:800;letter-spacing:-.02em;color:var(--ink);font-variant-numeric:tabular-nums}
.tb-tel:hover{background:var(--ice)}

/* the action field runs proud of the block's bottom rule and crosses into
   the drawing. That overlap is the depth here: the block sits ON the sheet
   rather than in the stack above it. */
.tb-cta{border-left:0;justify-content:center;align-items:center;
  background:var(--blue);color:#fff;margin-bottom:-9px;
  padding-inline:clamp(20px,2.5vw,36px);
  font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:14px;
  letter-spacing:-.01em;white-space:nowrap;transition:background .25s}
.tb-cta:hover{background:var(--blue-d)}

.burger{display:none;width:46px;border:0;border-left:1px solid var(--line);
  background:none;border-radius:0;cursor:pointer;padding:0}
.burger i{display:block;width:18px;height:2px;background:var(--ink);margin:0 auto;
  position:relative;transition:background .3s}
.burger i::before,.burger i::after{content:"";position:absolute;left:0;width:18px;height:2px;
  background:var(--ink);transition:transform .3s}
.burger i::before{top:-6px}.burger i::after{top:6px}
.burger[aria-expanded="true"] i{background:transparent}
.burger[aria-expanded="true"] i::before{transform:translateY(6px) rotate(45deg)}
.burger[aria-expanded="true"] i::after{transform:translateY(-6px) rotate(-45deg)}"""

rep(OLD_CSS, NEW_CSS, 'nav css')

# the breakpoint rules referred to .nav-cta, which no longer exists
rep("""@media (max-width:1010px){
  .nav-cta .tel{display:none}
  .nav-links{display:none}
  .burger{display:grid;place-items:center}
  .nav-links{gap:20px;font-size:14px}
}
@media (max-width:860px){
  .nav-links{gap:14px;font-size:13px}
}""",
"""@media (max-width:1010px){
  /* the phone field steps out first, then the links, at the same breakpoint,
     because between about 780 and 1010 the row was wider than the page. The
     number is still in the utility bar, the drawer, the hero and the footer. */
  .tb-tel,.nav-links{display:none}
  .burger{display:grid;place-items:center}
  .tblock{grid-template-columns:minmax(0,1fr) auto auto}
}
@media (max-width:560px){
  .tb-cta{padding-inline:16px;font-size:13px}
  .brand b{font-size:14.5px}
}""", 'nav breakpoints')

# ------------------------------------------------------------- MARKUP ------
rep("""    <div class="r">
      <a href="#services">Services</a>
      <a href="#about">Owner operated</a>
      <a href="#work">Recent work</a>
      <a href="#estimate">Contact</a>
    </div>""",
"""    <div class="r">
      <span>Owner operated in Mesa</span>
      <span>Residential and commercial</span>
      <span>Free estimates</span>
    </div>""", 'utility strip stops repeating the nav')

rep("""<header class="nav" id="nav">
  <div class="glass">
    <div class="wrap nav-in">
      <a class="brand" href="#top">
        <span class="mk">EV</span>
        <span><b>East Valley Window Cleaning</b><small>Mesa, Arizona</small></span>
      </a>
      <nav class="nav-links" aria-label="Primary">
        <a href="#services">Services</a><a href="#about">Owner operated</a><a href="#work">Recent work</a>
        <a href="#reviews">Reviews</a><a href="#area">Areas</a>
      </nav>
      <div class="nav-cta">
        <a class="tel" href="tel:+14808069455">480-806-9455</a>
        <a class="btn" href="#estimate">Free estimate</a>
      </div>
      <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i></button>
    </div>
  </div>
</header>""",
"""<header class="nav" id="nav">
  <div class="wrap tblock">
    <a class="tb-cell brand" href="#top">
      <b>East Valley<br>Window Cleaning</b>
      <small>Mesa, Arizona</small>
    </a>
    <nav class="tb-cell nav-links" aria-label="Primary">
      <a href="#services">Services</a><a href="#about">Owner operated</a><a href="#work">Recent work</a>
      <a href="#reviews">Reviews</a><a href="#area">Areas</a>
    </nav>
    <a class="tb-cell tb-tel" href="tel:+14808069455">
      <small>Call or text</small><b>480-806-9455</b>
    </a>
    <a class="tb-cell tb-cta" href="#estimate">Free estimate</a>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i></button>
  </div>
</header>""", 'nav markup')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
