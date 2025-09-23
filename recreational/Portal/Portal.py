"""
Portal game.

From the introduction of the model submitted to the 2024 mzn challenge.
The game is played on a 2D grid. The player can move up, down, left, or right.
The player can also shoot a portal in any direction. The portal will travel in a straight line until it hits a wall.
The player can then shoot a second portal. If they move onto a portal, they will be teleported to the other portal.
If they shoot a third portal, the first portal will disappear.
The player can only shoot one portal at a time. The player can only have two portals on the board at a time.
The player can only move one square at a time.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  rand-10-9-010.json

## Model
  constraints: Element, Table

## Execution
  python Portal.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  recreational, mzn24
"""

from pycsp3 import *
from pycsp3.dashboard import options

#  option set to avoid writing ((aux := Var()) == z - 1, a[aux] == MOVE)
#  instead of a[z - 1] == MOVE
options.force_element_index = True

board, k = data
n, m = len(board), len(board[0])

PLAYER_NORTH, PLAYER_SOUTH, PLAYER_EAST, PLAYER_WEST, WALL, WALL_NO_PORTAL, EMPTY, PIT, GOAL = cells = ('^', 'v', '>', '<', 'X', 'N', ' ', 'O', '!')
NORTH, SOUTH, EAST, WEST = headings = range(4)
LEFT, RIGHT, MOVE, SHOOT = actions = range(4)
nHeadings, nActions = len(headings), len(actions)

init = next(((i, j) for i in range(n) for j in range(m) if board[i][j] in (PLAYER_NORTH, PLAYER_SOUTH, PLAYER_EAST, PLAYER_WEST)), -1)
goal = next(((i, j) for i in range(n) for j in range(m) if board[i][j] == GOAL), -1)
assert init != -1 and goal != -1
init_heading = cells.index(board[init[0]][init[1]])

accessible = cp_array([[1 if board[i][j] in (EMPTY, PLAYER_NORTH, PLAYER_SOUTH, PLAYER_EAST, PLAYER_WEST, GOAL) else 0 for j in range(m)] for i in range(n)])

# next heading wrt a heading (first dimension) and an action (second dimension)
next_heading = cp_array([[WEST, EAST, NORTH, NORTH], [EAST, WEST, SOUTH, SOUTH], [NORTH, SOUTH, EAST, EAST], [SOUTH, NORTH, WEST, WEST]])


def wphor(i, j, h):
    if h == EAST:
        return next((k for k in range(j + 1, m) if board[i][k] in (WALL, WALL_NO_PORTAL)), -1)
    if h == WEST:
        return next((k for k in range(j - 1, -1, -1) if board[i][k] in (WALL, WALL_NO_PORTAL)), -1)
    return j


def wpver(i, j, h):
    if h == NORTH:
        return next((k for k in range(i - 1, -1, -1) if board[k][j] in (WALL, WALL_NO_PORTAL)), -1)
    if h == SOUTH:
        return next((k for k in range(i + 1, n) if board[k][j] in (WALL, WALL_NO_PORTAL)), -1)
    return i


Tw = [(i, j, h, ii if valid else -1, jj if valid else -1) for i in range(n) for j in range(m) for h in range(nHeadings)
      if (ii := wpver(i, j, h), jj := wphor(i, j, h), valid := ii != -1 and jj != -1 and board[ii][jj] == WALL)]

Td = [(i, j, h, ii if valid else -1, jj if valid else -1) for i in range(n) for j in range(m) for h in range(nHeadings)
      if (ii := i + (1 if h == SOUTH else -1 if h == NORTH else 0),
          jj := j + (1 if h == EAST else -1 if h == WEST else 0),
          valid := 0 <= ii < n and 0 <= jj < m)]

# x[i] is the position of the player on the x-axis at the ith step
x = VarArray(size=k, dom=range(n))

# y[i] is the position of the player on the y-axis at the ith step
y = VarArray(size=k, dom=range(m))

# h[i] is the heading of the player at the ith step
h = VarArray(size=k, dom=range(nHeadings))

# a[i] is the action of the player at the ith step
a = VarArray(size=k - 1, dom=range(nActions))

# px[k][i] is the position of the kth portal on the x-axis at the ith step
px = VarArray(size=[2, k], dom=range(-1, n))

# py[k][i] is the position of the kth portal on the y-axis at the ith step
py = VarArray(size=[2, k], dom=range(-1, m))

# nwx[i] is the position of the first meetable wall on the x-asis at the ith step
nwx = VarArray(size=k - 1, dom=range(-1, n))

# nwy[i] is the position of the first meetable wall on the y-asis at the ith step
nwy = VarArray(size=k - 1, dom=range(-1, m))

# dx[i] is the position of the player on the x-axis if moved at the ith step
dx = VarArray(size=k - 1, dom=range(-1, n + 1))

# dy[i] is the position of the player on the y-axis if moved at the ith step
dy = VarArray(size=k - 1, dom=range(-1, m + 1))

# z is the number of actions to reach the goal
z = Var(dom=range(k + 1))

# acc[i] is 1 if the next cell is accessible when moving at the ith step
acc = VarArray(size=k - 1, dom={0, 1})

satisfy(
    # some initialization
    [
        x[0] == init[0],
        y[0] == init[1],
        x[-1] == goal[0],
        y[-1] == goal[1],

        h[0] == init_heading,

        px[0][0] == -1,
        px[1][0] == -1,
        py[0][0] == -1,
        py[1][0] == -1
    ],

    # avoiding pits
    [(x[t], y[t]) in [(i, j) for i in range(n) for j in range(m) if board[i][j] != PIT] for t in range(k)],

    # ensuring that portals are different
    [
        If(
            px[0][t] != -1,
            Then=either(px[0][t] != px[1][t], py[0][t] != py[1][t])
        ) for t in range(k - 1)
    ],

    # computing new headings
    [h[t + 1] == next_heading[h[t]][a[t]] for t in range(k - 1)],

    # computing next reachable walls
    [(x[t], y[t], h[t], nwx[t], nwy[t]) in Tw for t in range(k - 1)],

    # computing next positions
    [(x[t], y[t], h[t], dx[t], dy[t]) in Td for t in range(k - 1)],

    # computing accessibility if moving
    [acc[t] == accessible[dx[t], dy[t]] for t in range(k - 1)],

    # managing action 'move'
    [
        If(
            a[t] == MOVE,
            Then=If(
                px[1][t] != -1,  # if two portals
                Then=If(
                    dx[t] == px[0][t], dy[t] == py[0][t],
                    Then=[x[t + 1] == px[1][t], y[t + 1] == py[1][t]],
                    Else=If(
                        dx[t] == px[1][t], dy[t] == py[1][t],
                        Then=[x[t + 1] == px[0][t], y[t + 1] == py[0][t]],
                        Else=[acc[t], x[t + 1] == dx[t], y[t + 1] == dy[t]]
                    )
                ),
                Else=[acc[t], x[t + 1] == dx[t], y[t + 1] == dy[t]]
            ),
            Else=[x[t + 1] == x[t], y[t + 1] == y[t]]
        ) for t in range(k - 1)
    ],

    # managing action 'shoot'
    [
        If(
            a[t] == SHOOT, nwx[t] != -1,
            Then=[px[0][t + 1] == nwx[t], py[0][t + 1] == nwy[t], px[1][t + 1] == px[0][t], py[1][t + 1] == py[0][t]],
            Else=[px[0][t + 1] == px[0][t], py[0][t + 1] == py[0][t], px[1][t + 1] == px[1][t], py[1][t + 1] == py[1][t]]
        ) for t in range(k - 1)
    ],

    # computing z
    [x[z] == goal[0], y[z] == goal[1]],

    # tag(symmetry-breaking)
    [
        a[z - 1] == MOVE,

        [
            If(
                t >= z,
                Then=[
                    x[t] == goal[0],
                    y[t] == goal[1],
                    a[t] == LEFT
                ]
            ) for t in range(k - 1)

        ],

        [a[t:t + 2] not in {(LEFT, RIGHT), (RIGHT, LEFT)} for t in range(k - 2)],

        [a[t:t + 3] not in {(RIGHT, RIGHT, RIGHT)} for t in range(k - 3)]  # (LEFT, LEFT, LEFT) is not compatible with imposed action LEFT after z
    ]
)

minimize(
    # minimizing the number of steps
    z + 1
)
