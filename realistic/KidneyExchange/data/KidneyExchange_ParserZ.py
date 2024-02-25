from pycsp3.problems.data.parsing import *

k = number_in(line())
v = number_in(next_line())
data['weights'] = [numbers_in(next_line()) for _ in range(v)]
data['k'] = k
