"""


This is the [problem 28](http://www.csplib.org/Problems/prob028) of the CSPLib:

Balanced Incomplete Block Design (BIBD) generation is a standard combinatorial problem from design theory, originally used in the design of
statistical experiments but since finding other applications such as cryptography.
It is a special case of Block Design, which also includes Latin Square problems.
BIBD generation is described in most standard textbooks on combinatorics.
A BIBD is defined as an arrangement of $v$ distinct objects into $b$ blocks such that each block contains exactly $k$ distinct objects,
each object occurs in exactly $r$ different blocks, and every two distinct objects occur together in exactly $\lambda$ blocks.
Another way of defining a BIBD is in terms of its incidence matrix, which is a $v$ by $b$ binary matrix with exactly $r$ ones per row, $k$ ones per column, and with a scalar product of $\lambda$ between any pair of distinct rows.
A BIBD is therefore specified by its parameters $(v,b,r,k,\lambda)$.




### Example

An example of a solution for (7,7,3,3,1) is:
```
    0 1 1 0 0 1 0
    1 0 1 0 1 0 0
    0 0 1 1 0 0 1
    1 1 0 0 0 0 1
    0 0 0 0 1 1 1
    1 0 0 1 0 1 0
    0 1 0 1 1 0 0
```

## Data
Data is specified by a list \[$v$,$b$,$r$,$k$,$\lambda$], corresponding to:
 - $v$: the number of objects
 - $b$: the number of blocks
 - $k$: the number of distinct objects per block
 - $r$: each object occurs in exactly $r$ different blocks
 - every two distinct objects occur together in exactly $\lambda$ blocks


## Model(s)

There are two variants:
 - a main variant
 - another one (called aux) with auxiliary variables.

You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Bibd/).

 constraints: Sum, LexIncreasing



## Command Line

python Bibd.py
python Bibd.py -data=[9,0,0,3,9]
python Bibd.py -data=[9,0,0,3,9] -variant=aux

## Tags
 academic csplib
"""

from pycsp3 import *

v, b, r, k, l = data or (6, 0, 0, 3, 8)
b = (l * v * (v - 1)) // (k * (k - 1)) if b == 0 else b  # when specified at 0, b is automatically computed
r = (l * (v - 1)) // (k - 1) if r == 0 else r  # when specified at 0, r is automatically computed

# x[i][j] is the value of the matrix at row i and column j
x = VarArray(size=[v, b], dom={0, 1})

if not variant():
    satisfy(
        # constraints on rows
        [Sum(row) == r for row in x],

        # constraints on columns
        [Sum(col) == k for col in columns(x)],

        # scalar constraints with respect to lambda
        [row1 * row2 == l for row1, row2 in combinations(x, 2)]
    )

elif variant("aux"):
    # s[i][j][k] is the product of x[i][k] and x[j][k]
    s = VarArray(size=[v, v, b], dom={0, 1})

    satisfy(
        # constraints on rows
        [Sum(x[i]) == r for i in range(v)],

        # constraints on columns
        [Sum(x[:, j]) == k for j in range(b)],

        # computing scalar variables
        [s[i][j][k] == x[i][k] * x[j][k] for i, j in combinations(v, 2) for k in range(b)],

        # scalar constraints with respect to lambda
        [Sum(s[i][j]) == l for i, j in combinations(v, 2)]
    )

satisfy(
    # Increasingly ordering both rows and columns  tag(symmetry-breaking)
    LexIncreasing(x, matrix=True)
)
