from pycsp3.problems.data.parsing import *

nLayers = number_in(line())
data['widths'] = numbers_in(next_line())
data['n'] = number_in(next_line())
e = number_in(next_line())
starts = decrement(numbers_in(next_line()))
ends = decrement(numbers_in(next_line()))
assert nLayers == len(data['widths']) and e == len(starts) == len(ends)
data['edges'] = [(starts[i], ends[i]) for i in range(e)]
