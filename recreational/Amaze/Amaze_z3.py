"""
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line sith horizontal or vertical segments,
while paying attention to not having crossed lines.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  simple.json

## Model
  constraints: Count

## Execution
  python Amaze_z3.py -data=<datafile.json>
  python Amaze_z3.py -data=<datafile.dzn> -parser=Amaze_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  recreational, mzn14, mzn19
"""

from pycsp3 import *

n, m, points = data  # points[v] gives the pair of points for value v+1
points = decrement(points)  # to make things easier
nPoints, nCells = len(points), n * m

free_cells = [(i, j) for i in range(n) for j in range(m) if [i, j] not in [p for pair in points for p in pair]]


def neighbours(i, j):
    return [(k, l) for (k, l) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if 0 <= k < n and 0 <= l < m]


# x[i][j] is the point value of the cell at row i and column j (0 if not in a path)
x = VarArray(size=[n, m], dom=range(nPoints + 1))

satisfy(
    # setting endpoints
    [x[i][j] == k + 1 for k in range(nPoints) for i, j in points[k]],

    # each cell with a fixed value has exactly one neighbour with the same value
    [
        ExactlyOne(
            within=x[neighbours(i, j)],
            value=k + 1
        ) for k in range(nPoints) for i, j in points[k]
    ],

    # ensuring interior cells have exactly two neighbours
    [
        If(
            x[i][j] != 0,
            Then=Count(
                within=x[neighbours(i, j)],
                value=x[i][j]
            ) == 2
        ) for i, j in free_cells
    ],

    # tag(redundant-constraints)
    [
        [
            Exist(
                within=x[i],
                value=k + 1
            ) for k, ((u, _), (v, _)) in enumerate(points) for i in range(min(u, v) + 1, max(u, v))
        ],
        [
            Exist(
                within=x[:, j],
                value=k + 1
            ) for k, ((_, u), (_, v)) in enumerate(points) for j in range(min(u, v) + 1, max(u, v))
        ]
    ]
)

""" Comments

1) Note that:
   x[neighbours(i, j)]
 is a shortcut for:
   [x[k][l] for k, l in neighbours(i, j)]
"""
