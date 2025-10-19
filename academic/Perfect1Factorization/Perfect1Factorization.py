"""
A 1-factorization is a partition of the edges of a graph into m-1 complete matchings.
For the 1-factorization to be perfect, every pair of matchings must form a Hamiltonian circuit of the graph.
To make the problem interesting it is specified as an optimization-problem, forcing an ordering on the solutions.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Mikael Zayenz Lagerkvist (Licence at https://github.com/MiniZinc/mzn-challenge/blob/develop/2021/p1f-pjs/LICENSE)

## Data
  An integer n

## Model
  constraints: AllDifferent, Channel, Circuit, Lex, Sum

## Execution
  python Perfect1Factorization.py -data=number

## Links
  - https://www.minizinc.org/challenge/2021/results/

## Tags
  academic, mzn09, mzn15, mzn20, mzn21
"""

from pycsp3 import *

assert not variant() or variant("dec")

n = data or 10  # number of nodes

m = n - 1  # number of matchings

# x[i] is the ith complete matching
x = VarArray(size=[m, n], dom=range(n))

# y[i1][i2] is the circuit wrt the matchings i1 and i2
y = VarArray(size=[m, m, n], dom=lambda i1, i2, _: range(n) if i1 < i2 else None)

satisfy(
    # ensuring no self-loops
    [x[i][j] != j for i in range(m) for j in range(n)],

    # ensuring that each row is a matching
    [Channel(x[i]) for i in range(m)],

    # rows form a partition
    [AllDifferent(x[:, j]) for j in range(n)],

    # computing values of y
    [
        either(
            y[i1][i2][j] == x[i1][j],
            y[i1][i2][j] == x[i2][j]
        ) for i1, i2 in combinations(m, 2) for j in range(1, n)
    ],

    # tag(symmetry-breaking)
    (
        [y[i1][i2][0] == x[i1][0] for i1, i2 in combinations(m, 2)],

        LexIncreasing(x, strict=True)
    )
)

if not variant():
    satisfy(
        # forming circuits
        Circuit(y[i1][i2]) for i1, i2 in combinations(m, 2)
    )

elif variant("dec"):

    # z is introduced for decomposing circuits
    z = VarArray(size=[m, m, n], dom=lambda i1, i2, j: None if i1 >= i2 else {0} if j == n - 1 else range(n))

    satisfy(
        # forming circuits (by decomposition)
        [
            [AllDifferent(y[i1][i2]) for i1, i2 in combinations(m, 2)],
            [AllDifferent(z[i1][i2]) for i1, i2 in combinations(m, 2)],
            [z[i1][i2][0] == y[i1][i2][0] for i1, i2 in combinations(m, 2)],
            [z[i1][i2][j] == y[i1][i2][z[i1][i2][j - 1]] for i1, i2 in combinations(m, 2) for j in range(1, n)]
        ]
    )

minimize(
    Sum((j + 1) * (x[0][j] + 1) for j in range(n))
)

""" Comments
1) Data used in challenges are:
  2009: 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
  2015: 12, 13, 14, 15, 17
  2020: 10, 16, 17, 20, 21
  2021: 12, 14, 17, 18, 22
2) Note that  the dec variant is used in 2009, 2020, and 2021
"""
