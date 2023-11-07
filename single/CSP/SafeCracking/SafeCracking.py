"""
From the Oz Primer.

The code of Professor Smart's safe is a sequence of 9 distinct
nonzero digits d1 .. d9 such that the following equations and
inequations are satisfied:

       d4 - d6   =   d7
  d1 * d2 * d3   =   d8 + d9
  d2 + d3 + d6   <   d8
            d9   <   d8
  d1 <> 1, d2 <> 2, ..., d9 <> 9

Can you find the correct combination?

## Data
all integrated (single instance)

## Model
  constraints: AllDifferent

## Execution
  python3 SafeCracking.py

## Links
 -  http://www.comp.nus.edu.sg/~henz/projects/puzzles/digits/index.html

## Tags
  single
"""

from pycsp3 import *

# x[i] is the i(+1)th digit
x = VarArray(size=9, dom=lambda i: {v for v in range(1, 10) if v != i + 1})

satisfy(
    AllDifferent(x),
    x[3] - x[5] == x[6],
    x[0] * x[1] * x[2] == x[7] + x[8],
    x[1] + x[2] + x[5] < x[7],
    x[8] < x[7]
)
