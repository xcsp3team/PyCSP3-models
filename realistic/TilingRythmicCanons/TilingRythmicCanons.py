"""
Given a period n and a rhythm A subset of Zn, the Aperiodic Tiling Complements Problem consists in finding all its aperiodic complements B,
i.e., all subsets B of Zn such that A ⊕ B = Zn.

## Data example
  {'t': 16, 'n': 420, 'D': [60, 84, 140, 210], 'A': [0, 12, 24, 36, 48, 70, 82, 94, 106, 118]}

## Model
  constraints: AllDifferent, NValues

## Execution
  python TilingRythmicCanons.py -data=<datafile.json>

## Links
  - https://link.springer.com/article/10.1007/s10601-024-09375-6

## Tags
  realistic, xcsp25


Version 1 : with non 01 variables
"""

from TilingRythmicCanons_Instances import instance
from pycsp3 import *

n, D, A = instance(data) if isinstance(data, int) else data
lD, lA, lB = len(D), len(A), n // len(A)

# x[i] is the ith value of the aperiodic tiling complement
x = VarArray(size=lB, dom=range(n))

# xc[k][i] is the ith value of the kth tiling complement equivalent to x under translation (and containing 0)  tag(symmetry-breaking)
xc = VarArray(size=[lB - 1, lB], dom=range(n))

satisfy(
    # starting with 0
    x[0] == 0,

    # ordering values of the tiling complement
    Increasing(x, strict=True),

    # tag(symmetry-breaking)
    [
        [xc[i][0] == n - x[i + 1] for i in range(lB - 1)],  # gap in the first column

        [xc[i][i + 1] == 0 for i in range(lB - 1)],  # 0 in the diagonal

        [xc[i][j] == (x[j] + xc[i][0]) % n for i in range(lB - 1) for j in range(1, lB) if j != i + 1],

        [LexIncreasing(x, xc[i][i + 1: i + 1 + lB], strict=True) for i in range(lB - 1)]  # strict=True because it also discards periodic rythms
    ] if not variant("table") else None,
)

if not variant() or variant("opt"):
    satisfy(
        # ensuring a tiling rhythmic canon with period 'n'
        AllDifferent((A[i] + x[j]) % n for i in range(lA) for j in range(lB)),

        # ensuring the complement is aperiodic  tag(aperiodicity)
        [NValues(x, [(d + x[j]) % n for j in range(lB)]) > lB for d in D]
    )

elif variant("table"):

    def T(k, j):
        return [(v, (v + k) % n) for v in range(n)]


    xa = VarArray(size=[lA, lB], dom=lambda i, j: range(n) if i != 0 else None)  # None because 0 first value of A

    # tag(aperiodicity)
    xd = VarArray(size=[lD, lB], dom=range(n))

    satisfy(
        [(x[j], xa[i][j]) in T(A[i], j) for i in range(1, lA) for j in range(lB)],

        # ensuring a tiling rhythmic canon with period 'n'
        AllDifferent(x, xa),

        # tag(aperiodicity)
        [(x[j], xd[i][j]) in T(d, j) for i, d in enumerate(D) for j in range(lB)],

        # tag(redundant)
        # [AllDifferent(xd[i]) for i in range(lD)],

        # to test more intensively (instead of NValues)
        # [Exist(AllHold(y[j] != x[i] for i in range(lB)) for j in range(lB)) for id, d in enumerate(D) if (y := xd[id],)],

        # # tag(aperiodicity) ensuring the complement is aperiodic
        # [NValues(x, xd[i]) > lB for i, d in enumerate(D)]
    )

elif variant("elt"):  # TODO many symmetries
    y = VarArray(size=lD, dom=range(lB))
    z = VarArray(size=lD, dom=range(n))

    satisfy(
        [z[i] == x[y[i]] for i in range(lD)],

        [z[i] != (d + x[j]) % n for i, d in enumerate(D) for j in range(lB)]
    )

elif variant("hyb"):  # TODO bug with java -ea ace TilingRythmicCanons-hyb-1.xml -s=all -trace -ev
    T = [tuple([ANY] * lB + [ne(col(i))] * lB) for i in range(lB)]
    satisfy(
        (x, [(d + x[j]) % n for j in range(lB)]) in T for d in D
    )

if variant("opt"):
    minimize(
        x[-1]
    )

""" Comments
1) it seems currently not possible to use n_tailing_eros with the way lex constraints are posted (ot NValues ?)
2) the variants are not finalized or totally tested
"""

# limit = -1  # hard limit (to be proved where it can be put)  avoid introducing many variables and constraints

# [
#     [xc[i][j] == (x[j] + xc[i][0]) % n for i in range(lB - 1) for j in [k % lB for k in range(i + 1, i + 1 + min(limit, lB))] if j != 0 and j != i + 1],
#     [LexIncreasing(x[:min(limit, lB)], xc[i][i + 1: i + 1 + min(limit, lB)]) for i in range(lB - 1)]
# ]
# if limit != -1 else
# [
#     [xc[i][j] == (x[j] + xc[i][0]) % n for i in range(lB - 1) for j in range(1, lB) if j != i + 1],
#     [LexIncreasing(x, xc[i][i + 1: i + 1 + lB]) for i in range(lB - 1)]
# ]

# minimize(  # if we want a COP (other objective ?)
#     Sum(x)
# )

# gc[k] is the gap (value to add) to get the kth equivalent tiling complement  tag(symmetry-breaking)
# gc = VarArray(size=lB - 1, dom=range(n))


# # tag(symmetry-breaking)
#    [
#        [gc[i - 1] == n - x[i] for i in range(1, lB)],
#
#        [xc[i][j] == (0 if j == i + 1 else (x[j] + gc[i]) % n) for i in range(lB - 1) for j in range(lB)],
#
#        [LexIncreasing(x, [xc[i][j] for j in range(i + 1, i + 1 + lB)]) for i in range(lB - 1)]
#    ]


# discarding values from A (already done by the AllDiff)
# [x[i] not in A for i in range(1, lB)],
