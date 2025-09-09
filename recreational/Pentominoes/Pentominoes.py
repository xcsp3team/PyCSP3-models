"""
The goal is to fill a grid of size n by m with different pentominoes.

## Data
  two integers n, and m

## Model
  constraints: AllDifferent, Table

## Execution
  python Pentominoes.py -data=[number,number]

## Links
  - https://en.wikipedia.org/wiki/Polyomino
  - https://www.researchgate.net/publication/333296614_Polyominoes
  - https://en.wikipedia.org/wiki/The_Art_of_Computer_Programming
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, recreational, xcsp24
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry
from pycsp3.tools.utilities import polyominoes

n, m = data
assert n * m in (60, 90, 120)  # for the moment
nPieces = (n * m) // 5

pentominoes = list(polyominoes[5].values())  # 12 distinct pentominoes


def table(pentomino):
    tbl = []
    for i in range(n):
        for j in range(m):
            for sym in TypeSquareSymmetry.symmetric_patterns(pentomino):
                if all(0 <= i + k < n and 0 <= j + l < m for k, l in sym):
                    tbl.append(tuple((i + k) * m + (j + l) for k, l in sym))
    return tbl


# x[i][j] is the board cell index where is put the jth piece of the ith pentomino
x = VarArray(size=[nPieces, 5], dom=range(n * m))

satisfy(
    # positioning all pentominoes correctly
    [x[i] in table(pentominoes[i % 12]) for i in range(nPieces)],

    # ensuring no overlapping pieces
    AllDifferent(x),

    # tag(symmetry-breaking)
    [x[i % 12][0] < x[i][0] for i in range(13, nPieces)]
)

""" Comments
1)  Data used for the 2024 Competition: [(3,20), (4,15), (5,12), (6,10), (3,30), (5,18), (6,15), (9,10), (3,40), (4,30), (5,24), (6,20), (8,15), (10,12)]
"""
