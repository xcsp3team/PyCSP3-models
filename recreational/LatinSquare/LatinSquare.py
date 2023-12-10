"""
A Latin square is an n × n array filled with n different symbols, each occurring exactly once in each row and exactly once in each column.

## Data Example
  qwh-030-h320.json

## Model
  constraints: AllDifferent

## Execution:
  python LatinSquare.py -data=[number,null]
  python LatinSquare.py -data=<datafile.json>

## Links
 - https://en.wikipedia.org/wiki/Latin_square

## Tags
  recreational
"""

from pycsp3 import *

n, clues = data  # if not -1, clues[i][j] is a value imposed at row i and col j

# x[i][j] is the value at row i and col j of the Latin Square
x = VarArray(size=[n, n], dom=range(n))

satisfy(
    AllDifferent(x, matrix=True),

    # tag(clues)
    [x[i][j] == clues[i][j] for i in range(n) for j in range(n) if clues and clues[i][j] != -1]
)
