#! python

import itertools
import functools
import numpy as np

# The first time around we needed to double blank lines, so we just did it in place. This time
# around we need to multiply blank lines by a million, which will likely not be remotely feasible
# to do that with.
#
# The Manhattan distance equation simply sums row and column values. So we can basically just
# modify our endpoints:
# - Find the rows and columns that need to be multiplied (done)
# - For each pair of points, count the expanded rows/cols that fall between the two points,
#   and increase the higher of the two numbers by 1M for each one, in both axes.
# - calculate as below.

# How much to increase empty rows/columns by
scale = 1_000_000

def distance(p1, p2, bonus_cols, bonus_rows):
    y0,y1 = sorted([p1[0], p2[0]])
    x0,x1 = sorted([p1[1], p2[1]])
    r = sum(1 for i in bonus_rows if y0 < i < y1)
    c = sum(1 for i in bonus_cols if x0 < i < x1)
    return y1-y0 + r*(scale-1) + x1-x0 + c*(scale-1)

space = np.genfromtxt('d11.txt', dtype="S1", comments=None, delimiter=1)
# Axis 0 is y (rows); axis 1 is x (columns)

dots = space == b'.'
empty_rows = np.logical_and.reduce(dots, axis=1).nonzero()[0]
empty_cols = np.logical_and.reduce(dots, axis=0).nonzero()[0]

galaxy_coords = (space == b'#').nonzero()
galaxy_pairs = zip(galaxy_coords[0], galaxy_coords[1])

print(sum(distance(a, b, empty_cols, empty_rows) 
          for a,b in itertools.combinations(galaxy_pairs, 2)))
