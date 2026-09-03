# -*- coding: utf-8 -*-
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---- CSS: the deck breaks the centre column and keeps its own gutter --------
rep(""".deck{--dw:clamp(214px,27vw,394px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 auto;touch-action:pan-y}
/* the surface the deck stands on, fading out equally at both ends */
.deck::before{content:"";position:absolute;left:50%;translate:-50% 0;bottom:0;height:1px;
  width:min(calc(100% + var(--gut) * 1.4),1240px);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.17) 24%,rgba(255,255,255,.17) 76%,transparent)}""",
""".deck{--dw:clamp(200px,27vw,500px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0;padding-inline:var(--gut);touch-action:pan-y}
/* the surface the deck stands on, running the full width inside the gutter */
.deck::before{content:"";position:absolute;left:var(--gut);right:var(--gut);bottom:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.17) 12%,rgba(255,255,255,.17) 88%,transparent)}""",
    'deck css')

# ---- markup: header and controls stay in the column, the deck does not ------
rep("""<section class="reels wrap" id="reels">
  <div class="rhead rv">""",
"""<section class="reels" id="reels">
  <div class="wrap">
  <div class="rhead rv">""", 'open wrap')

rep("""  </ul>

  <div class="deck rv" data-deck""",
"""  </ul>
  </div>

  <div class="deck rv" data-deck""", 'close wrap before deck')

rep("""  </div>

  <div class="deck-bar rv">""",
"""  </div>

  <div class="wrap">
  <div class="deck-bar rv">""", 'open wrap after deck')

rep("""    <figcaption class="dcap">Storefront glazing, Mesa</figcaption>
  </figure>
</section>""",
"""    <figcaption class="dcap">Storefront glazing, Mesa</figcaption>
  </figure>
  </div>
</section>""", 'close trailing wrap')

# ---- the band held the one photograph the deck was missing ------------------
rep("""/* ---------- band ---------- */
""", "", 'band comment')
rep("""<figure class="band" style="margin:0">
  <img src="assets/hero-pole.jpg" alt="A water-fed pole reaching a tall arched window on a tile-roofed Arizona home against a blue sky" loading="lazy" width="1200" height="1600">
  <figcaption>Two storey residential, water-fed pole</figcaption>
</figure>

""", "", 'drop band markup')

rep("""    <li><button class="pill" aria-pressed="false">Retail entry</button></li>""",
"""    <li><button class="pill" aria-pressed="false">Residential</button></li>
    <li><button class="pill" aria-pressed="false">Retail entry</button></li>""", 'residential pill')

rep("""    <figure class="slide" data-cap="Retail entry" data-sub="Door and window glass" data-pv="assets/storefront.jpg">""",
"""    <figure class="slide" data-cap="Two storey residential" data-sub="Water-fed pole, arched glass" data-pv="assets/hero-pole.jpg">
      <div class="frame"><img src="assets/hero-pole.jpg" alt="A water-fed pole reaching a tall arched window on a tile-roofed Arizona home against a blue sky" loading="lazy" width="1200" height="1600"></div>
    </figure>
    <figure class="slide" data-cap="Retail entry" data-sub="Door and window glass" data-pv="assets/storefront.jpg">""",
    'residential slide')

rep('<span class="dcount" aria-hidden="true">01 / 06</span>', '<span class="dcount" aria-hidden="true">01 / 07</span>', 'count')

# ---- JS: derive the gap from the width actually available ------------------
rep("""  var CLIP=[0,32,44], RAD=[18,42,64], GAP=14, DEPTH=2;
  var wide=matchMedia('(min-width: 761px)');

  function place(){
    if(wide.matches){
      var W=slides[cur].offsetWidth, xs=[0], k;
      for(k=1;k<=DEPTH;k++){
        xs[k]=xs[k-1]+(W*(1-2*CLIP[k-1]/100)+W*(1-2*CLIP[k]/100))/2+GAP;
      }
      slides.forEach(function(el,i){
        var o=i-cur; if(o>n/2)o-=n; if(o<-n/2)o+=n;
        var a=Math.abs(o), d=Math.min(a,DEPTH);""",
"""  var CLIP=[0,28,38,44.5], RAD=[18,40,58,74];
  var MAXD=Math.min(3,Math.floor((n-1)/2)), GMIN=.03, GMAX=.18;
  var wide=matchMedia('(min-width: 761px)');

  /* Solve for the gap that makes the row span exactly the width inside the
     gutter, then step down a rank if that would crowd the cards. Deriving it
     is the only way the deck reaches both edges at every viewport; a fixed
     step leaves a gutter of dead space on a wide screen. */
  function fit(W,A){
    for(var D=MAXD;D>=1;D--){
      var vw=[],B=[0],k;
      for(k=0;k<=D;k++) vw[k]=W*(1-2*CLIP[k]/100);
      for(k=1;k<=D;k++) B[k]=B[k-1]+(vw[k-1]+vw[k])/2;
      var g=(A-2*B[D]-vw[D])/(2*D);
      if(g>=W*GMIN||D===1) return {D:D,g:Math.max(W*GMIN,Math.min(g,W*GMAX)),B:B};
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
        var a=Math.abs(o), d=Math.min(a,DEPTH);""",
    'deck js fit')

open(p, 'w', encoding='utf-8').write(s)
print('D1 bleed:', len(done), 'edits ->', ', '.join(done))
