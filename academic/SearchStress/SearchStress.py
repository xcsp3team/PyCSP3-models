"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  Two integers n and k

## Execution
  python SearchStress.py -data=[number,number]

## Links
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  academic, mzn08
"""

from pycsp3 import *

n, k = data  # number of copies (of the graph) in sequence, and size of each subgraph (and number of colors)

# x[i] is the color of the ith node
x = VarArray(size=[n * k + 1], dom=range(k))

satisfy(
    [x[i * k] != x[i * k + j] for i in range(n) for j in range(1, k)],
    [x[(i + 1) * k] != x[i * k + j] for i in range(n) for j in range(1, k)],
    [x[i * k + j1] != x[i * k + j2] for i in range(n) for j1 in range(1, k) for j2 in range(j1 + 1, k)],

    x[0] != x[-1]
)

""" Comments
1) Data used in 2008 are: (4,4), (8,4), (8,8)
"""
