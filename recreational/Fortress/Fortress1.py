"""
From LPCP contest 2022 (problem 1):
     A map comprises nxm cells, some of them marked with a positive integer D to denote a point-of-interest that requires D free-of-walls cells around them;
     more specifically, no path of length D (Manhattan distance) originating from the point-of-interest can include walls.
     All point-of-interests must be inside the perimeter of the walls, the number of walls must be minimized,
     and as a second optimization criteria we prefer to minimize the amount of cells inside the perimeter of the walls.

Important: the model, below, has not been checked to exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data Example
  03.json

## Model
  constraints: Sum, Table

## Execution
  python Fortress1.py -data=<datafile.json>
  python Fortress1.py -data=<datafile.txt> -parser=Fortress_Parser.py

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2022/tree/main/problem-1
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, lpcp22, xcsp25
"""

from pycsp3 import *

grid = data or load_json_data("03.json")

n, m = len(grid), len(grid[0])
N, M = range(n), range(m)

points = [(i, j) for i in N for j in M if grid[i][j] != 0]

left = min(j - grid[i][j] for i, j in points) - 1
right = max(j + grid[i][j] for i, j in points) + 1
top = min(i - grid[i][j] for i, j in points) - 1
bot = max(i + grid[i][j] for i, j in points) + 1

neighborhoods = [[(k, q) for k in N for q in M if abs(k - i) + abs(q - j) < grid[i][j]] for i, j in points]

# w[i][j] is 1 iff the cell (i,j) is a wall
w = VarArray(size=[n, m], dom=lambda i, j: {0, 1} if i in range(top, bot + 1) and j in range(left, right + 1) else {0})

# f[i][j] is 1 iff it is free (we can leave from cell at coordinates (i,j))
f = VarArray(size=[n, m], dom={0, 1})

# nW is the number of walls
nW = Var(range(n * m + 1))

# nF is the number of free cells
nF = Var(range(n * m + 1))

satisfy(

    [w[i][j] == 0 for neighborhood in neighborhoods for i, j in neighborhood],

    # setting the status of the border
    [(w[i][j], f[i][j]) in {(0, 1), (1, 0)} for i in N for j in M if i in (0, n - 1) or j in (0, m - 1)],

    # setting the status of the point of interest
    [f[i][j] == 0 for i, j in points],

    [
        Table(
            scope=(w[i][j], f.cross(i, j)),
            supports={(0, 0, 0, 0, 0, 0), (0, 1, 1, ANY, ANY, ANY), (0, 1, ANY, 1, ANY, ANY), (0, 1, ANY, ANY, 1, ANY),
                      (0, 1, ANY, ANY, ANY, 1), (1, 0, ANY, ANY, ANY, ANY)}
        ) for i in N[1:-1] for j in M[1:- 1]
    ],

    # computing thr number of walls
    nW == Sum(w),

    # computing the number of free cells
    nF + Sum(f) + nW == n * m
)

minimize(
    Sum(w) * 10000 - Sum(f)
)

""" Comments
1) 10000, as coefficient in the objective expression,  is enough for a grid up to 100*100
"""
