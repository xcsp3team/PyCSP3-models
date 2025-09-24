from pycsp3.problems.data.parsing import *

n, nColors = numbers_in(line())
data['nColors'] = nColors
data['patch'] = [numbers_in(next_line()) for _ in range(n)]
