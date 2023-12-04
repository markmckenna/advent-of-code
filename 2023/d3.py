#! python

# 2d grid of numbers. Numbers can take up multiple cells. Adjacency works in any direction,
# including diagonal, but not wrapping. We need to identify numbers and add them up.

# Naive: read into grid; scan for numbers; find adjacent symbols to numbers; find adjacent
#   digits; integerize; sum and return.

# Is there an optimization by walking forward and collecting numbers and symbols into a
# pool? We only need to look back at most one row, so anything further back than that can be
# ditched.
#
# Try 2: linear scan for non-dots. When a number is encountered, look back for symbols. 
#   When a symbol is encountered look back for numbers. When a match is encountered, seek
#   to the number and collect backward and forward for all adjacent digits, then enter it into
#   the sum.

digits = []
symbols = []

with open('./d3.txt', 'r') as file:
    # Build indexed lists of digits and (non-dot) symbols
    for y,line in enumerate(file):
        for x,c in enumerate(line.strip()):
            match c:
                case '.': pass
                case c if c.isdigit(): digits.append((x,y,c))
                case _: symbols.append((x,y,c))

    # for each digit, look for nearby symbols
    selected_digits = [(x,y,digit) for x,y,digit in digits
            if any(True for x1,y1,_ in symbols if x-1<=x1<=x+1 and y-1<=y1<=y+1)]

    # Extend this list to include digits directly adjacent to any selected digit, twice
    # Twice is enough, because no number is longer than 3 digits
    for _ in range(2):
        selected_digits = [
            (x,y,digit) for x,y,digit in digits
                 if any(True for x1,y1,_ in selected_digits if x-1<=x1<=x+1 and y==y1)]

    # Sum up horizontally adjacent digits
    out,number,x0,y0 = [],0,-1,-1
    for x,y,digit in selected_digits:
        if x0!=x-1 or y0!=y:
            out.append(number)
            number=0
        number = number*10 + int(digit)
        x0,y0=x,y
    out.append(number)
    print(sum(out))
