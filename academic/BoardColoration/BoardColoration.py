"""
All squares of a board of a specified size (specified numbers of rows and columns) must be colored with the minimum number of colors.
The four corners of any rectangle inside the board must not be assigned the same color.

### Example
  A solution for 6 rows and 5 columns.
  ```
    0 0 0 0 0
    0 1 1 1 1
    0 1 2 2 2
    1 2 0 1 2
    1 2 0 2 1
    2 2 2 0 1
  ```

## Data
  a pair of numbers: the number of rows (n) and the number of columns (m)

## Model
  You can find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/COP/BoardColoration/).

  constraints: Maximum, NValues, Lex

## Execution
  python BoardColoration.py -data=[number,number]

## Tags
  academic, notebook
"""

from pycsp3 import *

n, m = data or (6, 5)

# x[i][j] is the color at row i and column j
x = VarArray(size=[n, m], dom=range(n * m))

satisfy(
    # at least two corners of different colors for any rectangle inside the board
    [
        NotAllEqual(
            x[i1][j1], x[i1][j2], x[i2][j1], x[i2][j2]
        ) for i1, i2 in combinations(n, 2) for j1, j2 in combinations(m, 2)
    ],

    # tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)
)

minimize(
    # minimizing the greatest used color index (and, consequently, the number of colors)
    Maximum(x)
)
