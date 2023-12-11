from pycsp3.problems.data.parsing import *
from random import seed, randrange

percentage = number_in(line())  # enlarging horizon by this percentage
s = number_in(next_line())  # seed
next_line(repeat=5)
nJobs = number_in(line()) - 2  # -2 as we discard the two fictive nodes
h = number_in(next_line())
next_line()
nRenewable = number_in(next_line())
nUnrenewable = number_in(next_line())
nDoubly = number_in(next_line())
assert nRenewable == 4 and nUnrenewable == nDoubly == 0
next_line(repeat=3)
t = numbers_in(line())
data['horizon'] = t[3] + ((t[3] * percentage) // 100)
seed(s)
data['costs'] = [randrange(1, 11) for _ in range(nRenewable)]
next_line(repeat=3)
successors = [[v - 2 for v in numbers_in(next_line())[3:] if v - 2 != nJobs] for _ in range(nJobs)]
next_line(repeat=5)
m = [numbers_in(next_line())[2:] for _ in range(nJobs)]
durations = [row[0] for row in m]
requirements = [row[1:] for row in m]
data['jobs'] = [OrderedDict([("duration", durations[i]), ("successors", successors[i]), ("requirements", requirements[i])]) for i in range(nJobs)]
