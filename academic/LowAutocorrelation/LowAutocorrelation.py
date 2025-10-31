"""
This is [Problem 005](https://www.csplib.org/Problems/prob005/) at CSPLib.

These problems have many practical applications in communications and electrical engineering.
The objective is to construct a binary sequence length n that minimizes the autocorrelations between bits.
Each bit in the sequence takes the value +1 or -1.

## Data
  A number n, the length of the sequence.

## Model
  constraints: Sum

## Execution
  python LowAutocorrelation.py -data=number

## Links
  - https://www.csplib.org/Problems/prob005/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  academic, csplib, xcsp25
"""

from pycsp3 import *

n = data or 8

K = range(n - 1)  # note that we stop at n-1

# x[i] is the ith value of the sequence to be built.
x = VarArray(size=n, dom={-1, 1})

# y[k][i] is the ith product value required to compute the kth auto-correlation
y = VarArray(size=[n - 1, n - 1], dom=lambda k, i: {-1, 1} if i < n - k - 1 else None)

# c[k] is the value of the kth auto-correlation
c = VarArray(size=n - 1, dom=lambda k: range(-n + k + 1, n - k))

satisfy(
    [y[k][i] == x[i] * x[i + k + 1] for k in K for i in range(n - k - 1)],

    [Sum(y[k]) == c[k] for k in K]
)

minimize(
    # minimizing the sum of the squares of the auto-correlation
    Sum(c[k] * c[k] for k in K)
)

""" Comments 
1) For the objective, c * c is possible, but parsers must be updated
2) Data used for the 2025 competition are: [10, 20, 40, 60, 80, 100, 120, 150, 200, 300, 500, 800]
"""
