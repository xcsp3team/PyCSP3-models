"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
The model was created by Hakan Kjellerstrand.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  an integer n

## Model
  constraints: AllDifferent, Element

## Execution
  python Quasigroup7.py -data=<integer>

## Links
  - https://www.csplib.org/Problems/prob003/
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  academic, csplib, mzn08
"""

from pycsp3 import *

n = data or 8

# x[i][j] is the value at row i and column j of the quasi-group
x = VarArray(size=[n, n], dom=range(n))

satisfy(
    # all rows must be different
    [AllDifferent(x[i]) for i in range(n)],

    # all columns must be different
    [AllDifferent(x[:, j]) for j in range(n)],

    # ensuring idempotence  tag(idempotence)
    [x[i][i] == i for i in range(n)],

    [x[i, x[j][i]] == x[x[j][i], j] for i in range(n) for j in range(n)],

    [x[i][-1] + 2 >= i for i in range(n)]
)

"""
1) data used in 2008 are: 5, 6, 7, 8, 9, 10, 11, 12, 13, 14
"""
