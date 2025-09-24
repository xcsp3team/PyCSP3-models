"""
Roller Splat is a ball game where you move the ball with your mouse over the course, and you try to fill up all the white squares with the colour of the ball.
It was created by Yello Games LTD.

 ## Data Example
  04.json

## Model
  constraints: Element, Table

## Execution
  python RollerSplat.py -data=[datafile.json,h=number]

## Links
  - https://play.google.com/store/apps/details?id=com.neonplay.casualrollersplat2&hl=fr&pli=1
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, xcsp25
"""

from pycsp3 import *

grid, horizon = data if isinstance(data, tuple) else (data, 3 * len(data))  # horizon is the number of allowed moves
n, m = len(grid), len(grid[0])

EMPTY, WALL, BALL = range(3)
origin_x, origin_y = next(((i, j) for i in range(n) for j in range(m) if grid[i][j] == BALL))

TOP, RGT, BOT, LFT = Directions = range(4)


def reachable(i, j, direction):
    tab = []
    if direction == TOP:
        while 0 <= i and grid[i][j] != WALL:
            tab.append((i, j))
            i -= 1
    elif direction == BOT:
        while i < n and grid[i][j] != WALL:
            tab.append((i, j))
            i += 1
    elif direction == LFT:
        while 0 <= j and grid[i][j] != WALL:
            tab.append((i, j))
            j -= 1
    elif direction == RGT:
        while j < m and grid[i][j] != WALL:
            tab.append((i, j))
            j += 1
    return None if len(tab) <= 1 else tab


Moves = []  # certainly, some moves could be discarded because they are not possible
for i in range(n):
    for j in range(m):
        # if grid[i][j] == WALL:
        if t := reachable(i - 1, j, TOP):
            Moves.append(t)
        if t := reachable(i + 1, j, BOT):
            Moves.append(t)
        if t := reachable(i, j - 1, LFT):
            Moves.append(t)
        if t := reachable(i, j + 1, RGT):
            Moves.append(t)

nMoves = len(Moves)

PaintingMoves = [[[k for k, t in enumerate(Moves) if (i, j) in t] for j in range(m)] for i in range(n)]

T = [(k, q) for k in range(nMoves) for q in range(nMoves) if Moves[k][-1] == Moves[q][0]] + [(ANY, -1)]

Cells = [(i, j) for i in range(n) for j in range(m) if grid[i][j] != WALL]

# x[i][j] is the time of the painting move (in y) for cell at position (i,j)
x = VarArray(size=[n, m], dom=lambda i, j: range(horizon) if grid[i][j] != WALL else None)

# y[t] is the move (index) performed at time t (or -1 if finished)
y = VarArray(size=horizon + 1, dom=lambda t: range(-1, nMoves) if t < horizon else {-1})

# z is the time when the grid is entirely painted
z = Var(range(horizon))

satisfy(
    # the initial move depends on the position of the ball
    y[0] in {k for k, t in enumerate(Moves) if t[0] == (origin_x, origin_y)},

    # each cell is painted by a move that traverses it
    [y[x[i][j]] in PaintingMoves[i][j] for i, j in Cells],

    # each move is followed by a compatible one
    [(y[t], y[t + 1]) in T for t in range(horizon - 1)],

    # avoiding wasting time
    [
        If(
            y[t] == -1,
            Then=y[t + 1] == -1
        ) for t in range(horizon - 1)
    ],

    # computing z
    [
        y[z] != -1,
        y[z + 1] == -1
    ],

    # tag(symmetry-breaking)
    [
        If(
            x[i][j] > t,
            Then=y[t] not in PaintingMoves[i][j]
        ) for i, j in Cells for t in range(horizon - 1)
    ]
)

minimize(
    z
)

""" Comments
1) Compilation example:  python3 RollerSplat.py -data=[inst7b.json,h=40]
"""
