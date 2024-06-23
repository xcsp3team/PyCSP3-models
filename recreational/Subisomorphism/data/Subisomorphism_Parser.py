from pycsp3.problems.data.parsing import *

n = number_in(line())
p_edges = [numbers_in(next_line())[1:] for _ in range(n)]
next_line()

m = number_in(line())
t_edges = [numbers_in(next_line())[1:] for _ in range(m)]

data['n'] = n
data['m'] = m
data["p_edges"] = [(i, j) for i, t in enumerate(p_edges) for j in t]
data['t_edges'] = [(i, j) for i, t in enumerate(t_edges) for j in t]  # t_edges
