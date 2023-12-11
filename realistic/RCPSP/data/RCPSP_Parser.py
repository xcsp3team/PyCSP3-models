from pycsp3.problems.data.parsing import *

n = number_in(next_line(4))
horizon = number_in(next_line())
n_renewables = number_in(next_line(1))
n_unrenewables = number_in(next_line())
assert number_in(next_line()) == 0

t = numbers_in(next_line(3))  # not useful
next_line(2)
m1 = [numbers_in(next_line()) for _ in range(n)]
assert all(t[1] == 1 for t in m1)  # only one mode assumed
next_line(3)
m2 = [numbers_in(next_line()) for _ in range(sum(row[1] for row in m1))]
prev = None
for i, row in enumerate(m2):
    if len(row) == 3 + n_renewables + n_unrenewables:
        prev = row
    else:
        assert len(row) == 2 + n_renewables + n_unrenewables
        m2[i] = [prev[0]] + row
resources = numbers_in(next_line(3))

jobs = [OrderedDict([("duration", m2[i][2]), ("successors", decrement(m1[i][3:])), ("usages", m2[i][3:3 + n_renewables])]) for i in range(n)]
# ("unrewableUsage", m2[i][3 + n_renewables:])]))
data["jobs"] = jobs
data["horizon"] = horizon
data["renewable"] = resources[:n_renewables]
data["unrewable"] = resources[n_renewables:]
