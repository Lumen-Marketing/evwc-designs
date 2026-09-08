# -*- coding: utf-8 -*-
# Stages 3 and 4 of 4.
#
#   work      -> split: the projector stage runs to the left edge, the contact
#                sheet and the words stand in the right pane
#   before /  -> full bleed 50/50 with no gutter at all, the two halves meeting
#   after        on the centre line. The page's signature moment: this is the
#                one piece of content that IS a split screen.
#   reviews   -> full width ruled run. A breaker, and it stops five split
#                family sections running back to back into the footer.
#   area      -> split: towns in the pane, the map running off the right edge
#   contact   -> left alone. It is already a photographic band, which is a
#                different family, and it closes the page.
p = '02-site.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ================================================================== CSS =====
rep("""/* ---------- RECENT WORK: the projector ----------""",
"""/* ---------- the projector, as the left half of a split ---------- */
.projx.split{margin-top:0;min-height:min(88dvh,940px)}
.projx.split .stage{aspect-ratio:auto;height:100%;box-shadow:none}
.projx.split .sp-copy{justify-content:center}
.projx.split .sheet{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:clamp(22px,2.6vw,34px)}
.projx.split .sheet .cell{aspect-ratio:16/11}
@media (max-width:900px){
  .projx.split{min-height:0}
  .projx.split .stage{aspect-ratio:4/3;height:auto}
}

/* ---------- BEFORE AND AFTER: the page's one true split screen ----------
   No gutter, no card, no container. Two halves of the viewport meeting on the
   centre line, which is the only layout that says "the same glass" without a
   caption having to say it. */
.basplit{display:grid;grid-template-columns:1fr 1fr;gap:0;
  height:min(82dvh,860px);margin-top:clamp(28px,3.6vw,48px)}
.basplit figure{position:relative;margin:0;overflow:hidden;background:#000}
.basplit img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;
  transition:scale .9s cubic-bezier(.16,1,.3,1)}
.basplit figure:hover img{scale:1.04}
/* the seam is a hairline of the accent, so the meeting point is deliberate */
.basplit figure+figure{box-shadow:inset 1px 0 0 rgba(111,226,242,.5)}
.basplit figcaption{position:absolute;left:0;right:0;bottom:0;z-index:2;
  padding:clamp(22px,3vw,40px);
  background:linear-gradient(180deg,rgba(7,12,20,0),rgba(7,12,20,.92));
  font-size:14.5px;color:var(--fg-2)}
.basplit figure+figure figcaption{text-align:right}
.basplit figcaption b{display:block;font-family:'Big Shoulders Display',sans-serif;
  font-size:clamp(26px,3.2vw,42px);font-weight:800;text-transform:uppercase;
  letter-spacing:.04em;color:#fff;margin-bottom:4px}
.basplit figure+figure figcaption b{color:var(--blue-2)}
@media (max-width:900px){
  .basplit{grid-template-columns:1fr;height:auto}
  .basplit figure{height:clamp(300px,66vw,430px)}
  .basplit figure+figure{box-shadow:inset 0 1px 0 rgba(111,226,242,.5)}
  .basplit figure+figure figcaption{text-align:left}
}

/* ---------- REVIEWS: a ruled run, full width ----------
   The breaker that stops work, before and after, area and contact running as
   four split family sections into the footer. Nothing is boxed: a rule, the
   quote at reading size, the name in small caps. */
.revrun{list-style:none;margin:clamp(30px,4vw,52px) 0 0;padding:0;
  border-top:1px solid rgba(255,255,255,.16)}
.revrun li{display:grid;grid-template-columns:minmax(0,1fr) clamp(160px,17vw,260px);
  gap:clamp(18px,3vw,56px);align-items:start;
  padding-block:clamp(22px,2.8vw,40px);
  border-bottom:1px solid rgba(255,255,255,.11);
  transition:background .4s cubic-bezier(.16,1,.3,1)}
.revrun li:hover{background:linear-gradient(90deg,rgba(18,196,222,.07),transparent 62%)}
.revrun p{margin:0;font-size:clamp(17px,1.55vw,21px);line-height:1.5;color:#e7edf2}
.revrun footer{font-size:13px;color:var(--fg-2);padding-top:4px}
.revrun footer b{display:block;font-family:'Big Shoulders Display',sans-serif;
  font-weight:700;font-size:17px;letter-spacing:.1em;text-transform:uppercase;color:#fff;
  margin-bottom:2px}
@media (max-width:760px){
  .revrun li{grid-template-columns:1fr;gap:12px}
}

/* ---------- SERVICE AREA: the towns in the pane, the map off the edge ---- */
.area-split{min-height:min(78dvh,820px)}
.area-split .sp-media{background:#0c1421}
.area-split .gmap{position:absolute;inset:0;height:100%}

/* ---------- RECENT WORK: the projector ----------""", 'css')

# the coverage band is replaced by the map pane
rep("""/* the coverage band. Edge to edge rather than a card beside the towns: the
   section audit says two column is already the most repeated shape on this
   page, and a route reads better as something that runs off both sides. */
.mapband{position:relative;margin-top:clamp(30px,4vw,50px);
  height:clamp(240px,30vw,440px);overflow:hidden;background:#0c1421;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14)}
.mapband::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  background:radial-gradient(120% 100% at 50% 50%,transparent 42%,rgba(7,12,20,.6) 100%)}
""", "", 'drop mapband')

# ================================================================ MARKUP ====
# ---- 7. work ---------------------------------------------------------------
start = s.index('<!-- ============ RECENT WORK ============ -->')
end = s.index('<!-- ============ BEFORE AND AFTER ============ -->')
old = s[start:end]
i = old.index('<div class="projx"')
j = old.index('</div>\n    </div>', i)  # end of .sheet
sheet_end = old.index('</div>', j + 6) + len('</div>')
stage = old[old.index('<div class="stage">'):old.index('      </div>\n      <div class="sheet">') + len('      </div>\n')]
sheet = old[old.index('<div class="sheet">'):sheet_end]

NEW_WORK = """<!-- ============ RECENT WORK ============ -->
<section class="sec" id="work" style="padding:0">
  <div class="projx split w58" role="group" aria-roledescription="carousel" aria-label="Recent work">
    <div class="sp-media" style="background:#000">
      %s
    </div>
    <div class="sp-copy">
      <h2 class="rv" style="font-size:clamp(34px,4.2vw,68px)">Straight from the van</h2>
      <p class="lede rv" style="margin-top:16px">Their own clips and job photographs, straight off Instagram. The two clips play here with the sound off.</p>
      %s
      <div class="hero-act" style="margin-top:32px">
        <a class="btn wire" href="https://www.instagram.com/eastvalleywindowcleaningllc/" target="_blank" rel="noopener"><span>See more on Instagram</span></a>
      </div>
    </div>
  </div>
</section>

""" % (stage.strip(), sheet.strip())
s = s[:start] + NEW_WORK + s[end:]
done.append('work split')

# ---- 8. before and after ---------------------------------------------------
rep("""    <div class="ba">
      <figure class="shot rv" style="margin:0">
        <img src="assets/ba-before.jpg" width="390" height="488" loading="lazy"
             alt="Commercial storefront glazing in Mesa before cleaning">
        <figcaption><b>Before</b>Monsoon dust and sprinkler overspray on the glass.</figcaption>
      </figure>
      <figure class="shot rv" style="margin:0">
        <img src="assets/ba-after.jpg" width="390" height="488" loading="lazy"
             alt="The same Mesa storefront glazing after cleaning">
        <figcaption><b>After</b>One visit. Frames and screens done at the same time.</figcaption>
      </figure>
    </div>
  </div>
</section>""",
"""  </div>
  <div class="basplit rv">
    <figure>
      <img src="assets/ba-before.jpg" width="390" height="488" loading="lazy"
           alt="Commercial storefront glazing in Mesa before cleaning">
      <figcaption><b>Before</b>Monsoon dust and sprinkler overspray on the glass.</figcaption>
    </figure>
    <figure>
      <img src="assets/ba-after.jpg" width="390" height="488" loading="lazy"
           alt="The same Mesa storefront glazing after cleaning">
      <figcaption><b>After</b>One visit. Frames and screens done at the same time.</figcaption>
    </figure>
  </div>
</section>""", 'before after split')

# ---- 9. reviews ------------------------------------------------------------
rep("""    <div class="revs">
      <figure class="rev rv" style="margin:0"><p>Jose did an outstanding job cleaning my windows! The team was incredibly friendly, professional, and detail-oriented. They left every window spotless, even cleaning the frames and screens to perfection.</p><footer><b>Lacey Shultz</b>Google review</footer></figure>
      <figure class="rev rv" style="margin:0"><p>Jose from East Valley Window Cleaning is a true professional. They are polite, easy to communicate with, and make you feel confident in their honesty and reliability.</p><footer><b>Nina Hanopol</b>Google review</footer></figure>
      <figure class="rev rv" style="margin:0"><p>Great job done! On time, on schedule. Windows and sliding doors look great.</p><footer><b>Kirkland Sanders</b>Google review</footer></figure>
      <figure class="rev rv" style="margin:0"><p>Really great service!</p><footer><b>Maria Sandoval</b>Google review</footer></figure>
    </div>""",
"""    <ol class="revrun">
      <li class="rv"><p>Jose did an outstanding job cleaning my windows! The team was incredibly friendly, professional, and detail-oriented. They left every window spotless, even cleaning the frames and screens to perfection.</p><footer><b>Lacey Shultz</b>Google review</footer></li>
      <li class="rv"><p>Jose from East Valley Window Cleaning is a true professional. They are polite, easy to communicate with, and make you feel confident in their honesty and reliability.</p><footer><b>Nina Hanopol</b>Google review</footer></li>
      <li class="rv"><p>Great job done! On time, on schedule. Windows and sliding doors look great.</p><footer><b>Kirkland Sanders</b>Google review</footer></li>
      <li class="rv"><p>Really great service!</p><footer><b>Maria Sandoval</b>Google review</footer></li>
    </ol>""", 'reviews run')

# ---- 10. area --------------------------------------------------------------
rep("""<section class="sec lit" id="area">
  <div class="wrap">
    <h2 class="rv" style="font-size:clamp(38px,6.88vw,99px)">Working the whole East Valley</h2>
    <p class="lede rv" style="margin-top:18px">Based in the East Valley and on the road daily. If you are near one of these, you are on the route.</p>
    <div class="towns rv">
      <span>Mesa</span><span>Gilbert</span><span>Chandler</span><span>Queen Creek</span>
      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
    <p class="maplbl"><b>On the route</b><span>Mesa to San Tan Valley, and everything between the 60 and the 202.</span></p>
  </div>
  <div class="mapband rv"><iframe class="gmap" title="Map of the East Valley service area, centred on Mesa" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Mesa,+Arizona&amp;z=10&amp;output=embed"></iframe></div>
</section>""",
"""<section class="lit split w58 area-split" id="area">
  <div class="sp-copy">
    <h2 class="rv" style="font-size:clamp(34px,4.2vw,68px)">Working the whole East Valley</h2>
    <p class="lede rv" style="margin-top:18px">Based in the East Valley and on the road daily. If you are near one of these, you are on the route.</p>
    <div class="towns rv">
      <span>Mesa</span><span>Gilbert</span><span>Chandler</span><span>Queen Creek</span>
      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
    <p class="maplbl"><b>On the route</b><span>Mesa to San Tan Valley, and everything between the 60 and the 202.</span></p>
  </div>
  <div class="sp-media rv"><iframe class="gmap" title="Map of the East Valley service area, centred on Mesa" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Mesa,+Arizona&amp;z=10&amp;output=embed"></iframe></div>
</section>""", 'area split')

open(p, 'w', encoding='utf-8').write(s)
print('split stages 3+4:', len(done), 'edits ->', ', '.join(done))
