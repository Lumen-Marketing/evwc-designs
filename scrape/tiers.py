# -*- coding: utf-8 -*-
import re
p = 'index.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---- pull the three cards out so they can be re-ordered as a ladder --------
start = s.index('<div class="cards" id="cards">')
end = s.index('</div>\n\n<section class="matrix">')
block = s[start:end]
cards = re.findall(r'  <article class="card">.*?\n  </article>\n', block, re.S)
assert len(cards) == 3, len(cards)
by_name = {}
for c in cards:
    for n in ('Daylight', 'Broadsheet', 'Hazard'):
        if '<h2>%s</h2>' % n in c:
            by_name[n] = c
assert len(by_name) == 3

TIERS = [
    ('Broadsheet', 'Basic', 't1',
     'Conventional patterns done well: a card grid, a poster hero, a stat row. Quickest to build, easiest for anyone to extend later.'),
    ('Hazard', 'Standard', 't2',
     'A designed system rather than a set of cards: a ruled construction grid, bolted plates, a picture strip and a machined control block, all drawn from one rule set.'),
    ('Daylight', 'Premium', 't3',
     'Full-bleed footage, a pane of frosted glass the headline crosses, a bespoke gallery engine and service rows that text a quote. The most custom engineering of the three.'),
]

new_cards = []
for name, tier, cls, blurb in TIERS:
    c = by_name[name]
    c = re.sub(r'<span class="no">\d+</span>',
               '<span class="tier %s">%s</span>' % (cls, tier), c, count=1)
    c = c.replace('    <div class="card-bd">\n      <p>',
                  '    <div class="card-bd">\n      <p class="tierline">%s</p>\n      <p>' % blurb, 1)
    new_cards.append(c)

s = s[:start] + '<div class="cards" id="cards">\n\n' + '\n'.join(new_cards) + s[end:]
done.append('cards reordered and labelled')

# ---- the chip itself is the ladder: outline, cyan outline, cyan filled -----
rep(""".card-hd .no{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.16em;color:var(--cy);font-weight:700}""",
""".card-hd .tier{font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;
  letter-spacing:.18em;text-transform:uppercase;padding:6px 10px;line-height:1;
  border:1px solid var(--s700);color:var(--s300)}
.card-hd .tier.t2{border-color:rgba(18,196,222,.55);color:var(--cy)}
.card-hd .tier.t3{background:var(--cy);border-color:var(--cy);color:#06232a}
.tierline{color:var(--paper)!important;font-weight:500}""", 'tier chip css')

rep("""<h1>Three industrial<br>homepage <em>directions</em></h1>""",
    """<h1>Three homepages,<br>three <em>tiers</em></h1>""", 'h1')

rep("""<p>Same business, same section order, three completely separate builds with no shared components. Every photo and every clip is <b>their own</b>, pulled from the Instagram account. The reels <b>auto-play muted and loop</b>, and pause when they scroll out of view.</p>""",
    """<p>Same business, same section order, three completely separate builds with no shared components. They ladder <b>basic, standard and premium</b> by how much bespoke work is in them, not by how much content they hold. Every photo and every clip is <b>their own</b>, pulled from the Instagram account. The reels <b>auto-play muted and loop</b>, and pause when they scroll out of view.</p>""",
    'lead')

rep("""<thead><tr><th>Section</th><th>01 Daylight</th><th>02 Broadsheet</th><th>03 Hazard</th></tr></thead>""",
    """<thead><tr><th>Section</th><th>Basic &middot; Broadsheet</th><th>Standard &middot; Hazard</th><th>Premium &middot; Daylight</th></tr></thead>""",
    'matrix head')

rep("""<meta name="description" content="Three industrial homepage design directions for East Valley Window Cleaning LLC, Mesa AZ. Real photos and auto-playing Instagram reels.">""",
    """<meta name="description" content="Three homepage tiers for East Valley Window Cleaning LLC, Mesa AZ: basic, standard and premium. Real photos and auto-playing Instagram reels.">""",
    'meta')

open(p, 'w', encoding='utf-8').write(s)
print('tiers:', len(done), 'edits ->', ', '.join(done))
