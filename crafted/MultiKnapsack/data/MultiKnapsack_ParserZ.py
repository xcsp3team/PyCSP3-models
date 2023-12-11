from pycsp3.problems.data.parsing import *

n = number_in(line())
m = number_in(next_line())
opt = number_in(next_line())
profits = numbers_in(next_line())
binSizes = numbers_in(next_line())
next_line()
data['weights'] = [numbers_in(next_line()) for _ in range(m)]
data['profits'] = profits
data['binSizes'] = binSizes
data['opt'] = opt
assert n == len(data['profits']) and m == len(data['binSizes'])
