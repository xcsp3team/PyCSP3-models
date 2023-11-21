"""
The purpose of the game is to fill a grid of size n × n with all values ranging from 1 to n*n such that:
  - if the next number in the sequence is going to be placed vertically or horizontally, then it must be placed exactly three squares away
  from the previous number (there must be a two square gap between the numbers);
  - if the next number in the sequence is going to be placed diagonally, then it must be placed exactly two squares away
  from the previous number (there must be a one square gap between the numbers).

## Data
  a unique integer n

## Model
  constraints: AllDifferent, Count, Table

## Execution
  - python CalvinPuzzle.py -data=[number]
  - python CalvinPuzzle.py -data=[number] -variant=table

## Links
  - https://chycho.blogspot.com/2014/01/an-exercise-for-mind-10-by-10-math.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

n = data or 5

# x[i][j] is the value in the grid at row i and column j
x = VarArray(size=[n, n], dom=range(1, n * n + 1))

# possible neighbours
offsets = [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (-2, 2), (2, -2), (2, 2)]
N = [[[x[i + oi][j + oj] for (oi, oj) in offsets if 0 <= i + oi < n and 0 <= j + oj < n] for j in range(n)] for i in range(n)]

satisfy(
    # putting all values from 1 to n*n in the grid
    AllDifferent(x),

    # tag(symmetry-breaking)
    x[0][0] == 1
)

if not variant():
    satisfy(
        # each cell must be linked to its neighbors
        If(
            x[i][j] < n * n,
            Then=Exist(y == x[i][j] + 1 for y in N[i][j])
        ) for i in range(n) for j in range(n)
    )


elif variant("table"):

    def table(i, j):
        r = len(N[i][j]) + 1
        return [tuple(k if i == 0 else (k + 1) if i == j else ANY for i in range(r)) for k in range(1, n * n) for j in range(1, r)] \
            + [(n * n, *[ANY] * (r - 1))]


    satisfy(
        # each cell must be linked to its neighbors
        (x[i][j], N[i][j]) in table(i, j) for i in range(n) for j in range(n)
    )

"""
1) using an hybrid table is possible
2) 552 solutions for n=5 (with the symmetry-breaking constraint)
"""
