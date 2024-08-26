from pycsp3.problems.data.parsing import *

nCourses = number_in(next_line())
# data['nCourses'] = nCourses
data['nPeriods'] = number_in(next_line())
data['loadLB'] = number_in(next_line())
data['loadUB'] = number_in(next_line())
data['coursesLB'] = number_in(next_line())
data['coursesUB'] = number_in(next_line())
data['loads'] = numbers_in(next_line())
next_line()
data['prerequisites'] = decrement(numbers_in(line) for line in remaining_lines())
assert nCourses == len(data['loads'])
