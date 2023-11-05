from pycsp3.problems.data.parsing import *

next_line(repeat=1)
data['nMachines'] = number_in(line())
nResources = number_in(next_line())
next_line(repeat=6)
data['resourceCapacities'] = numbers_in(next_line())
assert nResources == len(data['resourceCapacities'])
nTests = number_in(next_line())
durations = numbers_in(next_line())
machines = decrement([numbers_in(next_line()) for _ in range(nTests)])
line = next_line()
resources = decrement([numbers_in(tok) for tok in line[line.index("{") + 1:line.rindex("}")].split("}, {")])
data["tests"] = [OrderedDict([("duration", durations[i]), ("machines", machines[i]), ("resources", resources[i])]) for i in range(nTests)]
