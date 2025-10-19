"""
This is [Problem 023](https://www.csplib.org/Problems/prob023/) at CSPlib.

A magic hexagon  consists of the numbers 1 to 19 arranged in a hexagonal pattern.

## Data
  A pair of integers (n,s)

## Model
  constraints: AllDifferent, Sum

## Execution
  python MagicHexagon.py -data=[number,number]

## Links
  - https://www.csplib.org/Problems/prob023

## Tags
  academic, csplib
"""

from pycsp3 import *

n, s = data or (4, 3)

domain = range(s, s + 3 * n * n - 3 * n + 1)
assert sum(domain) % (2 * n - 1) == 0, "No magic hexagon for order=" + str(n) + " and start=" + str(s)
magic = sum(domain) // (2 * n - 1)

d = n + n - 1  # longest diameter
D = range(d)


def scope(i, right):
    v1 = max(0, d // 2 - i if right else i - d // 2)
    v2 = d // 2 - v1
    return [x[j + v1][i - max(0, v2 - j if right else j - v2)] for j in range(d - abs(d // 2 - i))]


# x represents the hexagon; on row x[i], only the first n - |n/2 - i| cells are useful (here, n = 'd').
x = VarArray(size=[d, d], dom=lambda i, j: domain if j < d - abs(d // 2 - i) else None)

satisfy(
    AllDifferent(x),

    # all rows sum to the magic value
    [Sum(x[i]) == magic for i in D],

    # all right-sloping diagonals sum to the magic value
    [Sum(scope(i, True)) == magic for i in D],

    # all left-sloping diagonals sum to the magic value
    [Sum(scope(i, False)) == magic for i in D],

    # tag(symmetry-breaking)
    [
        x[0][0] < x[0][n - 1],
        x[0][0] < x[n - 1][d - 1],
        x[0][0] < x[d - 1][n - 1],
        x[0][0] < x[d - 1][0],
        x[0][0] < x[n - 1][0],
        x[0][n - 1] < x[n - 1][0]
    ]
)
