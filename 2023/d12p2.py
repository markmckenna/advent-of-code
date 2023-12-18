#! python

# Overview: The input file lists sequences of springs, indicating each as damaged (#) or whole (.).
# Each row also indicates the sets of contiguous broken springs in that row as a series of numbers
# at the end of the row. However some rows contain damaged information, where springs are replaced
# by an equal number of ? symbols. You need to use the count info at the end of the row to work out
# how many possible ways there are to reconstruct each row, and add them together for the whole
# file.

# Strategy: this is a 1d version of one of those colour puzzles. A sequence of ? can cover a # only 
# if there is a number in the correct position that accommodates the visible pattern of adjacent
# symbols.
# 
# Examples:
# ??? matches 0 one way (...); 1,1 one way (#.#); 2 two ways (##. and .##); and 3 one way (###).
# #??? matches 1 (#...); 2 (##..); 3 (###.); 4 (####); 1,1 twice (#.#. #..#); 1,2 (#.##); 2,1 (##.#)
#
# The formula can be computed recursively, left to right, using a greedy choice based on options
# already taken. Visible hashes constrain the options by terminating the recursion early. Each
# sequence of numbers in a record of a given length has a finite number of matching configurations,
# and once a configuration is excluded, all of its child configurations (ones that match on the
# right but differ on the left) are also excluded.
#
# Optimizations: 
# - leading and trailing dots are non-constraining; consecutive visible dots are
#   non-constraining, so we can skip forward to shrink the search space.
# - fully visible hashes that match in a known location split the pattern; the two halves don't
#   affect each other, so we can take the option counts of each half and just multiply them.

# Idea: what if the record basically defines a regular expression? a pattern (1, 3, 1) is basically
#   a regex "[#?][.?]+[#?]{3}[.?]+[#?]". We can apply that pattern to the symbolic part of the record
#   to see if it matches. Can we ask python's regex mechanism how many different ways it could match?

# Can we do this by only looking at the first character and recursing?
# - if . just recurse (the rest of the string has to match the pattern)
# - if # deduct 1 from the first pattern number and recurse (the rest of the string has to match what remains)
# - if ? we do both (once for each possibility)
# Issue: we need to differentiate between:
# - a 'free' pattern (we think we had a . before, so we are allowed to not consume)
# - a 'bound' pattern (we think we had a # before, so we have to consume)
# We can address that by passing a 'bound' flag. Inputs are (bound, record, pattern)
# Crap -- we also need to indicate when we require a non-hash symbol. So we have one where
#   we require a hash, one where we require a dot, and one where we don't care. So the
#   'bound' flag is upgraded to an 'expect' flag.
# - in the below, the first arg indicates our expectation; * means anything is okay.

# (# * empty) won't happen (we only give # if we have pattern value left)
# (* # empty) ret 0  # We have a symbol but no pattern segment; reject
# (* * empty) recurse(* rest empty)  # gotta make sure there are no future #es

# (# . *)    ret 0  # we are bound, but have no symbol; reject
# (* . *)    recurse(* rest all)  # no constraint (or constraint satisfied); consume nothing

# (# # 1)     recurse(* rest rest)  # we finished the pattern
# (# ? 1)     recurse(* rest rest)  # same as (# # 1) because it's the only option
# (# # 2+)    recurse(# rest -1)  # continue the pattern
# (# ? 2+)    recurse(#, rest, -1)  # same as (# # 2+) because it's the only option

# (. # *)     ret 0  # we needed a dot but we got a hash
# (. ? *)     recurse(* rest all)  # ? can serve as a . so we are ok; keep looking

# (* # 1)     recurse(. rest rest)  # ate a full pattern, we now require .
# (* # 2+)    recurse(# rest -1)  # incomplete pattern, we now require #

# (* ? 1)     recurse(* rest all) + recurse(. rest rest)  # both (* # 1) and (* . 1)
# (* ? 2+)    recurse(* rest all) + recurse(# rest -1)  # both (* # 2+) and (* . 2+)

import functools
import itertools
import numpy as np

@functools.cache
def rec_match(expect, record, pattern):
    """record is a string like '##???..#' and pattern is a list like [2,1,1].
       Find all the ways that we can match [pattern] by replacing question marks in [record]
       with hashes, such that each number positionally counts consecutive hashes."""

    while len(pattern) > 0 and pattern[0] == 0: pattern = pattern[1:]

    #print(expect, record, pattern)
    # Base case: no more record.
    if len(record) == 0: return int(len(pattern) == 0)
    symbol, rest = record[0], record[1:]

    # Simple case: no more pattern. We only need to ensure there are no more #es.
    if len(pattern) == 0:
        if symbol == '#': return 0  # Saw a #, but out of pattern
        return rec_match('*', rest, ())  # Ensure there are no more #

    # Total cases: #.* vs #.? vs 12 -> 18 possible, but many are similar.

    # Complex case: both record and pattern remaining. Pattern elements always positive.
    match (expect, symbol, pattern[0]):
        case ('#', '.', _) | ('.', '#', _): # 4 cases: We didn't get what we needed
            return 0
        case ('*'|'.', '.', _) | ('.', '?', _): # 6 cases: Unconstrained, or we got what we needed; scan further
            return rec_match('*', rest, pattern)
        case ('*'|'#', '#', 1) | ('#', '?', 1): # 3 cases: We definitely finished a segment; we now need a .
            return rec_match('.', rest, pattern[1:])
        case ('*'|'#', '#', p) | ('#', '?', p) if p>1: # 3 cases: We definitely started a segment; we now need a #
            return rec_match('#', rest, (p-1,)+pattern[1:])
        case ('*', '?', 1): # 1 case: Both (* . 1) and (* # 1)
            return rec_match('.', rest, pattern[1:]) + rec_match('*', rest, pattern)
        case ('*', '?', p) if p>1: # 1 case: Both (* . 2) and (* # 2)
            return rec_match('#', rest, (p-1,)+pattern[1:]) + rec_match('*', rest, pattern)

def match(record, pattern): return rec_match('*', record, pattern)

with open('d12.txt') as file:
    sum = 0
    for line in file:
        record,pattern = line.split(' ')

        record = '?'.join([record]*5)
        pattern = ','.join([pattern]*5)

        pattern = tuple([int(i) for i in pattern.split(',')])

        result = match(record, pattern)
        sum += result
    print(sum)
