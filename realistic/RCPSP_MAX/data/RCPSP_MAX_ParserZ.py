from pycsp3.problems.data.parsing import *

nResources = number_in(line())
data['capacities'] = numbers_in(next_line())
nTasks = number_in(next_line())
data['durations'] = numbers_in(next_line())
data['requirements'] = [numbers_in(next_line()) for _ in range(nResources)]
diffs = []
while not next_line().endswith(";"):
    t = numbers_in(line())
    diffs.append((t[0] - 1, t[1], t[2] - 1))
data['dcons'] = diffs
nDC = number_in(next_line())
assert nResources == len(data['capacities']) and nTasks == len(data['durations']) and nDC == len(data['dcons'])
