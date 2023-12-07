"""
The Maximum Density Sill-Life Problem is to fill an n ×n board of cells with the maximum number of live cells
so that the board is stable under the rules of Conway’s Game of Life.
In the CP conference paper (whose reference is given below), the problem is to minimise “wastage” instead.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  An integer n, the order of the problem instance

## Model
  constraints: Sum

## Execution
  python StillLifeWastage.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Still_life_(cellular_automaton)
  - https://link.springer.com/chapter/10.1007/978-3-642-04244-7_22
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  academic, mzn12
"""

from pycsp3 import *

n = data
cells = [(i, j) for i in range(1, n + 1) for j in range(1, n + 1)]  # coordinates of valid cells

# x[i][j] is 1 iff the cell with coordinates (i,j) is alive (note the presence of a border)
x = VarArray(size=[n + 2, n + 2], dom=lambda i, j: {0} if i in {0, n + 1} or j in {0, n + 1} else {0, 1})

# w[i][j] is the wastage for the cell with coordinates (i,j)
w = VarArray(size=[n + 2, n + 2], dom={0, 1, 2})

# ws[i] is the wastage sum for cells at row i
ws = VarArray(size=n + 2, dom=range(2 * (n + 2) * (n + 2) + 1))

# s1[i][j] is the number of alive cells around the cell with coordinates (i,j)
s1 = VarArray(size=[n + 2, n + 2], dom=lambda i, j: {0} if i in {0, n + 1} or j in {0, n + 1} else range(9))

# s2[i][j] is a value computed from alive neighbours around the cell with coordinates (i,j)
s2 = VarArray(size=[n + 2, n + 2], dom=lambda i, j: {0} if i in {0, n + 1} or j in {0, n + 1} else range(9))

# s3[i][j] is the number of direct neighbours that are alive around the cell with coordinates (i,j)
s3 = VarArray(size=[n + 2, n + 2], dom=lambda i, j: {0} if i in {0, n + 1} or j in {0, n + 1} else range(5))

satisfy(

    # special restrictions on cells at the border
    [
        [x[1][j - 1] + x[1][j] + x[1][j + 1] <= 2 for j in range(1, n + 1)],
        [x[n][j - 1] + x[n][j] + x[n][j + 1] <= 2 for j in range(1, n + 1)],
        [x[i - 1][1] + x[i][1] + x[i + 1][1] <= 2 for i in range(1, n + 1)],
        [x[i - 1][n] + x[i][n] + x[i + 1][n] <= 2 for i in range(1, n + 1)]
    ],

    # computing auxiliary variables
    [
        [s1[i][j] == Sum(x.around(i, j)) for i, j in cells],
        [s2[i][j] == Sum(
            x[i - 1][j - 1] * x[i - 1][j + 1],
            x[i - 1][j + 1] * x[i + 1][j + 1],
            x[i + 1][j + 1] * x[i + 1][j - 1],
            x[i + 1][j - 1] * x[i - 1][j - 1],
            s3[i][j]
        ) for i, j in cells],
        [s3[i][j] == Sum(x.beside(i, j)) for i, j in cells]
    ],

    # implementing still life rules
    [
        (
            If(
                x[i][j] == 1,
                Then=s1[i][j] in {2, 3},
                Else=s1[i][j] != 3
            ),
            If(x[i][j] == 1, s2[i][j] <= 1, Then=w[i][j] >= 1),
            If(x[i][j] == 1, s2[i][j] <= 0, Then=w[i][j] >= 2),
            If(x[i][j] == 0, s3[i][j] >= 4, Then=w[i][j] >= 2),
            If(x[i][j] == 0, s3[i][j] <= 1, Then=w[i][j] >= 1),
            If(x[i][j] == 0, s3[i][j] <= 0, Then=w[i][j] >= 2)
        ) for i, j in cells
    ],

    # managing wastage on the border
    [
        (
            w[0][k] + x[1][k] == 1,
            w[n + 1][k] + x[n][k] == 1,
            w[k][0] + x[k][1] == 1,
            w[k][n + 1] + x[k][n] == 1
        ) for k in range(1, n + 1)
    ],

    # summing wastage
    [
        ws[0] == Sum(w[0]),
        [ws[i] == ws[i - 1] + Sum(w[i]) for i in range(1, n + 2)]
    ],

    # tag(redundant-constraints)
    [ws[n + 1] - ws[i] >= 2 * ((n - i) // 3) + n // 3 for i in range(n + 1)]
)

maximize(
    # maximizing the number of alive cells
    (2 * n * n + 4 * n - ws[-1]) // 4
)

"""
1) data used in 2012 are: 9, 10, 11, 12 and 13
"""
