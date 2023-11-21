"""
Problem 041 on CSPLib

## Data
all integrated (single instance)

## Model
  constraints: AllDifferent

## Execution
  python3 NFractions.py

## Links
 - https://www.csplib.org/Problems/prob041/

## Tags
  single, csplib

"""

from pycsp3 import *

digits = VarArray(size=9, dom=range(1, 10))
a, b, c, d, e, f, g, h, i = digits

satisfy(
    AllDifferent(digits),

    a * (10 * e + f) * (10 * h + i) + d * (10 * b + c) * (10 * h + i) + g * (10 * b + c) * (10 * e * f) == (10 * b + c) * (10 * e + f) * (10 * h + i)
)
