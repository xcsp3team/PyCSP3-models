"""
This problem is taken from Daily Telegraph and Sunday Times.
The problem is to find, for an equilateral triangular grid of size n (length of a side),
the maximum number of nodes that can be selected without having all selected corners of any equilateral triangle
of any size or orientation.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2019/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data
  an integer n

## Model
  constraints: Sum

## Execution
  python Triangular.py -data=<number>

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  academic, mzn15, mzn19, mzn22
"""

from pycsp3 import *

n = data

# x[i,j] is 1 iff the jth node in the ith row is selected
x = VarArray(size=[n, n], dom=lambda i, j: {0, 1} if i >= j else None)

satisfy(
    # avoiding the three corners of any equilateral triangle to be selected
    Sum(
        x[i + m][j],
        x[i + k][j + m],
        x[i + k - m][j + k - m]
    ) <= 2 for i in range(n) for j in range(i + 1) for k in range(1, n - i) for m in range(k)
)

maximize(
    # maximizing the number of selected nodes
    Sum(x)
)

"""
1) data used in challenges are:
   10, 16, 22, 28, 37 in 2015
   10, 17, 23, 29, 37 in 2019
   10, 18, 24, 30, 39 in 2022
"""
