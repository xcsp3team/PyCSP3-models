from pycsp3.problems.data.parsing import *

data['nBlockingPairs'] = number_in(line())
nResidents = number_in(next_line())
data['nCouples'] = number_in(next_line())
nHospitals = number_in(next_line())
max_rpref_len = number_in(next_line())
max_hpref_len = number_in(next_line())
data['rpref'] = [[v - 1 for v in numbers_in(next_line()) if v != 0] + [-1] for _ in range(nResidents)]  # we add -1 for better handling element constraints
# data['rpref'] = [[v - 1 for v in numbers_in(next_line()) if v != 0] for _ in range(nResidents)]  # we add -1 for better handling element constraints
rpref_len = numbers_in(next_line())
assert nResidents == len(data['rpref']) == len(rpref_len)
assert max_rpref_len == max(rpref_len)
assert all(len(data['rpref'][i]) - 1 == rpref_len[i] for i in range(nResidents))
hpref = [[v - 1 for v in numbers_in(next_line()) if v != 0] for _ in range(nHospitals)]
hpref_len = numbers_in(next_line())
hrank = [decrement(numbers_in(next_line())) for _ in range(nHospitals)]
hcap = numbers_in(next_line())
assert nHospitals == len(hpref) == len(hpref_len) == len(hrank) == len(hcap)
assert all(len(hpref[i]) == hpref_len[i] for i in range(len(hpref)))
assert max_hpref_len == max(hpref_len)
data['hospitals'] = [OrderedDict([("preferences", hpref[i]), ("ranks", hrank[i]), ("capacity", hcap[i])]) for i in range(nHospitals)]
