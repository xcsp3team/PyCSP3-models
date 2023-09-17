"""
You can see below, the beginning of the description provided by  [wikipedia](https://en.wikipedia.org/wiki/Graeco-Latin_square).

"*A Latin square of order n is an n by n array filled with n different symbols (for example, values between 1 and n),
each occurring exactly once in each row and exactly once in each column.
Two latin squares of the same order n are orthogonal if each pair of elements in the same position occurs exactly once.
The most easy way to see this is by concatenating elements in the same position and verify that no pair appears twice.*"

### Example

A solution for n=5:
```
[0, 1, 2, 3, 4]          [0, 1, 2, 3, 4]
[4, 2, 3, 0, 1]          [3, 4, 1, 2, 0]
[3, 4, 1, 2, 0]          [4, 2, 3, 0, 1]
[1, 3, 0, 4, 2]          [2, 0, 4, 1, 3]
[2, 0, 4, 1, 3]          [1, 3, 0, 4, 2]
```

## Data
A number n, the size of the square.

## Model(s)
constraints: AllDifferent, AllDifferentMatrix, Extension



## Command Line


```shell
  python Ortholatin.py
  python Ortholatin.py -data=7
 ```
"""

from pycsp3 import *

n = data or 5

# x is the first Latin square
x = VarArray(size=[n, n], dom=range(n))

# y is the second Latin square
y = VarArray(size=[n, n], dom=range(n))

# z is the matrix used to control orthogonality
z = VarArray(size=[n * n], dom=range(n * n))

table = {(i, j, i * n + j) for i in range(n) for j in range(n)}

satisfy(
    # ensuring that x is a Latin square
    AllDifferent(x, matrix=True),

    # ensuring that y is a Latin square
    AllDifferent(y, matrix=True),

    # ensuring that values on diagonals are different  tag(diagonals)
    [AllDifferent(t) for t in [diagonal_down(x), diagonal_up(x), diagonal_down(y), diagonal_up(y)]],

    # ensuring orthogonality of x and y through z
    AllDifferent(z),

    # computing z from x and y
    [(x[i][j], y[i][j], z[i * n + j]) in table for i in range(n) for j in range(n)],

    # tag(symmetry-breaking)
    [(x[0][j] == j, y[0][j] == j) for j in range(n)]
)

""" Comments
1) Note that a less compact way of posting symmetry_breaking constraints is:
 # tag(symmetry-breaking)
 [[x[0][j] == j for j in range(n)], [y[0][j] == j for j in range(n)]],
"""