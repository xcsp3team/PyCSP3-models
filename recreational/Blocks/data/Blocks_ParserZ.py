from pycsp3.problems.data.parsing import *
import re

skip_empty_lines(or_prefixed_by="%")

data["n"] = number_in(line())
data['k'] = number_in(next_line())
next_line(repeat=1)
data['start'] = numbers_in(next_line())
data['end'] = numbers_in(next_line())
assert len(data['start']) == len(data['end'])
