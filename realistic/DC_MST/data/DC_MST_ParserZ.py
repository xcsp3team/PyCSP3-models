from pycsp3.problems.data.parsing import *

data['diameter'] = number_in(line())
radius = number_in(next_line())
assert radius == data['diameter'] // 2
data['edges'] = split_with_rows_of_size(decrement(numbers_in(next_line())), 2)
data['n'] = n = number_in(next_line())
m = number_in(next_line())
next_line(repeat=n + m + 1)
data['weights'] = numbers_in(next_line())
assert m == len(data['edges']) == len(data['weights'])
