from pycsp3.problems.data.parsing import *

nIndustries = number_in(line())
nSteps = number_in(next_line())
assert nIndustries == 8 and nSteps == 24
data['max_capacity'] = number_in(next_line())
data['flows'] = numbers_in(next_line())
data['capacities'] = numbers_in(next_line())
next_line()
data['d'] = [numbers_in(next_line()) for _ in range(nIndustries)]
