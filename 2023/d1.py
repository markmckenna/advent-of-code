#! python

import re

digit_names = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
todigit = lambda s: int(s if s.isdigit() else digit_names.index(s)+1)
pattern = f'([0-9]|{"|".join(digit_names)})'

with open('./d1.txt', 'r') as file:
    sum = 0
    for line in file:
        first = todigit(re.search(pattern, line).group(1))
        last = todigit(re.search(f'.*{pattern}', line).group(1))
        sum += first*10 + last
    print(sum)
