"""
Hidato, also known as Hidoku is a logic puzzle game invented by Gyora M. Benedek, an Israeli mathematician.
The goal of Hidato is to fill the grid with consecutive numbers that connect horizontally, vertically, or diagonally.

## Data Example
  p1.json

## Model
  Two variants handle differently consecutive numbers:
  - a main variant involving logical (and Count) constraints
  - a variant 'table' involving table constraints

  constraints: AllDifferent, Count, Table

## Execution
  python Hidato.py -data=<datafile.json>
  python Hidato.py -data=<datafile.json> -variant=table
  python Hidato.py -data=[number,number,null] -variant=table

## Links
  - https://en.wikipedia.org/wiki/Hidato
  - http://www.hidato.com/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
"""

from pycsp3 import *

n, m, clues = data  # clues are given by strictly positive values

Cells = [(i, j) for i in range(n) for j in range(m)]

# x[i][j] is the value in the grid at row i and column j
x = VarArray(size=[n, m], dom=range(1, n * m + 1))

satisfy(
    # all values must be different
    AllDifferent(x),

    # respecting clues
    [x[i][j] == clues[i][j] for i, j in Cells if clues and clues[i][j] > 0]
)

if not variant():
    satisfy(
        # ensuring adjacent consecutive numbers
        If(
            x[i][j] != n * m,
            Then=ExactlyOne(
                within=x.around(i, j),
                value=x[i][j] + 1
            )
        ) for i, j in Cells
    )

elif variant('table'):
    def T(i, j):
        corners = {(0, 0), (0, m - 1), (n - 1, 0), (n - 1, m - 1)}
        r = 3 if (i, j) in corners else 5 if i in (0, n - 1) or j in (0, m - 1) else 8
        return [(v, *[v + 1 if l == k else ANY for l in range(r)]) for v in range(1, n * m) for k in range(r)] + [(n * m, *[ANY] * r)]


    satisfy(
        # ensuring adjacent consecutive numbers
        (x[i][j], x.around(i, j)) in T(i, j) for i, j in Cells
    )
