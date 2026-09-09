# -*- coding: utf-8 -*-
# The mobile drawer drops from a hard coded pixel offset that was the old nav
# height: 70px on 01 and 76px on 02. The new bars measure 79 to 81 and 84, and
# 02's tightens to 70 the moment you leave the top, so a fixed number is wrong
# in both directions.
#
# A ResizeObserver on the bar writes its real height into --navh, which also
# catches 02's stuck transition without a scroll listener.
import io

JOBS = [
    ('01-mesic.html', 'inset:70px 0 auto 0', 70),
    ('02-site.html',  'inset:76px 0 auto 0', 84),
    ('03-plate.html', 'inset:74px 0 auto 0', 74),
]

JS = """  /* the drawer drops from under the bar, and the bar is not a fixed height:
     01's brand steps down at 560 and 02's whole bar tightens off the top of
     the page. A ResizeObserver keeps --navh honest without a scroll listener. */
  (function(){
    var n=document.getElementById('nav');
    if(!n) return;
    function set(){ document.documentElement.style.setProperty('--navh', n.offsetHeight+'px'); }
    set();
    if('ResizeObserver' in window) new ResizeObserver(set).observe(n);
    else addEventListener('resize', set);
  })();
"""

ANCHOR = "  var b=document.getElementById('burger'),d=document.getElementById('drawer');"

for path, old_inset, fallback in JOBS:
    s = open(path, encoding='utf-8').read()
    done = []
    new_inset = 'inset:var(--navh,%dpx) 0 auto 0' % fallback
    if old_inset in s:
        s = s.replace(old_inset, new_inset, 1); done.append('drawer offset')
    else:
        print('!! MISS drawer offset', path)
    if ANCHOR in s:
        s = s.replace(ANCHOR, JS + ANCHOR, 1); done.append('navh observer')
    else:
        print('!! MISS anchor', path)
    open(path, 'w', encoding='utf-8').write(s)
    print('%-15s %s' % (path, ', '.join(done)))
