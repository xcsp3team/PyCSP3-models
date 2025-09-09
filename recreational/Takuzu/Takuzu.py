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

n, grid = data
assert n % 2 == 0
m = n // 2

# x[i][j] is the value in the cell of the grid at coordinates (i,j)
x = VarArray(size=[n, n], dom={0, 1})

satisfy(
    # ensuring that each row has the same number of 0s and 1s
    [Sum(x[i]) == m for i in range(n)],

    # ensuring that each colum has the same number of 0s and 1s
    [Sum(x[:, j]) == m for j in range(n)],
)

if not variant():
    satisfy(
        # ensuring no more than two adjacent equal values on each row
        [either(x[i][j] != x[i - 1][j], x[i][j] != x[i + 1][j]) for i in range(1, n - 1) for j in range(n)],

        # ensuring no more than two adjacent equal values on each column
        [either(x[i][j] != x[i][j - 1], x[i][j] != x[i][j + 1]) for j in range(1, n - 1) for i in range(n)],

        # forbidding identical rows
        AllDifferentList(x[i] for i in range(n)),

        # forbidding identical columns
        AllDifferentList(x[:, j] for j in range(n)),
    )

elif variant("mini"):
    T = [(0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0)]

    satisfy(
        # ensuring no more than two adjacent equal values on each row
        [(x[i - 1][j], x[i][j], x[i + 1][j]) in T for i in range(1, n - 1) for j in range(n)],

        # ensuring no more than two adjacent equal values on each column
        [(x[i][j - 1], x[i][j], x[i][j + 1]) in T for j in range(1, n - 1) for i in range(n)]
    )

satisfy(
    # respecting clues if any
    [x[i][j] == grid[i][j] for i in range(n) for j in range(n) if grid and grid[i][j] != -1]
)

if variant("cop"):
    maximize(
        Sum(x[:10, :10])
    )

"""
1) For the mini variant (used for competitions), AllDifferentList are discarded 
2) Data used for the 2024 competition: [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 150 200]
"""
