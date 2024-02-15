"""
This is [Problem 054](https://www.csplib.org/Problems/prob054/) at CSPLib.

Can n queens (of the same colour) be placed on a n×n chessboard so that none of the queens can attack each other?

## Example
  A solution for n=8
 ![Queens](http://pycsp.org/assets/notebooks/figures/queens.png)

## Data
  A number n, the size of the board.

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Queens/).

  There are 3 variants of this problem, one with AllDifferent constraints, the other ones with constraint in intension.

  constraints: AllDifferent

## Execution
  - python Queens.py -data=number
  - python Queens.py -data=number -variant=v1
  - python Queens.py -data=number -variant=v2

## Tags
  academic, notebook, csplib
"""

from pycsp3 import *

n = data or 8

# q[i] is the column where is put the ith queen (at row i)
q = VarArray(size=n, dom=range(n))

if not variant():
    satisfy(
        AllDifferent(q),

        # controlling no two queens on the same upward diagonal
        AllDifferent(q[i] + i for i in range(n)),

        # controlling no two queens on the same downward diagonal
        AllDifferent(q[i] - i for i in range(n))
    )
elif variant("v1"):
    satisfy(
        AllDifferent(q),

        [abs(q[i] - q[j]) != j - i for i, j in combinations(n, 2)]
    )

elif variant("v2"):
    satisfy(
        both(q[i] != q[j], abs(q[i] - q[j]) != j - i) for i, j in combinations(n, 2)
    )
