#! python

import re
import math

def process(list, converters): 
    """Turn the given list-like into a tuple using [converters] as a series of
    processing functions, one for each accepted element of the list.

    Any excess elements will be discarded."""
    return tuple([c(i) for c,i in zip(converters, list)])

def split(pat, str): return [s.strip() for s in str.split(pat)]

def to_dict(round): return dict(process(reversed(split(' ', i)), (str, int)) for i in round)

def power(set): return math.prod(set[k] for k in set)

def parse(line):
    print(line)
    id, line = split(':', line)

    id = int(split(' ', id)[1])

    rounds = [split(',', round) for round in split(';', line)]
    rounds = [to_dict(round) for round in rounds]

    return {'id': id, 'rounds': rounds}

def is_valid(game):
    """filter for part 1"""
    bag = { 'red': 12, 'green': 13, 'blue': 14 }
    for round in game:
        for colour in round:
            if bag[colour] < round[colour]: return False
    return True

def min_cubes_for(game):
    """computation for part 2"""
    set = {'red': 0, 'green': 0, 'blue': 0}
    for round in game:
        for colour in round:
            set[colour] = max(set[colour], round[colour])
    return set

with open('./d2.txt', 'r') as file:
    games = (parse(line) for line in file)
    minima = (min_cubes_for(game['rounds']) for game in games)
    print(sum(power(set) for set in minima))
