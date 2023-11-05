from pycsp3.problems.data.parsing import *

nWorkers = number_in(line())
workLoads = numbers_in(next_line())
data['nDays'] = number_in(next_line())
next_line()
m = [numbers_in(next_line(), offset=-1) for _ in range(nWorkers)]
m = [[v for v in t if v < data['nDays']] for t in m]
unavailable = m
next_line(repeat=1)
m = [numbers_in(next_line(), offset=-1) for _ in range(nWorkers)]
m = [[v for v in t if v < data['nDays']] for t in m]
fixed = m
assert len(workLoads) == len(unavailable) == len(fixed)
data['workers'] = [OrderedDict([("workload", workLoads[i]), ("unavailableDays", unavailable[i]), ("fixedDays", fixed[i])]) for i in range(len(workLoads))]
next_line()
data['offset'] = number_in(next_line())
data['adjacency'] = number_in(next_line())
data['wednesday'] = number_in(next_line())
