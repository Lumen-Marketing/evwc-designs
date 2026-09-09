# -*- coding: utf-8 -*-
# Two finishes on the 03 nav plate.
#
# 1. The bolts were on .nav-in, which is inside the 1300px wrap, so on a wide
#    screen four bolt heads floated in the middle of a plate that runs the
#    whole width. A plate is bolted at ITS corners. They move to the header.
#
# 2. The station mark on the channel needs something to mark. An observer
#    lights the link for whichever section is actually on screen, which is
#    the same thing the indexing rail's readout does lower down the page. It
#    is the only coloured mark on the bar and it carries real state.
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


rep("""<header class="nav" id="nav">
  <div class="wrap nav-in bolts"><span class="b2"></span><span class="b3"></span>""",
    """<header class="nav bolts" id="nav"><span class="b2"></span><span class="b3"></span>
  <div class="wrap nav-in">""", 'bolts to the plate corners')

# the plate is a stacking context of its own, so the bolts need to clear the
# recessed channel rather than sit under it
rep(""".nav.stuck{box-shadow:inset 0 1px 0 rgba(255,255,255,.26),""",
    """.nav>.b2,.nav>.b3,.nav::before,.nav::after{z-index:4}
.nav.stuck{box-shadow:inset 0 1px 0 rgba(255,255,255,.26),""", 'bolt stacking')

# ---- the station mark gets something to mark -------------------------------
rep("""  var b=document.getElementById('burger'),d=document.getElementById('drawer');""",
"""  /* the station mark on the channel: whichever section is on screen lights
     its link. Real state, the same readout the indexing rail runs on. */
  (function(){
    var links=[].slice.call(document.querySelectorAll('#navlinks a'));
    if(!links.length || !('IntersectionObserver' in window)) return;
    var secs=links.map(function(a){ return document.querySelector(a.getAttribute('href')); });
    var seen={};
    function paint(){
      var at=-1;
      secs.forEach(function(sec,i){ if(sec && seen[i]) at=i; });
      links.forEach(function(a,i){
        if(i===at) a.setAttribute('aria-current','true');
        else a.removeAttribute('aria-current');
      });
    }
    var o=new IntersectionObserver(function(es){
      es.forEach(function(e){
        var i=secs.indexOf(e.target);
        if(i>-1) seen[i]=e.isIntersecting;
      });
      paint();
    },{rootMargin:'-74px 0px -55% 0px'});
    secs.forEach(function(sec){ if(sec) o.observe(sec); });
  })();
  var b=document.getElementById('burger'),d=document.getElementById('drawer');""",
    'station mark observer')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
