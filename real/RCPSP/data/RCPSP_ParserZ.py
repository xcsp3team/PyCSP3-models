from pycsp3.problems.data.parsing import *

nResources = number_in(line())
data['capacities'] = numbers_in(next_line())
assert nResources == len(data['capacities'])
nTasks = number_in(next_line())
data['durations'] = numbers_in(next_line())
assert nTasks == len(data['durations'])
data['requirements'] = [numbers_in(next_line()) for _ in range(nResources)]
data['successors'] = decrement([numbers_in(next_line()) for _ in range(nTasks)])
