from pycsp3.problems.data.parsing import *

import re

n = number_in(line())
m = number_in(next_line())
data['tails'] = decrement(numbers_in(next_line()))
heads = decrement(numbers_in(next_line()))  # not used
assert m == len(data['tails']) == len(heads)
line = next_line()
line = re.split(',|\|', line[line.index("|") + 1:line.rindex("|")])
data['incidence_matrix'] = split_with_rows_of_size([0 if tok == "false" else 1 for tok in line], m)
line = next_line()
line = re.split(',|\|', line[line.index("|") + 1:line.rindex("|")])
outgoing = split_with_rows_of_size([0 if tok == "false" else 1 for tok in line], m)  # not used
assert n == len(data['incidence_matrix']) == len(outgoing)
