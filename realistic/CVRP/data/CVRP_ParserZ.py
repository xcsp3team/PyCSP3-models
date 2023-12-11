from pycsp3.problems.data.parsing import *

n = number_in(line())
data['capacity'] = number_in(next_line())
data['demands'] = numbers_in(next_line())
assert n == len(data['demands'])
data['distances'] = [numbers_in(next_line()) for _ in range(n + 1)]
