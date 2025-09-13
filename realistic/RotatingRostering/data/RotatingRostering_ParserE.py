""""
Parser for Essence (CSPLIB 87)
"""

from pycsp3.problems.data.parsing import *

next_line()
t = numbers_in(line())
assert len(t) == 28, "for the moment"
m = split_with_rows_of_size(t, 4)

data["nDaysPerWeek"] = 7
data["nWeeks"] = number_in(next_line())
data['shift_min'] = number_in(next_line())
data['shift_max'] = number_in(next_line())
data['requirements'] = m
