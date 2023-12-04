#! python

import re
import numpy as np

scores = [0,1,2,4,8,16,32,64,128,256,512,1024,2048]

with open('./d4.txt', 'r') as file:
    lines = [line for line in file]
    copies = np.ones(len(lines), dtype=np.int32)
    total=0
    for i,line in enumerate(lines):
        print(line)
        card,winners,mine = re.split(r'[|:]', line)
        card = int(re.findall(r'[0-9]+', card)[0])
        winners = [int(x) for x in re.split(r'\s+', winners.strip())]
        mine = [int(x) for x in re.split(r'\s+', mine.strip())]
        wins = len([i for i in mine if i in winners])
        print(wins)
        copies[i+1:i+1+wins] += copies[i]
    print(np.sum(copies))
