"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Hakan Kjellerstrand (optimization version of the problem, following idea by Mikael Zayenz Lagerkvist).
MIT Licence.

## Data Example
  p20.json

## Model
  constraints: AllDifferent, Sum

## Execution
  python SudokuOpt.py -data=<datafile.json>
  python SudokuOpt.py -data=<datafile.dzn> -parser=SudokuOpt_ParserZ.py

## Links
  - http://www.hakank.org/minizinc/sudoku_problems2/
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  recreational, mzn22
"""

import math

from pycsp3 import *

n, clues = data  # n (order of the grid) is typically 9 -- if not 0, clues[i][j] is a value imposed at row i and col j
base = int(math.sqrt(n))
assert base * base == n

# x[i][j] is the value of cell with coordinates (i,j)
x = VarArray(size=[n, n], dom=range(1, n + 1))

satisfy(
    # imposing distinct values on each row and each column
    AllDifferent(x, matrix=True),

    # imposing distinct values on each block  tag(blocks)
    [AllDifferent(x[i:i + base, j:j + base]) for i in range(0, n, base) for j in range(0, n, base)],

    # imposing clues  tag(clues)
    [x[i][j] == clues[i][j] for i in range(n) for j in range(n) if clues and clues[i][j] > 0]
)

minimize(
    Sum(x[i][j] * ((-1) ** (i + j)) for i in range(n) for j in range(n))
)
