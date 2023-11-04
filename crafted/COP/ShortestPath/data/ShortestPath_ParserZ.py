from pycsp3.problems.data.parsing import *

data['n'] = number_in(next_line())
m = number_in(next_line())
starts = decrement(numbers_in(next_line()))
ends = decrement(numbers_in(next_line()))
lengths = numbers_in(next_line())
assert m == len(starts) == len(ends) == len(lengths)
data['edges'] = [(starts[i], ends[i], lengths[i]) for i in range(m)]
data['start'] = decrement(number_in(next_line()))
data['end'] = decrement(number_in(next_line()))
