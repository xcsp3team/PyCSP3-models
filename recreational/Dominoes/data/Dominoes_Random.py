"""
for i in {0..500} ; do python3 Dominoes.py  -parser=Dominoes_Random.py 30 $i -export ; done
java ace Dominoes-4-000.xml -s=all => 448 solutions

The code should be improved in order to avoid dead-end instances
"""

import random

from pycsp3.compiler import Compilation
from pycsp3.problems.data.parsing import *

d = ask_number("Higher value")
seed = ask_number("Seed")
random.seed(seed)

dominoes = [(i, j) for i in range(d + 1) for j in range(i, d + 1)]
grid = [[-1] * (d + 2) for _ in range(d + 1)]


def first_cell():
    for i in range(d + 1):
        for j in range(d + 2):
            if grid[i][j] == -1:
                return i, j
    assert False


while len(dominoes) > 0:
    k = random.randrange(len(dominoes))
    v = dominoes[k]
    dominoes.remove(v)
    if random.randint(0, 1) == 1:
        v = (v[1], v[0])  # we reverse it
    i, j = first_cell()
    assert grid[i][j] == -1
    grid[i][j] = v[0]
    horizontal = True if i == d or grid[i + 1][j] != -1 else False if j == d + 1 or grid[i][j + 1] != -1 else random.randint(0, 1) == 1
    if horizontal:
        assert grid[i][j + 1] == -1
        grid[i][j + 1] = v[1]
    else:
        assert grid[i + 1][j] == -1
        grid[i + 1][j] = v[1]

data["grid"] = grid
Compilation.string_data = "-" + "-".join(str(v) for v in (d, "{:03d}".format(seed)))
