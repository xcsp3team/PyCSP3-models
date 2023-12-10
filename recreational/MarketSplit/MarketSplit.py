"""
See "A Class of Hard Small 0-1 Programs" by Gérard Cornuéjols and Milind Dawande, INFORMS J. Comput. 11(2): 205-210 (1999)

The feasibility problem consists of m 0-1 equality knapsack constraints defined on the same set of 10(m−1) variables.


## Data Example
  04.json

## Model
  constraints: Sum

## Execution:
  python MarketSplit.py -data=<datafile.json>

## Tags
  recreational
"""

from pycsp3 import *

n, constraints = data

x = VarArray(size=n, dom={0, 1})

satisfy(
    x * coeffs == k for (coeffs, k) in constraints
)
