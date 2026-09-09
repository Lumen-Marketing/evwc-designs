# -*- coding: utf-8 -*-
# 03 PLATE, the nav: from a glazed bar to a BOLTED CONTROL PLATE.
#
# The three navs in this set were one component. 02 and 03 shared their markup
# byte for byte, and the CSS differed only in font-family, colour tokens and a
# handful of pixel values: .nav-in height 76 vs 74, .nav-links gap 28 vs 26,
# .nav-right gap 22 vs 20, burger bars 19px vs 18px. Same selectors, same
# order, same underline that sweeps in from the right on hover. That is a
# skin, not a design, and the furniture matrix forbids it.
#
# This page's material is milled steel and its depth device is the bevel: a
# lit top edge, a dark foot, bolted plates and recessed panels. Every control
# on the page is built from it, and the nav was the one control that was not.
# So the nav becomes what the rest of the page already is:
#
#   the bar      a brushed plate with the bevel, bolted at four corners.
#                Opaque, because a plate is opaque. The blur goes: three
#                glazed navs was most of why they read as one.
#   the links    milled INTO the plate as a recessed channel, not printed on
#                top of it. Inset shadow, dark floor, the labels sitting in it.
#   the phone    a readout window, the same recessed cell with inset side
#                rules the indexing rail already uses for its station number.
#   the estimate a raised machined key, standing proud of the channel it sits
#                beside.
#
# The one coloured mark on the bar carries real state: an IntersectionObserver
# lights the station tick under whichever section you are actually in. No
# decorative dots.
p = '03-plate.html'
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
OLD = """.nav{position:sticky;top:0;z-index:60;background:rgba(12,17,25,.93);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid transparent;transition:border-color .3s}
.nav.stuck{border-bottom-color:var(--line);box-shadow:0 1px 0 rgba(255,255,255,.06)}
.nav-in{height:74px;display:flex;align-items:center;gap:26px}
.brand{text-decoration:none;font-family:'Saira Condensed',sans-serif;font-weight:800;font-size:24px;letter-spacing:.09em;text-transform:uppercase;line-height:1}
.brand em{font-style:normal;color:var(--bright)}
.nav-links{display:flex;gap:26px;margin-left:auto}
.nav-links a{font-family:'Saira Condensed',sans-serif;text-decoration:none;font-size:18px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--fg-2);position:relative;padding-block:4px;transition:color .25s}
.nav-links a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:2px;background:var(--bright);transform:scaleX(0);transform-origin:right;transition:transform .32s cubic-bezier(.16,1,.3,1)}
.nav-links a:hover{color:#fff}
.nav-links a:hover::after{transform:scaleX(1);transform-origin:left}
.nav-right{display:flex;align-items:center;gap:20px;margin-left:20px}
.nav-tel{text-decoration:none;font-family:'Saira Condensed',sans-serif;font-weight:700;font-size:20px;letter-spacing:.05em;white-space:nowrap}
.burger{display:none;width:44px;height:44px;border:1.5px solid rgba(255,255,255,.4);background:none;margin-left:auto;cursor:pointer;border-radius:0}
.burger i{display:block;width:18px;height:2px;background:#fff;margin:0 auto;position:relative;transition:background .3s}
.burger i::before,.burger i::after{content:"";position:absolute;left:0;width:18px;height:2px;background:#fff;transition:transform .3s}
.burger i::before{top:-6px}.burger i::after{top:6px}
.burger[aria-expanded="true"] i{background:transparent}
.burger[aria-expanded="true"] i::before{transform:translateY(6px) rotate(45deg)}
.burger[aria-expanded="true"] i::after{transform:translateY(-6px) rotate(-45deg)}"""

NEW = """/* ---------- NAV: a plate bolted across the head of the page ----------
   Everything else on this page is machined, and the nav was the one control
   that was not: a translucent bar with a hover underline, the same one 02
   was using. So it is built out of the same material as the rest.

   Opaque, because a steel plate is opaque. The blur is gone on purpose. */
.nav{position:sticky;top:0;z-index:60;
  background-color:var(--steel-2);
  background-image:var(--brush);
  box-shadow:var(--bevel);
  transition:box-shadow .35s}
/* off the top of the page the plate seats down: the lit edge picks up more
   and the cast shadow deepens, because it is now sitting on the page rather
   than against the hero */
.nav.stuck{box-shadow:inset 0 1px 0 rgba(255,255,255,.26),
  inset 0 -1px 0 rgba(0,0,0,.72),0 24px 46px -26px rgba(3,24,30,.95)}
.nav-in{height:74px;display:flex;align-items:center;gap:clamp(12px,1.6vw,24px)}
.brand{text-decoration:none;font-family:'Saira Condensed',sans-serif;font-weight:800;
  font-size:25px;letter-spacing:.09em;text-transform:uppercase;line-height:1;flex:none}
.brand em{font-style:normal;color:var(--bright)}

/* the channel: the links are milled INTO the plate. The floor is darker than
   the face and the lip is lit, which is what makes it read as a slot rather
   than as a box drawn on top. */
.nav-links{display:flex;align-items:stretch;gap:0;margin-left:auto;height:46px;
  background:var(--steel-3);box-shadow:var(--bevel-in)}
.nav-links a{display:flex;align-items:center;text-decoration:none;position:relative;
  padding:0 clamp(11px,1.35vw,20px);
  font-family:'Saira Condensed',sans-serif;font-size:18px;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase;color:var(--fg-2);white-space:nowrap;
  transition:color .25s,background .25s}
.nav-links a+a{box-shadow:inset 1px 0 0 rgba(0,0,0,.5),inset 2px 0 0 rgba(255,255,255,.045)}
.nav-links a:hover{color:#fff;background:rgba(255,255,255,.055)}
/* the station mark. It is the only coloured mark on this bar and it carries
   real state: an observer lights the section you are actually in. */
.nav-links a::after{content:"";position:absolute;left:11px;right:11px;bottom:7px;height:3px;
  background:var(--bright);opacity:0;transition:opacity .3s}
.nav-links a[aria-current="true"]{color:#fff}
.nav-links a[aria-current="true"]::after{opacity:1}

.nav-right{display:flex;align-items:center;gap:10px}
/* the readout window: the same recessed cell with inset side rules that the
   indexing rail uses for its station number */
.nav-tel{display:flex;align-items:center;height:46px;padding:0 clamp(13px,1.5vw,20px);
  background:var(--steel-3);box-shadow:var(--bevel-in);text-decoration:none;
  font-family:'Saira Condensed',sans-serif;font-weight:700;font-size:20px;
  letter-spacing:.06em;color:var(--bright);white-space:nowrap;
  font-variant-numeric:tabular-nums;transition:color .22s,background .22s}
.nav-tel:hover{color:#fff;background:#070B11}
/* the key stands proud of the channel beside it */
.navkey{height:46px;padding:0 clamp(15px,1.9vw,26px);font-size:17px;gap:0}

/* a machined key, not an outlined square */
.burger{display:none;width:46px;height:46px;border:0;border-radius:0;padding:0;
  background:var(--steel-3);box-shadow:var(--bevel-in);margin-left:auto;cursor:pointer}
.burger i{display:block;width:19px;height:2.5px;background:var(--bright);margin:0 auto;
  position:relative;transition:background .3s}
.burger i::before,.burger i::after{content:"";position:absolute;left:0;width:19px;height:2.5px;
  background:var(--bright);transition:transform .3s}
.burger i::before{top:-6.5px}.burger i::after{top:6.5px}
.burger[aria-expanded="true"] i{background:transparent}
.burger[aria-expanded="true"] i::before{transform:translateY(6.5px) rotate(45deg)}
.burger[aria-expanded="true"] i::after{transform:translateY(-6.5px) rotate(-45deg)}"""

rep(OLD, NEW, 'nav css')

# the plate is opaque now, so the later glazing override has to go
rep("""/* the sticky nav is glazing too */
.nav{
  background:linear-gradient(180deg,rgba(12,17,25,.72),rgba(12,17,25,.56));
  backdrop-filter:blur(20px) saturate(160%);
  -webkit-backdrop-filter:blur(20px) saturate(160%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.10);
}
.nav.stuck{background:linear-gradient(180deg,rgba(12,17,25,.9),rgba(12,17,25,.78))}
""", "", 'drop the glazing override')

rep("""  .nav,.nav.stuck{background:rgba(12,17,25,.98);backdrop-filter:none;-webkit-backdrop-filter:none}""",
    """  /* the nav is an opaque plate, so it has nothing to opt out of */""",
    'drop the transparency opt out')

rep("""@media (max-width:1010px){
  .nav-tel{display:none}
  .nav-links{gap:22px;font-size:14px}
}
@media (max-width:860px){
  .nav-links{gap:15px;font-size:13px}
}""",
"""@media (max-width:1060px){
  .nav-tel{display:none}
  .nav-links a{padding:0 13px;font-size:16px}
}
@media (max-width:900px){
  .nav-links a{padding:0 10px;font-size:15px;letter-spacing:.06em}
  .navkey{font-size:15px;padding:0 15px}
}""", 'nav breakpoints')

# ------------------------------------------------------------- MARKUP ------
rep("""<header class="nav" id="nav">
  <div class="wrap nav-in">
    <a class="brand" href="#top">East Valley<em>.</em></a>
    <nav class="nav-links" aria-label="Primary">
      <a href="#services">Services</a><a href="#work">Recent work</a><a href="#reviews">Reviews</a><a href="#area">Areas</a>
    </nav>
    <div class="nav-right">
      <a class="nav-tel" href="tel:+14808069455">480-806-9455</a>
      <a class="btn" href="#estimate"><span>Free estimate</span></a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i></button>
  </div>
</header>""",
"""<header class="nav" id="nav">
  <div class="wrap nav-in bolts"><span class="b2"></span><span class="b3"></span>
    <a class="brand" href="#top">East Valley<em>.</em></a>
    <nav class="nav-links" id="navlinks" aria-label="Primary">
      <a href="#services">Services</a><a href="#work">Recent work</a><a href="#reviews">Reviews</a><a href="#area">Areas</a>
    </nav>
    <div class="nav-right">
      <a class="nav-tel" href="tel:+14808069455">480-806-9455</a>
      <a class="btn navkey" href="#estimate"><span>Free estimate</span></a>
    </div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i></button>
  </div>
</header>""", 'nav markup')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
