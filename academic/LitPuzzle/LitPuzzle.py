"""
5x5 puzzle, by Martin Chlond (and mentioned by Håkan Kjellerstrand on his website).

Each of the squares in the grid (n by n) can be in one of two states, lit (white) or unlit (red).
If the player clicks on a square then that square and each orthogonal neighbour will toggle between the two states.
Each mouse click constitutes one move and the objective of the puzzle is to light all squares in the least number of moves.

## Data
  a number n

## Model
  constraints: Sum, Table

## Execution
  python LitPuzzle.py -data=number

## Links
  - https://www.hakank.org/webblogg/archives/001229.html
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
"""

from pycsp3 import *

assert not variant() or variant("aux") or variant("table")

n = data or 5

N = range(n)

# x[i][j] is 1 if the player clicks on the square at row i and column j
x = VarArray(size=[n, n], dom={0, 1})

if not variant():
    satisfy(
        # ensuring that all cells are lit
        Sum(x.cross(i, j)) in (1, 3, 5) for i in N for j in N
    )

elif variant("aux"):
    # d[i][j] is the number of pair of neighbors of the square at row i and column j being clicked
    d = VarArray(size=[n, n], dom={0, 1, 2})  # range(n + 1))

    satisfy(
        # ensuring that all cells are lit
        Sum(x.cross(i, j)) - 2 * d[i, j] == 1 for i in N for j in N
    )

elif variant("table"):
    def T(r):
        return [p for p in product({0, 1}, repeat=r) if sum(p) in (1, 3, 5)]


    satisfy(
        # ensuring that all cells are lit
        scp in T(r) for i in N for j in N if (scp := x.cross(i, j), r := len(scp))
    )

minimize(
    Sum(x)
)

""" Comments
1) Data used for the 2024 Competition: [10, 15, 16, 17, 18, 20, 25, 30, 40, 50]
"""
