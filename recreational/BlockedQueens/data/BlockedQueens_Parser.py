from pycsp3.problems.data.parsing import *

"""
parser for ASP-competition instances
"""

data['n'] = number_in(line())
t = []
line = next_line()
while line[0] != ']':
    t.append(numbers_in(line))
    line = next_line()
data['blocks'] = decrement(t)
