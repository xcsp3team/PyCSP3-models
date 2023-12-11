from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
data['horizon'] = number_in(line())
nResources = number_in(next_line())
data['resourceCosts'] = numbers_in(next_line())
assert nResources == len(data['resourceCosts'])
nTasks = number_in(next_line())
data['durations'] = numbers_in(next_line())
line = next_line()
data['successors'] = decrement([numbers_in(tok) for tok in line[line.index("{") + 1:line.rindex("}")].split("}, {")])
data['resourcesRequirements'] = [numbers_in(next_line()) for _ in range(nResources)]
# data["tasks"] = [OrderedDict([("duration", durations[i]), ("successors", successors[i]), ("resources", resources[i])]) for i in range(nTasks)]
