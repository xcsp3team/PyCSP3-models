from pycsp3.problems.data.parsing import *

n = number_in(line()) + 1  # +1 for node 0 (depot)
data['capacity'] = number_in(next_line())
data['demands'] = [0] + numbers_in(next_line())  # 0 as demand for depot
assert n == len(data['demands'])
data['distances'] = [numbers_in(next_line()) for _ in range(n)]
