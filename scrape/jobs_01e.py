# -*- coding: utf-8 -*-
# The photographic band directly under the services row was job-pole-wide.jpg:
# a wide frame of a dark storefront with an operator and a pole at the right.
# The new services lead is a wide frame of a storefront with an operator and a
# pole at the right. Two of those in a row, 280px apart, read as one picture
# printed twice.
#
# job-pole-wide.jpg is also the blurred ground of the Owner Operated section
# ABOVE the services row, so it was carrying the page twice already, once
# either side of the same section.
#
# The band takes restaurant.jpg instead: an interior looking OUT through clean
# commercial glazing. It is the opposite composition to the lead, it is the
# view through the glass rather than a person working on it, and the band's
# own copy is about what a customer sees. The veil on that band runs .9 to .22
# left to right and the type sits in the .9 end, so the swap cannot move the
# contrast.
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


rep("""<section class="photoband">
  <img src="assets/job-pole-wide.jpg" width="1280" height="722" loading="lazy"
       alt="A water-fed pole worked up the elevation of a two storey building">""",
    """<section class="photoband">
  <img src="assets/restaurant.jpg" width="1400" height="1750" loading="lazy"
       alt="The view out through cleaned restaurant frontage glazing to the car park">""",
    'photoband ground')

open(p, 'w', encoding='utf-8').write(s)
print('%s: %d edits -> %s' % (p, len(done), ', '.join(done)))
