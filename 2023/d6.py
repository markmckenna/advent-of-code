#! python

import re

with open('./d6.txt') as file:
    times = [int(i) for i in re.split(r'\s+', next(file).split(':')[1].strip())]
    distances = [int(i) for i in re.split(r'\s+', next(file).split(':')[1].strip())]

    games = list(zip(times, distances))
    print(games)

    # For each race, compute total distance traveled for each starting condition.
    # - filter out the ones that are too short
    # - opt: stop when you are worse than the record
    # - multiply the result

    product = 1
    for game in games:
        total = 0
        for i in range(1,game[0]):
            if i*(game[0]-i)> game[1]:
                total += 1
        product *= total

    print(product)
