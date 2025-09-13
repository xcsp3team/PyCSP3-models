from pycsp3.problems.data.parsing import *
from pycsp3.tools.utilities import combinations

data['cards'] = t = numbers_in(next_line())
assert all(t[i] != t[j] for i, j in combinations(len(t), 2))
