from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")

INF = 9999

nTanks = number_in(line())
data['limitJobs'] = number_in(next_line())
data['minTimes'] = numbers_in(next_line())
t = numbers_in(next_line())
t.insert(-2, INF)
t.insert(-2, INF)
data['maxTimes'] = t
assert nTanks == len(data['minTimes']) == len(data['maxTimes'])
next_line()
data['eTimes'] = [numbers_in(next_line()) for _ in range(nTanks + 1)]
data['fTimes'] = numbers_in(next_line(repeat=1))
assert nTanks + 1 == len(data['fTimes'])
t = numbers_in(next_line())
data['multiplier'] = t[0]
data['nHoists'] = t[1]
data['capacity'] = t[2]
