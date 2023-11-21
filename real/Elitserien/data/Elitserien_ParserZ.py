from pycsp3.problems.data.parsing import *

data['noHome'] = [numbers_in(next_line()) for _ in range(14)]
assert all(len(row) == 33 for row in data['noHome'])
next_line()
data['group1'] = decrement(numbers_in(next_line())[1:])
data['group2'] = decrement(numbers_in(next_line())[1:])
line = next_line()
derbySets = decrement([numbers_in(tok) for tok in line[line.index("{") + 1:line.rindex("}")].split("}, {")])
derbyPeriods = decrement(numbers_in(next_line()))
assert len(derbySets) == len(derbyPeriods)
data['derbys'] = [OrderedDict([("set", derbySets[i]), ("period", derbyPeriods[i])]) for i in range(len(derbySets))]
line = next_line()
data['cPairs'] = decrement([numbers_in(tok) for tok in line[line.index("{") + 1:line.rindex("}")].split("}, {")])
assert all(u <= v for u, v in data['cPairs'])
