"""
An OPD (v,b,r) problem is to find a binary matrix of v rows and b columns such that:
   - each row sums to r,
   - the dot product between any pair of distinct rows is minimal

## Data
  Three integers (v,b,r)

## Model
  constraints: Lex, Maximum, Sum

## Execution
  python OPD.py -data=[number,number,number]
  python OPD.py -data=[number,number,number] -variant=aux

## Links
  - https://www.csplib.org/Problems/prob065/
  - https://link.springer.com/article/10.1007/s10601-006-9014-4
  - https://www.sciencedirect.com/science/article/abs/pii/S1571065314000596?via%3Dihub
  - https://link.springer.com/chapter/10.1007/11564751_7
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  academic, csplib
"""

from pycsp3 import *

v, b, r = data or (4, 4, 4)

# x[i][j] is the value at row i and column j
x = VarArray(size=[v, b], dom={0, 1})

satisfy(
    # each row sums to 'r'
    Sum(x[i]) == r for i in range(v)
)

if not variant():
    minimize(
        # minimizing the maximum value of dot products between all pairs of distinct rows
        Maximum(x[i] * x[j] for i, j in combinations(v, 2))
    )

elif variant("aux"):
    # s[i][j][k] is the scalar variable for the product of x[i][k] and x[j][k]
    s = VarArray(size=[v, v, b], dom=lambda i, j, k: {0, 1} if i < j else None)

    satisfy(
        # computing scalar variables
        s[i][j][k] == x[i][k] * x[j][k] for i, j in combinations(v, 2) for k in range(b)
    )

    minimize(
        # minimizing the maximum value of dot products between all pairs of distinct rows
        Maximum(Sum(s[i][j]) for i, j in combinations(v, 2))
    )

satisfy(
    # tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)
)
