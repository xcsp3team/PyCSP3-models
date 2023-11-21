from pycsp3.problems.data.parsing import *

nNodes = number_in(line())
data['distances'] = [numbers_in(next_line()) for _ in range(nNodes)]
assert all(len(row) == nNodes for row in data['distances'])
data['windows'] = [numbers_in(next_line()) for _ in range(nNodes)]
assert all(len(row) == 2 for row in data['windows'])
