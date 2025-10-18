from pycsp3.problems.data.parsing import *

nResources = number_in(line())
rcap = numbers_in(next_line())
rtype = numbers_in(next_line())
assert nResources == len(rcap) == len(rtype)
data["resources"] = OrderedDict([("capacities", rcap), ("types", rtype)])

nTasks = number_in(next_line())
s = next_line()
modes = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
s = next_line()
successors = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
assert nTasks == len(modes) == len(successors)

nOptions = number_in(next_line())
data['mode_durations'] = numbers_in(next_line())
assert nOptions == len(data['mode_durations'])
requirements = [numbers_in(next_line()) for _ in range(nResources)]
data["tasks"] = OrderedDict([("modes", modes), ("successors", successors), ("requirements", requirements)])
