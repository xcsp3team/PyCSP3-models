"""
From archive.vector.org.uk
    In 1850, Carl Friedrich Gauss and Franz Nauck showed that it is possible to place eight queens on a chessboard such that no queen attacks any other queen.
    The problem of enumerating the 92 different ways there are to place 8 queens in this manner has become a standard programming example,
    and people have shown that it can be solved using many different search techniques.
    Now consider a variant of this problem: you must place an equal number of knights and queens on a chessboard such that no piece attacks any other piece.
    What is the maximum number of pieces you can so place on the board, and how many different ways can you do it?

A variant relaxes the fact that the number of queens and knights must be equal.
The variant "b" was used for the 2024 competition


## Data
  an integer n

## Model
  constraints: Sum

## Execution
  python SameQueensKnights.py -data=number
  python SameQueensKnights.py -data=number -variant=b
  python SameQueensKnights.py -data=number -variant=mini

## Links
  - http://archive.vector.org.uk/art10003900
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
"""
from pycsp3 import *

n = data

EMPTY, QUEEN, KNIGHT = range(3)

Cells = [(i, j) for i in range(n) for j in range(n)]


def queen_attack(i, j):
    return [(a, b) for a, b in Cells if (a, b) != (i, j) and (a == i or b == j or abs(i - a) == abs(j - b))]


def knight_attack(i, j):
    return [(a, b) for a, b in Cells if a != i and b != j and abs(i - a) + abs(j - b) == 3]


# x[i][j] indicates what is present in the cell with coordinates (i,j)
x = VarArray(size=[n, n], dom={EMPTY, QUEEN, KNIGHT})

# q is the number of queens
q = Var(dom=range(n + 1))

# k is the number of knights
k = Var(dom=range(n + 1))

if not variant():

    satisfy(
        # computing the number of queens
        q == Sum(x[i][j] == QUEEN for i, j in Cells),

        # computing the number of knights
        k == Sum(x[i][j] == KNIGHT for i, j in Cells),

        # ensuring that no two pieces (queens or knights) attack each other
        [
            Match(
                x[i][j],
                Cases={
                    QUEEN: Sum(x[queen_attack(i, j)]) == 0,
                    KNIGHT: Sum(x[knight_attack(i, j)]) == 0
                }
            ) for i, j in Cells
        ]
    )

elif variant("mini"):

    qb = VarArray(size=[n, n], dom={0, 1})
    kb = VarArray(size=[n, n], dom={0, 1})

    sb = VarArray(size=[n, n], dom=lambda i, j: range(len(queen_attack(i, j)) + 1))
    sk = VarArray(size=[n, n], dom=lambda i, j: range(len(knight_attack(i, j)) + 1))

    satisfy(
        [(qb[i][j], x[i][j]) in [(1, QUEEN), (0, EMPTY), (0, KNIGHT)] for i, j in Cells],
        [(kb[i][j], x[i][j]) in [(1, KNIGHT), (0, EMPTY), (0, QUEEN)] for i, j in Cells],

        # computing the number of queens
        q == Sum(qb),

        # computing the number of knights
        k == Sum(kb),

        [sb[i][j] == Sum(x[queen_attack(i, j)]) for i, j in Cells],
        [sk[i][j] == Sum(x[knight_attack(i, j)]) for i, j in Cells],

        [(x[i][j], sb[i][j], sk[i][j]) in [(QUEEN, 0, ANY), (KNIGHT, ANY, 0), (EMPTY, ANY, ANY)] for i, j in Cells]
    )

if not variant():

    satisfy(
        # ensuring the same number of queens and knights
        q == k
    )

    maximize(
        q
    )

elif variant("b"):

    maximize(
        q + k
    )
elif variant("mini"):
    z = Var(dom=range(2 * n + 1))

    satisfy(
        z == q + k
    )
    maximize(
        z
    )

"""
1) Data used for the 2024 Competition: [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
"""

# [
#         If(
#             x[i][j] == QUEEN,
#             Then=[
#                 Sum(x[queen_attack(i, j)]) == 0
#             ],
#             Else=If(x[i][j] == KNIGHT, Then=Sum(x[knight_attack(i, j)]) == 0)
#         ) for i in range(n) for j in range(n)
# ]
