"""
From JaneStreet:
    An almost magic square is, well, almost a magic square.
    It differs from a magic square in that the 8 sums may differ from each other by at most 1.
    For this puzzle, place distinct positive integers into the empty grid above such that each of four bold-outlined 3-by-3 regions is an almost magic square.
    Your goal is to do so in a way that minimizes the overall sum of the integers you use.


## Data
  two numbers n and p

## Model
  constraints: AllDifferent, Sum

## Execution
  python AlmostMagic.py -data=[number,number]
  python AlmostMagic.py -data=[number,number] -variant=opt

## Links
  - https://www.janestreet.com/puzzles/almost-magic-index/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, janestreet, xcsp25
"""

from pycsp3 import *
from pycsp3.classes.main.annotations import ValHeuristic

assert not variant() or variant("opt")

n, p = data or (3, 100)

# x[k][i][j] is the value at row i and column j in the kth region
x = VarArray(size=[4, n, n], dom=range(1, p))

# y[k] is the almost magic value of the kth region
y = VarArray(size=4, dom=range(p * 3))

distinct = flatten(x[0], x[1][0][1:], x[1][1][1:], x[1][2][2], x[2][0][0], x[2][1][:-1], x[2][2][:-1], x[3])


def ctr_sum(t, k):
    return (
        Sum(t) >= k,
        Sum(t) <= k + 1
    )


satisfy(
    # ensuring different values
    AllDifferent(distinct),

    # ensuring almost magic regions
    [
        (
            [ctr_sum(x[k][i], y[k]) for i in range(n)],
            [ctr_sum(x[k][:, j], y[k]) for j in range(n)],
            ctr_sum(diagonal_down(x[k]), y[k]),
            ctr_sum(diagonal_up(x[k]), y[k])
        ) for k in range(4)
    ],

    # dealing with overlapping cells
    [
        [x[0][i][-1] == x[1][i - 1][0] for i in range(1, n)],
        [x[0][-1][j - 1] == x[2][0][j] for j in range(1, n)],
        [x[1][-1][j - 1] == x[3][0][j] for j in range(1, n)],
        [x[2][i][-1] == x[3][i - 1][0] for i in range(1, n)]
    ]
)

if variant("opt"):
    minimize(
        Sum(distinct)
    )

""" Comments
1) data used for the 2025 competition are: [(3,30), (3,35), (3,40), (3,70), (4,50), (4,80), (5,70), (6,100), (7,130), (8,160), (9,200), (10,250)]
"""

# annotate(
#     valHeuristic=ValHeuristic().static(y, order=list(range(p * 3)))
# )
