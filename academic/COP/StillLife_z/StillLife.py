"""
The still life problem is to find an arrangement of cells that does not change from one generation to the next.
We want the solution with the largest number of live cells.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009 Minizinc challenge.
The MZN model was proposed by Ralph Becket.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  an integer n, the order of the problem instance

## Model
  constraints: Sum, Table

## Execution
  python StillLife.py -data=[number]
  python StillLife.py -variant=table -data=[number]

## Links
  - https://en.wikipedia.org/wiki/Still_life_(cellular_automaton)
  - https://www.minizinc.org/challenge2009/results2009.html

## Tags
  academic, mzn09
"""

from pycsp3 import *

n = data

cells = [(i, j) for i in range(n) for j in range(n)]

# x[i][j] is 1 iff the cell at row i and col j is alive
x = VarArray(size=[n, n], dom={0, 1})

# y[i][j] is the number of alive neighbours for the cell at row i and col j
y = VarArray(size=[n, n], dom=range(7))

satisfy(
    # imposing boundary restrictions
    [
        (
            Sum(x[0, k - 1:k + 2]) < 3,
            Sum(x[-1, k - 1:k + 2]) < 3,
            Sum(x[k - 1:k + 2, 0]) < 3,
            Sum(x[k - 1:k + 2, -1]) < 3
        ) for k in range(1, n - 1)
    ],

    # computing the number of alive neighbours
    [y[i][j] == Sum(x.around(i, j)) for i, j in cells]
)

if not variant():
    satisfy(
        # imposing still life rules
        [
            If(
                x[i][j] == 0,
                Then=y[i][j] != 3,
                Else=y[i][j] in {2, 3}
            ) for i, j in cells
        ]
    )

elif variant("table"):
    T = [(0, v) for v in range(7) if v != 3] + [(1, 2), (1, 3)]

    satisfy(
        # imposing still life rules
        (x[i][j], y[i][j]) in T for i, j in cells
    )

maximize(
    # maximizing the number of alive cells
    Sum(x)
)

"""
1) data used in 2009 are: 5, 6, 7, 8, 9
"""
