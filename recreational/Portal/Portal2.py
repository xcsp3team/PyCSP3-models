"""
Portal game (version with VarArrayMultiple).

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
from pycsp3.functions import VarArrayMultiple
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

ABSENT = -1
init = next(((i, j) for i in range(n) for j in range(m) if board[i][j] in (PLAYER_NORTH, PLAYER_SOUTH, PLAYER_EAST, PLAYER_WEST)), ABSENT)
goal = next(((i, j) for i in range(n) for j in range(m) if board[i][j] == GOAL), ABSENT)
assert init != ABSENT and goal != ABSENT
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

# pos[i] is the position of the player at the ith step
pos = VarArrayMultiple(size=k, fields={"x": range(n), "y": range(n)})

# h[i] is the heading of the player at the ith step
h = VarArray(size=k, dom=range(nHeadings))

# a[i] is the action of the player at the ith step
a = VarArray(size=k - 1, dom=range(nActions))

# p1[i] is the position of the first portal at the ith step
p1 = VarArrayMultiple(size=k, fields={"x": range(-1, n), "y": range(-1, m)})

# p2[i] is the position of the second portal at the ith step
p2 = VarArrayMultiple(size=k, fields={"x": range(-1, n), "y": range(-1, m)})

# wall[i] is the position of the first meetable wall at the ith step
wall = VarArrayMultiple(size=k - 1, fields={"x": range(-1, n), "y": range(-1, m)})

# delt[i] is the position of the player if moved at the ith step
delt = VarArrayMultiple(size=k - 1, fields={"x": range(-1, n + 1), "y": range(-1, m + 1)})

# z is the number of actions to reach the goal
z = Var(dom=range(k + 1))

# acc[i] is 1 if the next cell is accessible when moving at the ith step
acc = VarArray(size=k - 1, dom={0, 1})

satisfy(
    # some initializations
    [
        pos[0] == init,
        pos[-1] == goal,

        h[0] == init_heading,

        p1[0] == ABSENT,
        p2[0] == ABSENT
    ],

    # avoiding pits
    [pos[t] in {(i, j) for i in range(n) for j in range(m) if board[i][j] != PIT} for t in range(k)],

    # ensuring that portals are different
    [
        If(
            p1[t].x != ABSENT,  # if at least one portal
            Then=p1[t] != p2[t]
        ) for t in range(k - 1)
    ],

    # computing next headings
    [h[t + 1] == next_heading[h[t]][a[t]] for t in range(k - 1)],

    # computing next reachable walls
    [(pos[t], h[t], wall[t]) in Tw for t in range(k - 1)],

    # computing next positions
    [(pos[t], h[t], delt[t]) in Td for t in range(k - 1)],

    # computing accessibility if moving
    [acc[t] == accessible[delt[t]] for t in range(k - 1)],

    # managing action 'move'
    [
        If(
            a[t] == MOVE,
            Then=If(
                p2[t].x != ABSENT,  # if two portals
                Then=If(
                    delt[t] == p1[t],
                    Then=pos[t + 1] == p2[t],
                    Else=If(
                        delt[t] == p2[t],
                        Then=pos[t + 1] == p1[t],
                        Else=[acc[t], pos[t + 1] == delt[t]]
                    )
                ),
                Else=[acc[t], pos[t + 1] == delt[t]]
            ),
            Else=pos[t + 1] == pos[t]
        ) for t in range(k - 1)
    ],

    # managing action 'shoot'
    [
        If(
            a[t] == SHOOT, wall[t].x != ABSENT,
            Then=[p1[t + 1] == wall[t], p2[t + 1] == p1[t]],
            Else=[p1[t + 1] == p1[t], p2[t + 1] == p2[t]]
        ) for t in range(k - 1)
    ],

    # computing z
    pos[z] == goal,

    # tag(symmetry-breaking)
    [
        a[z - 1] == MOVE,

        [
            If(
                t >= z,
                Then=[
                    pos[t] == goal,
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

"""
1) should we be careful about acc[t] == accessible[delt[t]] 
"""

# pos.x == [int(v) for v in
#           "4 4 4 4 4 4 4 4 3 3 3 3 2 2 2 2 2 2 1 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2".split(
#               " ")]
