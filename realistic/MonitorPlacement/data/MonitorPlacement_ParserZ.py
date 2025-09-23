from pycsp3.problems.data.parsing import *

n = data['n'] = number_in(line())
r = number_in(next_line())
b = number_in(next_line())
next_line()
data['ends'] = decrement(split_with_rows_of_size(numbers_in(next_line()), 2))
next_line(repeat=1)
ln = line()
data['routes'] = decrement([numbers_in(token) for token in ln[ln.find("{") + 1:ln.rfind("}")].split("},{")])
assert r == len(data['ends']) == len(data['routes'])
data['leaves'] = decrement(numbers_in(next_line()))
data['bi_comp'] = decrement(split_with_rows_of_size(numbers_in(next_line(repeat=1)), 2))
assert b == len(data['bi_comp'])
