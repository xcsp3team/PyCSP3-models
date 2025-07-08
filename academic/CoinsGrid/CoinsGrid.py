"""
From Tony Hurlimann, A coin puzzle, SVOR-contest 2007.

## Data
  Two integers n and c

## Model
  constraints: Sum

## Execution
  python CoinsGrid.py -data=[number,number]

## Links
  - https://link.springer.com/book/10.1007/978-3-319-25883-6
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  academic, recreational, xcsp22
"""

from pycsp3 import *

n, c = data or (8, 4)

# x[i][j] is 1 if a coin is placed at row i and column j
x = VarArray(size=[n, n], dom={0, 1})

satisfy(
    # ensuring each row sums to c
    [Sum(x[i]) == c for i in range(n)],

    # ensuring each column sums to c
    [Sum(x[:, j]) == c for j in range(n)]
)

minimize(
    Sum(
        x[i][j] * abs(i - j) ** 2 for i in range(n) for j in range(n)
    )
)

""" Comments
1) There are other variants in Hurlimann's paper (TODO)
2) Some data: (8,4) (8,5) (9,4) (10,4) (31,14)
3) one could enforce a lower-bound sum(sorted([abs(i - j) ** 2 for i in range(n) for j in range(n)])[:n*c])
   but that does not seem very interesting 
"""
