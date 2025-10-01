"""
An optimisation variation of Peg Solitaire (named Fool’s Solitaire by Berlekamp, Conway and Guy)
is to reach a position where no further moves are possible in the shortest sequence of moves.

The model is written for the English style board (standard), with 33 holes

## Data
  Two integers

## Model
  constraints: Sum, Table

## Execution
  python FoolSolitaire.py -data=[number,number]
  python FoolSolitaire.py -data=[number,number] -variant=dec1
  python FoolSolitaire.py -data=[number,number] -variant=dec2
  python FoolSolitaire.py -data=[number,number] -variant=table

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054805000195
  - https://www.routledge.com/Winning-Ways-for-Your-Mathematical-Plays-Volume-2/Berlekamp-Conway-Guy/p/book/9781568811420
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
"""

from pycsp3 import *

from data.PegSolitaire_Generator import generate_boards
from pycsp3.classes.main.annotations import ValHeuristic

assert variant() in ("dec1", "dec2", "table", "hybrid")

origin_x, origin_y = data

init_board, final_board = generate_boards("english", origin_x, origin_y)
n, m = len(init_board), len(init_board[0])

horizon = sum(sum(v for v in row if v) for row in init_board) - sum(sum(v for v in row if v) for row in final_board)
assert horizon == 31
nMoves = horizon

points = [(i, j) for i in range(n) for j in range(m) if init_board[i][j] is not None]
_m = [[(i, j, i + 1, j, i + 2, j), (i, j, i, j + 1, i, j + 2), (i, j, i - 1, j, i - 2, j), (i, j, i, j - 1, i, j - 2)] for i, j in points]
transitions = sorted((t[0:2], t[2:4], t[4:6]) for row in _m for t in row if 0 <= t[4] < n and 0 <= t[5] < m and init_board[t[4]][t[5]] is not None)
nTransitions = len(transitions)

NADA = nTransitions

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


T2 = ([(k, q) for k, tr1 in enumerate(transitions) for q, tr2 in enumerate(transitions) if
       k != q and (k < q or not independent(tr1, tr2)) and len({tr1[0], tr1[1], tr2[0], tr2[1]}) == 4 and tr1[2] != tr2[2]]
      + [(ANY, NADA)])

T3 = [(k, q) for k, (p1, p2, p3) in enumerate(transitions) for q, (q1, q2, q3) in enumerate(transitions) if k == q or (
        p1 == q2 and p2 == q1)]  # + [(k, NADA) for k in range(nTransitions + 1)])  # not ANY because a negative table (and for the moment, no available algorithm)

# T5 = ([tuple([1 if (i, j) in (p1, p2) else 0 if (i, j) == p3 else ANY for i, j in points] + [1]) for k, (p1, p2, p3) in enumerate(transitions)]
#       + [tuple([ANY for i, j in points] + [0])])


# x[t][i](j] is the value at row i and column j at time t
x = VarArray(size=[nMoves + 1, n, m], dom=lambda t, i, j: None if init_board[i][j] is None else {0, 1})

# y[t] is the move (transition) performed at time t
y = VarArray(size=nMoves, dom=range(nTransitions + 1))  # +1 for NADA

# z is the smallest conflict level
z = Var(range(nMoves))

satisfy(
    # setting the initial board
    x[0] == init_board,

    # tag(symmetry-breaking)
    [(y[i], y[i + 1]) in T2 for i in range(nMoves - 1)],

    # tag(redundant-constraints)
    [[(y[i], y[i + 2]) not in T3 for i in range(nMoves - 2)]],

    # ensuring valid value of z
    y[z] == NADA,

    # ensuring no useless use of Nada
    [
        If(
            x[t][p1] == 1, x[t][p2] == 1, x[t][p3] == 0,
            Then=y[t] != NADA
        ) for k, (p1, p2, p3) in enumerate(transitions) for t in range(nMoves)
    ]
)

if variant() in ("dec1", "dec2"):

    def unchanged(i, j, t):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) in (p1, p2, p3)]  # + [NADA]
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
        return flatten([[(k, 0, 1), (k, 1, 0)] if k in V else [(k, 0, 0), (k, 1, 1)] for k in range(nTransitions + 1)], keep_tuples=True)


    def T0(i, j):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) in (p1, p2)]
        return flatten([[(k, 1, 0)] if k in V else [(k, 0, 0), (k, 0, 1), (k, 1, 1)] for k in range(nTransitions + 1)], keep_tuples=True)


    def T1(i, j):
        V = [k for k, (p1, p2, p3) in enumerate(transitions) if (i, j) == p3]
        return flatten([[(k, 0, 1)] if k in V else [(k, 0, 0), (k, 1, 0), (k, 1, 1)] for k in range(nTransitions + 1)], keep_tuples=True)


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
        return sum(1 for k in range(i) for p in range(m) if init_board[k][p] is None) + sum(1 for p in range(j) if init_board[i][p] is None)


    T = [
            tuple(
                # firstly, all x[t][i][j] for i for j
                [1 if (i, j) in (p1, p2) else 0 if (i, j) == p3 else ANY for i, j in points]
                # secondly, all x[t+1][i][j] for i for j
                + [0 if (i, j) in (p1, p2) else 1 if (i, j) == p3 else col(i * m + j - n_holes(i, j)) for i, j in points]
                # lastly, the transition (move)
                + [k]
            ) for k, (p1, p2, p3) in enumerate(transitions)
        ] + [tuple([ANY for i, j in points] + [col(i * m + j - n_holes(i, j)) for i, j in points] + [NADA])]

    satisfy(
        # ensuring valid transitions
        (x[t], x[t + 1], y[t]) in T for t in range(nMoves)
    )

satisfy(
    # tag(redundant-constraints)
    [
        If(
            t <= z,
            Then=Sum(x[t]) == 32 - t
        ) for t in range(nMoves)
    ],

    # possibly restricting first move  tag(symmetry-breaking)
    y[0] in [k for k, (p1, p2, p3) in enumerate(transitions) if org == p3 and direction(p1, p2) in sym_dirs[org]]
    if (org := (origin_x, origin_y)) in sym_dirs else None
)

minimize(
    z
)

# annotate(
#     valHeuristic=ValHeuristic().static(y, order=corners)
# )

"""
1) For the mini-tracks, we use:
  # ensuring no useless use of Nada
    [(x[t][p1], x[t][p2], x[t][p3], y[t]) in [(0, ANY, ANY, ANY), (ANY, 0, ANY, ANY), (ANY, ANY, 1, ANY)] + [(ANY, ANY, ANY, v) for v in range(nTransitions)]
     for k, (p1, p2, p3) in enumerate(transitions) for t in range(nMoves)],

and discard  If(
    #         t <= z,
    #         Then=Sum(x[t]) == 32 - t
    #     ) for t in range(nMoves)

2) Data used for the 2024 competition: [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0),
(3,1), (3,2), (3,3)]
"""

# [  CAPTURED by T2
#     If(
#         y[t] == NADA,
#         Then=y[t + 1] == NADA
#     ) for t in range(nMoves - 1)
# ],
