from pycsp3.problems.data.parsing import *

horizon = number_in(line())
nTrucks = number_in(next_line())
data['costs'] = numbers_in(next_line())
data['loads'] = numbers_in(next_line())
assert nTrucks == len(data['costs']) == len(data['loads'])
data['demands'] = numbers_in(next_line())
assert horizon == len(data['demands'])
data['truck1'] = decrement(numbers_in(next_line())[1])
data['truck2'] = decrement(numbers_in(next_line())[1])
