from pycsp3.problems.data.parsing import *

nSkills = number_in(line())
nWorkers = number_in(next_line())
s = next_line()
data['skills'] = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
assert nWorkers == len(data['skills'])
nTasks = number_in(next_line())
data['durations'] = numbers_in(next_line())
assert nTasks == len(data['durations'])
data['requirements'] = [numbers_in(next_line()) for _ in range(nSkills)]
s = next_line()
data['successors'] = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
assert nTasks == len(data['successors'])