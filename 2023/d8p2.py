#! python

from itertools import cycle
import re
import numpy as np

extract_node = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')
is_a = re.compile(r'^..A$')
is_z = re.compile(r'^..z$')

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

    # Tabulate the nodes
    #table = {k:i for i,k in enumerate(graph.keys())}

    # Rebuild the graph using tabulated identifiers
    #graph = {table[k]:(table[v[0]],table[v[1]]) for k,v in graph.items()}

    # Build sets for the starting and finishing nodes
    # terminal = {v for k,v in table.items() if is_z.match(k)}
    # start = {v for k,v in table.items() if is_a.match(k)}
    terminal = {i for i in graph.keys() if is_z.match(i)}
    start = {i for i in graph.keys() if is_a.match(i)}

    # Precompute each originator's route through the graph
    # There will be a point where the list starts to loop back on itself. Find that point
    routes = {}
    for node in start:
        route = routes[node] = []
        cur = node
        for j,step in enumerate(path):
            route.append((j,step,cur))
            j += 1

    # Starting with all nodes ending in A, simultaneously navigate them all, until every node ends in Z at the same time.
    # - Use a set to eliminate duplication as we move through the graph
    i, cur = 0, start
    while not all(x in terminal for x in cur):
        i = i+1
        print(f'Round {i}: {cur}')
        dir = direction(next(path))
        cur = {graph[i][dir] for i in cur}

    # Hmm. What's the non-brute-force solution?
    # - there are a fixed number of key possibilities, I can make the comparison faster by tabulating them
    # - when we land on the same node twice at the same time, we fall into lockstep from that point forward so we can prune
    # ... neither of those panned out.
    #
    # What about cycle detection? When there's a closed cycle you can determine how often the matching value will come back around.
    # - So each starting point will traverse a specific cyclical path through the graph. It could be a long cycle.
    # - Certain points along that path will be terminal (end in z).
    # - The question is, how long will it take to loop all the cycles in parallel before
    #   they line up?

    # - for each starting point, iterate through the walking route until it repeats
    # - identify which positions are terminal, by offset
    # - advance all routes by the distance to the nearest next terminal position
    # - if all are terminal, that's it
