#! python

# Overview: we have an input file that contains empty space ('.') and galaxies ('#').
# We need to twin all rows and columns that have no galaxies in them, and then
# compute the shortest distance between every pair of galaxies using only Manhattan
# distances.

# Strategy: Read the whole thing into an array, transform it based on row/column rules,
# and then for each pair of galaxies x and y, sum abs(x-y).

import itertools
import numpy as np

# WARNING: genfromtxt() uses # as a comment character.
space = np.genfromtxt('d11.txt', dtype="S1", comments=None, delimiter=1)
# Axis 0 is y (rows); axis 1 is x (columns)

# List all rows and columns that are entirely made up of dots
dots = space == b'.'
# Reducing along axis 1 (cols) yields results for axis 0 (rows)
empty_rows = np.logical_and.reduce(dots, axis=1).nonzero()[0]
empty_cols = np.logical_and.reduce(dots, axis=0).nonzero()[0]

# List all rows and columns with the ones above duplicated
new_cols = np.sort(np.append(empty_cols,range(space.shape[1])))
new_rows = np.sort(np.append(empty_rows,range(space.shape[0])))

# Expand the space using these row/column lists
space = space[:,new_cols][new_rows]

# Print the expanded space
for i in range(space.shape[0]):
    print(''.join(space[i].astype(str)))

# Now build an array with the coordinates of each galaxy
galaxy_coords = (space == b'#').nonzero()
galaxy_pairs = zip(galaxy_coords[0], galaxy_coords[1])

# Now compute the sum of distances of all pairs of coordinates!
total = sum(abs(a[0]-b[0]) + abs(a[1]-b[1]) for a,b in itertools.combinations(galaxy_pairs, 2))
print(total)
