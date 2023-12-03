"""
This is [Problem 017](https://www.csplib.org/Problems/prob017/) at CSPLib.

The edges of a complete graph (with n nodes) must be coloured with the minimum number of colours.
There must be no monochromatic triangle in the graph, i.e. in any triangle at most two edges have the same colour.
With 3 colours, the problem has a solution if n < 17.

## Data
  A number n, the number of nodes of the graph.

## Model
  constraints: Maximum, NValues

## Execution
  - python Ramsey.py -data=number

## Tags
  academic, csplib
"""

from pycsp3 import *

n = data or 8

# x[i][j] is the color of the edge between nodes i and j
x = VarArray(size=[n, n], dom=lambda i, j: range((n * (n - 1)) // 2) if i < j else None)

satisfy(
    # no monochromatic triangle in the graph
    NValues(x[i][j], x[i][k], x[j][k]) > 1 for (i, j, k) in combinations(n, 3)
)

minimize(
    Maximum(x)
)
