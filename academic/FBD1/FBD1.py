"""
FBD1 design construction

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
The original mzn model was proposed by Andrew Gill (MIT Licence assumed).

## Data
  an integer k

## Model
  constraints: AllDifferent

## Execution
  python FBD1.py -data=number

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  academic, mzn25
"""

from pycsp3 import *

k = data or 5

ub = 5 + k ** 3  # uUpper bound for the design size

# x[i] is the ith design variable
x = VarArray(size=k, dom=range(1, ub // 2 + 1))

x_star = Var(dom=range(1, ub + 2))

# z is the design size
z = Var(range(3, ub * 2 + 2))

satisfy(
    # design variables in strict order
    Increasing(x, strict=True),

    # computing z
    z == 2 * x[-1] + x_star,

    # ensuring that all indicator frequencies are unique
    AllDifferent(
        x,
        [2 * x[i] for i in range(k)],
        [x[j] + x[i] for i, j in combinations(k, 2)],
        [x[j] - x[i] for i, j in combinations(k, 2)],
        [z - x[j] - x[i] for i, j in combinations(k, 2)],
        [z - 2 * x[i] for i in range(k)]
    ),

    # upper bound
    x_star <= 2 * x[-1] + 1,

    # lower bounds
    [x[i] >= i + 1 for i in range(k)],

    # constraints from sequential approach
    [
        [x[j] != 2 * x[i] for i, j in combinations(k, 2)],
        [x[j] != 3 * x[i] for i, j in combinations(k, 2)]
    ]
)

minimize(
    z
)

""" Comments
1) Data used for the 2025 competition are: [4, 6, 7, 8, 9]

2) constraint forall([Q[i] >= 2*i | i in main_factors])
 not encoded here because useless
"""
