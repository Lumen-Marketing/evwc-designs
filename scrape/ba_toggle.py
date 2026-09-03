# -*- coding: utf-8 -*-
# Two changes to 01-daylight:
#   1. The statement band was type on black with nothing to look at. A wide plate
#      of the work goes under the claim and the four figures step up onto it.
#   2. The before and after was two static pictures side by side, which does not
#      explain itself. It becomes one frame you switch.
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ----------------------------------------------------- 1. statement band ----
rep("""/* four figures, every one of them checkable: the Google rating and its count,
   the number of services, the towns covered, and what an estimate costs */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(10px,1.3vw,18px);
  margin-top:clamp(44px,5.4vw,78px)}""",
"""/* a wide plate of the work under the claim. The figures then step up onto its
   bottom edge, so the two planes overlap instead of sitting in a stack: the
   occlusion is this direction's depth device doing a job. */
.sband{position:relative;margin:clamp(34px,4.4vw,64px) 0 0;border-radius:22px;overflow:hidden;
  aspect-ratio:16/7;background:var(--bg-2);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.09),var(--rim)}
.sband img{width:100%;height:100%;object-fit:cover;object-position:50% 44%;
  filter:saturate(.92) contrast(1.05)}
.sband::after{content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,rgba(8,9,10,.2),transparent 30%,rgba(8,9,10,.55) 72%,rgba(8,9,10,.9))}
/* four figures, every one of them checkable: the Google rating and its count,
   the number of services, the towns covered, and what an estimate costs */
.stats{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
  gap:clamp(10px,1.3vw,18px);margin-top:clamp(-78px,-6.4vw,-44px)}""", 'stats css')

rep("""  <div class="stats">""",
"""  <figure class="sband rv"><img src="assets/job-pole-wide.jpg" alt="A water-fed pole extended to the top of a commercial storefront, two cleaners working below it" loading="lazy" width="1280" height="722"></figure>
  <div class="stats">""", 'band markup')

# --------------------------------------------------- 2. before and after ----
rep("""/* the plate: two halves of one object, split by a seam, labelled at opposite corners */
.dip{margin:0 auto;max-width:clamp(292px,50vw,600px)}
.dip-in{padding:7px;border-radius:20px;background:linear-gradient(168deg,#2a2e30,#131517);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.1),var(--rim)}
.dip-g{display:grid;grid-template-columns:1fr 1fr;gap:2px;border-radius:13px;overflow:hidden;
  background:rgba(255,255,255,.16)}
.dip-g figure{margin:0;position:relative;aspect-ratio:4/5;overflow:hidden;background:var(--bg-2)}
.dip-g img{width:100%;height:100%;object-fit:cover}
.dip-g figcaption{position:absolute;inset:auto 0 0 0;padding:30px 13px 11px;font-size:12px;
  letter-spacing:.15em;text-transform:uppercase;color:#e9edee;
  background:linear-gradient(180deg,transparent,rgba(7,8,9,.88))}
.dip-g figure+figure figcaption{text-align:right;color:var(--acc)}
.dcap{margin:15px 0 0;text-align:center;font-size:13.5px;color:#777e81}""",
"""/* one frame, switched. Side by side never explained itself, and a wipe slider
   is not available: the two shots were taken from slightly different positions,
   so a moving seam would tear the window frame in half. Swapping the whole
   picture is the honest version, and the outgoing frame blurs on its way out so
   the eye reads one transformation rather than two photographs trading places. */
.ba{margin:0 auto;max-width:clamp(288px,46vw,560px)}
.ba-in{padding:8px;border-radius:22px;background:linear-gradient(168deg,#2a2e30,#131517);
  box-shadow:var(--lift-3),0 0 0 1px rgba(255,255,255,.1),var(--rim)}
.ba-frame{position:relative;display:block;width:100%;margin:0;padding:0;border:0;cursor:pointer;
  border-radius:15px;overflow:hidden;background:var(--bg-2);aspect-ratio:4/5;
  -webkit-tap-highlight-color:transparent}
.ba-frame img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  transition:opacity .52s var(--ez-out),filter .52s var(--ez-out),transform .52s var(--ez-out)}
.ba-frame img[data-off]{opacity:0;filter:blur(8px);transform:scale(1.025)}
.ba-frame::after{content:"";position:absolute;inset:auto 0 0 0;height:38%;pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(7,8,9,.82))}
.ba-tag{position:absolute;z-index:2;left:clamp(14px,2.4vw,20px);bottom:clamp(12px,2vw,17px);
  font-size:12.5px;letter-spacing:.2em;text-transform:uppercase;color:#e9edee;
  text-shadow:0 1px 12px rgba(0,0,0,.95);transition:color .4s var(--ez-out)}
.ba-tag.is-after{color:var(--acc)}
.ba-ctl{display:flex;justify-content:center;margin-top:clamp(16px,2vw,24px)}
.ba-seg{display:inline-flex;padding:5px;border-radius:999px;background:var(--bg-2);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.11),var(--lift-1)}
.ba-seg button{appearance:none;border:0;background:transparent;color:var(--fg-2);
  font-family:var(--b);font-size:12.5px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;
  padding:12px clamp(20px,2.6vw,32px);min-height:44px;border-radius:999px;cursor:pointer;
  transition:background .35s var(--ez-out),color .35s var(--ez-out)}
.ba-seg button:hover{color:var(--fg)}
.ba-seg button[aria-pressed="true"]{background:var(--acc);color:var(--acc-ink)}
.dcap{margin:15px 0 0;text-align:center;font-size:13.5px;color:#777e81}""", 'ba css')

rep("""  <figure class="dip rv">
    <div class="dip-in">
      <div class="dip-g">
        <figure><img src="assets/ba-before.jpg" alt="A commercial glass frontage before cleaning, the panes hazy with dust and hard water film" loading="lazy" width="390" height="488"><figcaption>Before</figcaption></figure>
        <figure><img src="assets/ba-after.jpg" alt="The same frontage after cleaning, the panes clear and reflecting the sky" loading="lazy" width="390" height="488"><figcaption>After</figcaption></figure>
      </div>
    </div>
    <figcaption class="dcap">Storefront glazing, Mesa</figcaption>
  </figure>""",
"""  <figure class="ba rv">
    <div class="ba-in">
      <button class="ba-frame" type="button" aria-label="Showing the glass after cleaning. Press to see it before.">
        <img data-state="before" data-off src="assets/ba-before.jpg" alt="A commercial glass frontage before cleaning, the panes hazy with dust and hard water film" loading="lazy" width="390" height="488">
        <img data-state="after" src="assets/ba-after.jpg" alt="The same frontage after cleaning, the panes clear and reflecting the sky" loading="lazy" width="390" height="488">
        <span class="ba-tag is-after" aria-live="polite">After</span>
      </button>
    </div>
    <div class="ba-ctl">
      <div class="ba-seg">
        <button type="button" data-state="before" aria-pressed="false">Before</button>
        <button type="button" data-state="after" aria-pressed="true">After</button>
      </div>
    </div>
    <figcaption class="dcap">Storefront glazing, Mesa</figcaption>
  </figure>""", 'ba markup')

# ---------------------------------------------------------------- script ----
rep("""</script>""",
"""
/* before and after. The picture plays itself through once when it first comes
   into view, because a control nobody presses explains nothing; after that it
   belongs to the visitor and the auto pass never runs again. */
(function(){
  var ba = document.querySelector('.ba');
  if (!ba) return;
  var frame = ba.querySelector('.ba-frame');
  var imgs  = [].slice.call(ba.querySelectorAll('.ba-frame img'));
  var tag   = ba.querySelector('.ba-tag');
  var btns  = [].slice.call(ba.querySelectorAll('.ba-seg button'));
  var cur = 'after', touched = false, timer = null;

  function set(state){
    cur = state;
    imgs.forEach(function(im){
      if (im.dataset.state === state) im.removeAttribute('data-off');
      else im.setAttribute('data-off','');
    });
    btns.forEach(function(b){ b.setAttribute('aria-pressed', String(b.dataset.state === state)); });
    tag.textContent = state === 'after' ? 'After' : 'Before';
    tag.classList.toggle('is-after', state === 'after');
    frame.setAttribute('aria-label', state === 'after'
      ? 'Showing the glass after cleaning. Press to see it before.'
      : 'Showing the glass before cleaning. Press to see it after.');
  }
  function stop(){ touched = true; if (timer) { clearTimeout(timer); timer = null; } }

  btns.forEach(function(b){ b.addEventListener('click', function(){ stop(); set(b.dataset.state); }); });
  frame.addEventListener('click', function(){ stop(); set(cur === 'after' ? 'before' : 'after'); });

  var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
  if (!reduce && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if (!e.isIntersecting || touched) return;
        io.disconnect();
        set('before');
        timer = setTimeout(function(){ if (!touched) set('after'); }, 1150);
      });
    }, { threshold: .5 });
    io.observe(ba);
  }
})();
</script>""", 'ba script')

open(p, 'w', encoding='utf-8').write(s)
print('ba+band:', len(done), 'edits ->', ', '.join(done))
