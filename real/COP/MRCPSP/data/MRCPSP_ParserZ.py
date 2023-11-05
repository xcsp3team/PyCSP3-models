from pycsp3.problems.data.parsing import *
import re
import re

nResources = number_in(line())
data['rcap'] = numbers_in(next_line())
data['rtype'] = numbers_in(next_line())
assert nResources == len(data['rcap']) == len(data['rtype'])
nTasks = number_in(next_line())
s = next_line()
data['modes'] = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
s = next_line()
data['successors'] = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
assert nTasks == len(data['modes']) == len(data['successors'])
nOptions = number_in(next_line())
data['durations'] = numbers_in(next_line())
assert nOptions == len(data['durations'])
data['requirements'] = [numbers_in(next_line()) for _ in range(nResources)]
