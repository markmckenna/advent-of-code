#! python

import re

# Best solution: quadratic formula
from math import sqrt, floor

def roots_of(time, distance):
    """Compute the roots of the problem curve for given time and distance parameters."""
    A = time/2
    B = sqrt(A**2 - distance)
    return (A-B, A+B)

with open('./d6.txt') as file:
    time = int(re.sub('\s+', '', next(file).split(':')[1]))
    distance = int(re.sub('\s+', '', next(file).split(':')[1].strip()))

    low, high = roots_of(time, distance)
    print(floor(high)-floor(low))


import sys
sys.exit(0)


def distance(time, i): 
    """Compute the distance value for a given hold time and race time."""
    return i*(time - i)

# There is a constant time solution here, I think.
# It's a simple 1-arg function, f(x) = x*(T-x) - K, where T is the total race time and
# K is the best time so far. The answer is the number of (integer) data points for which
# y > 0:
# 
# Inequality: all values x s.t. Tx - x^2 - K > 0
#
# Since we want to know just the range of x values for which y>0, we really just need
# to compute the two x intercepts which will act as the ends of that range.
# 
# Quadratic formula: -x^2 + Tx - K = 0
# 
# Quadratic root formula: x = (-b ± sqrt(b^2 - 4ac)) / 2a
#   where a=-1, b=T, c=-K
#   So our roots are at:  x = (-T ± sqrt(T^2 - 4K)) / -2
#
# Example: T=40, K=219
#   x = (-40 ± sqrt(1600-876)) / -2
#     = (-40 +- 26.9072) / -2
#     = (-13.0928, -66.9072) / -2
#     = (6.5464, 33.4536)
#
# Another formulation: x = T/2 +- sqrt((T/2)^2 -K)
#   x = 20 +- sqrt(20^2 - 219)
#     = 20 +- 13.4536
# -- that's also correct, and easier.

# Mathematica says the roots are 20-13.45, 20+13.45 -> 6-7, 33-34. Does that work?
#   d(6) = 6*(40-6) = 204
#   d(7) = 7(40-7) = 231
#   d(33) = 231
#   d(34) = 204
#  - Yes it does. So my problem is math, not method.

import numpy as np

with open('./d6.txt') as file:
    time = int(re.sub('\s+', '', next(file).split(':')[1]))
    distance = int(re.sub('\s+', '', next(file).split(':')[1].strip()))

    # geometric solution: compute the roots of the quadratic, round both in the same
    # direction, and subtract
    low, high = roots_of(time, distance)
    print(floor(high)-floor(low))

    # brute force solution: loop over all possible results, do math and sum
    total = 0
    for i in range(1,time):
        if i*(time-i)> distance:
            total += 1
    print(total)

    # numpy solution: build an array of all possible results, do vector math, filter and sum
    arr = np.arange(1,time)
    results = arr*(time-arr)
    diff = results > distance
    print(sum(diff))
