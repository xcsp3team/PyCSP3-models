from pycsp3.problems.data.parsing import *

n, e = numbers_in(line())
data['n'] = n
data['nColors'] = n  # a trivial upper bound
data['edges'] = [numbers_in(next_line()) for _ in range(e)]
