# -*- coding: utf-8 -*-
# Two things a real click on the burger found that a screenshot of the bar
# alone never would.
#
# 1. 01: the estimate cell runs 9px proud of the block's bottom rule, and
#    offsetHeight does not count a child's negative margin, so --navh came out
#    9px short and the teal cell sat on top of the drawer's first row. The
#    observer now measures to the furthest child edge.
#
# 2. 02: the seam and the gate are the SPLIT. Below 900 the splits collapse to
#    one column and there is no split behind the bar any more, so a seam at
#    50% marks nothing and the gate is a lighter rectangle over a dark ground,
#    which is the one thing glass must never be. Both come off at exactly the
#    breakpoint the splits do.
p = '01-mesic.html'
s = open(p, encoding='utf-8').read()
old = """    function set(){ document.documentElement.style.setProperty('--navh', n.offsetHeight+'px'); }"""
new = """    function set(){
      /* the estimate cell runs proud of the block's bottom rule and
         offsetHeight does not count that, so measure to the furthest edge */
      var h=n.offsetHeight, nb=n.getBoundingClientRect().bottom;
      [].forEach.call(n.querySelectorAll('.tb-cta'),function(el){
        h=Math.max(h, h + (el.getBoundingClientRect().bottom - nb));
      });
      document.documentElement.style.setProperty('--navh', Math.round(h)+'px');
    }"""
assert old in s, '01 observer'
open(p, 'w', encoding='utf-8').write(s.replace(old, new, 1))
print('01-mesic.html  navh measures to the proud edge')

p = '02-site.html'
s = open(p, encoding='utf-8').read()
anchor = """@media (max-width:900px){"""
assert anchor in s, '02 breakpoint'
add = """/* Below 900 the splits collapse to one column, so there is no split behind
   the bar for the seam to mark and nothing bright behind the gate for its
   tint to read against. Both come off at the same breakpoint the splits do,
   and the bar becomes one row. */
@media (max-width:900px){
  .nav-in{grid-template-columns:1fr;height:74px}
  .nav-in::after{display:none}
  .gate{background:none;box-shadow:none;backdrop-filter:none;-webkit-backdrop-filter:none;
    padding-left:0;padding-right:var(--pad);justify-content:flex-end}
  .gate::before{display:none}
  .brand{grid-row:1;grid-column:1;align-self:center}
  .gate{grid-row:1;grid-column:1}
  .nav{background:linear-gradient(180deg,rgba(9,15,26,.72),rgba(9,15,26,.56));
    backdrop-filter:blur(20px) saturate(160%);-webkit-backdrop-filter:blur(20px) saturate(160%);
    box-shadow:inset 0 1px 0 rgba(255,255,255,.13)}
  .navkey{padding:0 18px;font-size:16px}
}
"""
s = s.replace(anchor, add + anchor, 1)
open(p, 'w', encoding='utf-8').write(s)
print('02-site.html   seam and gate come off with the split')
