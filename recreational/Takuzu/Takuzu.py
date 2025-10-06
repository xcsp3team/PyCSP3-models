"""
From Wikipedia:
    Takuzu, also known as Binairo, is a logic puzzle involving placement of two symbols, often 1s and 0s, on a rectangular grid.
    The objective is to fill the grid with 1s and 0s, where there is an equal number of 1s and 0s in each row and column and no more than two of either number adjacent to each other.
    Additionally, there can be no identical rows or columns.

## Data
  an integer n, and clues (possibly None)

## Model
  constraints: AllDifferentList, Sum

## Execution
  python Takuzu.py -data=<datafile.json>
  python Takuzu.py -data=[number,None]
  python Takuzu.py -data=<datafile.json> -variant=mini

## Links
  - https://en.wikipedia.org/wiki/Takuzu
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, recreational, xcsp24
"""

from pycsp3 import *

assert not variant() or variant("mini")

n, grid = data or (30, None)

assert n % 2 == 0
m = n // 2
N = range(n)

# x[i][j] is the value in the cell of the grid at coordinates (i,j)
x = VarArray(size=[n, n], dom={0, 1})

satisfy(
    # ensuring that each row has the same number of 0s and 1s
    [Sum(x[i]) == m for i in N],

    # ensuring that each colum has the same number of 0s and 1s
    [Sum(x[:, j]) == m for j in N],
)

if not variant():
    satisfy(
        # ensuring no more than two adjacent equal values on each row
        [
            either(
                x[i][j] != x[i - 1][j],
                x[i][j] != x[i + 1][j]
            ) for i in N[1:- 1] for j in N
        ],

        # ensuring no more than two adjacent equal values on each column
        [
            either(
                x[i][j] != x[i][j - 1],
                x[i][j] != x[i][j + 1]
            ) for j in N[1:- 1] for i in N
        ],

        # forbidding identical rows
        AllDifferentList(x[i] for i in N),

        # forbidding identical columns
        AllDifferentList(x[:, j] for j in N),
    )

elif variant("mini"):
    T = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0)]

    satisfy(
        # ensuring no more than two adjacent equal values on each row
        [(x[i - 1][j], x[i][j], x[i + 1][j]) in T for i in N[1:- 1] for j in N],

        # ensuring no more than two adjacent equal values on each column
        [(x[i][j - 1], x[i][j], x[i][j + 1]) in T for j in N[1:- 1] for i in N]
    )

satisfy(
    # respecting clues if any
    [x[i][j] == grid[i][j] for i in N for j in N if grid is not None and grid[i][j] != -1]
)

"""
1) For the mini variant (used for competitions), AllDifferentList are discarded 
2) Data used for the 2024 competition: [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 150 200]
"""

# if variant("cop"):
#     maximize(
#         Sum(x[:10, :10])
#     )
