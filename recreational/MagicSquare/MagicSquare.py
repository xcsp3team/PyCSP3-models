"""
A mathematical puzzle.

## Data Example
  example01.json

## Model
  constraints: AllDifferent, Sum

## Execution:
  python MagicSquare.py -data=[number,null]
  python MagicSquare.py -data=<datafile.json>
  python MagicSquare.py -data=<datafile.txt>x -parser=MagicSquare_Parser.py

## Links
 - https://en.wikipedia.org/wiki/Magic_square

## Tags
  recreational
"""

from pycsp3 import *

n, clues = data
magic = n * (n * n + 1) // 2

# x[i][j] is the value at row i and column j of the magic square
x = VarArray(size=[n, n], dom=range(1, n * n + 1))

satisfy(
    # all values must be different
    AllDifferent(x),

    # ensuring the magic value for each row
    [Sum(row) == magic for row in x],

    # ensuring the magic value for each column
    [Sum(col) == magic for col in columns(x)],

    # ensuring the magic value for each diagonal  tag(diagonals)
    [Sum(dgn) == magic for dgn in [diagonal_down(x), diagonal_up(x)]],

    # respecting specified clues (if any)  tag(clues)
    [x[i][j] == clues[i][j] for i in range(n) for j in range(n) if clues and clues[i][j] != 0]
)
