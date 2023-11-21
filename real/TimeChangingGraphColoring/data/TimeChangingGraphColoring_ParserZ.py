from pycsp3.problems.data.parsing import *

data['k'] = number_in(line())
n = number_in(next_line())
m = number_in(next_line())
tails = decrement(numbers_in(next_line()))
heads = decrement(numbers_in(next_line()))
assert m == len(tails) == len(heads)
data['edges'] = [(heads[i], tails[i]) for i in range(m)]
next_line()
skip_empty_lines(or_prefixed_by="%")
data['init_coloring'] = decrement(numbers_in(line()))[3:]
data['final_coloring'] = decrement(numbers_in(next_line()))[3:]
assert n == len(data['init_coloring']) == len(data['final_coloring'])
