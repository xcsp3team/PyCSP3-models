"""
This is the [problem 049](https://www.csplib.org/Problems/prob049/) of the CSPLib:

This problem consists in finding a partition of numbers 1...n  into two sets A and B such that:
 - A and B have the same cardinality
 - sum of numbers in A = sum of numbers in B
 - sum of squares of numbers in A = sum of squares of numbers in B

### Example

A solution for n=8 : A = {1, 4, 6, 7} and B = {2,3,5,7}

## Data
A number n.

## Model(s)
constraints: AllDifferent, Increasing, Intension, Sum

## Command Line
  python NumberPartitioning.py
  python NumberPartitioning.py -data=10

## Tags
 academic
"""

from pycsp3 import *

n = data or 8
assert n % 2 == 0, "The value of n must be even"

# x[i] is the ith value of the first set
x = VarArray(size=n // 2, dom=range(1, n + 1))

# y[i] is the ith value of the second set
y = VarArray(size=n // 2, dom=range(1, n + 1))

satisfy(
    AllDifferent(x + y),

    # tag(power1)
    [
        Sum(x) == n * (n + 1) // 4,
        Sum(y) == n * (n + 1) // 4
    ],

    # tag(power2)
    [
        Sum(x[i] * x[i] for i in range(n // 2)) == n * (n + 1) * (2 * n + 1) // 12,
        Sum(y[i] * y[i] for i in range(n // 2)) == n * (n + 1) * (2 * n + 1) // 12
    ],

    # tag(symmetry-breaking)
    [
        x[0] == 1,
        Increasing(x, strict=True),
        Increasing(y, strict=True)
    ]
)
