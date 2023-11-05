from pycsp3.problems.data.parsing import *

nAgents = number_in(next_line())
next_line()
data['agents'] = decrement([numbers_in(next_line()) for _ in range(nAgents)])
next_line(repeat=1)
data['makespan'] = number_in(next_line())
nNodes = number_in(next_line(repeat=1))
next_line()
data['neighbors'] = decrement([numbers_in(next_line())[:-1] for _ in range(nNodes)])
k = number_in(next_line(repeat=1))
assert nAgents == k
