from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")

INF = 9999

nTanks = number_in(line())
data['nJobs'] = number_in(next_line())
data['tmin'] = numbers_in(next_line())
t = numbers_in(next_line())
t.insert(-2, INF)
t.insert(-2, INF)
data['tmax'] = t
assert nTanks == len(data['tmin']) == len(data['tmax'])
next_line()
data['e'] = [numbers_in(next_line()) for _ in range(nTanks + 1)]
data['f'] = numbers_in(next_line(repeat=1))
assert nTanks + 1 == len(data['f'])
t = numbers_in(next_line())
data['multiplier'] = t[0]
data['hoists'] = t[1]
data['capacity'] = t[2]
