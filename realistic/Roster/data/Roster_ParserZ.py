from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
data['nWeeks'] = number_in(line())
data['reqt'] = [numbers_in(next_line()) for _ in range(5)]
data['minobj'] = number_in(next_line())
