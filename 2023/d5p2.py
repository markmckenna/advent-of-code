#! python

# https://adventofcode.com/2023/day/5#part2
# 
# Strategy:
# - Put the input seed ranges into an interval tree of their own (the 'seed tree')
# - In each stage, intersect the seed tree with the stage map to produce a
#   more partitioned seed tree.
# - Transform the seed tree by applying the mapping from the stage map to each
#   interval (i.e. just the two endpoints of the newly partitioned intervals)
# - Aggregate adjacent intervals in the resulting map to form an 'annealed seed tree'
# - Find the least element in the final output tree. This will be the closest seed.

import sys
from utils import partition
from intervaltree import IntervalTree

def adjust(tree, value):
    entries = tree[value]
    if not entries: 
        return value
    offset = next(iter(entries)).data
    return value + offset

with open('./d5.txt', 'r') as file:
    lines = iter(file)

    # The first line is a list of ranges of seed numbers.
    seeds = [int(x.strip()) for x in next(lines).split(':')[1].strip().split()]
    next(lines) # consume a blank line

    # Build a 'seed tree' with original intervals
    seed_tree = IntervalTree()
    for i in range(len(seeds)//2):
        seed_tree[seeds[i*2]:seeds[i*2]+seeds[i*2+1]] = {}

    cur = seed_tree
    # Partition the remaining lines
    for section in partition(lines, lambda i: i != "\n"):
        label = next(section)
        # Build an interval tree storing the offset mapping.
        map_tree = IntervalTree()
        for line in section:
            dest,src,length = [int(x.strip()) for x in line.split()]
            map_tree[src:src+length] = dest-src

        # Slice up the intervals in the seed tree based on those in the map tree.
        for range in map_tree:
            cur.slice(range.begin)
            cur.slice(range.end)

        # Apply the tree to the begin and end of each seed range to get a new tree.
        new = IntervalTree()
        for range in cur:
            begin = adjust(map_tree, range.begin)
            end = adjust(map_tree, range.end-1)+1
            new[begin:end] = {}
        cur = new

    print(min(cur).begin)
