#! python

import numpy as np

parse = lambda line: np.array(line.split(), dtype=np.int32)

def extrapolate_back(iter):
    """Starting at the last line in the iterator, keep taking the difference between
    the current value and the first element of the prior line in the iterator."""
    cur = 0
    for arr in reversed(list(iter)):
        cur = arr[0] - cur
    return cur

def extract_pattern(array):
    yield array
    while array.any(): 
        yield (array := np.diff(array))

with open('./d9.txt') as file:
    print(sum(
        extrapolate_back(extract_pattern(parse(line))) for line in file
    ))
