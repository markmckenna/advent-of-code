#! python

import re
import numpy as np

# Cards are valued in this order, with later being more valuable.
card_ranks = 'J23456789TQKA'

def card_strength(x): return card_ranks.index(x)

def hand_strength(x):
    """Using poker-like ranking, with jacks being wild"""
    bins = np.bincount(np.fromstring(x, dtype='b'))

    jacks = 0
    if len(bins) >= 74:
        jacks = bins[74] # ASCII J
        bins = np.delete(bins, 74)

    ranked = np.sort(bins)[::-1]
    top = ranked[0] + jacks
    if top == 5: return 7
    if top == 4: return 6
    if top == 3:
        if ranked[1] == 2: return 5
        return 4
    if top == 2:
        if ranked[1] == 2: return 3
        return 2
    return 1

# Compute a key that starts with hand rank and is followed by original hand order
def hand_key(x): 
    return str(hand_strength(x)) + '-' + '-'.join([str(card_strength(i)).zfill(2) for i in x])

with open('./d7.txt') as file:
    hands = [line.strip().split(' ') for line in file]
    hands = [(hand[0], int(hand[1]), hand_key(hand[0])) for hand in hands]
    hands = sorted(hands, key=lambda x: x[2])

    total = 0
    for i,hand in enumerate(hands):
        hands[i] = (hand[0], hand[1], hand[2], (i+1)*int(hand[1]))
        total += (i+1)*int(hand[1])
    print(hands)
    print(total)
