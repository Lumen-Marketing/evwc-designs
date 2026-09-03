# -*- coding: utf-8 -*-
p = '03-hazard.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

DECK_JS = """(function(){
  /* The deck. Plates stand on the bench and scale from the foot, so stepping a
     plate back never lifts it off the baseline. Offsets accumulate from each
     step's scaled width to keep the overlap even. */
  var deck=document.querySelector('[data-deck]'); if(!deck) return;
  var slides=[].slice.call(deck.querySelectorAll('.slide'));
  var tabs=[].slice.call(document.querySelectorAll('.tab'));
  var capN=document.querySelector('.dcap b'), capS=document.querySelector('.dcap span');
  var count=document.querySelector('.dcount');
  var n=slides.length, cur=0, seen=true;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sd=navigator.connection&&navigator.connection.saveData;
  var SC=[1,.82,.66], LAP=-.08, DEPTH=2;
  var wide=matchMedia('(min-width: 761px)');

  function place(){
    if(wide.matches){
      var W=slides[cur].offsetWidth, xs=[0], k;
      for(k=1;k<=DEPTH;k++) xs[k]=xs[k-1]+W*(SC[k-1]+SC[k])/2+W*LAP;
      slides.forEach(function(el,i){
        var o=i-cur; if(o>n/2)o-=n; if(o<-n/2)o+=n;
        var a=Math.abs(o), d=Math.min(a,DEPTH);
        el.classList.toggle('far',a>DEPTH);
        el.style.setProperty('--x',(o<0?-xs[d]:xs[d])+'px');
        el.style.setProperty('--s',SC[d]);
        el.style.zIndex=String(30-d-(a>DEPTH?6:0));
      });
    }else{
      slides.forEach(function(el){
        el.classList.remove('far');
        el.style.removeProperty('--x');el.style.removeProperty('--s');el.style.zIndex='';
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
      if(on||!wide.matches){
        delete v.dataset.off;
        if(seen&&!reduce&&!sd){var pr=v.play(); if(pr&&pr.catch)pr.catch(function(){})}
      } else { v.dataset.off='1'; v.pause(); }
    });
    tabs.forEach(function(b,i){b.setAttribute('aria-selected',i===cur?'true':'false')});
    var el=slides[cur];
    if(capN) capN.textContent=el.getAttribute('data-cap')||'';
    if(capS) capS.textContent=el.getAttribute('data-sub')||'';
    if(count) count.textContent=('0'+(cur+1)).slice(-2)+' / '+('0'+n).slice(-2);
  }

  function go(i){ cur=((i%n)+n)%n; place(); }

  slides.forEach(function(el,i){el.addEventListener('click',function(){ if(wide.matches) go(i) })});
  tabs.forEach(function(b,i){b.addEventListener('click',function(){
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
  var sx=0,st=0,down=false;
  deck.addEventListener('pointerdown',function(e){ if(!wide.matches)return; down=true;sx=e.clientX;st=e.timeStamp });
  deck.addEventListener('pointerup',function(e){
    if(!down)return; down=false;
    var dx=e.clientX-sx, dt=e.timeStamp-st;
    if(Math.abs(dx)>44||Math.abs(dx)/Math.max(dt,1)>0.4) go(cur+(dx<0?1:-1));
  });
  deck.addEventListener('pointercancel',function(){down=false});

  if('IntersectionObserver' in window){
    new IntersectionObserver(function(es){
      var vis=es[0].isIntersecting;
      if(vis!==seen){ seen=vis; if(vis) paint(); }
    },{threshold:.15}).observe(deck);
  }
  wide.addEventListener('change',place);
  addEventListener('resize',place);
  place();
})();

(function(){
  var vids=[].slice.call(document.querySelectorAll('video[data-reel]'));"""

rep("""(function(){
  var vids=[].slice.call(document.querySelectorAll('video[data-reel]'));""", DECK_JS, 'deck js')

rep("""    if(e.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){})}else{v.pause()}""",
    """    if(e.isIntersecting&&!v.dataset.off){var p=v.play();if(p&&p.catch)p.catch(function(){})}else{v.pause()}""",
    'io respects deck')

open(p, 'w', encoding='utf-8').write(s)
print('D3 deck js:', len(done), 'edits ->', ', '.join(done))
