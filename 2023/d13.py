#! python

# Overview: The input file is a list of images. Each contains a reflection, either horizontal 
# or vertical. Reflections can pass the edge of the image and that's OK, but they can't be violated.
# Find the reflection in each image, and sum (cols left of reflection) + 100*(rows above reflection)
# across all images.

# Strategy:
# - Scan through the possible reflection lines in each image, scanning out to the edge of
#   the image until we either find a violation or run out of lines
# - We could optimize by representing each row/column by treating it as a bit pattern

from utils import partition
import numpy as np

trans = bytes.maketrans(b'#.', b'10')

def bitify(pattern): 
    """Turn the given string of # and . into number treating # as 1 and . as 0"""
    return int(pattern.translate(trans), 2)

def symmetrical(arr, idx):
    """Returns true iff [arr] is symmetrical about [idx], not counting overflow rows. An array
       is symmetrical if neither side of [idx] contains an entry that is mismatched to the
       corresponding entry on the other side. Note that this means that an array will always 
       be 'symmetrical' around 0 and [length], because there are no values to refute with."""

    l = len(arr)
    if not 0 <= idx <= l: raise IndexError('Index out of range')

    iters = max(idx, l-idx)
    for i in range(iters):
        low,high = idx-i-1,idx+i
        if low < 0 or high >= l: break
        if arr[low] != arr[high]:
            return False
    return True

with open('d13.txt') as file:
    total = 0
    for part in partition(file, lambda x: x != '\n'):
        image = np.genfromtxt(part, dtype='S1', delimiter=1, comments=None)
        # Turn the image into row values and column values
        image = ([bitify(row.tobytes()) for row in image],
                 [bitify(col.tobytes()) for col in image.T])

        # scan rows and columns for a reflection point
        reflection_value = 0
        for i in range(1, len(image[0])): # loop over non-edge positions
            if symmetrical(image[0], i):
                reflection_value = 100*i
                break
        if reflection_value == 0:
            for i in range(1, len(image[1])):
                if symmetrical(image[1], i):
                    reflection_value = i
                    break
        total += reflection_value
    print(total)
