"""
From the IBM Challenge "Ponder This".

There are people living in the separate squares of a rectangular grid.
Each resident's neighbours are those who live in the squares that have a common edge with that resident's square.
Each resident of the grid is assigned a natural number k in the range 1..5
with the condition that the numbers 1, 2, ..., k-1 are present in the squares of his/her neighbors.
Find a configuration (assignment of numbers) of all neighbours, so that the sum of their numbers are maximised.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The original MZN model was proposed by Peter J. Stuckey, with a Licence that sems to be like a MIT Licence.

## Data
  two integers (n,m)

## Model
  There are two variants:
    - a main one with intensional constraints,
    - a 'table" variant with extensional constraints

  Constraints: Count, Lex, Sum, Table

## Execution
  python Neighbours.py -data=[number,number]

## Links
  - https://research.ibm.com/haifa/ponderthis/challenges/December2012.html
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn18, mzn21
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry, TypeRectangleSymmetry

n, m = data  # number of rows and number of columns

symmetries = [sym.apply_on(n) for sym in TypeSquareSymmetry] if n == m else [sym.apply_on(n, m) for sym in TypeRectangleSymmetry]


def domain_x(i, j):
    if i in {0, n - 1} and j in {0, m - 1}:  # the four corners
        return range(1, 4)
    if i in {0, n - 1} or j in {0, m - 1}:  # the extreme lines or columns (border of the rectangle) without corners
        return range(1, 5)
    return range(1, 6)


# x[i][j] is the value in the grid at coordinates (i,j)
x = VarArray(size=[n, m], dom=domain_x)

if not variant():
    satisfy(
        # ensuring valid neighbours
        If(
            x[i][j] >= k,
            Then=Exist(x.beside(i, j), value=k - 1)
        ) for i in range(n) for j in range(m) for k in range(2, 6)
    )

elif variant("table"):
    def T(i, j):
        r = len(x.cross(i, j))
        t = [(1, *[ANY] * (r - 1))] + [(2, *[1 if j == i else ANY for j in range(r - 1)]) for i in range(r - 1)] + \
            [(3, *[1 if j == i1 else 2 if j == i2 else ANY for j in range(r - 1)]) for i1, i2 in product(range(r - 1), repeat=2) if i1 != i2]
        if r >= 4:
            t.extend(
                (4, *[1 if j == i1 else 2 if j == i2 else 3 if j == i3 else ANY for j in range(r - 1)]) for i1, i2, i3 in product(range(r - 1), repeat=3)
                if different_values(i1, i2, i3))
        if r == 5:
            t.extend((5, *perm) for perm in permutations(range(1, r), r - 1))
        return t


    satisfy(
        # ensuring valid neighbours
        x.cross(i, j) in T(i, j) for i in range(n) for j in range(m)
    )

satisfy(
    # tag(symmetry-breaking)
    LexIncreasing(x, x[symmetry]) for symmetry in symmetries
)

maximize(
    Sum(x)
)

""" Comments
1) data used in challenges are:
 2018: (5,5), (4,7), (7,8), (6,6), (9,4)
 2021: (9,14), (40,50), (20,19), (4,4), (4,9)
2) note that:
 Exist(y == k - 1 for y in x.beside(i, j))
  is an alternative to:
 Exist(x.beside(i, j), value= k - 1)
"""
