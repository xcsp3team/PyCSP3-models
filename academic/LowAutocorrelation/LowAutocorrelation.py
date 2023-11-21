"""
This is the [problem 005](https://www.csplib.org/Problems/prob005/) of the CSPLib:

These problems have many practical applications in communications and electrical engineering. The objective is to
construct a binary sequence $S_i$ of length $n$ that minimizes the autocorrelations between bits. Each bit in the sequence
takes the value +1 or -1. With non-periodic (or open) boundary conditions, the k-th autocorrelation,
$C_k$ is defined to be $\Sigma_{i=0}^{n−k−1}S_i\times S_{i+k}$. With periodic (or cyclic) boundary conditions, the k-th autocorrelation,
$C_k$ is defined to be $\Sigma_{i=0}^{n−k−1}S_i \times S_{i+k mod n}$. The aim is to minimize the sum of the squares of these autocorrelations.
That is, to minimize $\Sigma_{k=1}^{n−1}$C_k^2$.





## Data
A number n, the length of the sequence.

## Model(s)


constraints: Intension, Sum


## Command Line

python LowAutocorrelation.py
python LowAutocorrelation.py -data=16

## Tags
 academic csplib
"""

from pycsp3 import *

n = data or 8

# x[i] is the ith value of the sequence to be built.
x = VarArray(size=n, dom={-1, 1})

# y[k][i] is the ith product value required to compute the kth auto-correlation
y = VarArray(size=[n - 1, n - 1], dom=lambda k, i: {-1, 1} if i < n - k - 1 else None)

# c[k] is the value of the kth auto-correlation
c = VarArray(size=n - 1, dom=lambda k: range(-n + k + 1, n - k))

satisfy(
    [y[k][i] == x[i] * x[i + k + 1] for k in range(n - 1) for i in range(n - k - 1)],

    [Sum(y[k]) == c[k] for k in range(n - 1)]
)

minimize(
    # minimizing the sum of the squares of the auto-correlation
    Sum(c[k] * c[k] for k in range(n - 1))
)

""" Comments 
1) for the objective, c * c is possible, but parsers must be updated
"""