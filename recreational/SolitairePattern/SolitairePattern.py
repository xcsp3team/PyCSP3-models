"""
This is a variant of Peg Solitaire where a goal state (configuration) with a number of pegs in some specific arrangement must be reached.
The initial state is the same as that of central Solitaire (i.e., missing peg in the middle of the board).

The model is written for the English style board (standard), with 33 holes

## Data
  Three integers

## Model
  constraints: Sum, Table

## Execution
  python SolitaireParttern.py -data=[number,number,number]
  python SolitaireParttern.py -data=[number,number,number] -varinat=dec1
  python SolitaireParttern.py -data=[number,number,number] -variant=dec2
  python SolitaireParttern.py -data=[number,number,number] -variant=table

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054805000195
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  academic, xcsp24
"""

from pycsp3 import *

from PegSolitaire_Generator import generate_boards
from pycsp3.classes.main.annotations import ValHeuristic

assert variant() in ("dec1", "dec2", "table", "hybrid")

patterns = [  # 10 papers from Jefferson paper
    [(0, 2), (0, 3), (1, 2), (1, 4), (2, 2), (2, 4), (3, 2), (3, 4), (4, 2), (4, 4), (5, 2), (5, 4), (6, 2), (6, 3)],
    [(0, 2), (1, 2), (2, 3), (2, 5), (2, 6), (3, 2), (3, 4), (4, 0), (4, 1), (4, 3), (5, 4), (6, 4)],
    [(0, 2), (0, 3), (0, 4), (1, 2), (2, 0), (2, 3), (2, 5), (2, 6), (3, 0), (3, 2), (3, 4), (3, 6), (4, 0), (4, 1), (4, 3), (4, 6), (5, 4), (6, 2), (6, 3),
     (6, 4)],
    [(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 0), (2, 1), (2, 6), (3, 0), (3, 1), (3, 5), (3, 6), (4, 0), (4, 5), (4, 6), (5, 2), (5, 3), (6, 2), (6, 3),
     (6, 4)],
    [(0, 3), (0, 4), (2, 0), (2, 2), (2, 3), (2, 4), (3, 0), (3, 2), (3, 4), (3, 6), (4, 2), (4, 3), (4, 4), (4, 6), (6, 2), (6, 3)],
    [(0, 2), (0, 4), (1, 4), (2, 0), (2, 1), (2, 3), (2, 6), (3, 2), (3, 4), (4, 0), (4, 3), (4, 5), (4, 6), (5, 2), (6, 2), (6, 4)],
    [(0, 2), (0, 4), (1, 2), (1, 4), (2, 0), (2, 1), (2, 5), (2, 6), (3, 3), (4, 0), (4, 1), (4, 5), (4, 6), (5, 2), (5, 4), (6, 2), (6, 4)],
    [(0, 2), (0, 3), (0, 4), (2, 0), (2, 6), (3, 0), (3, 3), (3, 6), (4, 0), (4, 6), (6, 2), (6, 3), (6, 4)],
    [(0, 3), (3, 0), (3, 3), (3, 6), (6, 3)],
    [(2, 2), (2, 4), (4, 2), (4, 4)]
]

origin_x, origin_y, pattern = data
init_board, final_board = generate_boards("english", origin_x, origin_y)
n, m = len(init_board), len(init_board[0])

points = [(i, j) for i in range(n) for j in range(m) if init_board[i][j] is not None]
for i, j in points:
    final_board[i][j] = 1 if (i, j) in patterns[pattern] else 0

horizon = sum(sum(v for v in row if v) for row in init_board) - sum(sum(v for v in row if v) for row in final_board)
nMoves = horizon

_m = [[(i, j, i + 1, j, i + 2, j), (i, j, i, j + 1, i, j + 2), (i, j, i - 1, j, i - 2, j), (i, j, i, j - 1, i, j - 2)] for i, j in points]
transitions = sorted((t[0:2], t[2:4], t[4:6]) for row in _m for t in row if 0 <= t[4] < n and 0 <= t[5] < m and init_board[t[4]][t[5]] is not None)
nTransitions = len(transitions)

TOP, RGT, BOT, LFT = range(4)


def direction(p1, p2):
    if p1[0] > p2[0]:
        return TOP
    if p1[0] < p2[0]:
        return BOT
    if p1[1] > p2[1]:
        return LFT
    return RGT


sym_dirs = {  # only keeping some directions wrt the origin cell
    (3, 3): [TOP],
    (2, 2): [TOP, RGT],
    (4, 4): [TOP, RGT],
    (2, 4): [TOP, LFT],
    (4, 2): [TOP, LFT],
    (2, 3): [TOP, RGT, BOT],
    (4, 3): [TOP, RGT, BOT],
    (3, 2): [TOP, RGT, LFT],
    (3, 4): [TOP, RGT, LFT]
}

corners = [k for k, (p1, _, _) in enumerate(transitions) if p1 in [(0, 2), (0, 4), (2, 0), (2, 6), (4, 0), (4, 6), (6, 2), (6, 4)]]


def independent(tr1, tr2):
    return len(set(tr1 + tr2)) == 6


def reversible(p1, p2, p3):
    if direction(p1, p2) == TOP:
        i, j = p3[0] - 1, p3[1]
    if direction(p1, p2) == BOT:
        i, j = p3[0] + 1, p3[1]
    if direction(p1, p2) == LFT:
        i, j = p3[0], p3[1] - 1
    if direction(p1, p2) == RGT:
        i, j = p3[0], p3[1] + 1
    return 0 <= i < n and 0 <= j < m and init_board[i][j] is not None


T2 = [(k, q) for k, tr1 in enumerate(transitions) for q, tr2 in enumerate(transitions) if
      k != q and (k < q or not independent(tr1, tr2)) and len({tr1[0], tr1[1], tr2[0], tr2[1]}) == 4 and tr1[2] != tr2[2]]

T3 = [(k, q) for k, (p1, p2, p3) in enumerate(transitions) for q, (q1, q2, q3) in enumerate(transitions) if k == q or (p1 == q2 and p2 == q1)]

# x[t][i](j] is the value at row i and column j at time t
x = VarArray(size=[nMoves + 1, n, m], dom=lambda t, i, j: None if init_board[i][j] is None else {0, 1})

# y[t] is the move (transition) performed at time t
y = VarArray(size=nMoves, dom=range(nTransitions))

satisfy(
    # setting the initial board
    x[0] == init_board,

    # setting the final board
    x[-1] == final_board,

    # tag(symmetry-breaking)
    [(y[i], y[i + 1]) in T2 for i in range(nMoves - 1)],

    # tag(redundant-constraints)
    [[(y[i], y[i + 2]) not in T3 for i in range(nMoves - 2)]],

)

if variant() in ("dec1", "dec2"):

    def unchanged(i, j, t):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) in (p1, p2, p3)]
        cond = (y[t] not in V) if variant("dec1") else conjunction(y[t] != k for k in V)
        return cond == (x[t][i][j] == x[t + 1][i][j])


    def to0(i, j, t):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) in (p1, p2)]
        cond = (y[t] in V) if variant("dec1") else disjunction(y[t] == k for k in V)
        return cond == both(x[t][i][j] == 1, x[t + 1][i][j] == 0)


    def to1(i, j, t):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) == p3]
        cond = (y[t] in V) if variant("dec1") else disjunction(y[t] == k for k in V)
        return cond == both(x[t][i][j] == 0, x[t + 1][i][j] == 1)


    satisfy(
        # handling unchanged situations
        [unchanged(i, j, t) for (i, j) in points for t in range(nMoves)],

        # handling situations where a peg disappears
        [to0(i, j, t) for (i, j) in points for t in range(nMoves)],

        # handling situations where a peg appears
        [to1(i, j, t) for (i, j) in points for t in range(nMoves)]
    )

elif variant("table"):

    def Tu(i, j):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) in (p1, p2, p3)]
        return flatten([[(k, 0, 1), (k, 1, 0)] if k in V else [(k, 0, 0), (k, 1, 1)] for k in range(nTransitions)], keep_tuples=True)


    def T0(i, j):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) in (p1, p2)]
        return flatten([[(k, 1, 0)] if k in V else [(k, 0, 0), (k, 0, 1), (k, 1, 1)] for k in range(nTransitions)], keep_tuples=True)


    def T1(i, j):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) == p3]
        return flatten([[(k, 0, 1)] if k in V else [(k, 0, 0), (k, 1, 0), (k, 1, 1)] for k in range(nTransitions)], keep_tuples=True)


    satisfy(
        # handling unchanged situations
        [(y[t], x[t][i][j], x[t + 1][i][j]) in T for (i, j) in points if (T := Tu(i, j),) for t in range(nMoves)],

        # handling situations where a peg disappears
        [(y[t], x[t][i][j], x[t + 1][i][j]) in T for (i, j) in points if (T := T0(i, j),) for t in range(nMoves)],

        # handling situations where a peg appears
        [(y[t], x[t][i][j], x[t + 1][i][j]) in T for (i, j) in points if (T := T1(i, j),) for t in range(nMoves)]
    )


elif variant("hybrid"):
    def n_holes(i, j):
        return sum(1 for ii in range(i) for jj in range(m) if init_board[ii][jj] is None) + sum(1 for jj in range(j) if init_board[i][jj] is None)


    T = [
        tuple(
            # firstly, all x[t][i][j] for all points (i,j)
            [1 if (i, j) in (p1, p2) else 0 if (i, j) == p3 else ANY for i, j in points]
            # secondly, all x[t+1][i][j] for all points (i,j)
            + [0 if (i, j) in (p1, p2) else 1 if (i, j) == p3 else col(i * m + j - n_holes(i, j)) for i, j in points]
            # lastly, the transition (move)
            + [k]
        ) for k, (p1, p2, p3) in enumerate(transitions)
    ]

    satisfy(
        # ensuring valid transitions
        (x[t], x[t + 1], y[t]) in T for t in range(nMoves)
    )

satisfy(
    # tag(redundant-constraints)
    [Sum(x[t]) == 32 - t for t in range(nMoves)],

    # # possibly restricting first move  tag(symmetry-breaking)
    # y[0] in [k for k, (p1, p2, p3) in enumerate(transitions) if org == p3 and direction(p1, p2) in sym_dirs[org]]
    # if (org := (origin_x, origin_y)) in sym_dirs else None
)

# annotate(
#     valHeuristic=ValHeuristic().static(y, order=corners)
# )

""" Comments
1) Data used for the 2024 competition are:  [(3,3,0), (3,3,1), (3,3,2), (3,3,3), (3,3,4), (3,3,5), (3,3,6), (3,3,7), (3,3,8), (3,3,9)]
"""

# below, we have to find valid limits in the two following groups
# Is this correct something like this ? [Sum(x[t][0][2], x[t][0][4], x[t][2][0], x[t][2][6], x[t][4][0], x[t][4][6], x[t][6][2], x[t][6][4]) <= (nMoves - t) // 2 for t in
#  range(nMoves - 14, nMoves)]

# Is this correct something like this? Cardinality(y, occurrences={i: range(3) for i in range(nTransitions)})

# if subvariant("optb"):
#     zx = Var(range(n))
#     zy = Var(range(m))
#
#     satisfy(
#         If(
#             x[-1][i][j],
#             Then=both(zx == i, zy == j)
#         ) for i, j in points
#     )
#
#     minimize(
#         abs(zx - origin_x) + abs(zy - origin_y)
#     )
