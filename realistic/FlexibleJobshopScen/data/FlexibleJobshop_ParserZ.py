from pycsp3.problems.data.parsing import *


# Example with multi scenarii:
#    python3 FlexibleJobshopScen.py -data=[dh-5-16.dzn,"20"] -parser=FlexibleJobshop_ParserZ.py

def read_complex_line():
    s = next_line()
    t = s[s.index('[') + 1:s.rindex(']')].split(", ")
    return [numbers_in(tok[1:-1]) if tok[0] == '{' and tok[-1] == '}' else list(range(int(tok[:tok.index('.')]), int(tok[tok.rindex('.') + 1:]) + 1)) for
            tok in t]


skip_empty_lines(or_prefixed_by="%")
with_scenarii = line().startswith("first")
if with_scenarii:
    data['first_scen'] = decrement(number_in(line()))
    data['last_scen'] = decrement(number_in(next_line()))
    nbScen = number_in(next_line())
    next_line()

skip_empty_lines(or_prefixed_by="%")
data['nMachines'] = number_in(line())
nJobs = number_in(next_line())
nTasks = number_in(next_line())
nOptions = number_in(next_line())

data['tasks'] = decrement(read_complex_line())
data['optionalTasks'] = decrement(read_complex_line())

data['option_machines'] = decrement(numbers_in(next_line()))
if with_scenarii:
    data['weights'] = numbers_in(next_line())
    assert len(data['weights']) == nbScen
    data['durations'] = [numbers_in(next_line()) for _ in range(nbScen)]
    assert all(nOptions == len(t) for t in data['durations'])
else:
    data['durations'] = numbers_in(next_line())
    assert nOptions == len(data['durations'])

assert nJobs == len(data['tasks'])
assert nTasks == len(data['optionalTasks'])
assert nOptions == len(data['option_machines'])
assert all(max(data['tasks'][j]) == data['tasks'][j][-1] for j in range(nJobs))

if with_scenarii and next_line():
    data['last_scen'] = decrement(number_in(line()))
