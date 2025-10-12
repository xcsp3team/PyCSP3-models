from pycsp3.problems.data.parsing import *

nTasks = number_in(line())
nResources = number_in(next_line())
durations = numbers_in(next_line())
assert nTasks == len(durations)
next_line(repeat=3)
requirements = [numbers_in(next_line()) for _ in range(nResources)]
capacities = numbers_in(next_line(repeat=2))
assert nResources == len(capacities)
data['resources'] = [OrderedDict([("requirements", requirements[i]), ("capacity", capacities[i])]) for i in range(nResources)]
next_line()
successors = decrement([numbers_in(next_line()) for _ in range(nTasks)])
horizon = number_in(next_line(repeat=1))
next_line(repeat=3)
deadlines = [numbers_in(next_line()) for _ in range(nTasks)]
data['tasks'] = [OrderedDict([("duration", durations[i]), ("successors", successors[i]), ("deadline", deadlines[i])]) for i in range(nTasks)]
data['horizon'] = horizon

next_line(repeat=2)
earlinessMin = number_in(next_line())
earlinessMax = number_in(next_line())
data['earliness'] = OrderedDict([("min", earlinessMin), ("max", earlinessMax)])
tardinessMin = number_in(next_line())
tardinessMax = number_in(next_line())
data['tardiness'] = OrderedDict([("min", tardinessMin), ("max", tardinessMax)])
data['nSolutions'] = number_in(next_line())
