"""
From mathworld.wolfram.com:
    A heterosquare is an n×n array of the integers from 1 to n^2 such that the rows, columns, and diagonals have different sums.
    By contrast, in a magic square, they have the same sum.
    There are no heterosquares of order two, but heterosquares of every odd order exist.
    They can be constructed by placing consecutive integers in a spiral pattern.

Important: the variants of the model, below, are here for hardening the problem (when looking for a solution) ; it was written for the 2025 XCSP3 competition.

## Data
  a number n

## Model
  constraints: AllDifferent, Sum

## Execution
  python Heterosquare.py -data=number
  python Heterosquare.py -data=number -variant=easy
  python Heterosquare.py -data=number -variant=fair
  python Heterosquare.py -data=number -variant=hard

## Links
  - https://mathworld.wolfram.com/Heterosquare.html
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, xcsp25
"""

from pycsp3 import *

n = data or 8

lb, ub = (n * (n + 1)) // 2, ((n * n) * (n * n + 1)) // 2

if variant():
    assert variant() in ("easy", "fair", "hard")
    if variant("easy"):
        lb = lb * (n // 2)
    elif variant("fair"):
        lb = lb * (n - 1)
    elif variant("hard"):
        lb = lb * n
    ub = ub // (n // 2)

# x[i][j] is the value put in cell of the matrix at coordinates (i,j)
x = VarArray(size=[n, n], dom=range(1, n * n + 1))

# rs[i] is the sum of values in the ith row
rs = VarArray(size=n, dom=range(lb, ub + 1))

# cs[j] is the sum of values in the jth column
cs = VarArray(size=n, dom=range(lb, ub + 1))

# ds is the sum in the two diagonals
ds = VarArray(size=2, dom=range(lb, ub + 1))

satisfy(
    # all values must be different
    AllDifferent(x),

    # computing row sums
    [rs[i] == Sum(x[i]) for i in range(n)],

    # computing column sums
    [cs[j] == Sum(x[:, j]) for j in range(n)],

    # computing diagonal sums
    [ds[0] == Sum(diagonal_down(x)), ds[1] == Sum(diagonal_up(x))],

    # all sums must be different
    AllDifferent(rs, cs, ds),

    # ensuring Frenicle standard form  tag(symmetry-breaking)
    [
        x[0][0] < x[0][-1],
        x[0][0] < x[-1][0],
        x[0][0] < x[-1][-1],
        x[0][1] < x[1][0]
    ]
)

""" Comments
1) 3120 solution for n=3
2) This is not a NP-complete problem (it is trivial to build a solution)
3) Data used for the 2025 competition are: [20, 25, 30, 35, 40, 50, 60] for "easy" and [5, 10, 15, 20] for "fair" and "hard"
"""
