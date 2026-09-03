# -*- coding: utf-8 -*-
p = '01-daylight.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# 1. the headline was being squeezed by the header column and broke "van." onto
#    a line of its own. Only the body copy needs a measure.
rep(""".rhead{max-width:54ch;margin:0 auto clamp(56px,6.5vw,96px);text-align:center}
.rhead .sub{margin:18px auto 0;max-width:48ch}""",
    """.rhead{margin:0 auto clamp(52px,6vw,88px);text-align:center}
.rhead .sub{margin:20px auto 0;max-width:46ch}""", 'head measure')

# 2. the reflection was a rectangle of blurred poster: straight left and right
#    edges, no falloff, so it read as a grey smudge rather than thrown light.
#    One radial mask fades it on both axes at once, anchored to the bay's foot.
rep(""".bay::after{content:"";position:absolute;left:6%;right:6%;top:100%;height:clamp(56px,8vw,104px);
  pointer-events:none;background-image:var(--pv);background-size:cover;background-position:center;
  transform:scaleY(-1);filter:blur(13px) saturate(.62);opacity:.28;
  -webkit-mask-image:linear-gradient(to bottom,transparent,#000);
  mask-image:linear-gradient(to bottom,transparent,#000)}""",
    """.bay::after{content:"";position:absolute;left:2%;right:2%;top:100%;height:clamp(46px,6.4vw,88px);
  pointer-events:none;background-image:var(--pv);background-size:cover;background-position:center;
  transform:scaleY(-1);filter:blur(10px) saturate(1.2);opacity:.33;
  -webkit-mask-image:radial-gradient(124% 106% at 50% 100%,#000 4%,rgba(0,0,0,.4) 42%,transparent 74%);
  mask-image:radial-gradient(124% 106% at 50% 100%,#000 4%,rgba(0,0,0,.4) 42%,transparent 74%)}""",
    'reflection falloff')

# 3. tighten the drop from the table to the plate now the reflection is shorter
rep("  margin-bottom:clamp(104px,13vw,178px)}", "  margin-bottom:clamp(86px,10.5vw,146px)}", 'stage gap')

open(p, 'w', encoding='utf-8').write(s)
print('D1 pass 2:', len(done), 'edits ->', ', '.join(done))
