from pycsp3.problems.data.parsing import *

nAttributes = number_in(line())
next_line()
attributeDomains = decrement([numbers_in(next_line()) for _ in range(nAttributes)])
matchCosts = [numbers_in(next_line()) for _ in range(nAttributes)]
matchCostsSorted = [numbers_in(next_line()) for _ in range(nAttributes)]  # not used
data['attributes'] = [OrderedDict([("domain", attributeDomains[i]), ("matchCost", matchCosts[i])]) for i in range(nAttributes)]

next_line()  # attribute names
n = number_in(next_line())
m = number_in(next_line())
tails = decrement(numbers_in(next_line()))
heads = decrement(numbers_in(next_line()))
l = next_line()
data['matrix'] = [[1 if tok == "true" else 0 for tok in s.split(",")] for s in l[l.index("|") + 1:l.rindex("|")].split("|")]
assert n == len(data['matrix'])
cnodes = decrement(numbers_in(next_line()))
data['dnodes'] = decrement(numbers_in(next_line()))
data['anodes'] = decrement(numbers_in(next_line()))
assert len(data['anodes']) == 0  # for the current files
costs = numbers_in(next_line())  # costs of edges
assert m == len(tails) == len(heads) == len(costs)
data['arcs'] = [OrderedDict([("tail", tails[i]), ("head", heads[i]), ("cost", costs[i])]) for i in range(m)]
