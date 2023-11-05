from pycsp3.problems.data.parsing import *

n = number_in(line())
minDomain = number_in(next_line())
maxDomain = number_in(next_line())
l = next_line()
data['domains'] = [numbers_in(tok) for tok in l[l.index("{") + 1:l.rindex("}")].split("},{")]
data['costs'] = numbers_in(next_line())
assert n == len(data['domains'])
e2 = numbers_in(next_line())[1]
maxCtrs2 = numbers_in(next_line())[1]
f2x = decrement(numbers_in(next_line())[1:])
f2y = decrement(numbers_in(next_line())[1:])
nTuples2 = numbers_in(next_line())[1:]
offsets2 = numbers_in(next_line())[1:]
t2 = numbers_in(next_line())[1:]
assert e2 == len(f2x) == len(f2y) == len(nTuples2) == len(offsets2)
assert maxCtrs2 == len(t2)
data['c2s'] = [[f2x[j], f2y[j], t2[2 * offsets2[j]: 2 * offsets2[j] + nTuples2[j] * 2]] for j in range(e2)]
e3 = numbers_in(next_line())[1]
maxCtrs3 = numbers_in(next_line())[1]
f3x = decrement(numbers_in(next_line())[1:])
f3y = decrement(numbers_in(next_line())[1:])
f3z = decrement(numbers_in(next_line())[1:])
nTuples3 = numbers_in(next_line())[1:]
offsets3 = numbers_in(next_line())[1:]
t3 = numbers_in(next_line())[1:]
assert e3 == len(f3x) == len(f3y) == len(f3z) == len(nTuples3) == len(offsets3)
assert maxCtrs3 == len(t3)
data['c3s'] = [[f3x[j], f3y[j], f3z[j], t3[3 * offsets3[j]: 3 * offsets3[j] + nTuples3[j] * 3]] for j in range(e3)]
