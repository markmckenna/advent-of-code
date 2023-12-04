#! python

with open('./d3.txt', 'r') as file:
    gears,numbers=[],[]
    x0,y0,length,number=0,0,0,0
    for y,line in enumerate(file):
        for x,c in enumerate(line):
            if c.isdigit(): 
                if number==0: x0,y0=x,y
                number = number*10 + int(c)
                length+=1
            elif number>0:
                numbers.append((x0,y0,length,number))
                number,length=0,0
            if c == '*': gears.append((x,y))

    # Select pairs of numbers that are touching the same star.
    total=0
    for xg,yg in gears:
        adjacent = [(xn,yn,length,number) for xn,yn,length,number in numbers 
                    if xn-1<=xg<=xn+length and yn-1<=yg<=yn+1]
        if len(adjacent) == 2: total += adjacent[0][3]*adjacent[1][3]
    print(total)
