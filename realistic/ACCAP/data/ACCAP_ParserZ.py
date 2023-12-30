from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
opDur = numbers_in(line())
cNum = numbers_in(next_line())
xCoor = numbers_in(next_line())
assert len(opDur) == len(cNum) == len(xCoor)
data['flights'] = [OrderedDict([("opDur", opDur[i]), ("cNum", cNum[i]), ("xCoor", xCoor[i])]) for i in range(len(opDur))]
s = next_line()
data['airlines'] = [decrement(numbers_in(v)) for v in s[s.index("{") + 1:s.rindex("}")].split("},{")]
nAirlines = number_in(next_line())
nFlights = number_in(next_line())
assert nAirlines == len(data['airlines']) and nFlights == len(data['flights'])
times = number_in(next_line())  # not used
