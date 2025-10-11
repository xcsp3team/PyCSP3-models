from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
data['nWeeks'] = number_in(line())
data['requirements'] = [numbers_in(next_line()) for _ in range(5)]
data['obj_lb'] = number_in(next_line())
