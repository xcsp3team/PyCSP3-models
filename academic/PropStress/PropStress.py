"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  An integer n

## Execution
  python PropStress.py -data=number

## Links
  - https://www.minizinc.org/challenge2009/results2009.html

## Tags
  academic, mzn09
"""

from pycsp3 import *

n = data or 10  # number of iterations of change per loop
k = n  # number of times round the loop
m = n  # m^2 propagators per change of loop

x = VarArray(size=m + 1, dom=range(k * n + 1))

y = VarArray(size=n + 1, dom=range(k * n + 1))

satisfy(
    [y[i - 1] - y[i] <= 0 for i in range(2, n + 1)],

    [y[0] - y[i] <= n - i + 1 for i in range(1, n + 1)],

    y[n] - x[0] <= 0,

    [x[i] - x[j] <= 0 for i, j in combinations(m + 1, 2)],

    x[m] - y[0] <= -2
)

""" Comments
1) data used in 2009 are: 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000
"""
