from pycsp3.problems.data.parsing import *

nMinerals = number_in(line())
data['flows'] = numbers_in(next_line())
nRecipes = number_in(next_line())
line = next_line()
t = numbers_in(line[line.find("["):])
data['recipes'] = [[t[i * nMinerals + j] for j in range(nMinerals)] for i in range(nRecipes)]
nOrders = number_in(next_line())
ot = numbers_in(next_line(), offset=-1)
oh = numbers_in(next_line())
ow = numbers_in(next_line())
assert nOrders == len(ot) == len(oh) == len(ow)
data['orders'] = [OrderedDict([("t", ot[i]), ("h", oh[i]), ("w", ow[i])]) for i in range(nOrders)]
data['nLines'] = number_in(next_line())
nRules = number_in(next_line())
rt = numbers_in(next_line(), offset=-1)
rk1 = decrement(numbers_in(next_line())[1:])
rd = numbers_in(next_line())
rk2 = decrement(numbers_in(next_line())[1:])
assert nRules == len(rt) == len(rk1) == len(rd) == len(rk2)
data['rules'] = [OrderedDict([("t", rt[i]), ("k1", rk1[i]), ("d", rd[i]), ("k2", rk2[i])]) for i in range(nRules)]
