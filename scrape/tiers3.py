# -*- coding: utf-8 -*-
# Four directions become three, laddered Basic / Standard / Premium.
#
# The ladder is on how much bespoke build is in each one, because that is what
# actually costs money, and it means nothing has to be stripped out of the
# cheaper tiers to justify the ladder. Filenames do not change, so every link
# already sent still opens.
#
#   Basic     01 Mesic  conventional patterns done well. A drafting sheet grid,
#                       an accordion strip, a drag filmstrip. No scroll linked
#                       motion system at all.
#   Standard  03 Plate  a designed system rather than a set of components:
#                       bolted plates, a machined control block, an indexing
#                       rail, and machine motion driven by the scroll.
#   Premium   02 Site   a split screen archetype top to bottom, a camera motion
#                       system on GSAP, and a bespoke projector gallery.
import re, os

p = 'index.html'
s = open(p, encoding='utf-8').read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        print('!! MISS:', label); return
    s = s.replace(old, new, 1); done.append(label)

# ---- pull the cards out so they can be re-ordered and re-labelled ----------
start = s.index('<div class="cards" id="cards">')
end = s.index('</div>\n\n</main>')
block = s[start:end]
cards = re.findall(r'  <article class="card">.*?\n  </article>\n', block, re.S)
assert len(cards) == 4, len(cards)
by = {}
for c in cards:
    for n in ('Mesic', 'Site', 'Plate', 'Burst'):
        if '<h2>%s</h2>' % n in c:
            by[n] = c
assert len(by) == 4

# ---- what each tier buys when it is actually built -------------------------
# The three files here are homepage designs. This list is the SCOPE of the
# build, not a description of the mockup, and the card says so.
def rows(pages, contact, motion, seo):
    r = [('Homepage designed to this look', True, 'Every tier'),
         ('Their own photos, clips and reviews', True, 'Every tier'),
         ('Tap to call and tap to text', True, 'Every tier'),
         ('Service and contact pages', pages, 'Standard and up'),
         ('Working enquiry form, emailed and stored', contact, 'Standard and up'),
         ('Motion', motion, ''),
         ('SEO groundwork and Google Business schema', seo, 'Premium only')]
    out = []
    for label, on, note in r:
        if label == 'Motion':
            out.append('        <li class="yes"><b>Motion</b><span>%s</span></li>' % on)
            continue
        cls = 'yes' if on else 'no'
        mark = ('<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.4 6.2 12 13 4.6"/></svg>'
                if on else
                '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4.5 4.5 11.5 11.5M11.5 4.5 4.5 11.5"/></svg>')
        out.append('        <li class="%s">%s<b>%s</b>%s</li>'
                   % (cls, mark, label, ('<span>%s</span>' % note) if note and not on else ''))
    return '\n'.join(out)

TIERS = [
    ('Mesic', 'Basic', 't1',
     'Conventional patterns done well, and the only one of the three with no scroll driven motion system in it. That is the tier, not a criticism: it is the quickest to build and the easiest for anyone to pick up and extend later.',
     rows(False, False, 'Entry reveals only', False)),
    ('Plate', 'Standard', 't2',
     'A designed system rather than a set of components. One rule set draws the bolted plates, the machined control block, the recessed panels and the indexing rail, and the motion is driven by the scroll rather than by arrival.',
     rows(True, True, 'Scroll driven, throughout', False)),
    ('Site', 'Premium', 't3',
     'The most bespoke of the three. A split screen archetype carried top to bottom, a camera motion system, and a gallery engine built for this page and nothing else.',
     rows(True, True, 'Full editorial, scroll linked', True)),
]

new_cards = []
for name, tier, cls, why, incl in TIERS:
    c = by[name]
    c = re.sub(r'<span class="tier t\d">\d+</span>',
               '<span class="tier %s">%s</span>' % (cls, tier), c, count=1)
    c = c.replace('    <div class="card-bd">\n      <p class="tierline">',
                  '    <div class="card-bd">\n      <p class="whytier">%s</p>\n      <p class="tierline">' % why, 1)
    c = c.replace('      <div class="chips">',
                  '      <ul class="incl">\n%s\n      </ul>\n      <div class="chips">' % incl, 1)
    new_cards.append(c)

s = s[:start] + '<div class="cards" id="cards">\n\n' + '\n'.join(new_cards) + s[end:]
done.append('three cards, re-ordered and laddered')

# ---- the chip is the ladder: outline, cyan outline, cyan filled ------------
rep(""".card-hd .tier.t2{border-color:rgba(18,196,222,.55);color:var(--cy)}
.card-hd .tier.t3{background:var(--cy);border-color:var(--cy);color:#06232a}
.tierline{color:var(--paper)!important;font-weight:500}""",
""".card-hd .tier.t2{border-color:rgba(18,196,222,.55);color:var(--cy)}
.card-hd .tier.t3{background:var(--cy);border-color:var(--cy);color:#06232a}
.tierline{color:var(--paper)!important;font-weight:500}
.whytier{color:var(--s300)!important;font-size:13.5px!important;
  border-left:2px solid var(--cy);padding-left:13px}
/* what the tier buys when it is BUILT. The excluded rows are greyed rather
   than dropped, because the client has to be able to see what the next one up
   is for. */
.incl{list-style:none;margin:4px 0 0;padding:0;border-top:1px solid var(--s800)}
.incl li{display:flex;align-items:baseline;gap:9px;padding:9px 0;
  border-bottom:1px solid var(--s800);font-size:13px;line-height:1.4}
.incl li b{font-weight:500;color:var(--paper)}
.incl li span{margin-left:auto;font-family:'JetBrains Mono',monospace;font-size:9.5px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--s400);white-space:nowrap;padding-left:10px}
.incl svg{flex:0 0 13px;width:13px;height:13px;fill:none;stroke-width:2.2;
  stroke-linecap:round;stroke-linejoin:round;translate:0 2px}
.incl .yes{color:var(--paper)}
.incl .yes svg{stroke:var(--cy)}
.incl .no{color:var(--s500)}
.incl .no b{color:var(--s500);font-weight:400}
.incl .no svg{stroke:var(--s600)}""", 'tier chip and inclusion list css')

# the third card takes the full row rather than being stranded beside nothing
rep("""@media (min-width:900px){.cards{grid-template-columns:1fr 1fr}}""",
"""@media (min-width:900px){
  .cards{grid-template-columns:1fr 1fr}
  /* three cards in a two column grid strands the last one beside half a screen
     of nothing, so it takes the whole row */
  .cards .card:last-child{grid-column:1 / -1}
}""", 'third card spans')

rep("""    <h1>One page,<br>four <em>directions</em></h1>""",
    """    <h1>One page,<br>three <em>tiers</em></h1>""", 'h1')

rep("""      <p>Same business, same section order, same words and the same photographs. Four completely separate builds with <b>no shared components</b>: each one owns its own material, its own type pairing and its own depth device, so they read as four designs rather than four colourways. Every photo and every clip is <b>their own</b>, pulled from the Instagram account. The reels <b>play muted and loop</b>, and pause when they scroll out of view.</p>""",
"""      <p>Same business, same section order, same words and the same photographs. Three completely separate builds with <b>no shared components</b>: each one owns its own material, its own type pairing and its own depth device, so they read as three designs rather than three colourways. They ladder on <b>how much bespoke build is in them</b>, not on how much content they hold, so nothing has been stripped out of the cheaper one to justify the ladder. Every photo and every clip is <b>their own</b>, pulled from the Instagram account. The reels <b>play muted and loop</b>, and pause when they scroll out of view.</p>
      <p class="mono note">All three previews are the <b>homepage</b>. The list on each card is what that tier includes when it is built.</p>""",
    'lead')

rep("""<meta name="description" content=""",
    """<meta name="description" content=""", 'noop')

open(p, 'w', encoding='utf-8').write(s)
print('index:', len(done), 'edits ->', ', '.join(done))

# ---- the file itself -------------------------------------------------------
if os.path.exists('04-burst.html'):
    os.remove('04-burst.html'); print('removed 04-burst.html')
