"""
Multi-agent Collective Construction (MACC).

The multi-agent collective construction problem tasks agents to construct any given three-dimensional structure on a grid by repositioning blocks.
Agents are required to also use the blocks to build ramps in order to access the higher levels necessary to construct the building,
and then remove the ramps upon completion of the building.
See CP paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The MZN model was proposed by Edward Lam.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  037.json

## Model
  constraints: Count, Sum

## Execution
  python CollectiveConstruction.py -data=<datafile.json>
  python CollectiveConstruction.py -data=<datafile.dzn> -parser=CollectiveConstruction_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-030-58475-7_43
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  realistic, mzn20
"""

from pycsp3 import *

nAgents, horizon, width, depth, height, building = data
assert width == depth  # for simplicity, the model is built with this assumption
n = width

UNUSED, MOVE, BLOCK = actions = 0, 1, 2


def P(start=1, stop=horizon - 1):
    return ((t, i) for t in range(start, stop) for i in range(n * n))


def at_border(i):
    return i < n * n and (i // n in {0, n - 1} or i % n in {0, n - 1})


def neighbours(i, *, off=False, itself=False):
    assert 0 <= i < n * n
    row, col = i // n, i % n
    t = [(row - 1) * n + col] if 0 < row else []
    t += [(row + 1) * n + col] if row + 1 < n else []
    t += [row * n + col - 1] if 0 < col else []
    t += [row * n + col + 1] if col + 1 < n else []
    return sorted(t + ([i] if itself else []) + ([n * n, n * n + 1] if off and at_border(i) else []))


# hgt[t][i] is the height at time t of the ith position (cell)
hgt = VarArray(size=[horizon, n * n + 2],
               dom=lambda t, i: {building[i // n][i % n]} if t >= horizon - 2 and i < n * n else {0} if t < 2 or i >= n * n or at_border(i) else range(height))

# act[t][i] is the action at time t of the agent in the ith position
act = VarArray(size=[horizon, n * n + 2], dom=lambda t, i: {MOVE} if i >= n * n else {UNUSED} if t in {0, horizon - 1} and i < n * n else range(len(actions)))

# nxt[t][i] is the next position at time t of the agent in the ith position
nxt = VarArray(size=[horizon, n * n + 2], dom=lambda t, i: {i} if i >= n * n else neighbours(i, off=True, itself=True))

# car[t][i] is 1 if at time t the agent in the ith position is carrying
car = VarArray(size=[horizon, n * n + 2], dom=lambda t, i: {1} if i == n * n else {0} if i == n * n + 1 else {0, 1})

# blp[t][i] is the block position at time t of the agent in the ith position
blp = VarArray(size=[horizon, n * n], dom=lambda t, i: {i} if t in {0, horizon - 1} else neighbours(i, itself=True))

# pik[t][i] is 1 if at time t the agent in the ith position makes a pickup
pik = VarArray(size=[horizon, n * n], dom=lambda t, i: {0} if t in {0, horizon - 1} else {0, 1})

# pik[t][i] is 1 if at time t the agent in the ith position makes a delivery
dlv = VarArray(size=[horizon, n * n], dom=lambda t, i: {0} if t in {0, horizon - 1} else {0, 1})

satisfy(
    # change in height: the height of a cell evolves of at most 1 at each step
    [abs(hgt[t + 1][i] - hgt[t][i]) <= 1 for t, i in P(0, horizon - 2)],

    # agents stay at the same position when doing a block operation
    [
        If(
            act[t][i] == BLOCK,
            Then=nxt[t][i] == i
        ) for t, i in P()
    ],

    # when moving, the carrying status remains the same
    [
        If(
            act[t][i] == MOVE,
            Then=car[t + 1][nxt[t][i]] == car[t][i]
        ) for t, i in P()
    ],

    # when blocking, the carrying status is inverted
    [
        If(
            act[t][i] == BLOCK,
            Then=car[t + 1][i] != car[t][i]
        ) for t, i in P()
    ],

    # carrying status - pickup
    [pik[t][i] == both(act[t][i] == BLOCK, car[t][i] == 0) for t, i in P()],

    # carrying status - delivery
    [dlv[t][i] == both(act[t][i] == BLOCK, car[t][i] == 1) for t, i in P()],

    # flow out
    [
        either(
            act[t][i] == UNUSED,
            act[t + 1][nxt[t][i]] != UNUSED
        ) for t, i in P()
    ],

    # flow in
    [
        If(
            act[t + 1][i] != UNUSED,
            Then=Exist(both(act[t][j] != UNUSED, nxt[t][j] == i) for j in neighbours(i, itself=True))
        ) for t, i in P(0, horizon - 1) if not at_border(i)
    ],

    # vertex collision
    [

        Sum(
            [both(act[t][j] == MOVE, nxt[t][j] == i) for j in neighbours(i, itself=True)],
            act[t][i] == BLOCK,
            [both(act[t + 1][j] == BLOCK, blp[t + 1][j] == i) for j in neighbours(i)]
        ) <= 1
        for t, i in P()
    ],

    # edge collision
    [
        If(
            act[t][i] == MOVE, nxt[t][i] != i, act[t][nxt[t][i]] == MOVE,
            Then=nxt[t][nxt[t][i]] != i
        ) for t, i in P()
    ],

    # maximum number of agents
    [
        Sum(
            [act[t][i] != UNUSED for i in range(n * n)],
            [both(act[t - 1][i] == MOVE, nxt[t - 1][i] >= n * n) for i in range(n * n) if at_border(i)]
        ) <= nAgents
        for t in range(1, horizon)
    ],

    # height of move
    [
        If(
            act[t][i] == MOVE,
            Then=abs(hgt[t + 1][nxt[t][i]] - hgt[t][i]) <= 1
        ) for t, i in P(1, horizon - 2)
    ],

    # height of wait
    [
        If(
            act[t][i] == MOVE, nxt[t][i] == i,
            Then=hgt[t + 1][i] == hgt[t][i]
        ) for t, i in P(1, horizon - 2)
    ],

    # height of pickup
    [
        If(
            pik[t][i],
            Then=[
                hgt[t][blp[t][i]] == hgt[t][i] + 1,
                hgt[t][blp[t][i]] == hgt[t + 1][blp[t][i]] + 1
            ]
        ) for t, i in P(1, horizon - 2)
    ],

    # height of delivery
    [
        If(
            dlv[t][i],
            Then=[
                hgt[t][blp[t][i]] == hgt[t][i],
                hgt[t][blp[t][i]] == hgt[t + 1][blp[t][i]] - 1
            ]
        ) for t, i in P(1, horizon - 2)
    ],

    # height change
    [hgt[t + 1][i] == hgt[t][i] + Sum((blp[t][j] == i) * (dlv[t][j] - pik[t][j]) for j in neighbours(i)) for t, i in P()]
)

minimize(
    Sum(act[t][i] != UNUSED for t, i in P())
)

""" Comments
1) Not sure that the model is exactly the same as the Minizinc one. 
2) Use -dontuseauxcache when compiling (otherwise, too long)
"""
