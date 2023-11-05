from pycsp3.problems.data.parsing import *
import re

nComponents = numbers_in(line())[1]
nPorts = numbers_in(next_line())[1]
nMultiplePorts = numbers_in(next_line())[1]
nLocations = numbers_in(next_line())[1]
nResources = numbers_in(next_line())[1]
assert nComponents == nPorts == 4 and nMultiplePorts == 5 and nResources == 1
next_line()
requirement_port_nums = split_with_rows_of_size(numbers_in(next_line()), nPorts)
next_line()
provide_port_nums = split_with_rows_of_size(numbers_in(next_line()), nMultiplePorts)
line = next_line(repeat=1)
line = re.split(',|\|', line[:line.rindex("|")])
conflicts = split_with_rows_of_size([0 if tok == "false" else 1 for tok in line], nPorts)
assert nComponents == len(requirement_port_nums) == len(provide_port_nums) == len(conflicts)
line = next_line(repeat=1)
line = re.split(',|\|', line[:line.rindex("|")])
data['multiprovides'] = split_with_rows_of_size([0 if tok == "false" else 1 for tok in line], nPorts)
costs = numbers_in(next_line())
resourceProvisions = numbers_in(next_line(repeat=1))
assert nLocations == len(costs) == len(resourceProvisions)
data['locations'] = [OrderedDict([("cost", costs[i]), ("resource", resourceProvisions[i])]) for i in range(nLocations)]
resourceConsumptions = numbers_in(next_line(repeat=1))
assert nComponents == len(resourceConsumptions)
data['components'] = [OrderedDict(
    [("requiring", requirement_port_nums[i]), ("providing", provide_port_nums[i]), ("conflicts", conflicts[i]), ("consumption", resourceConsumptions[i])]) for i
                      in range(nComponents)]
