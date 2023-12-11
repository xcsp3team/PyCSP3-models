from pycsp3.problems.data.parsing import *

nSeats = number_in(line())
data["nPersons"] = number_in(next_line())
starts = decrement(numbers_in(next_line()))
goals = decrement(numbers_in(next_line()))
assert nSeats == len(starts) == len(goals)
data['seats'] = [OrderedDict([("start", starts[i]), ("goal", goals[i])]) for i in range(nSeats)]
line = next_line()
line = line[line.index("[") + 1:line.rindex("]")].split(',')
data["swaps"] = [v.strip() == "true" for v in line]
assert data["nPersons"] == len(data["swaps"])
