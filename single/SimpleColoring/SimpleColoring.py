"""
A simple coloring problem

## Data
  all integrated (single problem)

## Execution
  python SimpleColoring.py

## Tags
  single
"""
from pycsp3 import *

n = 4

x = VarArray(size=n, dom={"r", "g", "b"})

satisfy(
    x[i] != x[j] for i, j in combinations(n, 2)
)
