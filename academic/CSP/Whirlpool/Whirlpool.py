"""
Perfect diagonal extended whirlpool permutation

A whirlpool permutation is an n x m matrix containing number 1..n*m where every 2x2 sub matrix is either ordered cw (clockwise) or ccw (counter-clockwise).
An extended whirlpool permutation requires that the outside ring is ordered cw or ccw, and the ring inside it, etc
A perfect diagonal whirlpool permutation required n = m and that the sum of both diagonals is n*(n+1)*(n+1) div 2.

The model, below, is close to (can be seen as the close translation of) the one submitted to the M2020 inizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data
  two integers (n,m)

## Model
  Constraints: Sum

## Execution
  python Whirlpool.py -data=[number,number]

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  academic, mzn20
"""

from pycsp3 import *

n, m = data

# x[i][j] is the value of the cell at coordinates (i,j)
x = VarArray(size=[n, m], dom=range(n * m))


def whirlpool(y):
    r = len(y)
    return Sum(y[i] < y[(i + 1) % r] for i in range(r)) in {1, r - 1}


satisfy(
    # every 2 x 2 sub matrix is either ordered clockwise or counter-clockwise
    [whirlpool([x[i][j], x[i][j + 1], x[i + 1][j + 1], x[i + 1][j]]) for i in range(n - 1) for j in range(m - 1)],

    # every ring is either ordered clockwise or counter-clockwise
    [whirlpool(ring(x, k)) for k in range(min(n, m) // 2)]
)

if n == m:
    satisfy(
        # for a perfect diagonal whirlpool permutation, the sum of both diagonals is n*(n+1)*(n+1) div 2
        (
            Sum(x[i][i] for i in range(n)) == n * (n + 1) * (n + 1) // 2,
            Sum(x[i][-i - 1] for i in range(n)) == n * (n + 1) * (n + 1) // 2
        )
    )

"""
1) data used in 2020 are: (8,8), (12,12), (21,21), (29,29), (30,30)
"""
