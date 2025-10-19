"""
from CP'23 paper whose URL is given below:
    The multiplication of two matrices A and B of sizes n×m and m×p results in a product matrix C of size n×p.
    This operation can be represented by a binary third-order tensor T.
    An entry Ti,j,k of this tensor is equal to 1 if and only if the kth entry in the output matrix C uses the scalar product of the ith entry of A and the jth entry of B.
    The FMM (Fast Matrix Multiplication) problem for a given tensor T, rank R, and field F (e.g., F = {−1, 0, +1}) asks:
    can each entry Ti,j,k of T be expressed as the sum of exactly R trilinear terms involving the factor matrices U, V, and W, as follows:
    Ti,j,k = Σ^R_r=1 Ui,r × Vj,r × Wk,r, ∀i ∈ {1, ..., n×m}, j ∈ {1, ..., m×p}, k ∈ {1, ..., n×p}.

## Data
  four integers n, m, p, and R

## Model
  constraints: Lex, Precedence, Sum, Table

## Execution
  python FastMatrixMultiplication.py -data=[number,number,number,number]
  python FastMatrixMultiplication.py -data=[number,number,number,number] -variant=table

## Links
  - https://drops.dagstuhl.de/storage/00lipics/lipics-vol280-cp2023/LIPIcs.CP.2023.14/LIPIcs.CP.2023.14.pdf
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
"""

from pycsp3 import *
from pycsp3.classes.main.annotations import ValHeuristic

assert not variant() or variant("table") or variant("mini")

n, m, p, R = data or (2, 2, 2, 7)

U, V, W = n * m, m * p, n * p

T = []
for k in range(n * p):
    M = [[0] * V for _ in range(U)]
    i, j = k // p, k % p
    for a in range(m):
        M[i * m + a][j + (p * a)] = 1
    T.append(M)

# x is the first factor matrix
x = VarArray(size=[U, R], dom={-1, 0, 1})

# y is the second factor matrix
y = VarArray(size=[V, R], dom={-1, 0, 1})

# z is the third factor matrix
z = VarArray(size=[W, R], dom={-1, 0, 1})

if not variant():

    satisfy(
        # ensuring that the tensor is produced
        [Sum(x[i][r] * y[j][r] * z[k][r] for r in range(R)) == T[k][i][j] for i in range(U) for j in range(V) for k in range(W)],

        # tag(symmetry-breaking)
        [
            [LexIncreasing(x[:, r] + y[:, r], x[:, r + 1] + y[:, r + 1]) for r in range(R - 1)],

            [Precedence(x[:, r], values=[-1, 1]) for r in range(R)],

            [Precedence(z[:, r], values=[-1, 1]) for r in range(R)]
        ]
    )

elif variant("table"):
    T1 = [
        (0, ANY, ANY, 0),
        (ANY, 0, ANY, 0),
        (ANY, ANY, 0, 0),
        (-1, -1, -1, -1),
        (-1, -1, 1, 1),
        (-1, 1, -1, 1),
        (-1, 1, 1, -1),
        (1, -1, -1, 1),
        (1, -1, 1, -1),
        (1, 1, -1, -1),
        (1, 1, 1, 1)]

    # aux[i][j][k][r] is the product of the rtr trilinear term for (i,j,k)
    aux = VarArray(size=[U, V, W, R], dom={-1, 0, 1})

    satisfy(
        # computing the sums of terms
        [(x[i][r], y[j][r], z[k][r], aux[i][j][k][r]) in T1 for i in range(U) for j in range(V) for k in range(W) for r in range(R)],

        # ensuring that the tensor is produced
        [Sum(aux[i][j][k]) == T[k][i][j] for i in range(U) for j in range(V) for k in range(W)]
    )

elif variant("mini"):

    p = VarArray(size=[U, V, W, R], dom={-1, 0, 1})

    satisfy(

        [p[i][j][k][r] == x[i][r] * y[j][r] * z[k][r] for i in range(U) for j in range(V) for k in range(W) for r in range(R)],

        # ensuring that the tensor is produced
        [Sum(p[i][j][k]) == T[k][i][j] for i in range(U) for j in range(V) for k in range(W)]

    )

# annotate(
#     valHeuristic=ValHeuristic().static(flatten(x, y, z), order=[0, -1, 1])
# )

""" Comments
1) Data used for the 2024 Competition: [(2,2,2,3), (2,2,2,4), (2,2,2,5), (2,2,2,6), (2,2,2,7), (1,3,3,9), (3,1,3,9), (2,2,3,11), (2,3,2,11)]
"""

# [aux[i][j][k] in T2s[T[k][i][j]] for i in range(U) for j in range(V) for k in range(W)]

# def T2(v):
#     assert v in (-1, 0, 1)
#     return [ t for t in product((-1, 0, 1), repeat=15) if sum(t) == v ]

# java ace FastMatrixMultiplication-2-2-2-7.xml -ea -eqm
