#! python

import re

scores = [0,1,2,4,8,16,32,64,128,256,512,1024,2048]

with open('./d4.txt', 'r') as file:
    total=0
    for line in file:
        print(line)
        card,winners,mine = re.split(r'[|:]', line)
        card = int(re.findall(r'[0-9]+', card)[0])
        winners = [int(x) for x in re.split(r'\s+', winners.strip())]
        mine = [int(x) for x in re.split(r'\s+', mine.strip())]
        matches = [i for i in mine if i in winners]
        total += scores[len(matches)]
    print(total)
