# Problem Talisman
## Description
The definition can be found in [here](https://mathworld.wolfram.com/TalismanSquare.html).

An $n\times n$ array  of the integers from 1 to n<sup>2</sup> such that the difference between any integer
and its neighbor (horizontally, vertically, or diagonally, without wrapping around)
is greater than or equal to some value k is called a (n,k)-talisman square.

### Example
A solution for the (4,2)-talisman square:
```
      1  8 11 14
      4 16  5  2
     12  9 13 10
     15  6  3  7
```
## Data
A couple \[n,k] defined above.

## Model(s)
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Intension](http://pycsp.org/documentation/constraints/Intension)

## Command Line
```
python Talisman.py
python Talisman.py -data=[5,4]
```

## Tags
 academic
 """

from pycsp3 import *

n, k = data or (4, 2)
limit = (n * (n * n + 1)) // 2

# x[i][j] is the value in the talisman square at row i and column j
x = VarArray(size=[n, n], dom=range(1, n * n + 1))

satisfy(
    # all values must be different
    AllDifferent(x),

    # the distance between two neighbouring cells must be strictly greater than k
    [
        [abs(x[i][j] - x[i][j + 1]) > k for i in range(n) for j in range(n - 1)],
        [abs(x[i][j] - x[i + 1][j]) > k for j in range(n) for i in range(n - 1)],
        [abs(dgn[i] - dgn[i + 1]) > k for dgn in diagonals_down(x) for i in range(len(dgn) - 1)],
        [abs(dgn[i] - dgn[i + 1]) > k for dgn in diagonals_up(x) for i in range(len(dgn) - 1)]
    ],

    # tag(symmetry-breaking)
    x[0][0] == 1
)
