# -*- coding: utf-8 -*-
import sys

FIT_JS = """  /* Solve for the step that makes the row span exactly the width inside the
     gutter, then drop a rank if that would crowd the cards. Deriving it is the
     only way the deck reaches both edges at every viewport; a fixed step
     leaves a band of dead space on a wide screen. */
  function fit(W,A){
    for(var D=MAXD;D>=1;D--){
      var sw=[],B=[0],k;
      for(k=0;k<=D;k++) sw[k]=W*SC[k];
      for(k=1;k<=D;k++) B[k]=B[k-1]+(sw[k-1]+sw[k])/2;
      var g=(A-2*B[D]-sw[D])/(2*D);
      if(g>=W*LMIN||D===1) return {D:D,g:Math.max(W*LMIN,Math.min(g,W*LMAX)),B:B};
    }
  }

  function place(){
    if(wide.matches){
      var W=slides[cur].offsetWidth, cs=getComputedStyle(deck), k;
      var A=deck.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
      var f=fit(W,A), DEPTH=f.D, xs=[0];
      for(k=1;k<=DEPTH;k++) xs[k]=f.B[k]+k*f.g;
      slides.forEach(function(el,i){
        var o=i-cur; if(o>n/2)o-=n; if(o<-n/2)o+=n;
        var a=Math.abs(o), d=Math.min(a,DEPTH);"""

CONF = {
 '02-broadsheet.html': dict(
   sc="  var SC=[1,.84,.70,.58];\n  var MAXD=Math.min(3,Math.floor((n-1)/2)), LMIN=-.26, LMAX=.10;",
   old_sc="  var SC=[1,.84,.70], LAP=-.15, DEPTH=2;",
   old_place="""  function place(){
    if(wide.matches){
      var W=slides[cur].offsetWidth, xs=[0], k;
      for(k=1;k<=DEPTH;k++) xs[k]=xs[k-1]+W*(SC[k-1]+SC[k])/2+W*LAP;
      slides.forEach(function(el,i){
        var o=i-cur; if(o>n/2)o-=n; if(o<-n/2)o+=n;
        var a=Math.abs(o), d=Math.min(a,DEPTH);""",
   old_css=""".deck{--dw:clamp(196px,23vw,320px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 auto clamp(72px,9vw,126px);touch-action:pan-y}""",
   new_css=""".deck{--dw:clamp(196px,24vw,430px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 0 clamp(72px,9vw,126px);
  padding-inline:var(--gut);touch-action:pan-y;overflow-x:clip;overflow-y:visible}"""),
 '03-hazard.html': dict(
   sc="  var SC=[1,.82,.66,.52];\n  var MAXD=Math.min(3,Math.floor((n-1)/2)), LMIN=-.24, LMAX=.10;",
   old_sc="  var SC=[1,.82,.66], LAP=-.08, DEPTH=2;",
   old_place="""  function place(){
    if(wide.matches){
      var W=slides[cur].offsetWidth, xs=[0], k;
      for(k=1;k<=DEPTH;k++) xs[k]=xs[k-1]+W*(SC[k-1]+SC[k])/2+W*LAP;
      slides.forEach(function(el,i){
        var o=i-cur; if(o>n/2)o-=n; if(o<-n/2)o+=n;
        var a=Math.abs(o), d=Math.min(a,DEPTH);""",
   old_css=""".deck{--dw:clamp(188px,22vw,312px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 auto clamp(58px,7.2vw,102px);touch-action:pan-y}
.deck::before{content:"";content:"";position:absolute;left:50%;translate:-50% 0;bottom:-1px;height:1px;
  width:min(calc(100% + var(--gut) * 1.2),1320px);background:var(--line2)}""",
   new_css=""".deck{--dw:clamp(188px,23vw,420px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 0 clamp(58px,7.2vw,102px);
  padding-inline:var(--gut);touch-action:pan-y;overflow-x:clip;overflow-y:visible}
.deck::before{content:"";position:absolute;left:var(--gut);right:var(--gut);bottom:-1px;height:1px;
  background:var(--line2)}"""),
}

for p, c in CONF.items():
    s = open(p, encoding='utf-8').read(); done = []
    def rep(old, new, label):
        global s
        if old not in s:
            print('!! MISS [%s]:' % p, label); return
        s = s.replace(old, new, 1); done.append(label)

    rep(c['old_css'], c['new_css'], 'deck css')
    rep(c['old_sc'], c['sc'], 'scale table')
    rep(c['old_place'], FIT_JS, 'fit')

    # header and controls stay in the centre column, the deck does not
    rep("""    </ul>

    <div class="deck" data-deck""",
        """    </ul>
  </div>

    <div class="deck" data-deck""", 'close wrap before deck')
    rep("""    </div>

    <div class="deck-bar">""",
        """    </div>

  <div class="wrap">
    <div class="deck-bar">""", 'open wrap after deck')

    # the rail no longer needs to break out: the deck is already full width
    rep("""    scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:4px;
    margin-inline:calc(var(--gut) * -1);padding-inline:var(--gut)}""",
        """    scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:4px;
    overflow-y:visible;padding-inline:var(--gut)}""", 'rail bleed d2')
    rep("""    scroll-snap-type:x mandatory;scrollbar-width:none;
    margin-inline:calc(var(--gut) * -1);padding-inline:var(--gut)}""",
        """    scroll-snap-type:x mandatory;scrollbar-width:none;
    overflow-y:visible;padding-inline:var(--gut)}""", 'rail bleed d3')

    open(p, 'w', encoding='utf-8').write(s)
    print(p, len(done), 'edits ->', ', '.join(done))
