from pycsp3.problems.data.parsing import *
from random import seed, shuffle

data['nYears'] = number_in(next_line())
data['nPeriodsPerYear'] = number_in(next_line())
nCourses = number_in(next_line())
nCurricula = number_in(next_line())
t = numbers_in(next_line())
data['loadBounds'] = OrderedDict([("min", t[0]), ("max", t[1])])
nPrecedences = number_in(next_line())
nUndesired = number_in(next_line())
next_line()
d = {t[0]: (i, int(t[1])) for i, t in enumerate([next_line().split(" ") for _ in range(nCourses)])}
data['courseLoads'] = [v for k, (_, v) in d.items()]
next_line()
data['curricula'] = [[d[t][0] for tt in [next_line().split(" ")[2:]] for t in tt] for _ in range(nCurricula)]
next_line()
data['precedences'] = [[d[t][0] for tt in [next_line().split(" ")] for t in tt] for _ in range(nPrecedences)]
next_line()
data['undesiredPeriods'] = [(d[t[0]][0], int(t[1])) for t in [next_line().split(" ") for _ in range(nUndesired)]]
