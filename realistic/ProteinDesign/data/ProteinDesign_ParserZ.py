from pycsp3.problems.data.parsing import *

n = data['n'] = number_in(line())
d = data['d'] = number_in(next_line())
domains = numbers_in(next_line())
assert n == len(domains) and d == domains[0] and all(domains[i] == domains[0] for i in range(1, n))
top = number_in(next_line())  # not used
e1 = numbers_in(next_line())[1]
maxCtrs1 = numbers_in(next_line())[1]
data['maxCosts1'] = numbers_in(next_line())[1]
e2 = numbers_in(next_line())[1]
maxCtrs2 = numbers_in(next_line())[1]
data['maxCosts2'] = numbers_in(next_line())[1]

f1x = decrement(numbers_in(next_line())[1:])
nTuples1 = numbers_in(next_line())[1:]
offsets1 = numbers_in(next_line())[1:]
t1 = numbers_in(next_line())[1:]
assert data['maxCosts1'] == max(t1)
assert e1 == len(f1x) == len(nTuples1) == len(offsets1) and maxCtrs1 == len(t1)
data['c1s'] = [[f1x[j], t1[2 * offsets1[j]: 2 * offsets1[j] + nTuples1[j] * 2]] for j in range(e1)]

f2x = decrement(numbers_in(next_line())[1:])
f2y = decrement(numbers_in(next_line())[1:])
nTuples2 = numbers_in(next_line())[1:]
offsets2 = numbers_in(next_line())[1:]
t2 = numbers_in(next_line())[1:]
assert data['maxCosts2'] == max(t2)
assert e2 == len(f2x) == len(f2y) == len(nTuples2) == len(offsets2) and maxCtrs2 == len(t2)
data['c2s'] = [[f2x[j], f2y[j], t2[3 * offsets2[j]: 3 * offsets2[j] + nTuples2[j] * 3]] for j in range(e2)]
