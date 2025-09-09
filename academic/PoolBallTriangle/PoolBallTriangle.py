"""
From Martin Gardner:
  Given n*(n+1) div 2 numbered pool balls in a triangle, is it possible to place them so that the number of each ball below
  two balls is the difference of (the number of) those two balls?

## Data
  an integer n

## Model
  constraints: AllDifferent

## Execution
  python PoolBallTriangle.py -data=number

## Links
  - https://archive.org/details/penrose-tiles-to-trapdoor-ciphers/mode/2up
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
"""

from pycsp3 import *

n = data or 5
k = (n * (n + 1)) // 2

x = VarArray(size=[n, n], dom=lambda i, j: range(1, k + 1) if i < n - j else None)

satisfy(
    AllDifferent(x),

    [x[i][j] == abs(x[i - 1][j] - x[i - 1][j + 1]) for i in range(1, n) for j in range(n - i)],

    # tag(symmetry-breaking)
    x[-2][0] < x[-2][1]
)

""" Comments
1) There are no solutions for n from 6 to 10
2) Data used for the 2024 Competition are: [5, 7, 10, 11, 12, 13, 14, 15, 16, 18, 20]
"""
