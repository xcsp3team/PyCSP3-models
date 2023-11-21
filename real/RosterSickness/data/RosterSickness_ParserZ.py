from pycsp3.problems.data.parsing import *


def booleans_in(line):
    assert line is not None
    return [1 if tok == "true" else 0 for tok in line[line.index("|") + 1:line.rindex("|")].replace(" |", ",").split(", ")]


nShifts = number_in(line())
nEmployees = number_in(next_line())
nExpertises = number_in(next_line())
next_line()
contracts = numbers_in(next_line())
l = next_line()
expertises = [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("}, {")]
assert nEmployees == len(contracts) == len(expertises)
next_line()
starts = numbers_in(next_line())
stops = numbers_in(next_line())
requireds = numbers_in(next_line())
assert nShifts == len(starts) == len(stops) == len(requireds)
data['shifts'] = [OrderedDict([("start", starts[i]), ("stop", stops[i]), ("required", requireds[i])]) for i in range(nShifts)]
perHour = number_in(next_line())
assigneds = split_with_rows_of_size(booleans_in(next_line()), nShifts)
assert nEmployees == len(assigneds)
data['emplyees'] = [OrderedDict([("contract", contracts[i]), ("expertise", expertises[i]), ("assigned", assigneds[i])]) for i in range(nEmployees)]
