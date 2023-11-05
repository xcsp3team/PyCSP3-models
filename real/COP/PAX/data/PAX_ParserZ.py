from pycsp3.problems.data.parsing import *

# skip_empty_lines(or_prefixed_by="%")
data['objType'] = number_in(next_line())
data['forwardTW'] = number_in(next_line())
data['backwardTW'] = number_in(next_line())
next_line()
skip_empty_lines(or_prefixed_by="%")
next_line(repeat=1)
l = line()
data['stationLines'] = decrement([numbers_in(tok) for tok in l[l.index('{') + 1:l.rindex('}')].split("},{")])
data['maxPAX'] = number_in(next_line())
lines = decrement(numbers_in(next_line()))
nServices = len(lines)
next_line()
schedules = [numbers_in(next_line()) for _ in range(nServices)]
data['services'] = [OrderedDict([("line", lines[i]), ("schedule", schedules[i])]) for i in range(nServices)]
next_line()
skip_empty_lines(or_prefixed_by="%")
next_line()
m = [numbers_in(l) for l in remaining_lines()]
for t in m:
    t[1] -= 1
    t[2] -= 1
data['trips'] = m
