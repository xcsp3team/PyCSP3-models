from pycsp3.problems.data.parsing import *

nTasks, nShifts, minNShifts = numbers_in(line())
data["nTasks"] = nTasks
data["shifts"] = [numbers_in(next_line())[2:] for _ in range(nShifts)]
