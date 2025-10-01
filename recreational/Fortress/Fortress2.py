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
  python Fortress2.py -data=<datafile.json>
  python Fortress2.py -data=<datafile.txt> -parser=Fortress_Parser.py

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2022/tree/main/problem-1
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, lpcp22, xcsp25
"""

from pycsp3 import *

grid = data or load_json_data("03.json")

n, m = len(grid), len(grid[0])
assert n <= 100 and m <= 100  # otherwise, we have for example to change the constant 10000 by n*m

OUT, IN, WALL = 0, 1, 10000  # 10000 is enough for a grid up to 100*100

points = [(i, j) for i in range(n) for j in range(m) if grid[i][j] != 0]
in_required = [(i, j) for i in range(n) for j in range(m) if any((k, l) for k, l in points if abs(k - i) + abs(l - j) < grid[k][l])]

# table used for computing states of cells
T = {(OUT, OUT, ANY, ANY, ANY), (OUT, ANY, OUT, ANY, ANY), (OUT, ANY, ANY, OUT, ANY), (OUT, ANY, ANY, ANY, OUT),
     (IN, ne(OUT), ne(OUT), ne(OUT), ne(OUT)), (WALL, ANY, ANY, ANY, ANY)}

top = min(i - grid[i][j] for i, j in points)
bot = max(i + grid[i][j] for i, j in points)
left = min(j - grid[i][j] for i, j in points)
right = max(j + grid[i][j] for i, j in points)
assert top > 0 and bot < n - 1 and left > 0 and right < m - 1  # otherwise, it is always possible to add a dummy border in the data


def domain_x(i, j):
    if i < top or i > bot or j < left or j > right:
        return {OUT}  # ensuring OUT outside the possible frontier for the walls
    if (i, j) in in_required:
        return {IN}  # ensuring that cells at proximity of the points of interest are inside the walls
    return {OUT, IN, WALL}


# x[i][j] is the status of the cell (i,j)
x = VarArray(size=[n, m], dom=domain_x)

satisfy(
    # computing the state of cells with respect to their (cross) neighbors
    x.cross(i, j) in T for i in range(top, bot + 1) for j in range(left, right + 1)
)

minimize(
    # minimizing the number of walls and then the number of inside cells
    Sum(x)
)

# seems not interesting to add something like:
# a) [(x[i][j] != WALL) | (Count(x.around(i, j, with_center=False), value=WALL) == 2) for i in range(1, n - 1) for j in range(1, m - 1)]

# or b) [x.around(i, j, with_center=True) in {(OUT, ANY, ANY, ANY, ANY, ANY, ANY, ANY, ANY),
#                                       (IN, ANY, ANY, ANY, ANY, ANY, ANY, ANY, ANY),
#                                       (WALL, WALL, WALL, ne(WALL), ne(WALL), ne(WALL), ne(WALL), ne(WALL), ne(WALL)),
#                                       (WALL, WALL, ne(WALL), WALL, ne(WALL), ne(WALL), ne(WALL), ne(WALL), ne(WALL)),
#                                       (WALL, ne(WALL), WALL, WALL, ne(WALL), ne(WALL), ne(WALL), ne(WALL), ne(WALL)),
#                                       ...
#                                       }   for i in range(1, n - 1) for j in range(1, m - 1)],

# Not interesting to (because it perturbates the variable ordering heuristic on important variables?):
# a) add  in domain_x:
#     if i in (top, bot) or j in (left, right):
#       return {OUT, WALL}  # ensuring no possible IN on the possible frontier of the walls
# b) write consequently:
#     x.cross(i, j) in T for i in range(top + 1, bot) for j in range(left + 1, right)


# java ace Fortress2-instance.10.xml => 1802052 in 500s

# tt = [(i,j) for i in range(n) for j in range(m) if t[i][j] !=0 ]
# print(len(tt))
# for i,j in tt:
#     print(i, j)
