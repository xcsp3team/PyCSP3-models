""""
Parser for problem instances at http://people.brunel.ac.uk/~mastjjb/jeb/orlib/pmedinfo.html
"""
from pycsp3.problems.data.parsing import *

n, e, p = numbers_in(line())
m = [numbers_in(line) for line in [next_line() for _ in range(e)]]

c = [[float('inf')] * n for _ in range(n)]
for i in range(n):
    c[i][i] = 0
for i, j, v in m:
    c[i - 1][j - 1] = c[j - 1][i - 1] = v
for k in range(n):
    for i in range(n):
        for j in range(n):
            c[i][j] = min(c[i][j], c[i][k] + c[k][j])

data['distances'] = c
data['k'] = p
