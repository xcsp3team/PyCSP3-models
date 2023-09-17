"""
This is the [problem 019](https://www.csplib.org/Problems/prob019/) of the CSPLib:

"*A magic sequence of length n is a sequence of integers $x_0...x_{n−1}$ between 0 and n−1, such that for all i in 0 to n−1,
the number i occurs exactly $x_i$ times in the sequence.*"

### Example

A magic sequence for n=10.
```
6 2 1 0 0 0 1 0 0 0
```

## Data
A number n, the size of the sequence.

## Model(s)
You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/MagicSequence/).

constraints: Cardinality, Sum

## Command Line
  python MagicSequence.py
  python MagicSequence.py -data=10

## Tags
 academic notebook

"""

from pycsp3 import *

n = data or 8

# x[i] is the ith value of the sequence
x = VarArray(size=n, dom=range(n))

satisfy(
    # each value i occurs exactly x[i] times in the sequence
    Cardinality(x, occurrences={i: x[i] for i in range(n)}),

    # tag(redundant-constraints)
    [Sum(x) == n, Sum((i - 1) * x[i] for i in range(n)) == 0]
)

""" Comments
1) Sum((i - 1) * x[i] for i in range(n)) == 0
   could be equivalently written x * range(-1, n - 1) == 0
   but range(-1, n - 1) * x == 0 is currently not possible (requires 'cursing' * for range objects)
"""