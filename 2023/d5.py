#! python

from utils import partition
from intervaltree import IntervalTree

def adjust(tree, value):
    entries = tree[value]
    if not entries: 
        print(f'no mapping for {value}, returning unchanged')
        return value
    offset = next(iter(entries)).data
    print(f'mapping {value}: adjusting by {offset}')
    return value + offset

# The file is broken into blank line delimited sections.
# The first section is one line that lists seeds to plant.
# Each following section defines a mapping from the previous domain to the next.
# Each section beyond the first has a header that we can ignore.
# The format is a set of lines 'dstrange, srcrange, length':
#   srcrange is the base of a range in the source domain
#   dstrange is the base of the same range in the destination domain
#   length is how long the range is.

with open('./d5.txt', 'r') as file:
    lines = iter(file)

    # The first line is a list of seeds.
    seeds = [int(x.strip()) for x in next(lines).split(':')[1].strip().split()]
    next(lines) # consume a blank line

    mapped = seeds
    # Partition the remaining lines
    for section in partition(lines, lambda i: i != "\n"):
        print('processing ', next(section)) # Discard the section header

        # Build an interval tree storing the offset mapping.
        tree = IntervalTree()
        for line in section:
            dest,src,length = [int(x.strip()) for x in line.split()]
            print(f'loading range from {src} to {src+length} with adjustment ({dest-src})')
            tree[src:src+length] = dest-src

        # Apply the tree to each seed to get its position in the new domain.
        mapped = [adjust(tree, x) for x in mapped]

    print(min(mapped))
