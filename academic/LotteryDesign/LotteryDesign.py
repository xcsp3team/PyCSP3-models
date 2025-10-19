"""
X is a set of balls labelled 1 to d.
Find a set B of n tickets each containing m of these numbers, such that for any draw D of p distinct
balls from X, we can find at least one ticket B ∈ B which matches D in at least t places.

Important: the model, below, does not exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data
   five numbers: d, m, p, t, n

## Model
  constraints: AllDifferentList

## Execution
  python LotteryDesign.py -data=[number,number,number,number,number]

## Links
  - https://doi.org/10.1007/s10601-024-09368-5
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

d, m, p, t, n = data or (32, 6, 6, 2, 17)

assert t == 2  # for the moment

# x[i][j] is the jth value on the ith ticket
x = VarArray(size=[n, m], dom=range(d))

draw = VarArray(size=p, dom=range(d))

tol = VarArray(size=n, dom=range(p))

satisfy(
    AllDifferentList(x),

    # tag(symmetry-breaking)
    [Increasing(x[i], strict=True) for i in range(n)],

    Increasing(draw, strict=True),

    [
        If(
            tol[i] != k,
            Then=x[i][j] != draw[k]
        ) for i in range(n) for j in range(m) for k in range(p)
    ]
)

"""
1) Data used for the 2025 competition are: [32, 6, 6, 2, k] with k in [7, 17, 47, 67, 87, 107, 207, 307, 407, 1000, 2000, 3000]
"""
