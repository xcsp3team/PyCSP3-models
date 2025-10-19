"""
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line with horizontal or vertical segments,
while paying attention to not having crossed lines.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  simple.json

## Model
  constraints: Count, Element

## Execution
  python Amaze_z2.py -data=<datafile.json>
  python Amaze_z2.py -data=<datafile.dzn> -parser=Amaze_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html
  - https://github.com/MiniZinc/minizinc-benchmarks/tree/master/amaze

## Tags
  recreational, mzn12
"""

from pycsp3 import *

n, m, points = data or load_json_data("simple.json")  # points[v] gives the pair of points for value v+1

nPoints, nCells = len(points), n * m

starts = [(v - 1) * m + w - 1 for (v, w), _ in points]
ends = [(v - 1) * m + w - 1 for _, (v, w) in points]


def neighbours(v):
    i, j = v // m, v % m
    return [k * m + l for (k, l) in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)] if 0 <= k < n and 0 <= l < m]


# x[i] is the point value of the ith cell (0 if not in a path)
x = VarArray(size=nCells, dom=range(nPoints + 1))  # +1 for 0

# y[i] is the cell following the ith cell (itself if not in a path)
y = VarArray(size=nCells, dom=range(n * m))

satisfy(
    # setting endpoints
    [
        (
            x[starts[k]] == k + 1,
            x[ends[k]] == k + 1,
            NotExist(y[j] == starts[k] for j in neighbours(starts[k])),
            y[ends[k]] == ends[k]
        ) for k in range(nPoints)
    ],

    # cells in a path have the same value as their successors
    [x[i] == x[y[i]] for i in range(nCells) if i not in ends],

    # cells in a path (except when starting points) must have exactly one predecessor
    [
        If(
            x[i] != 0,
            Then=ExactlyOne(y[j] == i for j in neighbours(i))
        ) for i in range(nCells) if i not in starts
    ],

    # handling cells not in a path
    [
        If(
            x[i] == 0,
            Then=y[i] == i
        ) for i in range(nCells)
    ]
)
