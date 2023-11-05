from pycsp3.problems.data.parsing import *

nPlanks = number_in(line())
data['plankWidths'] = numbers_in(next_line())
nPillars = number_in(next_line())
data['pillarHeights'] = numbers_in(next_line())
data['pillarWidths'] = numbers_in(next_line())
data['width'] = number_in(next_line())
data['height'] = number_in(next_line())

assert nPlanks == len(data['plankWidths']) and nPillars == len(data['pillarHeights']) == len(data['pillarWidths'])
