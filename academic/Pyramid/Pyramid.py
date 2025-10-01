"""
Build a pyramid such as each brick of the pyramid is the sum of the two bricks situated below it.
Minimize the root value (0 not permitted) while using different values

## Data
  Two integers n and k

## Model
  constraints: AllDifferent

## Execution
  python Pyramid.py -data=[number,number]

## Links
  - http://www.rosettacode.org/wiki/Pyramid_of_numbers
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, xcsp24
"""

from pycsp3 import *

n, k = data or (7, 500)

# x[o,p] is the value of A(o,p)
x = VarArray(size=[n, n], dom=lambda i, j: range(k + 1) if j <= i else None)

satisfy(
    # imposing a non-null root
    x[0][0] != 0,

    # imposing different values
    AllDifferent(x),

    # computing triangle sums
    [x[i][j] == x[i + 1][j] + x[i + 1][j + 1] for i in range(n - 1) for j in range(i + 1)]
)

minimize(
    # minimizing the root value of the triangle
    x[0][0]
)

""" Comments
1) Data used for the 2024 Competition:  [(7,500), (8,800), (9,1300), (10,2500), (11,5000), (12,10000), (13,20000), (14,45000), (15,80000), (16,200000)]
"""
