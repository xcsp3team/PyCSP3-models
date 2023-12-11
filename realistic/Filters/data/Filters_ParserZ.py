from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
data['del_add'] = number_in(line())
next_line()
skip_empty_lines(or_prefixed_by="%")
data['del_mul'] = number_in(line())

next_line()
data['number_add'] = number_in(line())
next_line()
data['number_mul'] = number_in(line())
next_line()
n = number_in(line())

data['last'] = numbers_in(next_line(), offset=-1)
data['add'] = numbers_in(next_line(), offset=-1)
mul = numbers_in(next_line(), offset=-1)  # no need to record it as it is complementary of add
next_line()
data["dependencies"] = [numbers_in(next_line(), offset=-1) for _ in range(n)]
