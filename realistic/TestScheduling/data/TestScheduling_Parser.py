from pycsp3.problems.data.parsing import *

next_line()
nTests = number_in(line())
nMachines = number_in(next_line())
nResources = number_in(next_line())
nFamilies = number_in(next_line())
assert nFamilies == 1
minDuration = number_in(next_line(repeat=1))
maxDuration = number_in(next_line())
next_line()

tests = []
for i in range(nTests):
    line = next_line()
    line = line[line.index(",") + 1:line.rindex("]") + 1]
    duration = int(line[:line.index(",")])
    machines = line[line.index("[") + 1:line.index("]")].replace("'", "").split(",")
    resources = line[line.rindex("[") + 1:line.rindex("]")].replace("'", "").split(",")
    tests.append(OrderedDict([("duration", duration),
                              ("machines", sorted([int(m[1:]) - 1 for m in machines if m])),
                              ("resources", sorted([int(r[1:]) - 1 for r in resources if r]))]))

data['nMachines'] = nMachines
data['nResources'] = nResources
#data['minDuration'] = minDuration
#data['maxDuration'] = maxDuration
data['tests'] = tests

# should we control names of machines and resources?
for i in range(nMachines):
    line = next_line()
next_line()
for i in range(nResources):
    line = next_line()
