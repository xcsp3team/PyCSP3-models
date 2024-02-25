"""
Place knights, rooks, queens, bishops on an n*n chessboard so that none takes each other.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  03.json

## Model
  constraints: Count, Element, Sum

## Execution
  python Chessboard.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  recreational, mzn23
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry

n, values, limits = data
nPieces = 5
KNIGHT, BISHOP, ROOK, QUEEN, EMPTY = range(nPieces)

symmetries = [sym.apply_on(n) for sym in TypeSquareSymmetry]

skips = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
knight_neighbors = [[[(i + oi, j + oj) for (oi, oj) in skips if 0 <= i + oi < n and 0 <= j + oj < n] for j in range(n)] for i in range(n)]

# x[i][j] is the piece in the cell of coordinates s(i,j)
x = VarArray(size=[n, n], dom=range(nPieces))

# y[p] is the number of occurrences of the pth piece
y = VarArray(size=nPieces, dom=lambda p: range(limits[p] + 1) if p != EMPTY else range(n * n - sum(limits) + limits[EMPTY], n * n + 1))

satisfy(
    Cardinality(x, occurrences=y),

    # a rook or a queen prevents putting any other piece in the same row
    [
        If(
            Exist(x[i][j] in {ROOK, QUEEN} for j in range(n)),  # we can also write x[i][j].among(R,Q)
            Then=Sum(x[i][j] != EMPTY for j in range(n)) <= 1
        ) for i in range(n)
    ],

    # a rook or a queen prevents any other piece in the same column
    [
        If(
            Exist(x[i][j] in {ROOK, QUEEN} for i in range(n)),
            Then=Sum(x[i][j] != EMPTY for i in range(n)) <= 1
        ) for j in range(n)
    ],

    # a bishop or a queen prevents putting any other piece in the same upward diagonal
    [
        If(
            Exist(y in {BISHOP, QUEEN} for y in diag),
            Then=Sum(y != EMPTY for y in diag) <= 1
        ) for diag in diagonals_up(x)
    ],

    # a bishop or a queen prevents putting any other piece in the same downward diagonal
    [
        If(
            Exist(y in {BISHOP, QUEEN} for y in diag),
            Then=Sum(y != EMPTY for y in diag) <= 1
        ) for diag in diagonals_down(x)
    ],

    # taking care of knights
    [
        If(
            x[i][j] == KNIGHT,
            Then=x[k][l] == EMPTY
        ) for i in range(n) for j in range(n) for (k, l) in knight_neighbors[i][j]
    ],

    # tag(redundant-constraints)
    [
        y[ROOK] + y[QUEEN] <= n,
        y[BISHOP] + y[QUEEN] <= 2 * n - 1,
        y[KNIGHT] <= (n * n + 1) // 2
    ],

    # dominance rules
    [
        If(y[QUEEN] > 0, Then=y[BISHOP] == limits[BISHOP]) if values[QUEEN] <= values[BISHOP] else None,
        If(y[QUEEN] > 0, Then=y[ROOK] == limits[ROOK]) if values[QUEEN] <= values[ROOK] else None
    ],

    # tag(symmetry-breaking)
    [LexIncreasing(x, [x[row] for row in symmetry]) for symmetry in symmetries]
)

maximize(
    # maximizing the summed values of placed pieces
    Sum(values[x[i][j]] for i in range(n) for j in range(n))
)

"""
1) bounds on y are enforced when declaring domains
2) is it interesting to only post binary constraints instead of the complex imply expressions?
3)  the reverse array from the Minizinc model not introduced here (useful for output?)
4) we can choose among the following statements:
  Exist(x[i][j] in {ROOK, QUEEN} for j in range(n)),  
  Exist(x[i][j].among(ROOK, QUEEN) for j in range(n)),  
  Exist(belong(x[i][j],{ROOK, QUEEN}) for j in range(n)),  
"""
