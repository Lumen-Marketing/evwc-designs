# -*- coding: utf-8 -*-
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---------------------------------------------------------------- CSS ------
OLD = """/* the stage: two equal bays, one baseline, symmetric about the centre */
.stage{--bay:clamp(184px,24vw,330px);
  position:relative;display:grid;grid-template-columns:repeat(2,minmax(0,var(--bay)));
  justify-content:center;align-items:end;gap:clamp(20px,3.6vw,58px);
  margin-bottom:clamp(86px,10.5vw,146px)}
/* the surface they stand on, fading out equally at both ends */
.stage::before{content:"";position:absolute;left:50%;translate:-50% 0;bottom:0;height:1px;
  width:min(calc(100% + var(--gut) * 1.4),1240px);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.17) 24%,rgba(255,255,255,.17) 76%,transparent)}

.bay{margin:0;position:relative}
/* tray and core, concentric: the core radius is the tray radius less its padding */
.bay-in{padding:7px;border-radius:20px;background:linear-gradient(168deg,#2a2e30,#131517);
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.1),var(--rim);
  transition:transform 420ms var(--ez-out),box-shadow 420ms var(--ez-out)}
.bay .m{position:relative;aspect-ratio:9/16;overflow:hidden;border-radius:13px;background:var(--bg-2);
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.62)}
.bay video,.bay img{width:100%;height:100%;object-fit:cover}
/* the caption lives inside the tray, so a bay is one object rather than a
   card with loose text floating under it */
.bay figcaption{display:flex;align-items:baseline;justify-content:space-between;gap:10px;
  padding:11px 6px 3px;font-size:14px;color:var(--fg)}
.bay figcaption span{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:#767d80;
  white-space:nowrap}
/* the light each lit screen throws down onto the table */
.bay::after{content:"";position:absolute;left:2%;right:2%;top:100%;height:clamp(46px,6.4vw,88px);
  pointer-events:none;background-image:var(--pv);background-size:cover;background-position:center;
  transform:scaleY(-1);filter:blur(10px) saturate(1.2);opacity:.33;
  -webkit-mask-image:radial-gradient(124% 106% at 50% 100%,#000 4%,rgba(0,0,0,.4) 42%,transparent 74%);
  mask-image:radial-gradient(124% 106% at 50% 100%,#000 4%,rgba(0,0,0,.4) 42%,transparent 74%)}
@media (hover:hover) and (pointer:fine){
  .bay:hover .bay-in{transform:translateY(-6px);box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.15),var(--rim)}
}
"""

NEW = """/* the index: every item in the deck, named. Clicking one brings it forward. */
.pills{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;list-style:none;
  margin:0 0 clamp(34px,4.4vw,58px);padding:0}
.pill{appearance:none;font:inherit;font-size:13.5px;line-height:1;cursor:pointer;
  min-height:44px;padding:0 18px;border-radius:800px;background:transparent;color:var(--fg-2);
  border:1px solid rgba(255,255,255,.15);
  transition:background .24s var(--ez-out),color .24s var(--ez-out),border-color .24s var(--ez-out)}
.pill:hover{color:var(--fg);border-color:rgba(255,255,255,.34)}
.pill[aria-selected="true"]{background:var(--fg);color:var(--bg);border-color:var(--fg)}

/* the deck: one card holds focus at full width and its neighbours are clipped
   down to standing slivers, evenly spaced either side of the same centre line.
   Positions come from the visible width of each step, which is the only way to
   keep the gaps even once the cards are narrowed. */
.deck{--dw:clamp(214px,27vw,394px);--dh:calc(var(--dw) * 4 / 3);
  position:relative;height:var(--dh);margin:0 auto;touch-action:pan-y}
/* the surface the deck stands on, fading out equally at both ends */
.deck::before{content:"";position:absolute;left:50%;translate:-50% 0;bottom:0;height:1px;
  width:min(calc(100% + var(--gut) * 1.4),1240px);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.17) 24%,rgba(255,255,255,.17) 76%,transparent)}
/* the light the focused card throws down onto that surface */
.deck::after{content:"";position:absolute;left:50%;translate:-50% 0;top:100%;
  width:calc(var(--dw) * .94);height:clamp(46px,6.2vw,86px);pointer-events:none;
  background-image:var(--pv);background-size:cover;background-position:center;
  transform:scaleY(-1);filter:blur(11px) saturate(1.2);opacity:.32;
  -webkit-mask-image:radial-gradient(124% 106% at 50% 100%,#000 4%,rgba(0,0,0,.4) 42%,transparent 74%);
  mask-image:radial-gradient(124% 106% at 50% 100%,#000 4%,rgba(0,0,0,.4) 42%,transparent 74%)}

.slide{position:absolute;left:50%;top:0;margin:0;width:var(--dw);height:var(--dh);cursor:pointer;
  -webkit-tap-highlight-color:transparent;
  transform:translate3d(calc(-50% + var(--x,0px)),0,0);
  /* drop-shadow rather than box-shadow: it follows the clipped silhouette,
     so a narrowed sliver casts a sliver-shaped shadow */
  filter:drop-shadow(0 8px 16px rgba(0,0,0,.55)) drop-shadow(0 32px 58px rgba(0,0,0,.62));
  transition:transform .66s var(--ez-out),opacity .5s var(--ez-out),filter .5s var(--ez-out)}
.slide.far{opacity:0;pointer-events:none}
.slide.on{cursor:default}
.frame{position:relative;width:100%;height:100%;overflow:hidden;background:var(--bg-2);
  clip-path:inset(0 var(--ci,0%) round var(--cr,18px));
  transition:clip-path .66s var(--ez-out)}
.frame img,.frame video{width:100%;height:100%;object-fit:cover}
/* neighbours sit back in the light rather than competing with the focused card */
.frame::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:rgba(9,10,11,.5);opacity:1;transition:opacity .5s var(--ez-out)}
.slide.on .frame::after{opacity:0}

/* caption, count and the two controls, all on the centre line */
.deck-bar{display:flex;flex-direction:column;align-items:center;gap:clamp(16px,2vw,24px);
  margin-top:clamp(88px,10vw,140px);margin-bottom:clamp(80px,9.5vw,132px)}
.dcap{margin:0;text-align:center}
.dcap b{display:block;font-family:var(--d);font-weight:600;letter-spacing:-.025em;
  font-size:clamp(19px,2.2vw,27px)}
.dcap span{display:block;margin-top:6px;font-size:13.5px;color:var(--fg-2)}
.dctl{display:flex;align-items:center;gap:14px}
.dnav{appearance:none;width:46px;height:46px;border-radius:50%;cursor:pointer;
  background:transparent;color:var(--fg);border:1px solid rgba(255,255,255,.2);
  display:inline-flex;align-items:center;justify-content:center;
  transition:background .2s var(--ez-out),border-color .2s var(--ez-out),transform .16s var(--ez-out)}
.dnav:hover{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.4)}
.dnav:active{transform:scale(.94)}
.dnav svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round}
.dcount{min-width:74px;text-align:center;font-size:12.5px;letter-spacing:.16em;color:#7d8386;
  font-variant-numeric:tabular-nums}
"""
rep(OLD, NEW, 'deck css')

# the deck now carries every one of these photographs, so the separate bento
# underneath it was showing the same work twice
rep("""/* ---------- proof: asymmetric, unequal ---------- */
.proof{display:grid;grid-template-columns:repeat(12,1fr);gap:clamp(12px,1.6vw,22px);padding-bottom:clamp(72px,10vw,148px)}
.proof figure{margin:0;position:relative;overflow:hidden;background:var(--bg-2);border-radius:16px;
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.06);transition:box-shadow .7s var(--ez),transform .7s var(--ez)}
.proof figure:hover{box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.12);transform:translateY(-5px)}
.pb{margin-top:clamp(18px,3vw,52px)}
.proof img{width:100%;height:100%;object-fit:cover;transition:transform .9s var(--ez)}
.proof figure:hover img{transform:scale(1.035)}
.pa{grid-column:span 7;aspect-ratio:4/3}
.pb{grid-column:span 5;aspect-ratio:3/4;align-self:end}
.pc{grid-column:span 5;aspect-ratio:1}
.pd{grid-column:span 7;aspect-ratio:16/10}

""", "", 'drop proof css')

# ------------------------------------------------------------- markup ------
OLD_HTML = """  <div class="stage">
    <figure class="bay rv" style="--pv:url(assets/poster-storefront.jpg)">
      <div class="bay-in">
        <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
        <figcaption>Commercial storefront <span>Mesa</span></figcaption>
      </div>
    </figure>
    <figure class="bay rv" style="--pv:url(assets/poster-solar.jpg)">
      <div class="bay-in">
        <div class="m"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
        <figcaption>Solar array rinse <span>Tile roof</span></figcaption>
      </div>
    </figure>
  </div>
"""

NEW_HTML = """  <ul class="pills rv" role="tablist" aria-label="Recent work">
    <li><button class="pill" role="tab" aria-selected="true">Storefront</button></li>
    <li><button class="pill" role="tab" aria-selected="false">Solar</button></li>
    <li><button class="pill" role="tab" aria-selected="false">Restaurant</button></li>
    <li><button class="pill" role="tab" aria-selected="false">Retail entry</button></li>
    <li><button class="pill" role="tab" aria-selected="false">Junk removal</button></li>
    <li><button class="pill" role="tab" aria-selected="false">The rig</button></li>
  </ul>

  <div class="deck rv" data-deck aria-roledescription="carousel" aria-label="Recent work">
    <figure class="slide" data-cap="Commercial storefront" data-sub="Mesa, exterior glass" data-pv="assets/poster-storefront.jpg">
      <div class="frame"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-storefront.jpg" aria-label="Cleaning a commercial storefront with a water-fed pole"><source src="assets/reel-storefront.mp4" type="video/mp4"></video></div>
    </figure>
    <figure class="slide" data-cap="Solar array rinse" data-sub="Tile roof, panel wash" data-pv="assets/poster-solar.jpg">
      <div class="frame"><video data-reel autoplay muted loop playsinline preload="metadata" poster="assets/poster-solar.jpg" aria-label="Rinsing dust off rooftop solar panels"><source src="assets/reel-solar.mp4" type="video/mp4"></video></div>
    </figure>
    <figure class="slide" data-cap="Restaurant frontage" data-sub="Interior and exterior glass" data-pv="assets/restaurant.jpg">
      <div class="frame"><img src="assets/restaurant.jpg" alt="Looking out through a spotless full height restaurant window onto an Arizona parking lot" loading="lazy" width="1400" height="1750"></div>
    </figure>
    <figure class="slide" data-cap="Retail entry" data-sub="Door and window glass" data-pv="assets/storefront.jpg">
      <div class="frame"><img src="assets/storefront.jpg" alt="A clean glass shopfront with door and window signage" loading="lazy" width="1200" height="1200"></div>
    </figure>
    <figure class="slide" data-cap="Junk removal" data-sub="Yard cleared and hauled away" data-pv="assets/junk.jpg">
      <div class="frame"><img src="assets/junk.jpg" alt="A backyard before and after being cleared of debris" loading="lazy" width="1024" height="1024"></div>
    </figure>
    <figure class="slide" data-cap="The rig" data-sub="Owner operated, ladder racked" data-pv="assets/rig.jpg">
      <div class="frame"><img src="assets/rig.jpg" alt="The work vehicle with a ladder racked on the roof at sunset" loading="lazy" width="1200" height="1200"></div>
    </figure>
  </div>

  <div class="deck-bar rv">
    <p class="dcap" aria-live="polite"><b>Commercial storefront</b><span>Mesa, exterior glass</span></p>
    <div class="dctl">
      <button class="dnav" data-dir="-1" aria-label="Previous item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.5 5.5 8 12l6.5 6.5"/></svg></button>
      <span class="dcount" aria-hidden="true">01 / 06</span>
      <button class="dnav" data-dir="1" aria-label="Next item"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9.5 5.5 16 12l-6.5 6.5"/></svg></button>
    </div>
  </div>
"""
rep(OLD_HTML, NEW_HTML, 'deck html')

rep("""    <p class="sub">Filmed on their own jobs and posted to Instagram. Both clips play here with the sound off.</p>""",
    """    <p class="sub">Their own clips and job photographs, straight off Instagram. The two clips play here with the sound off.</p>""",
    'sub copy')

rep("""<div class="wrap">
  <div class="proof">
    <figure class="pa rv"><img src="assets/restaurant.jpg" alt="Looking out through a spotless full height restaurant window onto an Arizona parking lot" loading="lazy" width="1400" height="1750"></figure>
    <figure class="pb rv"><img src="assets/storefront.jpg" alt="A clean glass shopfront with door and window signage" loading="lazy" width="1200" height="1200"></figure>
    <figure class="pc rv"><img src="assets/junk.jpg" alt="A backyard before and after being cleared of debris" loading="lazy" width="1024" height="1024"></figure>
    <figure class="pd rv"><img src="assets/rig.jpg" alt="The work vehicle with a ladder racked on the roof at sunset" loading="lazy" width="1200" height="1200"></figure>
  </div>
</div>

""", "", 'drop proof markup')

# --------------------------------------------------------- responsive ------
rep("  .stage{grid-template-columns:minmax(0,330px);margin-bottom:clamp(88px,17vw,120px)}\n", "", 'drop stage mq')
rep("  .pa,.pb,.pc,.pd{grid-column:span 12}\n  .pb{aspect-ratio:4/3}\n", "", 'drop proof mq')

rep("""@media (prefers-reduced-motion:reduce){""",
"""/* below this the deck stops being a deck: a swipeable rail is the honest
   control on a touch screen, and every card stays legible */
@media (max-width:760px){
  .deck{height:auto;display:flex;gap:12px;overflow-x:auto;overscroll-behavior-x:contain;
    scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:4px;
    margin-inline:calc(var(--gut) * -1);padding-inline:var(--gut)}
  .deck::-webkit-scrollbar{display:none}
  .deck::before,.deck::after{display:none}
  .slide{position:static;flex:0 0 76%;width:auto;height:auto;scroll-snap-align:center;
    transform:none;opacity:1;filter:drop-shadow(0 10px 24px rgba(0,0,0,.6))}
  .slide.far{opacity:1;pointer-events:auto}
  .frame{aspect-ratio:3/4;height:auto;clip-path:none;border-radius:18px}
  .frame::after{opacity:0}
  .deck-bar{margin-top:clamp(30px,7vw,44px)}
  .dctl .dnav{display:none}
}
@media (prefers-reduced-motion:reduce){""", 'deck mq')

# ------------------------------------------------------------------ JS -----
rep("""/* Play clips only while visible. Save data and reduced motion get a paused
   player with controls rather than autoplay. */
(function(){
  var vids=[].slice.call(document.querySelectorAll('video[data-reel]'));""",
"""/* The deck. One card holds focus; its neighbours are clipped down to slivers.
   Offsets are measured from each step's visible width so the gaps stay even,
   which a plain scale falloff cannot do. Nothing animates but transform,
   opacity and clip-path. */
(function(){
  var deck=document.querySelector('[data-deck]'); if(!deck) return;
  var slides=[].slice.call(deck.querySelectorAll('.slide'));
  var pills=[].slice.call(document.querySelectorAll('.pill'));
  var capN=document.querySelector('.dcap b'), capS=document.querySelector('.dcap span');
  var count=document.querySelector('.dcount');
  var n=slides.length, cur=0;
  var CLIP=[0,32,44], RAD=[18,42,64], GAP=14, DEPTH=2;
  var wide=matchMedia('(min-width: 761px)');

  function place(){
    if(wide.matches){
      var W=slides[cur].offsetWidth, xs=[0], k;
      for(k=1;k<=DEPTH;k++){
        xs[k]=xs[k-1]+(W*(1-2*CLIP[k-1]/100)+W*(1-2*CLIP[k]/100))/2+GAP;
      }
      slides.forEach(function(el,i){
        var o=i-cur; if(o>n/2)o-=n; if(o<-n/2)o+=n;
        var a=Math.abs(o), d=Math.min(a,DEPTH);
        el.classList.toggle('far',a>DEPTH);
        el.style.setProperty('--x',(o<0?-xs[d]:xs[d])+'px');
        el.style.setProperty('--ci',CLIP[d]+'%');
        el.style.setProperty('--cr',RAD[d]+'px');
        el.style.zIndex=String(30-d-(a>DEPTH?6:0));
      });
    }else{
      slides.forEach(function(el){
        el.classList.remove('far');
        el.style.removeProperty('--x');el.style.removeProperty('--ci');
        el.style.removeProperty('--cr');el.style.zIndex='';
      });
    }
    paint();
  }

  function paint(){
    slides.forEach(function(el,i){
      var on=i===cur;
      el.classList.toggle('on',on);
      var v=el.querySelector('video');
      if(!v) return;
      if(on||!wide.matches){ delete v.dataset.off; }
      else { v.dataset.off='1'; v.pause(); }
    });
    pills.forEach(function(b,i){b.setAttribute('aria-selected',i===cur?'true':'false')});
    var s=slides[cur];
    if(capN) capN.textContent=s.getAttribute('data-cap')||'';
    if(capS) capS.textContent=s.getAttribute('data-sub')||'';
    if(count) count.textContent=('0'+(cur+1)).slice(-2)+' / '+('0'+n).slice(-2);
    deck.style.setProperty('--pv','url('+s.getAttribute('data-pv')+')');
  }

  function go(i){ cur=((i%n)+n)%n; place(); }

  slides.forEach(function(el,i){el.addEventListener('click',function(){ if(wide.matches) go(i) })});
  pills.forEach(function(b,i){b.addEventListener('click',function(){
    go(i);
    if(!wide.matches) slides[i].scrollIntoView({block:'nearest',inline:'center',behavior:reduce?'auto':'smooth'});
  })});
  [].slice.call(document.querySelectorAll('.dnav')).forEach(function(b){
    b.addEventListener('click',function(){ go(cur+Number(b.getAttribute('data-dir'))) });
  });
  document.getElementById('reels').addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'){go(cur-1)} else if(e.key==='ArrowRight'){go(cur+1)} else return;
    e.preventDefault();
  });
  /* a flick past the threshold moves one card, the same gesture the rail uses
     on touch, so the two modes do not feel like different components */
  var sx=0,st=0,down=false;
  deck.addEventListener('pointerdown',function(e){ if(!wide.matches)return; down=true;sx=e.clientX;st=e.timeStamp });
  deck.addEventListener('pointerup',function(e){
    if(!down)return; down=false;
    var dx=e.clientX-sx, dt=e.timeStamp-st;
    if(Math.abs(dx)>44||Math.abs(dx)/Math.max(dt,1)>0.4) go(cur+(dx<0?1:-1));
  });
  deck.addEventListener('pointercancel',function(){down=false});

  wide.addEventListener('change',place);
  addEventListener('resize',place);
  place();
})();

/* Play clips only while visible. Save data and reduced motion get a paused
   player with controls rather than autoplay. The deck marks the clips it is
   not showing, so this never wakes one that is parked off to the side. */
(function(){
  var vids=[].slice.call(document.querySelectorAll('video[data-reel]'));""", 'deck js')

rep("""    if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){})}else{v.pause()}""",
    """    if(e.isIntersecting&&!v.dataset.off){var p=v.play();if(p&&p.catch)p.catch(function(){})}else{v.pause()}""",
    'io respects deck')

open(p, 'w', encoding='utf-8').write(s)
print('D1 deck:', len(done), 'edits ->', ', '.join(done))
