# -*- coding: utf-8 -*-
# Found at 940 by screenshotting the band above the hamburger breakpoint, which
# is exactly where the house rules say to look: SERVICES was clipped to CES.
#
# The reason is structural rather than a stray pixel. This nav only gets HALF
# the bar, because the gate stands on the photograph and the photograph is half
# the page. Measured at 940: the four labels plus the key want about 545px and
# half the bar is 470px. A full width bar would have coped; a split one cannot.
#
# So the links hand over to the drawer a long way above the usual breakpoint,
# at 1180, and the drawer has to exist that high up too. The estimate key
# stays, because a bar with no way to act on it is worse than a bar with no
# links.
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


rep("""/* ---------- responsive ---------- */
/* the nav has to hold one line. Between 760 and 1010 it did not,
   so the phone link steps out first. It is still in the hero, the
   drawer and the footer. */
@media (max-width:1010px){
  .nav-tel{display:none}
  .nav-links{gap:22px;font-size:14px}
}
@media (max-width:860px){
  .nav-links{gap:15px;font-size:13px}
  /* measured: between 760 and 860 the three children want 715px and the row's
     content box is 687, so the brand and the links were being squeezed until
     they wrapped mid-word. The 28px comes back out of the gutters, not out of
     the type. */
  .nav-in{gap:16px}
  .nav-right{margin-left:12px;gap:16px}
}""",
"""/* ---------- responsive ---------- */
/* The bar only gets HALF the width, because the gate stands on the photograph
   and the photograph is half the page. Measured at 940: the four labels plus
   the estimate key want about 545px and half the bar is 470px, so SERVICES was
   being clipped to CES by the gate's own overflow. A full width bar would have
   coped down to 860; a split one cannot.

   So the links hand over to the drawer at 1180, which is a long way above the
   usual hamburger breakpoint and is the honest consequence of the archetype.
   The key stays: a bar you cannot act on is worse than a bar with no links. */
@media (max-width:1320px){
  .nav-tel{display:none}
}
@media (max-width:1180px){
  .nav-links{display:none}
  .burger{display:grid;place-items:center}
  .drawer{display:block;position:fixed;inset:var(--navh,84px) 0 auto 0;z-index:59;
    background:var(--bg-2);border-bottom:1px solid var(--line);
    padding:10px var(--pad) 26px;transform:translateY(-130%);
    transition:transform .44s cubic-bezier(.16,1,.3,1)}
  .drawer.open{transform:translateY(0)}
  .drawer a{display:block;padding:16px 0;border-bottom:1px solid var(--line);text-decoration:none;
    font-family:'Big Shoulders Display',sans-serif;font-weight:700;font-size:26px;
    text-transform:uppercase;letter-spacing:.04em}
  .drawer .btn{width:100%;justify-content:center;margin-top:20px}
}""", 'nav hands over at 1180')

# the 760 block no longer needs to declare what 1180 already has
rep("""@media (max-width:760px){
  body{font-size:16px}
  .nav{background:rgba(7,12,20,.9);backdrop-filter:blur(12px)}
  .nav-links,.nav-right{display:none}
  .burger{display:grid;place-items:center}
  .drawer{display:block;position:fixed;inset:var(--navh,84px) 0 auto 0;z-index:59;background:var(--bg-2);border-bottom:1px solid var(--line);padding:10px var(--pad) 26px;transform:translateY(-130%);transition:transform .44s cubic-bezier(.16,1,.3,1)}
  .drawer.open{transform:translateY(0)}
  .drawer a{display:block;padding:16px 0;border-bottom:1px solid var(--line);text-decoration:none;
    font-family:'Big Shoulders Display',sans-serif;font-weight:700;font-size:26px;text-transform:uppercase;letter-spacing:.04em}
  .drawer .btn{width:100%;justify-content:center;margin-top:20px}""",
"""@media (max-width:760px){
  body{font-size:16px}
  .nav{background:rgba(7,12,20,.9);backdrop-filter:blur(12px)}
  .nav-right{display:none}""", 'drop what 1180 already declares')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
