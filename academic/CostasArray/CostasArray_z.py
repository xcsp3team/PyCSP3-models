"""
An order-n Costas array is a permutation on {1,...,n} such that the distances in each row of the triangular difference table are distinct.
For example, the permutation {1,3,4,2,5} has triangular difference table {2,1,-2,3}, {3,-1,1}, {1,2}, and {4}.
Since each row contains no duplications, the permutation is therefore a Costas array.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011/2015 Minizinc challenges.
The MZN model was proposed by Barry O'Sullivan (Cork Constraint Computation Centre, Ireland).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  A number n

## Model
  constraints: AllDifferent

## Execution
  python CostasArray_z.py -data=number

## Links
  - https://mathworld.wolfram.com/CostasArray.html
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  academic, mzn10, mzn11, mzn15
"""
from pycsp3 import *

n = data

# x[i] is the ith value of the Costas array
x = VarArray(size=n, dom=range(1, n + 1))

# y[i] is the triangular difference table on row i
y = VarArray(size=[n, n], dom=lambda i, j: range(-n + 1, n) if i < j else None)

satisfy(
    # ensuring a permutation
    AllDifferent(x),

    # computing differences
    [y[i][j] == x[j] - x[j - i - 1] for i, j in combinations(n, 2)],

    # ensuring distinct distances on each row
    [AllDifferent(y[i]) for i in range(n - 1)],

    # tag(symmetry-breaking)
    x[0] < x[-1],

    #  tag(redundant-constraints)
    [
        [y[i][j] != 0 for i, j in combinations(n, 2)],  # not possible to have 0

        [y[k - 2][l - 1] + y[k][l] == y[k - 1][l - 1] + y[k - 1][l] for k, l in combinations(range(2, n), 2)]
    ]
)

""" Comments
1) Without symmetry-breaking, the number of solutions for n increasing is: 
   1, 2, 4, 12, 40,116, 200, 444, 760, 2160, 4368, 7852, 12828, 17252, 19612, 21104, 18276, 15096, 10240, 6464, 3536, 2052, 872, 200, 88, 56, 204

2) we can write: 
    [AllDifferent(y[i]) for i in range(n - 1)]
  instead of:
    [AllDifferent(y[i][i + 1:]) for i in range(n - 1)]
  because None are automatically discarded
3) data used in challenges are:
  14 15 16 17 19 in 2010
  14 15 16 17 18 in 2011
  16 17 18 19 20 in 2015
"""
