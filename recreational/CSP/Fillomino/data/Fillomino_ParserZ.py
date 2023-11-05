from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
n = number_in(line())
m = number_in(next_line())
next_line()
data['clues'] = [numbers_in(next_line()) for _ in range(n)]
