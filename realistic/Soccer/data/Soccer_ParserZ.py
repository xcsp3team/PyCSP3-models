from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
n = number_in(line())
next_line()
skip_empty_lines(or_prefixed_by="%")
data['games'] = decrement(split_with_rows_of_size(numbers_in(line()), 2))
next_line()
skip_empty_lines(or_prefixed_by="%")
data['initial_points'] = numbers_in(line())
next_line()
skip_empty_lines(or_prefixed_by="%")
m = split_with_rows_of_size(numbers_in(line()), 3)
assert all(v == 1 for _, v, _ in m)
data['positions'] = [(u - 1, w) for u, _, w in m]  # m #split_with_rows_of_size(numbers_in(line()), 3)

assert n == len(data['initial_points'])
