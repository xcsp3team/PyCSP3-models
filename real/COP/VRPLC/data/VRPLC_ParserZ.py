from pycsp3.problems.data.parsing import *

data['T'] = number_in(line())
V = data['V'] = number_in(next_line())
data['Q'] = number_in(next_line())
data['L'] = number_in(next_line())
data['C'] = number_in(next_line())
P = data['P'] = number_in(next_line())
R = 2 * P
N = R + 2 * V
data["times"] = split_with_rows_of_size(numbers_in_lines_until(";"), N)
l = decrement(numbers_in(next_line()))
a = numbers_in(next_line())
b = numbers_in(next_line())
s = numbers_in(next_line())
q = numbers_in(next_line())
assert R == len(l) == len(a) == len(b) == len(s) == len(q)
data["requests"] = [OrderedDict([("l", l[i]), ("a", a[i]), ("b", b[i]), ("s", s[i]), ("q", q[i])]) for i in range(R)]
