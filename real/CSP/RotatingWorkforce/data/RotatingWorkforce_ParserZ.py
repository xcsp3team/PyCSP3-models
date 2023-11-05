from pycsp3.problems.data.parsing import *

data['weekLength'] = number_in(line())
data['nWorkers'] = number_in(next_line())
min_daysoff = number_in(next_line())
max_daysoff = number_in(next_line())
data['daysOff'] = OrderedDict([("min", min_daysoff), ("max", max_daysoff)])
min_work = number_in(next_line())
max_work = number_in(next_line())
data['workBlockLength'] = OrderedDict([("min", min_work), ("max", max_work)])
nShifts = number_in(next_line())
data['temporalRequirements'] = [numbers_in(next_line()) for _ in range(nShifts)]
next_line()  # shift names
starts = numbers_in(next_line())  # not used
lengths = numbers_in(next_line())  # not used
block_mins = numbers_in(next_line())
block_maxs = numbers_in(next_line())
assert nShifts == len(starts) == len(lengths) == len(block_mins) == len(block_maxs)
data['shifts'] = [OrderedDict([("blockMin", block_mins[i]), ("blockMax", block_maxs[i])]) for i in range(nShifts)]
nForbidden = number_in(next_line())
befores = decrement(numbers_in(next_line()))
afters = decrement(numbers_in(next_line()))
l = next_line()
daysoffs = [1 if tok == "true" else 0 for tok in l[l.index("[") + 1:l.rindex(']')].split(", ")]
assert nForbidden == len(befores) == len(afters) == len(daysoffs)
data['forbids'] = [OrderedDict([("before", befores[i]), ("after", afters[i]), ("daysOff", daysoffs[i])]) for i in range(nForbidden)]
