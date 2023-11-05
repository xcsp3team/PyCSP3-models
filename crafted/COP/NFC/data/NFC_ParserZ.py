from pycsp3.problems.data.parsing import *

n = number_in(line())
data['shift'] = number_in(next_line())
data['workers'] = numbers_in(next_line())[3:]
assert n == len(data['workers'])

