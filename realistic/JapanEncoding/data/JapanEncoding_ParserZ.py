from pycsp3.problems.data.parsing import *

n = number_in(line())
next_line()
data['stream'] = [number_in(next_line()) for _ in range(n)]
