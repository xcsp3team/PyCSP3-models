from pycsp3.problems.data.parsing import *


def shorten(t):
    return [v for v in t if v >= 0]


n = number_in(line())
m = number_in(next_line())
maxlen = number_in(next_line())
data['rows'] = [shorten(numbers_in(next_line())) for _ in range(n)]
next_line()
data['cols'] = [shorten(numbers_in(next_line())) for _ in range(m)]
