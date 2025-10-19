from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")

data["n"] = number_in(line())
data['nPiles'] = number_in(next_line())
next_line(repeat=1)
data['start'] = numbers_in(next_line())
data['goal'] = numbers_in(next_line())
assert len(data['start']) == len(data['goal'])
