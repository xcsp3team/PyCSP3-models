from pycsp3.problems.data.parsing import *

# example: python3 BlockModeling.py -data=[kansas,3] -parser=BlockModeling_Parser.py
t = numbers_in(line())
n = len(t)
m = [t] + [numbers_in(next_line()) for _ in range(n - 1)]
data["matrix"] = m
data['k'] = number_in(next_line())
