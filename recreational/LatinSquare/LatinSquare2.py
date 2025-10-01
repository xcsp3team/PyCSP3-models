"""
A Latin square is an n × n array filled with n different symbols, each occurring exactly once in each row and exactly once in each column.

## Data Example
  7-2-0.json

## Model
  constraints: AllDifferent

## Execution:
  python LatinSquare.py -data=<datafile.json>

## Links
 - https://en.wikipedia.org/wiki/Latin_square

## Tags
  recreational
"""

from pycsp3 import *

n, clues = data or load_json_data("7-2-0.json")  # clues are given by tuples of the form (row, col, value)

# x[i][j] is the value at row i and col j of the Latin Square
x = VarArray(size=[n, n], dom=range(n))

satisfy(
    AllDifferent(x, matrix=True),

    # tag(clues)
    [x[i][j] == v for (i, j, v) in clues] if clues else None,

    # tag(diagonals)
    [AllDifferent(dgn) for dgn in diagonals_down(x, broken=True) + diagonals_up(x, broken=True)]
)
