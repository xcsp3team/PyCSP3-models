"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Krzysztof Kuchcinski, and data come from the paper cited below.
The licence seems to be like a MIT Licence.

## Data Example
  057.json

## Model
  constraints: NoOverlap

## Execution
  python PerfectSquare.py -data=<datafile.json>

## Links
  - https://hal.science/hal-01245074
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  recreational, mzn21
"""

from pycsp3 import *

size, squares = data
nSquares = len(squares)

# x[i] is the x-coordinate where is put the ith square
x = VarArray(size=nSquares, dom=range(size + 1))

# y[i] is the y-coordinate where is put the ith square
y = VarArray(size=nSquares, dom=range(size + 1))

satisfy(
    # unary constraints on x
    [x[i] + squares[i] <= size for i in range(nSquares)],

    # unary constraints on y
    [y[i] + squares[i] <= size for i in range(nSquares)],

    # no overlap on boxes
    NoOverlap(origins=[(x[i], y[i]) for i in range(nSquares)], lengths=[(w, w) for w in squares])
)
