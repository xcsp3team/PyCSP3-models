from pycsp3.problems.data.parsing import *

n = number_in(line())
data['inv'] = numbers_in(next_line())
assert n == len(data['inv'])
data['tab'] = split_with_rows_of_size(numbers_in(next_line()), n)
next_line(repeat=1)
data['k'] = number_in(next_line())
data['m'] = number_in(next_line())
data['ld'] = number_in(next_line())
