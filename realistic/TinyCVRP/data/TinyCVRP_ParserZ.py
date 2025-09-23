from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
nVehicles = number_in(line())
nCustomers = number_in(next_line())
data['capacities'] = numbers_in(next_line())
assert nVehicles == len(data['capacities'])
data['demands'] = numbers_in(next_line())
assert nCustomers + 1 == len(data['demands'])
# print(nVehicles, nCustomers, capacities, demands)
next_line()
data['etas'] = [numbers_in(next_line()) for _ in range(nCustomers + 1)]
