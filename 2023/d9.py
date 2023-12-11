#! python

import numpy as np

def parse(line): return np.array(line.split(), dtype=np.int32)

def extrapolate(array):
    layers = [array]
    while layers[-1].any():
        layers.append(np.diff(layers[-1])) 
    return sum(arr[-1] for arr in layers)

with open('./d9.txt') as file:
    print(sum([extrapolate(parse(line)) for line in file]))
