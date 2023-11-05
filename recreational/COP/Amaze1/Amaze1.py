"""
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line sith horizontal or vertical segments,
while paying attention to not having crossed lines.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  2012-03-08.json

## Model
  constraints: Count, Sum

## Execution
  python Amaze1.py -data=<datafile.json>
  python Amaze1.py -data=<datafile.dzn> -parser=Amaze_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html
  - https://github.com/MiniZinc/minizinc-benchmarks/tree/master/amaze

## Tags
  recreational, mzn12
"""

from pycsp3 import *

n, m, points = data  # points[v] gives the pair of points for value v+1
nValues = len(points) + 1  # number of pairs of points + 1 (for 0)

free_cells = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1) if (i, j) not in [tuple(p) for pair in points for p in pair]]

# x[i][j] is the value in the cell at row i and column j (a boundary is put around the board)
x = VarArray(size=[n + 2, m + 2], dom=lambda i, j: {0} if i in {0, n + 1} or j in {0, m + 1} else range(nValues))

satisfy(
    # setting endpoints
    [x[i][j] == v for v in range(1, nValues) for i, j in points[v - 1]],

    # each cell with a fixed value has exactly one neighbour with the same value
    [ExactlyOne(x.beside(i, j), value=v) for v in range(1, nValues) for i, j in points[v - 1]],

    # each empty cell either contains 0 or has exactly two neighbours with the same value
    [
        If(
            x[i][j] != 0,
            Then=Count(x.beside(i, j), value=x[i][j]) == 2
        ) for i, j in free_cells
    ]
)

minimize(
    Sum(x)
)

""" Comments
1) Note that x.beside(i,j) is equivalent to [x[i - 1][j], x[i + 1][j], x[i][j - 1], x[i][j + 1]]
"""
