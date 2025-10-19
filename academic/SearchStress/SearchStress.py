"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data
  Two integers n and k

## Execution
  python SearchStress.py -data=[number,number]

## Links
  - https://www.minizinc.org/challenge/2008/results/

## Tags
  academic, mzn08
"""

from pycsp3 import *

n, k = data or (8, 8)  # number of copies (of the graph) in sequence, and size of each subgraph (and number of colors)

N, K = range(n), range(1, k)

# x[i] is the color of the ith node
x = VarArray(size=[n * k + 1], dom=range(k))

satisfy(
    [x[i * k] != x[i * k + j] for i in N for j in K],

    [x[(i + 1) * k] != x[i * k + j] for i in N for j in K],

    [x[i * k + j1] != x[i * k + j2] for i in N for j1, j2 in combinations(K, 2)],

    x[0] != x[-1]
)

""" Comments
1) Data used in 2008 are: (4,4), (8,4), (8,8)
"""
