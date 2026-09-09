# -*- coding: utf-8 -*-
# Finishing the 02 gate.
#
# 1. "RECENT WORK" wrapped to two lines inside the gate. The old bar had the
#    links in a flex row that could not wrap; the gate can, so they need to be
#    told not to.
# 2. The light on the pane has to move, or it is a tint. One passive
#    pointermove, coalesced into a single animation frame, writing --gx and
#    --gi. Dim at rest, which is also what keeps the labels legal against a
#    bright frame of the photograph.
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


rep(""".nav-links{display:flex;align-items:center;gap:clamp(14px,1.7vw,26px)}""",
    """.nav-links{display:flex;align-items:center;gap:clamp(14px,1.7vw,26px);white-space:nowrap}""",
    'links do not wrap')

# find the inline script's stuck-observer line and hang the pointer light off it
anchor = """  var b=document.getElementById('burger'),d=document.getElementById('drawer');"""
JS = """  /* the light on the gate. A pane in the sun has a hot spot that moves as
     you move, and a tint that does not is just a dark rectangle. One passive
     listener, coalesced into a single frame, and dim again the moment the
     pointer leaves. */
  (function(){
    var g=document.getElementById('gate');
    if(!g || !matchMedia('(hover:hover)').matches) return;
    if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    var raf=0,px=0;
    g.addEventListener('pointermove',function(e){
      px=e.clientX; if(raf) return;
      raf=requestAnimationFrame(function(){
        raf=0;
        var r=g.getBoundingClientRect();
        g.style.setProperty('--gx',(((px-r.left)/r.width)*100).toFixed(1)+'%');
        g.style.setProperty('--gi','1');
      });
    },{passive:true});
    g.addEventListener('pointerleave',function(){ g.style.setProperty('--gi','0'); });
  })();
"""
rep(anchor, JS + anchor, 'pointer light')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
