"""
Peg Solitaire is played on a board with a number of holes.
In the English version of the game considered here, the board is in the shape of a cross with 33 holes.
Pegs are arranged on the board so that at least one hole remains. By making horizontal or vertical draughts-like moves,
the pegs are gradually removed until a goal configuration is obtained.
In the classic ‘central’ Solitaire, the goal is to reverse the starting position, leaving just a single peg in the central hole

## Data
  Three integers

## Model
  Here, the model is for the English style (standard), with 33 holes.

## Execution
  python PegSolitaire.py -data=[number,number,number] -variant=english

## Links
  - https://www.cs.york.ac.uk/aig/projects/implied/docs/CPAIOR03.pdf
  - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  academic, recreational, xcsp23
"""

from pycsp3 import *

from data.PegSolitaire_Generator import generate_boards, build_transitions

assert variant() in {"english", "french"}

origin_x, origin_y, nMoves = data or (0, 2, 0)  # nMoves computed automatically when initially at 0

init_board, final_board = generate_boards(variant(), origin_x, origin_y)
n, m = len(init_board), len(init_board[0])
transitions = build_transitions(init_board)
nTransitions = len(transitions)

horizon = sum(sum(v for v in row if v) for row in init_board) - sum(sum(v for v in row if v) for row in final_board)
nMoves = horizon if nMoves <= 0 or horizon < nMoves else nMoves
assert 0 < nMoves <= horizon

pairs = [(i, j) for i in range(n) for j in range(m) if init_board[i][j] is not None]


def unchanged(i, j, t):
    valid = [k for k, tr in enumerate(transitions) if (i, j) in (tr[0:2], tr[2:4], tr[4:6])]
    return conjunction(y[t] != k for k in valid) == (x[t][i][j] == x[t + 1][i][j])


def to0(i, j, t):
    valid = [k for k, tr in enumerate(transitions) if (i, j) in (tr[0:2], tr[2:4])]
    return disjunction(y[t] == k for k in valid) == both(x[t][i][j] == 1, x[t + 1][i][j] == 0)


def to1(i, j, t):
    valid = [k for k, tr in enumerate(transitions) if (i, j) == tr[4:6]]
    return disjunction(y[t] == k for k in valid) == both(x[t][i][j] == 0, x[t + 1][i][j] == 1)


# x[i][j][t] is the value at row i and column j at time t
x = VarArray(size=[nMoves + 1, n, m], dom=lambda t, i, j: {0, 1} if init_board[i][j] is not None else None)

# y[t] is the move (transition) performed at time t
y = VarArray(size=nMoves, dom=range(nTransitions))

satisfy(
    # setting the initial board
    x[0] == init_board,

    # setting the final board
    x[-1] == final_board,

    # handling unchanged situations
    [unchanged(i, j, t) for (i, j) in pairs for t in range(nMoves)],

    # handling situations where a peg disappears
    [to0(i, j, t) for (i, j) in pairs for t in range(nMoves)],

    # handling situations where a peg appears
    [to1(i, j, t) for (i, j) in pairs for t in range(nMoves)]
)

""" Comments
1) x[0] == init_board is possible because cells with None (either in variables or values) are discarded
   This is equivalent to [x[0][i][j] == init_board[i][j] for (i, j) in pairs]
2) What about replacing conjunction and disjunction with AllHold and Exist?
"""
