"""
Fillomino is played on a rectangular grid, with some cells containing numbers.
The goal is to divide the grid into regions called polyominoes (by filling in their boundaries)
such that each given number n in the grid satisfies the following constraints:
  - each clue n is part of a polyomino of size n
  - no two polyominoes of matching size (number of cells) are orthogonally adjacent (share a side)

## Data Example
  08.json

## Model
  constraints: Element, Sum, Table

## Execution
  python Fillomino.py -data=<datafile.json>

## Links
  - https://en.wikipedia.org/wiki/Fillomino

## Tags
  recreational
"""

from pycsp3 import *

puzzle = data
n, m = len(puzzle), len(puzzle[0])

Values = {puzzle[i][j] for i in range(n) for j in range(m) if puzzle[i][j] > 0}

seen = set()
preassigned = []
for i in range(n):
    for j in range(m):
        if puzzle[i][j] == 1 or (puzzle[i][j] > 1 and puzzle[i][j] not in seen):  # the second part is important
            preassigned.append((len(preassigned), puzzle[i][j], i + 1, j + 1))  # +1 because of the border
            seen.add(puzzle[i][j])

remaining = n * m - sum(sz for (_, sz, _, _) in preassigned)
nRegions = len(preassigned) + remaining  # n max regions
maxDistance = max(max(Values), remaining) + 1  # this is the maximal distance + 1

Points = [(i, j) for i in range(1, n + 1) for j in range(1, m + 1)]


def tables():
    t = {(1, ANY, ANY, ANY, ANY, ANY, 0, ANY, ANY, ANY, ANY)}
    for k in range(nRegions):  # we force the root to be the first cell of the region wrt top left
        # t.add((gt(1), k, k, ANY, ANY, ANY, 0, 1, ANY, ANY, ANY))
        t.add((gt(1), k, ANY, k, ANY, ANY, 0, ANY, 1, ANY, ANY))
        # t.add((gt(1), k, ANY, ANY, k, ANY, 0, ANY, ANY, 1, ANY))
        t.add((gt(1), k, ANY, ANY, ANY, k, 0, ANY, ANY, ANY, 1))
        for v in range(1, maxDistance):
            t.add((gt(1), k, k, ANY, ANY, ANY, v, v - 1, ANY, ANY, ANY))
            t.add((gt(1), k, ANY, k, ANY, ANY, v, ANY, v - 1, ANY, ANY))
            t.add((gt(1), k, ANY, ANY, k, ANY, v, ANY, ANY, v - 1, ANY))
            t.add((gt(1), k, ANY, ANY, ANY, k, v, ANY, ANY, ANY, v - 1))
    return t, {(v, v, k, k) for v in Values for k in range(nRegions)} | {(v, ne(v), k, ne(k)) for v in Values for k in range(nRegions)}


Tc, Tr = tables()  # tables for connections and regions

# x[i][j] is the region (number) where the square at row i and column j belongs (borders are inserted for simplicity)
x = VarArray(size=[n + 2, m + 2], dom=range(nRegions), dom_border={-1})

# y[i][j] is the value of the square at row i and column j
y = VarArray(size=[n + 2, m + 2], dom=lambda i, j: {puzzle[i - 1][j - 1]} if puzzle[i - 1][j - 1] != 0 else Values, dom_border={-1})

# d[i][j] is the distance of the square at row i and column j wrt the starting square of the (same) region
d = VarArray(size=[n + 2, m + 2], dom=range(maxDistance), dom_border={-1})

# s[k] is the size of the kth region
s = VarArray(size=nRegions, dom={0} | Values)  # it is important to have 0

satisfy(
    # setting starting squares of pre-assigned regions
    [
        (
            x[i][j] == k,
            y[i][j] == sz,
            s[k] == sz
        ) for k, sz, i, j in preassigned
    ],

    # setting values according to the size of the regions
    [y[i][j] == s[x[i][j]] for i, j in Points if puzzle[i - 1][j - 1] == 0],

    # controlling the size of each region
    [s[k] == Sum(x[i][j] == k for i, j in Points) for k in range(nRegions)],

    # ensuring connection
    [(y[i][j], x.cross(i, j), d.cross(i, j)) in Tc for i, j in Points],

    # two regions of the same size cannot have neighbouring squares
    [
        [(y[i][j], y[i][j + 1], x[i][j], x[i][j + 1]) in Tr for i in range(1, n + 1) for j in range(1, m)],
        [(y[i][j], y[i + 1][j], x[i][j], x[i + 1][j]) in Tr for j in range(1, m + 1) for i in range(1, n)]
    ],

    # ensuring a single root for each region  tag(symmetry-breaking)
    [
        If(
            d[i][j] == 0, d[p][q] == 0,
            Then=x[i][j] != x[p][q]
        ) for (i, j) in Points for (p, q) in Points if (i, j) != (p, q)
    ],

    # pushing regions of size 0 on the right  tag(symmetry-breaking)
    [
        If(
            s[k] == 0,
            Then=s[k + 1] == 0
        ) for k in range(nRegions - 1)
    ]
)

""" Comments

1) cross() is a predefined method on matrices of variables (of type ListVar).
   Hence, x.cross(i, j) is equivalent to :
   [t[i][j], t[i][j - 1], t[i][j + 1], t[i - 1][j], t[i + 1][j]] 
   
2) gt(1) when building a tuple allows to handle all tuples with a value > 1
   Later, it will be possible to generate smart tables instead of starred tables 
   
3) For the mini-track of the competition, we replace the group "controlling the size of each region") by:
    [(a[i][j][k], x[i + 1][j + 1]) in [(1, k)] + [(0, v) for v in range(nRegions) if v != k] for i in range(n) for j in range(n) for k in range(nRegions)],

    # controlling the size of each region
    [s[k] == Sum(a[:, :, k]) for k in range(nRegions)],

 after introducing: 
    a = VarArray(size=[n, n, nRegions], dom={0, 1})
 and commenting out the symmetry-breaking constraints
 while using -mini when compiling
"""
