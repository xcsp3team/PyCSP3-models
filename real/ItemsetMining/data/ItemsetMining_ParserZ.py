from pycsp3.problems.data.parsing import *

skip_empty_lines(or_prefixed_by="%")
data['nItems'] = number_in(line())
nPos = number_in(next_line())
nNeg = number_in(next_line())
next_line()
data['pos'] = decrement([numbers_in(next_line()) for _ in range(nPos)])
next_line()
data['neg'] = decrement([numbers_in(next_line()) for _ in range(nNeg)])
data['k'] = number_in(next_line())
