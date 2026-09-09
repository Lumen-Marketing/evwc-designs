# -*- coding: utf-8 -*-
# Two corrections that only a screenshot could have found.
#
# 1. The title plate was hung off the bottom RIGHT of the lead picture, which
#    is where the operator and the squeegee are. It covered the only part of
#    the frame that shows the work. It moves to the left, over the plain
#    glazed door, which is the dead quarter of that photograph and also where
#    the eye enters the section.
#
# 2. The drawn detail boundary was var(--line) at 1px, which on a sheet that
#    already carries 24px grid rules at .075 was indistinguishable from the
#    grid. A boundary that reads as graph paper is not a boundary. It goes to
#    a .26 ink rule, between the sheet's minor (.075) and major (.16) rules
#    and above both, so it reads as something drawn ON the sheet.
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


rep(""".det .vp::after{content:"";position:absolute;inset:-9px;
  border:1px solid var(--line);pointer-events:none}""",
    """.det .vp::after{content:"";position:absolute;inset:-9px;
  border:1px solid rgba(10,61,74,.26);pointer-events:none}""",
    'boundary weight')

rep(""".det.lead .cap{position:absolute;z-index:2;right:0;bottom:0;""",
    """.det.lead .cap{position:absolute;z-index:2;left:0;bottom:0;""",
    'plate to the left')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
