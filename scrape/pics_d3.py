# -*- coding: utf-8 -*-
p = '03-hazard.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep(""".svc .wide p{max-width:44ch;font-size:15px}""",
""".svc .wide p{max-width:44ch;font-size:15px}
/* the lead cell carries the job it describes, recessed into the plate */
.svc .wide{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,.86fr);
  gap:clamp(20px,2.4vw,34px);align-items:center}
.svc .wide .txt{min-width:0}
.wpic{margin:0;position:relative;overflow:hidden;background:#000;aspect-ratio:4/3;
  box-shadow:var(--bevel-deep),0 0 0 1px #000}
.wpic img{width:100%;height:100%;object-fit:cover;filter:saturate(.94) contrast(1.04)}

/* a strip of the same table, four cells wide, carrying pictures instead of copy */
.strip{display:grid;grid-template-columns:repeat(4,1fr);border-left:1px solid var(--line);
  border-bottom:1px solid var(--line)}
.strip figure{margin:0;position:relative;overflow:hidden;border-right:1px solid var(--line);
  aspect-ratio:4/3;background:#000}
.strip img{width:100%;height:100%;object-fit:cover;filter:saturate(.92) contrast(1.04);
  transition:transform .8s var(--ez)}
.strip figcaption{position:absolute;left:0;bottom:0;z-index:2;background:var(--yellow);color:#000;
  padding:6px 12px;font-family:var(--m);font-size:9.5px;font-weight:700;letter-spacing:.16em;
  text-transform:uppercase}
@media (hover:hover) and (pointer:fine){.strip figure:hover img{transform:scale(1.05)}}""",
    'd3 pics css')

rep("""      <article class="wide" data-no="01">
        <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M12 3v18M3 12h18"/></svg></div>
        <h3>Window cleaning, inside &amp; out</h3>
        <p>Streak-free glass on homes and businesses, single storey to multi-storey, using purified water and a water-fed pole where the height calls for it.</p>
      </article>""",
"""      <article class="wide" data-no="01">
        <div class="txt">
          <div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="1"/><path d="M12 3v18M3 12h18"/></svg></div>
          <h3>Window cleaning, inside &amp; out</h3>
          <p>Streak-free glass on homes and businesses, single storey to multi-storey, using purified water and a water-fed pole where the height calls for it.</p>
        </div>
        <figure class="wpic"><img src="assets/job-glass-wide.jpg" alt="A squeegee on a pole clearing water off a commercial glass frontage" loading="lazy" width="1280" height="722"></figure>
      </article>""", 'wide photo')

rep("""        <h3>Junk removal</h3>
        <p>Monsoon debris, rental clear-outs and listing prep loaded up and taken away.</p>
      </article>
    </div>
  </div>
</section>""",
"""        <h3>Junk removal</h3>
        <p>Monsoon debris, rental clear-outs and listing prep loaded up and taken away.</p>
      </article>
    </div>
    <div class="strip">
      <figure><img src="assets/job-pole-wide.jpg" alt="A water-fed pole extended to the top of a commercial storefront, two cleaners working below it" loading="lazy" width="1280" height="722"><figcaption>Two storey reach</figcaption></figure>
      <figure><img src="assets/job-solar-sky.jpg" alt="A rooftop solar array on terracotta tile under a bank of cloud" loading="lazy" width="540" height="960"><figcaption>Rooftop array</figcaption></figure>
      <figure><img src="assets/job-haul.jpg" alt="A pile of dumped furniture and cardboard in a walled back yard before it was hauled away" loading="lazy" width="820" height="1094"><figcaption>Yard clear-out</figcaption></figure>
      <figure><img src="assets/job-crew.jpg" alt="A cleaner working a tall storefront window with a water-fed pole" loading="lazy" width="608" height="1080"><figcaption>Owner operated</figcaption></figure>
    </div>
  </div>
</section>""", 'photo strip')

rep("""  .svc{grid-template-columns:repeat(2,1fr)}
  .svc .wide{grid-column:span 2}""",
"""  .svc{grid-template-columns:repeat(2,1fr)}
  .svc .wide{grid-column:span 2}
  .strip{grid-template-columns:repeat(2,1fr)}""", 'strip mq')

open(p, 'w', encoding='utf-8').write(s)
print('D3 pics:', len(done), 'edits ->', ', '.join(done))
