# -*- coding: utf-8 -*-
p = '02-broadsheet.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep(""".svc .feature:hover{background:#0d3946}""",
""".svc .feature:hover{background:#0d3946}
/* the feature carries the job it describes, cut to a band across its foot */
.svc .feature{padding-bottom:0;overflow:hidden}
.fpic{margin:clamp(24px,2.6vw,36px) 0 0;border-radius:var(--r-sm) var(--r-sm) 0 0;overflow:hidden;
  aspect-ratio:21/8;background:var(--ink)}
.fpic img{width:100%;height:100%;object-fit:cover}
/* a card that is only a photograph, which squares the grid off as well */
.svc .pic{padding:9px;background:var(--limestone);position:relative;overflow:hidden}
.svc .pic .m{position:relative;height:100%;min-height:clamp(190px,20vw,270px);overflow:hidden;
  border-radius:calc(var(--r-card) - 9px);background:var(--deep)}
.svc .pic img{width:100%;height:100%;object-fit:cover}
.svc .pic figcaption{position:absolute;left:14px;bottom:14px;background:var(--limestone);
  border-radius:var(--r-pill);padding:7px 15px;font-size:11.5px;font-weight:700;letter-spacing:.08em;
  text-transform:uppercase}

/* a wide plate of the work, offset straight down so it stays on the centre line */
.pband{margin:0;position:relative;isolation:isolate}
.pband::before,.pband::after{content:"";position:absolute;inset:0;border-radius:var(--r-card);z-index:0}
.pband::before{background:var(--deep);transform:translate(0,24px)}
.pband::after{background:var(--cyan);transform:translate(0,12px)}
.pband-in{position:relative;z-index:1;padding:10px;border-radius:var(--r-card);background:var(--limestone);
  box-shadow:var(--lift-3)}
.pband .m{position:relative;border-radius:calc(var(--r-card) - 10px);overflow:hidden;aspect-ratio:21/9;
  background:var(--deep)}
.pband img{width:100%;height:100%;object-fit:cover}
.pband .cap{position:absolute;left:clamp(16px,2vw,26px);bottom:clamp(16px,2vw,26px);
  background:var(--limestone);border-radius:var(--r-pill);padding:9px 19px;font-size:12.5px;
  font-weight:700;letter-spacing:.1em;text-transform:uppercase}""",
    'svc pics css')

rep("""        <p>Streak-free glass on homes and businesses, single storey to multi-storey, using purified water and a water-fed pole where the height calls for it.</p>
      </article>""",
"""        <p>Streak-free glass on homes and businesses, single storey to multi-storey, using purified water and a water-fed pole where the height calls for it.</p>
        <figure class="fpic"><img src="assets/job-glass-wide.jpg" alt="A squeegee on a pole clearing water off a commercial glass frontage" loading="lazy" width="1280" height="722"></figure>
      </article>""", 'feature photo')

rep("""        <h3>Junk removal</h3>
        <p>Monsoon debris, rental clear-outs and listing prep loaded up and taken away.</p>
      </article>
    </div>""",
"""        <h3>Junk removal</h3>
        <p>Monsoon debris, rental clear-outs and listing prep loaded up and taken away.</p>
      </article>
      <article class="pic">
        <div class="m"><img src="assets/job-crew.jpg" alt="A cleaner working a tall storefront window with a water-fed pole" loading="lazy" width="608" height="1080"><figcaption>On the job</figcaption></div>
      </article>
    </div>""", 'photo card')

rep("""<section id="reels">""",
"""<section style="padding-top:0">
  <div class="wrap">
    <figure class="pband">
      <div class="pband-in">
        <div class="m"><img src="assets/job-pole-wide.jpg" alt="A water-fed pole extended to the top of a commercial storefront, two cleaners working below it" loading="lazy" width="1280" height="722"><span class="cap">Two storey reach, no ladder</span></div>
      </div>
    </figure>
  </div>
</section>

<section id="reels">""", 'plate band')

open(p, 'w', encoding='utf-8').write(s)
print('D2 pics:', len(done), 'edits ->', ', '.join(done))
