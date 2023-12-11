#! python

from itertools import cycle
import re
import numpy as np

extract_node = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')

dirs = {'L':0, 'R':1}
direction = lambda x: dirs[x]

with open('./d8.txt') as file:
    # Build a cyclic buffer for directions
    path = cycle(iter(next(file).strip()))
    next(file) # eat blank

    # Build a directed 2-graph for the network
    graph = {}
    for line in file:
        key,left,right = extract_node.match(line).groups()
        graph[key] = (left, right)

    print(graph)
        
    # Navigate the graph by following edges
    i,cur = 0,'AAA'
    while cur != 'ZZZ':
        i = i+1
        cur = graph[cur][direction(next(path))]
    print(i)
