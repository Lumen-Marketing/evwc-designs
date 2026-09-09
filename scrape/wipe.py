# -*- coding: utf-8 -*-
# BEFORE AND AFTER becomes a WIPE on all four, to the reference the client sent.
#
# One caveat, stated once and then built anyway because he has now seen the
# device and asked for it: these two frames were taken from slightly different
# camera positions (a scale sweep and phase cross correlation put them at NCC
# -0.04), so the mullions do not line up across the seam. The reference has the
# same property, a truck shot head on against the same truck shot from the side,
# and it works because the divider is a hard line rather than a pretence that
# the two halves are one continuous photograph. So the divider here is a hard
# rule with a handle on it, and the labels name both sides.
#
# The MECHANISM is shared across the four, which is the one time that is right:
# the client asked for this specific control. The frame, the divider, the handle
# and the labels stay in each direction's own material.

BASE = """/* ---------- BEFORE AND AFTER: a wipe ----------
   The divider is a hard rule, not a blend. The two frames were shot from
   slightly different positions, so pretending they are one continuous
   photograph would tear the window frame across the seam; a rule with a handle
   on it says "two pictures, drag between them" and is honest about it.

   The control is a real <input type="range"> covering the whole box at zero
   opacity. Pointer drag, touch drag, arrow keys, Home and End and the screen
   reader announcement all come from the browser, and there is no drag handler
   to get wrong. */
.wipe{--x:50%%;position:relative;overflow:hidden;isolation:isolate;
  aspect-ratio:3/2;background:#000;touch-action:pan-y}
.wipe img{position:absolute;inset:0;width:100%%;height:100%%;object-fit:cover;display:block;
  -webkit-user-drag:none;user-select:none;pointer-events:none}
/* the BEFORE sits over the AFTER and is clipped back to the handle. Clipping,
   not resizing: a width driven overlay would rescale its own picture as it
   moved and the two halves would stop matching. */
.wipe .w-b{position:absolute;inset:0;z-index:2;clip-path:inset(0 calc(100%% - var(--x)) 0 0)}
.w-line{position:absolute;top:0;bottom:0;left:var(--x);z-index:4;width:%(lw)s;
  margin-left:calc(%(lw)s / -2);background:%(line)s;pointer-events:none}
.w-grip{position:absolute;top:50%%;left:var(--x);z-index:5;translate:-50%% -50%%;
  width:48px;height:48px;display:grid;place-items:center;pointer-events:none;
  %(grip)s}
.w-grip svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;
  stroke-linecap:round;stroke-linejoin:round}
.w-tag{position:absolute;top:%(tagtop)s;z-index:3;%(tag)s}
.w-tag.a{left:%(tagtop)s}
.w-tag.b{right:%(tagtop)s}
.w-range{position:absolute;inset:0;z-index:6;width:100%%;height:100%%;margin:0;padding:0;
  appearance:none;-webkit-appearance:none;background:transparent;opacity:0;cursor:ew-resize}
.w-range::-webkit-slider-thumb{-webkit-appearance:none;width:56px;height:100%%}
.w-range::-moz-range-thumb{width:56px;height:100%%;border:0}
.w-range:focus-visible ~ .w-grip{outline:2px solid %(line)s;outline-offset:4px}
@media (max-width:760px){.wipe{aspect-ratio:4/3}.w-grip{width:44px;height:44px}}
"""

JS = """
  /* ---------- the wipe ----------
     Sweeps itself once when it first arrives, because a handle nobody drags
     explains nothing, then hands over for good. Cancelled by the first touch,
     skipped entirely under reduced motion, and it never runs twice. */
  (function(){
    var boxes=[].slice.call(document.querySelectorAll('.wipe'));
    if(!boxes.length) return;
    var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
    boxes.forEach(function(box){
      var input=box.querySelector('.w-range');
      if(!input) return;
      var touched=false, raf=0;
      function set(v){
        box.style.setProperty('--x', v+'%');
        input.setAttribute('aria-valuenow', Math.round(v));
        input.setAttribute('aria-valuetext', Math.round(v)+'% before, '+(100-Math.round(v))+'% after');
      }
      function stop(){ touched=true; if(raf){cancelAnimationFrame(raf); raf=0;} }
      input.addEventListener('input', function(){ stop(); set(+input.value); });
      input.addEventListener('pointerdown', stop);
      input.addEventListener('keydown', stop);
      set(+input.value);
      if(reduce || !('IntersectionObserver' in window)) return;
      new IntersectionObserver(function(es,o){
        if(!es[0].isIntersecting || touched) return;
        o.disconnect();
        /* out to the before, back past centre to the after, then rest */
        var legs=[[50,88,620],[88,38,1150]], leg=0, t0=0;
        (function step(ts){
          if(touched) return;
          if(!t0) t0=ts;
          var L=legs[leg], p=Math.min((ts-t0)/L[2],1), e=1-Math.pow(1-p,3);
          var v=L[0]+(L[1]-L[0])*e;
          input.value=v; set(v);
          if(p<1){ raf=requestAnimationFrame(step); }
          else if(++leg<legs.length){ t0=0; raf=requestAnimationFrame(step); }
        })(performance.now());
      },{threshold:.45}).observe(box);
    });
  })();"""

ARROWS = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
          '<path d="M9.5 7 5 12l4.5 5M14.5 7 19 12l-4.5 5"/></svg>')

def wipe_markup(indent, before_alt, after_alt, tag_a, tag_b, label):
    i = ' ' * indent
    return (
f'{i}<div class="wipe">\n'
f'{i}  <img src="assets/ba-after.jpg" width="390" height="488" loading="lazy" alt="{after_alt}">\n'
f'{i}  <div class="w-b"><img src="assets/ba-before.jpg" width="390" height="488" loading="lazy" alt="{before_alt}"></div>\n'
f'{i}  <span class="w-tag a">{tag_a}</span>\n'
f'{i}  <span class="w-tag b">{tag_b}</span>\n'
f'{i}  <input class="w-range" type="range" min="0" max="100" value="50" step="0.1"\n'
f'{i}         aria-label="{label}">\n'
f'{i}  <span class="w-line" aria-hidden="true"></span>\n'
f'{i}  <span class="w-grip" aria-hidden="true">{ARROWS}</span>\n'
f'{i}</div>')

BEFORE_ALT = 'Commercial storefront glazing in Mesa before cleaning, hazed with dust and hard water'
AFTER_ALT  = 'The same Mesa storefront glazing after cleaning, clear and streak free'
LABEL      = 'Drag to compare the storefront glazing before and after cleaning'
