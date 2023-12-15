#! python

import numpy as np
from collections import deque

# For this part, the goal is to find the area enclosed by the pipe.
# This is a directional winding puzzle: we need to traverse the pipe in one direction
# all the way back to the origin, flagging tiles that are reachable from the same side
# of the pipe without crossing it.
# Since the pipe doesn't cross itself we don't have to deal with negative excluded areas,
# and all enclosed areas will be connected if you include the pipe itself as part of the
# enclosed area. We have to deduct the cost of the pipe itself from the final number, 
# though.
#
# Approach: 
# - traverse the pipe to collect all cells that are included.
#   - keep a 'winding' number: start at 0, +1 for CW, -1 for CCW. It should end at +4 or -4.
# - add pipe elements to a unique queue of starting cells. Mark which of each is the 'out' end.
# - if the winding number is negative, we walked the loop net-counterclockwise: reverse the queue
# - walk the queue. For each cell in the queue:
#   - if it's on the pipe loop, add the cell one step clockwise from the 'out' end to the set.
#     - since it's a unique queue, if we have seen this cell already, we won't add it again
#   - if it's not on the pipe loop, count it as 'contained' and enqueue its neighbours.
# - once we've walked the whole queue, our counter should be correct.

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

left,right,up,down = point(0,-1), point(0,1), point(-1,0), point(1,0)

# Relative positions indicated by each special symbol
directions = {
    b'F': points([right, down]),
    b'L': points([right, up]),
    b'J': points([left, up]),
    b'7': points([left, down]),
    b'|': points([up, down]),
    b'-': points([left, right]),
    b'.': points([[0, 0], [0, 0]])
}

def points_equal(left, right):
    """Pairwise compare points in left/right. Left and right have to be size compatible.
       The resultant array will be 1 dimension lower than the input arrays, returning
       True or False for every full point (pair of coordinates) in both inputs once
       broadcasted."""
    return np.logical_and.reduce(left == right, axis=-1)

def points_unequal(left, right):
    return np.logical_or.reduce(left != right, axis=-1)

counterclockwise = [(left, b'J'), (up, b'L'), (right, b'F'), (down, b'7')]
clockwise = [(left, b'7'), (up, b'J'), (right, b'L'), (down, b'F')]

def turn_dir(side, symbol):
    """Return -1, 0 or +1 depending on whether this is a left, straight or right
    piece relative to the side we came in on."""
    if any(points_equal(a, side) and b == symbol for a,b in counterclockwise): return -1
    if any(points_equal(a, side) and b == symbol for a,b in clockwise): return 1
    return 0

with open('./d10-mod.txt') as file:
    # Read 2d grid of bytes from file into a 2d array of bytes
    network = np.genfromtxt(file, dtype="S1", delimiter=1)

    # Get the position of the start node
    start = find(network, b'S')[0]

    # Find the first neighbour with one end pointing back at start
    neighbours = start + points([left, up, right, down])
    neighbour_ends = neighbours[:,None,:] + [directions[s] for s in network[indices(neighbours)]]
    matches = np.logical_or.reduce(points_equal(neighbour_ends, start), axis=-1)
    next = neighbours[np.argwhere(matches)][0,0]

    # Enumerate the path all the way back to the start. Store the winding value, and enqueue
    # each pipe segment for later consumption.
    wind = 0
    queue = deque()
    last = start
    while True:
        direction = last-next
        symbol = network[index(next)]
        queue.append((next, symbol))
        if points_equal(start, next): break
        wind += turn_dir(direction, symbol)
        candidates = next + directions[symbol]
        last,next = next,candidates[points_unequal(candidates, last)][0]

    # If the winding direction is counterclockwise (negative), reverse the queue
    # To reverse the queue, we need to reverse every element in the queue, but we also
    # have to invert the direction we are approaching each element from.
    # Should we divorce from that field maybe?
    if wind < 0: queue.reverse()

    # Record all items in the queue as 'seen'; start counting contained squares.
    seen = {(y,x) for (y,x),_ in queue}
    count = 0

    def dequeue(): return queue.popleft()

    def enqueue(*points):
        """Enqueue all given points, if they haven't already been seen. Also mark each as seen.
           Also performs grid bounds checking."""
        for point in points:
            y,x = point
            if not 0 <= y < network.shape[0] or not 0 <= x < network.shape[1]: 
                # This should never happen, because we're only inspecting enclosed things.
                return
            if (y,x) in seen: return
            queue.append((point, b'.'))
            seen.add((y,x))

    last_pipe = start
    while len(queue) > 0:
        next,symbol = queue.popleft()

        # Any non-pipe square that made it into the queue is considered inside the pipe. We
        # count this toward our total of enclosed spaces, and we also enqueue all four
        # neighbours, unless they've already been seen.
        if symbol == b'.':
            network[index(next)] = b'I'
            count += 1
            enqueue(next+up, next+down, next+right, next+left)
            continue

        direction = last_pipe-next
        last_pipe = next

        # Enqueue any items that could be located on the inside of a clockwise-winding curve.
        # For example if we enter from the left, a tight clockwise turn would be a '7' exiting
        # downward. This adds nothing to the set of contained entities, because it has no
        # neighbour between the exit and the entrance in a clockwise direction. However if we
        # saw a '-' then the square below it is potentially included in the set, and if we saw
        # a 'J', then the squares below and to the right would both be potentials.
        if points_equal(direction, left):
            match symbol:
                case b'7': pass
                case b'-': enqueue(next+down)
                case b'J': enqueue(next+right, next+down)
        elif points_equal(direction, up):
            match symbol:
                case b'J': pass
                case b'|': enqueue(next+left)
                case b'L': enqueue(next+left, next+down)
        elif points_equal(direction, right):
            match symbol:
                case b'L': pass
                case b'-': enqueue(next+up)
                case b'F': enqueue(next+up, next+left)
        elif points_equal(direction, down):
            match symbol:
                case b'F': pass
                case b'|': enqueue(next+right)
                case b'7': enqueue(next+right, next+up)

    for j in range(network.shape[1]):
        for i in range(network.shape[0]):
            if (i,j) not in seen:
                network[i,j] = b'O'

    for i in range(network.shape[0]):
        print(''.join(network[i].astype(str)))
    print(wind)
    print(count)
