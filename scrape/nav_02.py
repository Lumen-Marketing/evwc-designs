# -*- coding: utf-8 -*-
# 02 SITE, the nav: it splits at the seam.
#
# This page's whole archetype is the split screen: a vertical seam down the
# middle with copy on one side and the picture on the other, section after
# section. The nav was the one element that ignored it. It was a bar laid
# across the top, and it was the SAME bar 03 was using, byte for byte in the
# markup.
#
# So the nav joins the archetype:
#
#   the seam    the hero's split line carried up to the top of the window, so
#               the bar reads as part of the page rather than a lid on it.
#   left half   the wordmark on the dark plane, on the same left margin as the
#               h1 below it. No ground at all: there is nothing there to sit on.
#   right half  a FILM GATE over the photograph: smoked glass, lit on the top
#               face only, with the highlight tracking the pointer. Glass over
#               a photograph is glass. The left half is dark ground, which is
#               exactly where a tint reads as a rectangle instead, so it does
#               not get one.
#   the key     the estimate runs flush into the corner of the window at full
#               bar height, so the accent lands on a surface rather than on a
#               small element.
#
# Off the top of the page there is no split behind it any more, so the gate
# gives its glass up to the whole bar and the bar tightens. That is the state
# change: you have left the hero.
p = '02-site.html'
s = open(p, encoding='utf-8').read()
done = []


def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label)
        return
    s = s.replace(old, new, 1)
    done.append(label)


OLD = """.nav{position:fixed;top:0;left:0;right:0;z-index:60;transition:background .35s,border-color .35s;border-bottom:1px solid transparent}
.nav.stuck{background:rgba(7,12,20,.94);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom-color:var(--line)}
.nav-in{height:76px;display:flex;align-items:center;gap:28px}
.brand{text-decoration:none;font-family:'Big Shoulders Display',sans-serif;font-weight:900;font-size:25px;letter-spacing:.05em;text-transform:uppercase;line-height:1}
.brand em{font-style:normal;color:var(--blue)}
.nav-links{display:flex;gap:28px;margin-left:auto}"""

NEW = """/* ---------- NAV: it splits at the seam ----------
   Every section on this page is a split screen. The nav was the one thing
   laid across the top of them, and it was the same bar 03 was using. It is
   now built out of the archetype instead: the seam runs up through it, the
   wordmark stands on the dark plane and the controls stand on the picture
   inside a smoked gate.

   The gate is the only part of the bar with a ground, because it is the only
   part with a photograph behind it. A tint over the dark left plane would be
   a rectangle, not glass. */
.nav{position:fixed;top:0;left:0;right:0;z-index:60;
  transition:background .35s,box-shadow .35s,backdrop-filter .35s}
.nav-in{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);
  align-items:stretch;height:84px;position:relative;
  transition:height .35s cubic-bezier(.16,1,.3,1)}
/* the seam, carried up from the hero */
.nav-in::after{content:"";position:absolute;left:50%;top:0;bottom:0;width:1px;
  background:var(--line);z-index:3;transition:opacity .35s}

.brand{align-self:center;justify-self:start;padding-left:clamp(24px,5vw,90px);
  text-decoration:none;font-family:'Big Shoulders Display',sans-serif;font-weight:900;
  font-size:clamp(23px,1.9vw,28px);letter-spacing:.05em;text-transform:uppercase;line-height:1}
.brand em{font-style:normal;color:var(--blue)}

/* the gate */
.gate{position:relative;isolation:isolate;overflow:hidden;
  display:flex;align-items:stretch;justify-content:flex-end;
  gap:clamp(12px,1.9vw,30px);padding-left:clamp(16px,2vw,34px);
  --gx:72%; --gi:0;
  background:linear-gradient(180deg,rgba(7,12,20,.60),rgba(7,12,20,.42));
  backdrop-filter:blur(20px) saturate(190%) brightness(.9);
  -webkit-backdrop-filter:blur(20px) saturate(190%) brightness(.9);
  /* the top face only. An even rim on four sides is a frame, not a material. */
  box-shadow:inset 0 1px 0 rgba(255,255,255,.22),
             inset 0 14px 24px -20px rgba(255,255,255,.5);
  transition:background .35s,box-shadow .35s}
/* the light on the pane, tracking the pointer. Dim at rest, which is also
   what keeps the labels legal against a bright frame. */
.gate::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:radial-gradient(360px 190px at var(--gx) 0%,rgba(255,255,255,.15),transparent 72%);
  opacity:var(--gi);transition:opacity .45s}

.nav-links{display:flex;align-items:center;gap:clamp(14px,1.7vw,26px)}"""

rep(OLD, NEW, 'nav css head')

OLD2 = """.nav-links a::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1.5px;background:var(--blue);transform:scaleX(0);transform-origin:right;transition:transform .32s cubic-bezier(.16,1,.3,1)}
.nav-links a:hover{color:#fff}
.nav-links a:hover::after{transform:scaleX(1);transform-origin:left}
.nav-right{display:flex;align-items:center;gap:22px;margin-left:22px}
.nav-tel{text-decoration:none;font-weight:600;font-size:15px;white-space:nowrap;font-variant-numeric:tabular-nums}
.burger{display:none;width:44px;height:44px;border:1.5px solid rgba(255,255,255,.5);background:none;margin-left:auto;cursor:pointer;border-radius:0}
.burger i{display:block;width:19px;height:1.6px;background:#fff;margin:0 auto;position:relative;transition:background .3s}
.burger i::before,.burger i::after{content:"";position:absolute;left:0;width:19px;height:1.6px;background:#fff;transition:transform .3s}
.burger i::before{top:-6px}.burger i::after{top:6px}"""

NEW2 = """/* the mark sits ABOVE the label, because the underline that sweeps in from
   the right is what 03 does and no two directions share a component */
.nav-links a::after{content:"";position:absolute;left:0;right:0;top:-9px;height:2px;
  background:var(--blue);transform:scaleX(0);transition:transform .3s cubic-bezier(.16,1,.3,1)}
.nav-links a:hover{color:#fff}
.nav-links a:hover::after{transform:scaleX(1)}
.nav-right{display:flex;align-items:stretch;gap:clamp(12px,1.7vw,24px)}
.nav-tel{display:flex;align-items:center;text-decoration:none;font-weight:600;font-size:15px;
  white-space:nowrap;font-variant-numeric:tabular-nums}
/* the key runs flush into the corner of the window at full bar height, so the
   accent lands on a surface rather than on a small element */
.navkey{align-self:stretch;height:auto;padding:0 clamp(20px,2.4vw,38px);border:0;
  font-size:clamp(16px,1.35vw,19px)}
.navkey:hover{transform:none;box-shadow:none}
.burger{display:none;width:52px;border:0;background:none;cursor:pointer;border-radius:0;
  align-self:stretch;padding:0}
.burger i{display:block;width:22px;height:1.6px;background:#fff;margin:0 auto;position:relative;transition:background .3s}
.burger i::before,.burger i::after{content:"";position:absolute;left:0;width:22px;height:1.6px;background:#fff;transition:transform .3s}
.burger i::before{top:-7px}.burger i::after{top:7px}"""

rep(OLD2, NEW2, 'nav css tail')

# the later "sticky nav becomes real glass" override becomes the state change
rep("""/* the sticky nav becomes real glass rather than a flat dark bar */
.nav.stuck{
  background:linear-gradient(180deg,rgba(9,15,26,.66),rgba(9,15,26,.5));
  backdrop-filter:blur(22px) saturate(160%);
  -webkit-backdrop-filter:blur(22px) saturate(160%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14),0 20px 40px -30px #000;
}""",
"""/* Off the top of the page there is no split behind the bar any more, so the
   gate hands its glass to the whole bar and the seam goes with it. The bar
   tightens at the same time: that is the state change, not decoration. */
.nav.stuck{
  background:linear-gradient(180deg,rgba(9,15,26,.68),rgba(9,15,26,.52));
  backdrop-filter:blur(22px) saturate(170%);
  -webkit-backdrop-filter:blur(22px) saturate(170%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.15),0 20px 40px -30px #000;
}
.nav.stuck .nav-in{height:70px}
.nav.stuck .nav-in::after{opacity:0}
.nav.stuck .gate{background:none;box-shadow:none;
  backdrop-filter:none;-webkit-backdrop-filter:none}
.nav.stuck .gate::before{opacity:0}""", 'stuck state')

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
  <div class="nav-in">
    <a class="brand" href="#top">East Valley<em>.</em></a>
    <div class="gate" id="gate">
      <nav class="nav-links" aria-label="Primary">
        <a href="#services">Services</a><a href="#work">Recent work</a><a href="#reviews">Reviews</a><a href="#area">Areas</a>
      </nav>
      <div class="nav-right">
        <a class="nav-tel" href="tel:+14808069455">480-806-9455</a>
        <a class="btn navkey" href="#estimate"><span>Free estimate</span></a>
      </div>
      <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="drawer"><i></i></button>
    </div>
  </div>
</header>""", 'nav markup')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
