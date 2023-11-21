from pycsp3.problems.data.parsing import *

nJobs = number_in(line())
data['nMachines'] = number_in(next_line())
next_line()
data['durations'] = [numbers_in(next_line()) for _ in range(nJobs)]
