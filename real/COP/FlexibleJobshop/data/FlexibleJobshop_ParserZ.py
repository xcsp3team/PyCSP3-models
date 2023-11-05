from pycsp3.problems.data.parsing import *


def read_complex_line():
    s = next_line()
    t = s[s.index('[') + 1:s.rindex(']')].split(", ")
    return [numbers_in(tok[1:-1]) if tok[0] == '{' and tok[-1] == '}' else list(range(int(tok[:tok.index('.')]), int(tok[tok.rindex('.') + 1:]) + 1)) for
            tok in t]


skip_empty_lines(or_prefixed_by="%")
data['nMachines'] = number_in(line())
nJobs = number_in(next_line())
nTasks = number_in(next_line())
nOptions = number_in(next_line())

data['tasks'] = decrement(read_complex_line())
data['optionalTasks'] = decrement(read_complex_line())

data['machines'] = decrement(numbers_in(next_line()))
data['durations'] = numbers_in(next_line())

assert nJobs == len(data['tasks'])
assert nTasks == len(data['optionalTasks'])
assert nOptions == len(data['machines']) == len(data['durations'])
assert all(max(data['tasks'][j]) == data['tasks'][j][-1] for j in range(nJobs))
