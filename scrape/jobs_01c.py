# -*- coding: utf-8 -*-
# Two photographs swap places, for a reason that only showed up once the lead
# detail ran at the full 1240px measure.
#
# storefront.jpg is a shopfront covered in ANOTHER business's advertising. At
# 627px that was a picture of clean glass. At 1240px the most legible text in
# the section became "NOTARY SERVICES, SHREDDING, FED EX, UPS, US MAIL" and a
# working phone number that is not the client's. A homepage cannot carry a
# competitor-sized advert for a third party, or a number a customer might ring.
#
# job-glass-wide.jpg is the trade itself: a pole and a squeegee being worked
# across commercial glass, with the operator in frame. It is 16:9, so the
# 2.15:1 crop barely touches it, and it is a far stronger lead for Glass than
# a static shopfront.
#
# The shopfront moves down to the accordion, where it sits at about 180px and
# the third party signage is illegible.
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


# the lead detail takes the working shot
rep("""      <div class="vp"><img src="assets/storefront.jpg" width="1200" height="1200" loading="lazy" alt="Clean commercial storefront glazing at street level"></div>""",
    """      <div class="vp"><img src="assets/job-glass-wide.jpg" width="1280" height="722" loading="lazy" alt="A water-fed pole and squeegee worked across commercial glazing"></div>""",
    'lead photo')

# the accordion gives up the working shot and takes the shopfront
rep("""        <img src="assets/job-glass-wide.jpg" width="1280" height="722" loading="lazy" alt="Window frames and screens being worked on">""",
    """        <img src="assets/storefront.jpg" width="1200" height="1200" loading="lazy" alt="Storefront frames, mullions and sliding tracks at street level">""",
    'accordion photo')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
