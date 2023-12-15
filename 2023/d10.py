#! python

import numpy as np

# OK so basically we are working with up to 3 dimensional arrays here. The rightmost (deepest)
# dimension is always the two coordinates of the points. When there is a second dimension, we
# are always dealing with a simple list of points. When we add a third dimension though, we
# are usually grouping lists of points, so that each pointlist maps to a single input point.

# What that means is that, when we compare or adjust a 2d array to a 3d array, we almost 
# always want to broadcast the second dimension of the 2d array. This has the effect of taking
# each point in the list and multiplying it out so that it is repeated in each layer of the
# 3d list; as opposed to taking all the points in the 2d array, and mapping them into each
# grouped list in the 3d array.
#
# This is easier to see if we collapse the points into symbols, where each symbol represents
# a 1d array. Imagine the points in question were A1 B1 A2 B2. If my 2d array is [A1 B1] and my 3d 
# array is [[A1 A2]  [B1 B2]], then numpy will naturally want to broadcast so that the first
# array becomes [[A1 B1]  [A1 B1]]. Instead of associating each point in the list with a whole
# sublist, we end up cloning the list once for each sublist, which for our purposes links up
# points in irrelevant ways. We actually want the broadcasted list to look like
# [[A1 A1] [B1 B1]], multiplying each point in the first list so it gets consistently used
# with the whole first sublist.
#
# To make this happen we use numpy's broadcast placeholder indexing scheme: array[:,None,:].
# The colons represent axes that are kept, while the None represents the axis that is expanded.
# Numpy's default mode would look like array[None,:,:], spreading across the leftmost (outer) 
# axis; with this indexer we are telling numpy to keep that grouped and spread on the deeper
# axis.
#
# It may help to label each dimension with an intention. i.e. 'list of positions', versus
# 'sets of endpoints for positions'. This verbiage indicates that in the 3d case, each set
# of endpoints is associated with a position, so when mapping positions to endpoint sets, 
# you need to broadcast the positions within the endpoint sets, rather than across them.

# Match rules:
# - First, match [start] against all neighbour ends. This broadcasts
#   naturally in the right way, comparing coordinates directly against one another.
# - But we only want points that match exactly, so we apply AND to the rightmost dimension
#   (axis=-1), collapsing that dimension and returning true for each point individually.
# - But then, we want all neighbours that contain at least one matching point; so we
#   apply OR to the remaining rightmost dimension (axis=-1 of the collapsed array, which
#   would be axis=-2 of the original boolean array). This collapses it to a 1d array
#   where each element corresponds to one of the four original neighbours.
# - then we want to select neighbours using that array.

def point(x,y): 
    """Build a point from x/y indices as a numpy array"""
    return np.array((x,y))

def points(data): 
    """Build a 2d array of points from data that numpy will understand as pairs of numbers
       Input options: iterable of pairs, iterable of (2,1, int32) numpy arrays, 
         (2,n, int32) numpy array
    """
    if isinstance(data, np.ndarray): return data
    if isinstance(data, list): return np.array(data)
    return np.fromiter(data, dtype=np.dtype((np.int32, 2)))

def index(point):
    """Use the given point as an index into a 2d array"""
    return (point[0], point[1])

def indices(points): 
    """Return a selector treating the given 2*n array as a list of 2d coordinates."""
    return (points[:,0], points[:,1])

def equal_points(lhs, rhs):
    """Return True iff both x/y coordinates of both inputs are equal."""
    return np.any(lhs == rhs)

def first(iter): 
    """Take the first element of the iterator. Just for cognitive load purposes."""
    return next(iter)

def find(grid, item):
    """Return the position of all elements matching the given item."""
    return points(i for i,v in np.ndenumerate(network) if v == item)

# Note these are stored y/x, not x/y
left,right,up,down = point(0,-1), point(0,1), point(-1,0), point(1,0)

# Relative positions indicated by each special symbol
directions = {
    b'F': points([right, down]),
    b'L': points([right, up]),
    b'J': points([left, up]),
    b'7': points([left, down]),
    b'|': points([up, down]),
    b'-': points([left, right]),
}

def points_equal(left, right):
    """Pairwise compare points in left/right. Left and right have to be size compatible.
       The resultant array will be 1 dimension lower than the input arrays, returning
       True or False for every full point (pair of coordinates) in both inputs once
       broadcasted."""
    return np.logical_and.reduce(left == right, axis=-1)

def points_unequal(left, right):
    return np.logical_or.reduce(left != right, axis=-1)

with open('./d10.txt') as file:
    # Read 2d grid of bytes from file into a 2d array of bytes
    network = np.genfromtxt(file, dtype="S1", delimiter=1)

    def traverse(points):
        """Given a list of points, return the pipe neighbours of each"""
        symbols = network[indices(points)]
        # points is list of coords, but latter is list of lists of coords; so promote points
        return points[:,None,:] + [directions[s] for s in symbols]

    # Get the position of the start node
    start = find(network, b'S')[0]

    # Select all of the neighbours whose pipes have an end that points at the start
    #   (i.e. are validly connected to the start). There should be two.
    neighbours = start + points([left, right, up, down])
    neighbour_ends = traverse(neighbours)
    next = neighbours[
            np.logical_or.reduce(
                points_equal(neighbour_ends, start),
                axis=-1)]

    # Enumerate the path in both directions, capturing the two adjacent points for 
    #  each next point, excluding the one that we just traveled along. Count 
    #  how many steps we take until we find that the two branches have converged.
    i = 1
    last = points([start, start])
    while points_unequal(next[0], next[1]):
        i += 1
        candidates = traverse(next)
        matches = points_unequal(candidates, last[:,None,:])
        last,next = next,candidates[matches]
    print(i)
