"""
This is [Problem 110](https://www.csplib.org/Problems/prob110/) at CSPLib.

In the “Armies of queens” problem, we are required to place two equal-sized armies of black and white queens on a chessboard
so that the white queens do not attack the black queens (and necessarily vice versa) and to find the maximum size of two such armies.

## Example
  The optimum for a chessboard of size 8 is 9.
  A possible solution is
  ```
    W . . W W W . .
    . . . . W W . .
    W . . . . . . .
    W . . W . . . .
    . . . . . . B .
    . . . . . . B B
    . B B . . . . B
    . B B . . . B .
  ```

## Data
  A number n, the size of the chessboard

## Model
  There are two variants "m1" and "m2"

  constraints: Count, Sum

## Execution
  - python PeacableArmies.py -data=number -variant=m1
  - python PeacableArmies.py -data=number -variant=m2

## Tags
  academic, csplib
"""

from pycsp3 import *

n = data or 6

if variant("m1"):

    def less_equal(i1, j1, i2, j2):
        if (i1, j1) == (i2, j2):
            return b[i1][j1] + w[i1][j1] <= 1
        if i1 < i2 or (i1 == i2 and j1 < j2):
            if i1 == i2 or j1 == j2 or abs(i1 - i2) == abs(j1 - j2):  # maybe we can simplify something here
                return b[i1][j1] + w[i2][j2] <= 1, w[i1][j1] + b[i2][j2] <= 1


    # b[i][j] is 1 if a black queen is in the cell at row i and column j
    b = VarArray(size=[n, n], dom={0, 1})

    # w[i][j] is 1 if a white queen is in the cell at row i and column j
    w = VarArray(size=[n, n], dom={0, 1})

    satisfy(
        # no two opponent queens can attack each other
        [less_equal(i1, j1, i2, j2) for (i1, j1, i2, j2) in product(range(n), repeat=4)],

        # ensuring the same numbers of black and white queens
        Sum(b) == Sum(w)
    )

    maximize(
        # maximizing the number of black queens (and consequently, the size of the armies)
        Sum(b)
    )

if variant("m2"):

    def different(i1, j1, i2, j2):
        if i1 < i2 or (i1 == i2 and j1 < j2):
            if i1 == i2 or j1 == j2 or abs(i1 - i2) == abs(j1 - j2):
                return x[i1][j1] + x[i2][j2] != 3


    # x[i][j] is 1 (resp., 2), if a black (resp., white) queen is in the cell at row i and column j. It is 0 otherwise.
    x = VarArray(size=[n, n], dom={0, 1, 2})

    # nb is the number of black queens
    nb = Var(dom=range(n * n // 2))

    # nw is the number of white queens
    nw = Var(dom=range(n * n // 2))

    satisfy(
        # no two opponent queens can attack each other
        [different(i1, j1, i2, j2) for (i1, j1, i2, j2) in product(range(n), repeat=4)],

        # counting the number of black queens
        Count(x, value=1) == nb,

        # counting the number of white queens
        Count(x, value=2) == nw,

        # ensuring equal-sized armies
        nb == nw
    )

    maximize(
        # maximizing the number of black queens (and consequently, the size of the armies)
        nb
    )
