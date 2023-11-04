"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  two integers m and n

## Model
  constraints: Sum

## Execution
  python SearchStress2.py -data=[number,number]

## Links
  - https://www.minizinc.org/challenge2009/results2009.html

## Tags
  academic, mzn09
"""

from pycsp3 import *

m, n = data  # number of copies of equality, and size of domains


def eq1(x, y, z):
    return [
        [
            (
                z[i] != 0,
                z[i] != x,
                z[i] != y,
                [z[i] != z[j] for j in range(i + 1, n)]
            ) for i in range(1, n)
        ],
        z[n] == 0,
        x != 0,
        y != 0
    ]


def eq2(x, y, z):
    return [
        [z[i] <= 1 for i in range(1, n + 1)],
        x == Sum(z[1:]),
        y == Sum(z[1:]),
        x != 0,
        y != 0
    ]


def eq3(x, y, z):
    return [
        x <= z[1],
        [z[i - 1] <= z[i] for i in range(2, n + 1)],
        z[n] <= y,
        x >= y,
        x != 0,
        y != 0
    ]


def eq4(x, y, z):
    return [
        (x == y) | ((x >= y) & (x <= y)) | ~(x != y),
        [z[i] == 0 for i in range(1, n + 1)],
        x != 0,
        y != 0
    ]


funcs = [eq4, eq1, eq2, eq3]

t = VarArray(size=[m, n + 1], dom=range(n + 1))

satisfy(
    [funcs[i % 4](t[i - 1][0], t[i][0], t[i - 1]) for i in range(1, m)],

    t[0][0] != t[-1][0]
)

""" Comments
1) data used in 2009 are: (2,7),(3,6),(4,5),(4,6),(5,5),(5,6),(6,4),(6,5),(6,6),(7,2)
"""
