from pycsp3.problems.data.parsing import *

data['nCourses'] = nCourses = number_in(next_line())
data['nPeriods'] = number_in(next_line())
data['load_per_period_bounds'] = OrderedDict([("min", number_in(next_line())), ("max", number_in(next_line()))])
data['courses_per_period_bounds'] = OrderedDict([("min", number_in(next_line())), ("max", number_in(next_line()))])
data['course_loads'] = numbers_in(next_line())
next_line()
data['prerequisites'] = decrement(numbers_in(line) for line in remaining_lines())
assert nCourses == len(data['course_loads'])
