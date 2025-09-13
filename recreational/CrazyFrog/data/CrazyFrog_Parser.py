from pycsp3.problems.data.parsing import *

n, i, j = numbers_in(line())
data['frog'] = [i - 1, j - 1]
data['grid'] = [numbers_in(next_line()) for _ in range(n)]
