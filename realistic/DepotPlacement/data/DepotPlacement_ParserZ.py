from pycsp3.problems.data.parsing import *

data['PSize'] = number_in(line())
next_line()
data['dists'] = [numbers_in(next_line()) for _ in range(14)]
