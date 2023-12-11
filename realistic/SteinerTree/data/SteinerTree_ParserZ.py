from pycsp3.problems.data.parsing import *

n = number_in(next_line())
m = number_in(next_line())
t = number_in(next_line())

adj = [[0 if tok == "false" else 1 for tok in line[line.index("|") + 1:].split(",")] for line in [next_line() for _ in range(n)]]
next_line()
data['endNodes'] = [[0 if tok == "false" else 1 for tok in line[line.index("|") + 1:].split(",")] for line in [next_line() for _ in range(m)]]
next_line()
data['terminals'] = decrement(numbers_in(next_line()))
data['weights'] = numbers_in(next_line())
