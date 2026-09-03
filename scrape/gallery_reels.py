# -*- coding: utf-8 -*-
p = 'index.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

rep("Media sits in lit enclosures with diffused shadows, the reel wall staggers on the z-axis, and everything resolves out of a blur as it enters.",
    "Media sits in lit enclosures with diffused shadows, the two clips stand as a symmetric pair on a lit table, and everything resolves out of a blur as it enters.",
    'd1 body')

rep("<tr><td>Reels</td><td>Three tall frames edge to edge, captions sitting underneath</td><td>Three 40px-radius blocks, floating pill captions</td><td>Three taped channel bays, two REC and one marked still</td></tr>",
    "<tr><td>Reels</td><td>Two clips as a symmetric pair on a lit table, captions set inside the tray, before and after as one hinged plate below</td><td>Two clips with their colour planes mirrored outward, before and after as a wide plate on the centre line</td><td>Two bolted bays with mirrored hard offsets, before and after in one taped housing</td></tr>",
    'matrix reels row')

rep("<p>Their third reel turned out to be a <b>static image</b> posted as a reel, so it runs as a still rather than as fake footage.</p>",
    "<p>A third post turned out to be a <b>static before and after</b> rather than footage. Both halves of it were cut out as separate photographs and are shown as a matched pair, so nothing on the page pretends to be moving when it is not.</p>",
    'still note')

rep("""No invented statistics, and <b>no offer or discount anywhere</b>, because there isn't one running. The "20% off" burned into their before/after reel has been masked out.""",
    """No invented statistics, and <b>no offer or discount anywhere</b>, because there isn't one running. The "20% off" that was burned into their before/after post falls outside the two crops used here.""",
    'offer note')

rep('<span class="chip">Three planes</span><span class="chip">Diffused lift</span>',
    '<span class="chip">Three planes</span><span class="chip">Light table</span>', 'd1 chips')

open(p, 'w', encoding='utf-8').write(s)
print('gallery:', len(done), 'edits ->', ', '.join(done))
