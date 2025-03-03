#! python

# Overview: The input file is a list of images. Each contains a reflection, either horizontal 
# or vertical. Reflections can pass the edge of the image and that's OK, but they can't be violated.
# Find the reflection in each image, and sum (cols left of reflection) + 100*(rows above reflection)
# across all images.

# Strategy:
# - Scan through the possible reflection lines in each image, scanning out to the edge of
#   the image until we either find a violation or run out of lines
# - We could optimize by representing each row/column by treating it as a bit pattern

# Part 2: We now have to find a single 'smudge' on each image where one symbol should be flipped,
# creating a different line of reflection. We don't know where the smudge is, but we know that
# there is exactly one, and that the image will have a different reflection line afterward.
# - Q: do we have to account for the possible continued existence of the first reflection line?
#   It's possible that the smudge exists somewhere that isn't a part of the original line's
#   reflected image, so it doesn't stop being a reflection after being de-smudged. I think we'd
#   better account for this by finding and discounting that option first.

# Strategy: We know there is one smudge, but we don't know which. We do know that the smudge will
# have to be in a region that is reflected, otherwise it wouldn't have been invalid before erasing
# the smudge. So we never have to look at the last row/column as it can only ever reflect something
# we've already seen. This is a small optimization though.
# - There will be a lot of repeat comparisons. Each smudge test only flips a single bit in the
#   whole image.
# - Let's try it naively first and see how fast it is--I don't think it'll break the bank.
# - If we want to make it faster, we should come up with a scheme for reusing subsections of each
#   reflection test. Dynamic programming solution probably works.

from utils import partition
import numpy as np

trans = bytes.maketrans(b'#.', b'10')

def bitify(pattern): 
    """Turn the given string of # and . into number treating # as 1 and . as 0"""
    return int(pattern.translate(trans)[::-1], 2)

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

def flip(image, row, col):
    """Flip the bit at the given row/col position, in both axes of image."""
    image[0][row] ^= (1 << col)
    image[1][col] ^= (1 << row)

def find_reflection(image, ignore=0):
    """Find a reflection axis somewhere in the image. If the axis is horizontal, return 100*index
       of the row at which it was found. If the axis is vertical, return just the index.
       If [ignore] matches the located value, ignore it and continue."""
    rows,cols = image[0], image[1]
    for i in range(1, len(rows)): # loop over the row gaps
        if symmetrical(rows, i): # if the image is symmetrical around that gap, return
            if 100*i != ignore: return 100*i
    for i in range(1, len(cols)): # loop over the column gaps
        if symmetrical(cols, i): # if the image is symmetrical, return
            if i != ignore: return i
    return 0

def print_image(image):
    print('rows', image[0])
    print('cols', image[1])

with open('d13.txt') as file:
    total = 0
    for part in partition(file, lambda x: x != '\n'):
        image = np.genfromtxt(part, dtype='S1', delimiter=1, comments=None)
        # Turn the image into row values and column values
        image = ([bitify(row.tobytes()) for row in image],
                 [bitify(col.tobytes()) for col in image.T])

        # scan rows and columns for a reflection point
        unsmudged_reflection = find_reflection(image)

        # That locates the un-smudged reflection point. Now, scan through possible smudge locations
        # until we find a *different* reflection point.
        # Un-smudging entails flipping one bit somewhere in the whole image. That bit contributes
        # to one number in each axis. 
        # To flip symbol (1,2) in row/col order:
        # - In the list of rows, select entry 1 (a number). In that number, select bit 2.
        # - In the list of columns, select entry 2. In that number, select bit 1.
        # For every bit (i,j), flip it, test for reflection, and flip it back. Return when found.
        result = 0
        for i in range(len(image[0])):
            for j in range(len(image[1])):
                flip(image, i, j)
                result = find_reflection(image, unsmudged_reflection)
                flip(image, i, j)
                if result != 0: break
            if result != 0: break

        total += result
    print(total)
