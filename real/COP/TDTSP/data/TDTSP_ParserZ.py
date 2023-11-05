from pycsp3.problems.data.parsing import *

n = number_in(line())
data['durations'] = numbers_in(next_line())
assert n == len(data['durations'])
q = number_in(next_line())
assert q == 0
prec = numbers_in(next_line())[5:]
assert len(prec) == 0
data['nSteps'] = nSteps = number_in(next_line())
data['l'] = number_in(next_line())
r = number_in(next_line())
assert r == 0
which = numbers_in(next_line())
interval = numbers_in(next_line())[5:]
assert len(which) == len(interval) == 0
t = numbers_in(next_line())[7:]
assert len(t) == (n + 1) * (n + 1) * (nSteps + 1)
tt = split_with_rows_of_size(t, (n + 1) * (nSteps + 1))
for i in range(n + 1):
    tt[i] = split_with_rows_of_size(tt[i], nSteps + 1)
data['matrix'] = tt
