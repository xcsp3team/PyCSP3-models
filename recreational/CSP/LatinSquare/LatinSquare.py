"""
Wikipedia definition: a Latin square is an n × n array filled with n different symbols, each occurring exactly once in each row and exactly once in each column.

## Data
 TODO

## Model
 constraints: AllDifferent

## Execution:
  python3 LatinSquare.py -data=[8,-1]
  python3 LatinSquare.py -data=LatinSquare_qwh-o030-h320.json

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
