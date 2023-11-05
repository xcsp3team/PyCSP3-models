from pycsp3.problems.data.parsing import *

data['nDays'] = nDays = number_in(line())
nRoads = number_in(next_line())
nCenters = number_in(next_line())
nWorksheets = number_in(next_line())
nActivities = number_in(next_line())
data['perturbationCosts'] = split_with_rows_of_size(numbers_in(next_line())[2:], nDays)
assert nRoads + 1 == len(data['perturbationCosts'])
ids = numbers_in(next_line())[1:]
data['aworkers'] = numbers_in(next_line())[1:]
assert nCenters == len(ids) == len(data['aworkers'])
w_id = numbers_in(next_line())[1:]
wcenters = numbers_in(next_line())[1:]
mandatory = numbers_in(next_line())[1:]
importance = numbers_in(next_line())[1:]
est = numbers_in(next_line())[1:]
lst = numbers_in(next_line())[1:]
durations = numbers_in(next_line())[1:]
assert nWorksheets == len(w_id) == len(wcenters) == len(mandatory) == len(importance) == len(est) == len(lst) == len(durations)
roads = split_with_rows_of_size(numbers_in(next_line())[1:], nActivities)
assert nWorksheets == len(roads)
workers = split_with_rows_of_size(numbers_in(next_line())[1:], nActivities)
assert nWorksheets == len(workers)
data['worksheets'] = [(wcenters[i], mandatory[i], importance[i], est[i], lst[i], durations[i], roads[i], workers[i]) for i in range(nWorksheets)]
nBlocks = number_in(next_line())  # blockedMax
blockedAmount = numbers_in(next_line())
l = next_line()
blockedRoads = [] if l.endswith("[];") else [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("},{")]
assert nBlocks == len(blockedAmount) == len(blockedRoads)
data['blocks'] = [(blockedAmount[i], blockedRoads[i]) for i in range(nBlocks)]
nPrecedences = number_in(next_line())
preds = numbers_in(next_line())
succs = numbers_in(next_line())
assert nPrecedences == len(preds) == len(succs)
data['arcs'] = [(preds[i], succs[i]) for i in range(len(preds))]
