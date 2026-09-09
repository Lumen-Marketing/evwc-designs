# -*- coding: utf-8 -*-
# Sweep up after jobs_01.py: .pcard and .cards were the old services furniture
# and nothing else on the page uses them, so the rules go with the markup
# rather than sitting in the sheet as dead weight. The comment that described
# the old layout is rewritten to describe the new one.
p = '01-mesic.html'
s = open(p, encoding='utf-8').read()
done = []


def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label)
        return
    s = s.replace(old, new, 1)
    done.append(label)


rep("""/* ---------- photo card grids, the reference's service cards ---------- */
.pcard{background:var(--white);border:1px solid var(--line);border-radius:var(--r);padding:12px;text-align:center;
  transition:transform .32s cubic-bezier(.16,1,.3,1),box-shadow .32s,border-color .3s}
.pcard:hover{transform:translateY(-5px);box-shadow:var(--sh);border-color:var(--blue)}
.pcard .shot{border-radius:var(--r-sm);overflow:hidden;aspect-ratio:16/10;margin-bottom:14px}
.pcard .shot img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.16,1,.3,1)}
.pcard:hover .shot img{transform:scale(1.06)}
.pcard h3{font-size:16.5px;margin-bottom:6px}
.pcard p{color:var(--muted);font-size:13.5px;padding:0 6px 10px;line-height:1.55}

""", "", 'drop .pcard base block')

rep(""".pcard,.rev,.q,.mapcard,.trio div,.towns span,.hint,""",
    """.rev,.q,.mapcard,.trio div,.towns span,.hint,""", 'drop .pcard from the de-slop list')

rep("""/* services and truck: photo does the work, caption sits under it, left set */
.pcard{text-align:left;padding-bottom:32px;border-bottom:1px solid var(--line)}
.pcard .shot{border-radius:0;margin-bottom:20px}
.pcard h3{font-size:22px;margin-bottom:8px;letter-spacing:-.02em}
.pcard p{color:var(--muted);font-size:15px;padding:0;line-height:1.6;font-weight:400;max-width:34ch}
.pcard:hover{box-shadow:none;transform:none}
.pcard:hover .shot img{transform:scale(1.04)}

""", "", 'drop the .pcard de-slop block')

rep("""  .cards,.revs,.strip3{grid-template-columns:1fr 1fr}""",
    """  .revs,.strip3{grid-template-columns:1fr 1fr}""", 'drop .cards from 1040 mq')

rep("""   what is in them. Core Services is now one large item beside two
   stacked, so it is a different layout family from the three up that
   follows it.""",
    """   what is in them. On The Job is now three drawn details on the sheet,
   the primary one running the full measure with its title plate hung
   into the corner of the picture, so it is a different layout family
   from the accordion strip that follows it.""", 'refresh the layout note')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
