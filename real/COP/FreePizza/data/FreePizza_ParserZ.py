from pycsp3.problems.data.parsing import *

n = number_in(line())
data['prices'] = numbers_in(next_line())
m = number_in(next_line())
data['buy'] = numbers_in(next_line())
data['free'] = numbers_in(next_line())
assert n == len(data['prices']) and m == len(data['buy']) == len(data['free'])
