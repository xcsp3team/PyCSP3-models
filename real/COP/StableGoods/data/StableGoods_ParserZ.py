from pycsp3.problems.data.parsing import *

m = number_in(line())  # number of people
n = number_in(next_line())  # number of goods
available = numbers_in(next_line())
value = numbers_in(next_line())
data['goods'] = [OrderedDict([("available", available[i]), ("value", value[i])]) for i in range(n)]

np = numbers_in(next_line())
gp = decrement(numbers_in(next_line()))
rp = numbers_in(next_line())

offset = 0
t = []
for i in range(m):
    t.append(OrderedDict([("good_pref", gp[offset:offset + np[i]]), ("req_pref", rp[offset:offset + np[i]])]))
    offset += np[i]
data['people'] = t
