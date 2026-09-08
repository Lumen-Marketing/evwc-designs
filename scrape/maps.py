# -*- coding: utf-8 -*-
# A real map of the service area, on all four.
#
# There is no storefront to pin: this is a mobile trade working out of a van, so
# the honest thing to show is the AREA, not an address. The keyless Google embed
# centred on Mesa at zoom 10 happens to frame Mesa, Gilbert, Chandler, Queen
# Creek, Apache Junction and San Tan Valley in one view, which is the route.
# That also resolves the SWAP: comment 01 was carrying.
#
# Four different frames, because the four directions do not share components,
# and only 01 keeps it as a two column pair. The section audit says 2-col is
# already the most repeated shape on every one of these pages, so the other
# three take the map as a wide band instead of another split.
IFRAME = ('<iframe class="gmap" title="Map of the East Valley service area, centred on Mesa" '
          'loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
          'src="https://www.google.com/maps?q=Mesa,+Arizona&amp;z=10&amp;output=embed"></iframe>')

def patch(path, edits):
    s = open(path, encoding='utf-8').read()
    done = []
    for old, new, label in edits:
        if old not in s:
            print('!! MISS %s: %s' % (path, label)); continue
        s = s.replace(old, new, 1); done.append(label)
    open(path, 'w', encoding='utf-8').write(s)
    print('%-14s %d edits -> %s' % (path, len(done), ', '.join(done)))

BASE = """/* the map itself. Same embed on all four; the frame around it is what
   changes, because these four do not share components. */
.gmap{display:block;width:100%;height:100%;border:0;filter:saturate(.9)}
"""

# ------------------------------------------------------------------ 01 -----
patch('01-mesic.html', [
 (""".mapcard img{width:100%;height:100%;object-fit:cover}""",
  """.mapcard img{width:100%;height:100%;object-fit:cover}
""" + BASE, 'css'),
 ("""      <!-- SWAP: replace with a real Google Maps embed for the service area -->
      <div class="shot"><img src="assets/job-pole-wide.jpg" width="1280" height="722" loading="lazy" alt="A water-fed pole worked up a building elevation in the East Valley"></div>""",
  """      <div class="shot">%s</div>""" % IFRAME, 'markup'),
])

# ------------------------------------------------------------------ 02 -----
# film stock: the map runs edge to edge as a letterboxed band, lit like a screen
# on a dark page, with the vignette this direction already uses over its edges.
patch('02-site.html', [
 ("""/* ---------- RECENT WORK: the projector ----------""",
  BASE + """/* the coverage band. Edge to edge rather than a card beside the towns: the
   section audit says two column is already the most repeated shape on this
   page, and a route reads better as something that runs off both sides. */
.mapband{position:relative;margin-top:clamp(30px,4vw,50px);
  height:clamp(240px,30vw,440px);overflow:hidden;background:#0c1421;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.14)}
.mapband::after{content:"";position:absolute;inset:0;pointer-events:none;z-index:2;
  background:radial-gradient(120% 100% at 50% 50%,transparent 42%,rgba(7,12,20,.6) 100%)}
.maplbl{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:baseline;
  margin-top:14px;font-size:13.5px;color:var(--fg-2)}
.maplbl b{font-family:'Big Shoulders Display',sans-serif;font-weight:700;font-size:15px;
  letter-spacing:.18em;text-transform:uppercase;color:#fff}

/* ---------- RECENT WORK: the projector ----------""", 'css'),
 ("""      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
  </div>
</section>""",
  """      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
    <p class="maplbl"><b>On the route</b><span>Mesa to San Tan Valley, and everything between the 60 and the 202.</span></p>
  </div>
  <div class="mapband rv">%s</div>
</section>""" % IFRAME, 'markup'),
])

# ------------------------------------------------------------------ 03 -----
# milled metal: the map is a panel recessed into the plate, bolted at four
# corners, with a machined label bar under it.
patch('03-plate.html', [
 ("""/* ---------- RECENT WORK: the indexing rail ----------""",
  BASE + """/* recessed into the plate and bolted at four corners, the way every other
   panel on this page is fixed down. Full width rather than a second column:
   two column is already the most repeated shape here. */
.mappanel{position:relative;margin-top:clamp(26px,3.4vw,44px);
  background:var(--steel-2);box-shadow:var(--bevel);padding:10px}
.mappanel>div{height:clamp(240px,30vw,420px);overflow:hidden;
  box-shadow:inset 0 0 0 1px rgba(0,0,0,.7),inset 0 2px 5px rgba(0,0,0,.55)}
.maplbl{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:baseline;
  padding:13px 4px 3px;font-size:14px;color:var(--fg-2)}
.maplbl b{font-family:'Saira Condensed',sans-serif;font-weight:700;font-size:16px;
  letter-spacing:.18em;text-transform:uppercase;color:#fff}

/* ---------- RECENT WORK: the indexing rail ----------""", 'css'),
 ("""      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
  </div>
</section>""",
  """      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
    <figure class="mappanel bolts rv" style="margin:0"><span class="b2"></span><span class="b3"></span>
      <div>%s</div>
      <figcaption class="maplbl"><b>On the route</b><span>Mesa to San Tan Valley, and everything between the 60 and the 202.</span></figcaption>
    </figure>
  </div>
</section>""" % IFRAME, 'markup'),
])

# ------------------------------------------------------------------ 04 -----
# screen print: a keyline with a second block pulled two pixels off register,
# because a hand pulled print never lines up.
patch('04-burst.html', [
 ("""</style>""",
  BASE + """/* keylined and pulled off register, the way every plate on this page is */
.mapprint{position:relative;margin-top:clamp(26px,3.4vw,44px);isolation:isolate}
.mapprint::before{content:"";position:absolute;inset:0;z-index:0;
  background:var(--blue);transform:translate(6px,6px)}
.mapprint>div{position:relative;z-index:1;height:clamp(240px,30vw,420px);overflow:hidden;
  background:#fff;border:2px solid var(--ink)}
.maplbl{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:baseline;
  margin-top:12px;font-size:14px;color:var(--ink-2)}
.maplbl b{font-family:'Archivo Black',sans-serif;font-size:14px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--ink)}
</style>""", 'css'),
 ("""      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
  </div>
</section>""",
  """      <span>San Tan Valley</span><span>Apache Junction</span><span>Johnson Ranch</span><span>Bella Vista Farms</span>
    </div>
    <figure class="mapprint rv" style="margin:0">
      <div>%s</div>
      <figcaption class="maplbl"><b>On the route</b><span>Mesa to San Tan Valley, and everything between the 60 and the 202.</span></figcaption>
    </figure>
  </div>
</section>""" % IFRAME, 'markup'),
])
