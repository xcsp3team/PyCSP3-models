"""
This is the [problem 065](https://www.csplib.org/Problems/prob065/) of the CSPLib:

An OPD problem ⟨v,b,r⟩ is to find a matrix of v rows and b columns of 0-1 values such that each row sums to r,
and the maximum, denoted $\lambda$, of the dot products beween all pairs of distinct rows is minimal.
Equivalently, the objective is to find v subsets of cardinality r drawn from a given set of b elements,
such that the largest intersection of any two of the v sets has minimal cardinality, denoted $\lambda$.

### Example
The optimum for \[4,4,4] is 4 and a solution is

```
    1 1 1 1
    1 1 1 1
    1 1 1 1
    1 1 1 1
```


## Data
A triplet \[v,b,r] as defined above.

## Model(s)


There are two variants, one with auxilliary variables, one without.

 constraints: Intension, LexIncreasing, Sum


## Command Line

python Opd.py
python Opd.py -data=[4,6,4]
python Opd.py -data=[4,6,4] -variant=aux

## Tags
 academic csplib
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
        Maximum(x[i] * x[j] for i, j in combinations(range(v), 2))
    )

elif variant("aux"):
    # s[i][j][k] is the scalar variable for the product of x[i][k] and x[j][k]
    s = VarArray(size=[v, v, b], dom=lambda i, j, k: {0, 1} if i < j else None)

    satisfy(
        # computing scalar variables
        s[i][j][k] == x[i][k] * x[j][k] for i, j in combinations(range(v), 2) for k in range(b)
    )

    minimize(
        # minimizing the maximum value of dot products between all pairs of distinct rows
        Maximum(Sum(s[i][j]) for i, j in combinations(range(v), 2))
    )

satisfy(
    # tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)
)
