from pycsp3.problems.data.parsing import *

data['width'] = number_in(line())
data['height'] = number_in(next_line())
filled = number_in(next_line())
assert filled == 1
nTiles = number_in(next_line())
size = number_in(next_line())
data['tiles'] = [numbers_in(next_line()) for _ in range(nTiles)]
data['dfa'] = numbers_in(next_line(repeat=1))
assert size == len(data['dfa'])
