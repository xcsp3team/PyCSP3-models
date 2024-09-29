"""
On a square grid of size n × n, all numbers ranging from 1 to n*n must be put so that the numbers surrounding each number add to a multiple of that number.

## Data
  A unique integer n

## Model
  constraints: AllDifferent, Sum

## Execution
  python AnotherMagicSquare.py -data=number

## Links
  - http://benvitale-funwithnum3ers.blogspot.com/2010/12/another-kind-of-magic-square.html
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

n = data or 3

# x[i][j] is the value at row i and column j
x = VarArray(size=[n, n], dom=range(1, n * n + 1))

satisfy(
    AllDifferent(x),

    # ensuring that the numbers surrounding a number v add to a multiple of v
    [Sum(x.around(i, j)) % x[i][j] == 0 for i in range(n) for j in range(n)]
)

""" Comments
1) There are 0, 8 and 0 solutions for n = 2, 3 and 4
2) For being compatible with the competition mini-track, we use:
   # y[i,j] is the multiple used for the cell at row i and column j
   y = VarArray(size=[n, n], dom=range(1, 8*(n * n) + 1))

   # ensuring that the numbers surrounding a number v add to a multiple of v
   [Sum(x.around(i, j)) == x[i][j] * y[i][j] for i in range(n) for j in range(n)]
"""
