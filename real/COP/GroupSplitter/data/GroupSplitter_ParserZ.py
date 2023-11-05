from pycsp3.problems.data.parsing import *


def sec(line):
    t = numbers_in(line)
    assert len(t) == 2 and t[0] == 1, str(t)
    return t[1]


k = sec(line())
data['nGroups'] = sec(next_line())
nUsers = number_in(next_line())
assert k == nUsers
data['minGroupSize'] = number_in(next_line())
data['startAfter'] = number_in(next_line())
data['maxWait'] = number_in(next_line())
data['eta'] = number_in(next_line())
p1 = numbers_in(next_line())[1:]
p2 = numbers_in(next_line())[1:]
n1 = sec(next_line().replace("ty1", ""))
n2 = sec(next_line().replace("ty2", ""))
# data["nActivities1"] = n1
# data["nActivities2"] = n2
assert len(p1) == k * n1 and len(p2) == k * n2
data['preferences1'] = [p1[i * n1:(i + 1) * n1] for i in range(k)]
data['preferences2'] = [p2[i * n2:(i + 1) * n2] for i in range(k)]
nCells = sec(next_line())
oid1 = numbers_in(next_line())[1:]  # not used
assert n1 == len(oid1)
oid2 = numbers_in(next_line())[1:]  # not used
assert n2 == len(oid2)
data['nTimeSlots'] = sec(next_line())
a1 = numbers_in(next_line())[1:]
a2 = numbers_in(next_line())[1:]
data['activities1'] = [a1[i * 5:(i + 1) * 5] for i in range(n1)]
data['activities2'] = [a2[i * 5:(i + 1) * 5] for i in range(n2)]
assert len(a1) == 5 * n1 and len(a2) == 5 * n2
data['distances'] = split_with_rows_of_size(numbers_in(next_line()), nCells)
