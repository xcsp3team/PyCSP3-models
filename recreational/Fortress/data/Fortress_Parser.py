from pycsp3.problems.data.parsing import *

n, m = numbers_in(line())
data['grid'] = [numbers_in(next_line()) for _ in range(n)]
