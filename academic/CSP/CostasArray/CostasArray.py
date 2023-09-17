"""
This is the [problem 076](https://www.csplib.org/Problems/prob076/) of the CSPLib and a [NumberJack](https://github.com/eomahony/Numberjack) example.
A costas array is a pattern of n marks on an n∗n grid, one mark per row and one per column, in which the n∗(n−1)/2
vectors between the marks are all-different.

### Example

An example of a solution for n=7 is:
```
   4  3  6  2  0  7  1  5
```

## Data
a number n, the size of the grid.

## Model(s)

constraints: AllDifferent, Intension


## Command Line


python CostasArrays.py
python CostasArrays.py -data=10

## Tags
 academic
"""

from pycsp3 import *

n = data or 8

# x[i] is the row where is put the ith mark (on the ith column)
x = VarArray(size=n, dom=range(n))

satisfy(
    # all marks are on different rows (and columns)
    AllDifferent(x),

    # all displacement vectors between the marks must be different
    [AllDifferent(x[i] - x[i + d] for i in range(n - d)) for d in range(1, n - 1)]
)

""" Comments
1) how to break all symmetries?  x[0] <= math.ceil(n / 2), x[0] < x[-1], ... ? TODO
"""
