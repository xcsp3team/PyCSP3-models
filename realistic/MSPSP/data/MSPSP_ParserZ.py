from pycsp3.problems.data.parsing import *

nSkills = number_in(line())
nWorkers = number_in(next_line())
s = next_line()
data['worker_skills'] = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
assert nWorkers == len(data['worker_skills'])
nTasks = number_in(next_line())
durations = numbers_in(next_line())
assert nTasks == len(durations)
data['skill_requirements'] = [numbers_in(next_line()) for _ in range(nSkills)]
s = next_line()
successors = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("}, {")]
assert nTasks == len(successors)
data["tasks"] = OrderedDict([("durations", durations), ("successors", successors)])
