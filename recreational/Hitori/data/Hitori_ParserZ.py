from pycsp3.problems.data.parsing import *

n = number_in(line())
data['clues'] = [numbers_in(next_line()) for _ in range(n)]
