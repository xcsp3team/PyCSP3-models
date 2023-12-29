"""
The feasibility problem consists of m 0-1 equality knapsack constraints defined on the same set of 10(m−1) variables.

## Data Example
  04.json

## Model
  constraints: Sum

## Execution:
  python MarketSplit.py -data=<datafile.json>

## Links
  - https://pubsonline.informs.org/doi/abs/10.1287/ijoc.11.2.205?journalCode=ijoc
  - https://link.springer.com/chapter/10.1007/3-540-69346-7_22

## Tags
  recreational
"""

from pycsp3 import *

n, constraints = data

x = VarArray(size=n, dom={0, 1})

satisfy(
    x * coeffs == k for (coeffs, k) in constraints
)
