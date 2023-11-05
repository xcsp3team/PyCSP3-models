from pycsp3.problems.data.parsing import *

nResources = number_in(line())
data['capacities'] = numbers_in(next_line())
assert nResources == len(data['capacities'])
nTasks = number_in(next_line())
data['requirements'] = [numbers_in(next_line()) for _ in range(nTasks)]
nPrecedences = number_in(next_line())
precedences = [numbers_in(next_line()) for _ in range(nPrecedences)]
for precedence in precedences:
    precedence[0] -= 1
    precedence[1] -= 1
assert all(precedence[2] >= 0 for precedence in precedences)
data['precedences'] = precedences
