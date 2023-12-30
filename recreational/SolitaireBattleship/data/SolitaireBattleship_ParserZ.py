from pycsp3.problems.data.parsing import *

n = number_in(line())  # height
width = number_in(next_line())
assert n == width
maxShip = number_in(next_line())
data['ships'] = numbers_in(next_line())
assert maxShip == len(data['ships'])
next_line()
data['hints'] = [numbers_in(next_line()) for _ in range(n)]
data['rsums'] = numbers_in(next_line())
data['csums'] = numbers_in(next_line())
assert n == len(data['rsums']) == len(data['csums'])