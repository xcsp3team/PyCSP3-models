"""
The rectangle (square) packing problem consists of n squares of size 1x1, 2x2, 3x3, ..., nxn,
to be put in an enclosing rectangle (container) without overlapping of the squares.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2014 Minizinc challenges.
The MZN model has Copyright (C) 2009-2014 The University of Melbourne and NICTA.

## Data
  Two integers (n,k)

## Model
  constraints: Cumulative, NoOverlap

## Execution
  python RectPacking_z.py -data=[number,number]

## Links
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  academic, mzn09, mzn14
"""

from pycsp3 import *
from math import floor, ceil, sqrt

n, including_square1 = data

max_width = sum(i for i in range(1, n + 1) if i >= (n // 2) + 1)
min_height = n if n % 2 == 1 else n + 1
min_area = sum(i * i for i in range(1, n + 1))
max_area = max_width * min_height
max_height = floor(sqrt(max_area))
min_width = ceil(sqrt(min_area))

starting_square = 1 if including_square1 == 1 else 2
squares = range(starting_square, n + 1)

gaps = [0, 2, 3, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10]


def forbidden_gaps(axis, c, limit, max_value):
    bl = VarArray(size=n, dom=lambda i: {0, 1} if i + 1 >= starting_square else None, id="bl" + axis)
    br = VarArray(size=n, dom=lambda i: {0, 1} if i + 1 >= starting_square and 2 * gaps[i] + 2 <= max_value - (i + 1) else None, id="br" + axis)

    return [
        (
            If(
                bl[i - 1],
                Then=c[i - 1] <= 0,
                Else=c[i - 1] > gaps[i - 1]
            ),
            If(
                br[i - 1],
                Then=c[i - 1] >= limit - i,
                Else=c[i - 1] < limit - i - gaps[i - 1]
            ),
            either(
                bl[i - 1] == 0,
                br[i - 1] == 0
            )
        ) if 2 * gaps[i - 1] + 2 <= max_value - i else
        (
            If(
                bl[i - 1],
                Then=c[i - 1] <= 0,
                Else=c[i - 1] >= limit - i
            )
        ) for i in squares
    ]


# x[i] is the x-coordinate of the ith square (left lower corner)
x = VarArray(size=n, dom=range(max_width + 1))

# y[i] is the y-coordinate of the ith square (left lower corner)
y = VarArray(size=n, dom=range(max_height + 1))

# the width of the rectangle
w = Var(dom=range(min_width, max_width + 1))

# the height of the rectangle
h = Var(dom=range(min_height, max_height + 1))

# the area of the rectangle
a = Var(dom=range(min_area, max_area + 1))

satisfy(
    # preventing squares to overlap
    NoOverlap(
        origins=[(x[i - 1], y[i - 1]) for i in squares],
        lengths=[(i, i) for i in squares]
    ),

    # constraining the container (bounding rectangle)
    [
        h <= w,
        a == h * w
    ],

    # squares must be inside the rectangle
    (
        (
            x[i - 1] + i <= w,
            y[i - 1] + i <= h
        ) for i in squares
    ),

    # ensuring a non-overload wrt rectangle height
    Cumulative(
        tasks=[Task(origin=x[i - 1], length=i, height=i) for i in squares]
    ) <= h,

    # ensuring a non-overload wrt rectangle width
    Cumulative(
        tasks=[Task(origin=y[i - 1], length=i, height=i) for i in squares]
    ) <= w,

    # when the unit square is not considered, its origin is assigned to (0, 0)
    [
        x[0] == 0,
        y[0] == 0
    ] if including_square1 == 0 else None,

    # tag(symmetry-breaking)
    [
        2 * x[-1] <= w - n,
        2 * y[-1] <= h - n
    ],

    # forbidden gaps wrt width
    forbidden_gaps("x", x, w, max_width),

    # forbidden gaps wrt height
    forbidden_gaps("y", y, h, max_height)
)

""" Comments
1) Data used in challenges are:
  (5,1),(9,0),(12,1),(14,0),(15,1),(19,0),(22,1),(24,0) for 2009
  (18,1), (21,0), (22,0), (23,0), (26,0) for 2014
2) Note that in 2009, the NoOverlap constraints (diffn) were decomposed
3) Note that we need to specify the id of the arrays defined locally to a function.
 Otherwise, this would be the same ids.
"""
