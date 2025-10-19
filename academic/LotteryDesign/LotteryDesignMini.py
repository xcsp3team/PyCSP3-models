"""
X is a set of balls labelled 1 to d.
Find a set B of n tickets each containing m of these numbers, such that for any draw D of p distinct
balls from X, we can find at least one ticket B ∈ B which matches D in at least t places.

Important: the model, below, does not exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data
   five numbers: d, m, p, t, n

## Model
  constraints: AllDifferent

## Execution
  python LotteryDesign.py -data=[number,number,number,number,number]

## Links
  - https://doi.org/10.1007/s10601-024-09368-5

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

d, m, p, t, n = data or (32, 6, 6, 2, 17)

assert t == 2  # for the moment

T = lambda k: build_table([range(p), range(d), range(d)], lambda v1, v2, v3: not (v1 != k) or (v2 != v3))

# x[i][j] is the jth value on the ith ticket
x = VarArray(size=[n, m], dom=range(d))

draw = VarArray(size=p, dom=range(d))

tol = VarArray(size=n, dom=range(p))

pos = VarArray(size=[n, n], dom=lambda i1, i2: range(m) if i1 < i2 else None)

pos1 = VarArray(size=[n, n], dom=lambda i1, i2: range(m) if i1 < i2 else None)

pos2 = VarArray(size=[n, n], dom=lambda i1, i2: range(m) if i1 < i2 else None)

satisfy(
    [x[i1][pos[i1][i2]] == pos1[i1][i2] for i1, i2 in combinations(n, 2)],
    [x[i2][pos[i1][i2]] == pos2[i1][i2] for i1, i2 in combinations(n, 2)],
    [pos1[i1][i2] != pos2[i1][i2] for i1, i2 in combinations(n, 2)],

    # tag(symmetry-breaking)
    [Increasing(x[i], strict=True) for i in range(n)],

    Increasing(draw, strict=True),

    [
        Table(
            scope=(tol[i], x[i][j], draw[k]),
            supports=T(k)
        ) for i in range(n) for j in range(m) for k in range(p)
    ]
)
