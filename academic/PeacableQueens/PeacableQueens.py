"""
On a board, put the maximal number of black and white queens while having no attack from opposing sides.
The number of black queens must be equal to the number of white queens.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The model was created by Hendrik 'Henk' Bierlee, with a licence that seems to be like a MIT Licence.

## Data
  An integer n

## Model
  constraints: Count, Lex, Precedence, Regular

## Execution
  python PeacableQueens.py -data=[integer]

## Links
  - https://link.springer.com/chapter/10.1007/978-3-540-24664-0_19
  - https://oeis.org/A250000
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn21
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.ptypes import TypeSquareSymmetry

n = data  # the order (number of rows and columns) of the board
symmetries = [sym.apply_on(n) for sym in TypeSquareSymmetry]

NONE, BLACK, WHITE = colors = 0, 1, 2


def automaton():
    q0, q1, q2 = Automaton.states_for(colors)
    t = [(q0, 0, q0), (q0, 1, q1), (q0, 2, q2), (q1, [0, 1], q1), (q2, [0, 2], q2)]
    return Automaton(start=q0, final=[q0, q1, q2], transitions=t)


A = automaton()  # the automaton used to impose that queens are at peace

# x[i][j] is 1 (resp., 2), if a black (resp., white) queen is in the cell at row i and column j. It is 0 otherwise.
x = VarArray(size=[n, n], dom=colors)

# the number of queens of each color (the same for black and white)
z = Var(dom=range(n * n // 2))

satisfy(
    # counting the number of black queens
    Count(x, value=BLACK) == z,

    # counting the number of white queens
    Count(x, value=WHITE) == z,

    # at peace on every row
    [x[i] in A for i in range(n)],

    # at peace on every column
    [x[:, j] in A for j in range(n)],

    # at peace on all down-right diagonals (except corners)
    [[x[i][j] for i in range(n) for j in range(n) if i + j == k] in A for k in range(1, 2 * n - 2)],

    # at peace on all up-right diagonals (except corners)
    [[x[i][j] for i in range(n) for j in range(n) if i - j == k] in A for k in range(-n + 2, n - 1)],

    # tag(symmetry-breaking)
    (
        Precedence(x, values=[BLACK, WHITE]),
        [LexIncreasing(x, [x[row] for row in symmetry]) for symmetry in symmetries]
    )
)

maximize(
    # maximizing the number of queens on the board
    z
)

""" Comments
1) note that (q2, [0,2], q2) is a shortcut for {(q2, 0, q2), (q2, 2, q2)} 
   It is also possible to save the automatas in this compact form with the option -keepSmartTransitions
2) data used in 2021 are:  8, 11, 25, 40, 50
3) [x[row] for row in symmetry]
 is equivalent to:
 [[x[k][l] for k, l in row] for row in symmetry]
"""
