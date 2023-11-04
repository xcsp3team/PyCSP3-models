"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2008 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  an integer n

## Execution
  python SlowConvergence.py -data=[number]

## Links
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  academic, mzn08
"""

from pycsp3 import *

n = data

y = VarArray(size=n + 1, dom=range(10 * n + 1))

x = VarArray(size=n + 1, dom=range(10 * n + 1))

satisfy(
    [y[i - 1] - y[i] <= 0 for i in range(2, n + 1)],

    [y[0] - y[i] <= n - i + 1 for i in range(1, n + 1)],

    y[-1] - x[0] <= 0,

    [x[i] - x[j] <= 0 for i in range(1, n) for j in range(i + 1, n + 1)],

    y[0] >= n
)

"""
1) data used in 2008 are: 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000
"""
