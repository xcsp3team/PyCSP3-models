from pycsp3.problems.data.parsing import *
from pycsp3.problems.data.parsing import split_with_rows_of_size, split_with_structure

resources = numbers_in(line())
assert all(v == i + 1 for i, v in enumerate(resources))
nResources = resources[-1]
next_line()
assert line() == "Activities = {T, S, W, o, b};"
Activities = ["T", "S", "W", "o", "b"]
nActivities = 5

nSlots = number_in(next_line())
next_line()
data['fixed'] = [
    [(nActivities if v == "None" else -1 if v == "<>" else Activities.index(v[v.index('(') + 1:v.index(")")])) for tok in ln[ln.index(':') + 1:].split(", ") if
     (v := tok.strip(),)] for _ in range(nResources) if (ln := next_line(),)]
next_line(repeat=1)
data['requirements'] = [numbers_in(ln) for _ in range(nActivities) if (ln := next_line(),)]
next_line(repeat=1)
data['run_costs'] = [numbers_in(ln) for _ in range(nActivities) if (ln := next_line(),)]
next_line(repeat=1)
data['frequency_costs'] = [numbers_in(ln) for _ in range(nActivities) if (ln := next_line(),)]

assert all(len(row) == nSlots + 1 for row in data['run_costs']) and all(len(row) == nSlots + 1 for row in data['frequency_costs'])
