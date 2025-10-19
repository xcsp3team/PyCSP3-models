"""
Generalized Peaceable Queens.

On a board, put the maximal number of black and white queens while having no attack from opposing sides.
The number of black queens must be equal to the number of white queens.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Hendrik 'Henk' Bierlee, under the MIT Licence.

## Data
  two integers (n,q)

## Model
  constraints: Cardinality, Lex, Precedence, Regular

## Execution
  python GeneralizedPeacableQueens.py -data=[number,number]

## Links
  - https://oeis.org/A250000
  - https://link.springer.com/chapter/10.1007/978-3-540-24664-0_19
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  academic, mzn22
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry

n, q = data or (8, 3)  # the order (number of rows and columns) of the board and the number of armies

N, Colors = range(n), range(q + 1)  # colors including 0


def automaton():
    qs = Automaton.states_for(Colors)
    trs = [(qs[0], 0, qs[0])] + [(qs[0], v, qs[v]) for v in Colors[1:]] + [(qs[v], [0, v], qs[v]) for v in Colors[1:]]
    return Automaton(start=qs[0], final=qs, transitions=trs)


A = automaton()  # the automaton used to impose that queens are at peace

# x[i][j] is the color is in the cell at row i and column j (0 if no queen)
x = VarArray(size=[n, n], dom=Colors)

# z[i] is the number of queens for the ith color (excluding 0)
z = VarArray(size=q, dom=range(n * n // q))

satisfy(
    # at peace on every row
    [x[i] in A for i in N],

    # at peace on every column
    [x[:, j] in A for j in N],

    # at peace on all down-right diagonals (except corners)
    [[x[i][j] for i in N for j in N if i + j == k] in A for k in range(1, 2 * n - 2)],

    # at peace on all up-right diagonals (except corners)
    [[x[i][j] for i in N for j in N if i - j == k] in A for k in range(-n + 2, n - 1)],

    # counting the number of queens of each color
    Cardinality(
        within=x,
        occurrences={i: z[i - 1] for i in Colors[1:]}
    ),

    # ensuring the same number of queens of each color
    AllEqual(z),

    # tag(symmetry-breaking)
    Precedence(
        within=x,
        values=Colors[1:]
    ),

    # tag(symmetry-breaking)
    [x <= x[symmetry] for symmetry in [f.apply_on(n) for f in TypeSquareSymmetry]]
)

maximize(
    # maximizing the number of queens on the board
    z[0]
)

"""
1) Data used in 2022 are:  (8,3), (9,5), (11,5), (13,5), (25,4)
2) Note that:
 x[symmetry]
   is a shortcut for
 [x[row] for row in symmetry]
   which, itself, is a shortcut for:
 [[x[k][l] for k, l in row] for row in symmetry]
3) Note that:
 [x <= x[symmetry] for symmetry in symmetries]
   is equivalent to:
 [LexIncreasing(x, x[symmetry]) for symmetry in symmetries]  
"""
