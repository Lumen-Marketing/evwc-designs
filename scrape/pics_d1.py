# -*- coding: utf-8 -*-
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep(""".cluster{display:grid;grid-template-columns:minmax(0,.34fr) minmax(0,1fr);gap:clamp(20px,4vw,64px);
  padding-block:clamp(30px,3.6vw,52px);border-top:1px solid var(--line)}""",
""".cluster{display:grid;grid-template-columns:minmax(0,.3fr) minmax(0,1fr) minmax(0,.6fr);
  gap:clamp(20px,3.4vw,56px);padding-block:clamp(30px,3.6vw,52px);border-top:1px solid var(--line)}
/* the photograph takes the column the copy was leaving empty, and stretches to
   whatever height its group runs to rather than setting one of its own */
.cpic{margin:0;position:relative;overflow:hidden;border-radius:18px;background:var(--bg-2);
  min-height:clamp(210px,24vw,400px);
  box-shadow:var(--lift-2),0 0 0 1px rgba(255,255,255,.07),var(--rim)}
.cpic img{width:100%;height:100%;object-fit:cover;transition:transform 1.1s var(--ez)}
.cpic figcaption{position:absolute;inset:auto 0 0 0;z-index:2;padding:26px 15px 13px;font-size:12.5px;
  color:#e6eaeb;background:linear-gradient(180deg,transparent,rgba(8,9,10,.8))}
@media (hover:hover) and (pointer:fine){.cluster:hover .cpic img{transform:scale(1.04)}}""",
    'cluster css')

PICS = [
    ("Glass", 'job-squeegee.jpg', 540, 720,
     "A squeegee on a pole drawing an arc of water down a commercial glass frontage",
     "Purified water, water-fed pole"),
    ("Film and panels", 'job-solar-sky.jpg', 540, 960,
     "A rooftop solar array on terracotta tile under a bank of cloud",
     "Rooftop array, Mesa"),
    ("Property", 'job-haul.jpg', 820, 1094,
     "A pile of dumped furniture and cardboard in a walled back yard before it was hauled away",
     "Yard clear-out, before"),
]

for h3, f, w, hgt, alt, cap in PICS:
    old = "    </ul>\n  </div>"
    # anchor each insert to its own cluster heading
    idx = s.index("<h3>%s</h3>" % h3)
    end = s.index("    </ul>\n  </div>", idx)
    ins = ('    </ul>\n'
           '    <figure class="cpic"><img src="assets/%s" alt="%s" loading="lazy" width="%d" height="%d">'
           '<figcaption>%s</figcaption></figure>\n  </div>' % (f, alt, w, hgt, cap))
    s = s[:end] + ins + s[end + len(old):]
    done.append('pic ' + h3)

rep("  .cluster{grid-template-columns:1fr;gap:16px}",
    "  .cluster{grid-template-columns:1fr;gap:16px}\n  .cpic{min-height:0;aspect-ratio:16/10;margin-top:6px}",
    'cluster mq')

open(p, 'w', encoding='utf-8').write(s)
print('D1 pics:', len(done), 'edits ->', ', '.join(done))
