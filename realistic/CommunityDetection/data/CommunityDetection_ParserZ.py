from pycsp3.problems.data.parsing import *

n = number_in(line())
data['nCommunities'] = number_in(next_line())
next_line(repeat=3)
data['together'] = split_with_rows_of_size(numbers_in_lines_until(";"), 2)
data['separate'] = split_with_rows_of_size(numbers_in_lines_until(";"), 2)
data['graph'] = split_with_rows_of_size(numbers_in_lines_until(";"), n)
data['W'] = W = split_with_rows_of_size(numbers_in_lines_until(";"), n)
assert all(len(t) == len(W) for t in W)
assert all(W[i][j] == W[j][i] for i in range(n) for j in range(n))
