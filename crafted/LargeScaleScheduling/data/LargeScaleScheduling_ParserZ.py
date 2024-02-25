from pycsp3.problems.data.parsing import *

nTasks = number_in(line())
data['limit'] = number_in(next_line())
data['durations'] = numbers_in(next_line())
data['heights'] = numbers_in(next_line())
assert nTasks == len(data['durations']) == len(data['heights'])
