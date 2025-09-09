"""
Hyper Sudoku differs from Sudoku by having additional constraints.
When the base of the grid is 3 (as usually for Sudoku) there are four 3-by-3 blocks in addition to the major 3-by-3 blocks
that also require exactly one entry of each numeral from 1 through 9.

The model is given below for an empty grid (no clues).

## Data
  an integer

## Model
  constraints: AllDifferent

## Execution:
  python HyperSudoku.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Sudoku
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, recreational, xcsp24
"""

from pycsp3 import *

base = data  # base of the grid
assert base >= 2
n = base * base

# x[i][j] is the value of cell with coordinates (i,j)
x = VarArray(size=[n, n], dom=range(1, n + 1))

satisfy(
    # imposing distinct values on each row and each column
    AllDifferent(x, matrix=True),

    # imposing distinct values on (main) blocks
    [AllDifferent(x[i:i + base, j:j + base]) for i in range(0, n, base) for j in range(0, n, base)],

    # imposing distinct values on shaded blocks
    [AllDifferent(x[i:i + base, j:j + base]) for i in range(1, n - base, base + 1) for j in range(1, n - base, base + 1)]
)

""" Comments
1) Data used for the 2024 Competition: [3, 4, 5, 6, 7, 8, 9, 10]
"""
