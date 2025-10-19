"""
This is [Problem 019](https://www.csplib.org/Problems/prob019/) at CSPLib.

A magic sequence of length n is a sequence of integers x between 0 and n−1, such that for all i in 0 to n−1,
the number i occurs exactly x[i] times in the sequence.


## Data
  An integer n, the size of the sequence.

## Example
  A magic sequence for n=10.
  ```
    6 2 1 0 0 0 1 0 0 0
  ```

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/MagicSequence/).

  constraints: Cardinality, Sum

## Execution
  python MagicSequence.py -data=number

## Tags
 academic, notebook, csplib
"""

from pycsp3 import *

n = data or 8

N = range(n)

# x[i] is the ith value of the sequence
x = VarArray(size=n, dom=N)

satisfy(
    # each value i occurs exactly x[i] times in the sequence
    Cardinality(
        within=x,
        occurrences={i: x[i] for i in N}
    ),

    # tag(redundant)
    [
        Sum(x) == n,
        Sum((i - 1) * x[i] for i in N) == 0
    ]
)

""" Comments
1) Sum((i - 1) * x[i] for i in range(n)) == 0
   can be equivalently written x * range(-1, n - 1) == 0  (or range(-1, n - 1) * x == 0 )
2) Note that
 occurrences=x
  is equivalent to:
 occurrences={i: x[i] for i in range(n)}
"""
