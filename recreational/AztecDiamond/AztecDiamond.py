"""
An Aztec diamond of order n consists of 2n centered rows of unit squares, of respective lengths 2, 4, ..., 2n-2, 2n, 2n-2, ..., 4, 2.
An Aztec diamond of order n has exactly 2^(n*(n+1)/2) tilings by dominos.

It is easy to build a solution, but finding a random solution is more complex.
A CP model is interesting as one can easily add side constraints to form Aztec diamonds with some specific properties.

## Data
  a unique integer, the order of the diamond

## Model
  constraints: Table

## Execution
  - python AztecDiamond.py -data=[number]

## Links
  - https://en.wikipedia.org/wiki/Aztec_diamond
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
"""

from pycsp3 import *

n = data or 8  # order of the Aztec diamond


def valid(i, j):
    if i < 0 or i >= n * 2 or j < 0 or j >= n * 2:
        return False
    if i < n - 1 and (j < n - 1 - i or j > n + i):
        return False
    if i > n and (j < i - n or j > 3 * n - i - 1):
        return False
    return True


def inner(i, j):
    return valid(i, j - 1) and valid(i, j + 1) and valid(i - 1, j) and valid(i + 1, j)


# all valid cells
valid_cells = [(i, j) for i in range(2 * n) for j in range(2 * n) if valid(i, j)]

# all inner cells, i.e., valid cells that are not situated on the border of the diamond
inners = [(i, j) for i, j in valid_cells if inner(i, j)]

# all border cells, i.e., valid cells that are situated on the border of the diamond
borders = [(i, j) for i, j in valid_cells if not inner(i, j)]

# x[i][j] is the position (0: left, 1: right, 2:top, 3: bottom) of the second part of the domino whose first part occupies the cell ar row i and column j
x = VarArray(size=[2 * n, 2 * n], dom=lambda i, j: range(4) if valid(i, j) else None)

satisfy(
    # constraining cells situated on the top left border
    [(x[i][j], x[i][j + 1], x[i + 1][j]) in {(1, 0, ANY), (3, ANY, 2)} for i, j in borders if not valid(i, j - 1) and not valid(i - 1, j)],

    # constraining cells situated on the top right border
    [(x[i][j], x[i][j - 1], x[i + 1][j]) in {(0, 1, ANY), (3, ANY, 2)} for i, j in borders if not valid(i, j + 1) and not valid(i - 1, j)],

    # constraining cells situated on the bottom left border
    [(x[i][j], x[i][j + 1], x[i - 1][j]) in {(1, 0, ANY), (2, ANY, 3)} for i, j in borders if not valid(i, j - 1) and not valid(i + 1, j)],

    # constraining cells situated on the bottom right border
    [(x[i][j], x[i][j - 1], x[i - 1][j]) in {(0, 1, ANY), (2, ANY, 3)} for i, j in borders if not valid(i, j + 1) and not valid(i + 1, j)],

    # constraining inner cells
    [(x[i][j], x[i][j - 1], x[i][j + 1], x[i - 1][j], x[i + 1][j])
     in {(0, 1, ANY, ANY, ANY), (1, ANY, 0, ANY, ANY), (2, ANY, ANY, 3, ANY), (3, ANY, ANY, ANY, 2)} for i, j in inners]
)
