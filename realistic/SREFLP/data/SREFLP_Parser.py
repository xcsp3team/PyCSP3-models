from pycsp3.problems.data.parsing import *

nDepartments = number_in(line())
data['lengths'] = numbers_in(next_line())
data['traffics'] = [numbers_in(next_line()) for _ in range(nDepartments)]
assert all(len(row) == nDepartments for row in data['traffics'])
