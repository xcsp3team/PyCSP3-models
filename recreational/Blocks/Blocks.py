"""
Blocks World Puzzle

Some numbered blocks are stacked into piles. The objective is to transform a start configuration into a goal configuration
by moving one block at a time, with a minimal number of moves.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Mats Carlsson, under the MIT Licence.

## Data Example
  16-4-05.json

## Model
  constraints: Cardinality, Element

## Execution
  python Blocks.py -data=<datafile.json>
  python Blocks.py -data=<datafile.dzn> -parser=Blocks_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  recreational, mzn22
"""

from pycsp3 import *

n, nPiles, start, goal = data if data else (5, 3, [5, 0, 2, 0, 4], [2, 3, 0, 5, 0])

start, goal = [0] + start, [0] + goal
nCubes, horizon = n + 1, n * nPiles + 1  # nCubes includes the dummy cube 0

# x[i][t] is the cube that follows the ith cube at time t (or 0)
x = VarArray(size=[nCubes, horizon], dom=lambda i, t: {0} if i == 0 else range(nCubes))

# nb[i][t] is the number of times the ith cube occurs in the configuration at time t
nb = VarArray(size=[nCubes, horizon], dom=lambda i, t: {0, 1} if i > 0 else range(1, nPiles + 1))

# done[t] is 1 if the goal configuration is present at time t
done = VarArray(size=horizon, dom={0, 1})

# move[t] is a pair (v,w) indicating that w becomes the successor of v at time t
move = VarArrayMultiple(size=horizon, fields={"src": lambda t: None if t == 0 else range(nCubes), "dst": lambda t: None if t == 0 else range(nCubes)})

# locked[i][t] is 1 if the ith cube is locked at time t
locked = VarArray(size=[nCubes, horizon], dom=lambda i, t: {0} if i == 0 else {0, 1})

# z is the number of steps to achieve the goal
z = Var(dom=range(horizon))

satisfy(
    # setting start configuration
    x[:, 0] == start,

    # setting goal configuration
    x[:, -1] == goal,

    # recording new states when moving
    [move[t].dst == x[move[t].src][t] for t in range(1, horizon)],

    # computing the number of times cubes occur in configurations
    [
        Cardinality(
            within=x[1:, t],
            occurrences=nb[:, t]
        ) for t in range(horizon)
    ],

    # ensuring that we have two phases
    Increasing(done),

    # when finished, no more move
    [done[t - 1] == (move[t].src == 0) for t in range(1, horizon)],

    # handling how cubes move
    [
        If(
            done[t - 1],
            Then=x[1:, t - 1] == x[1:, t],
            Else=[
                [(x[i][t - 1] != x[i][t]) == (i == move[t].src) for i in range(nCubes)],
                nb[move[t].src][t - 1] == 0
            ]
        ) for t in range(1, horizon)
    ],

    # tag(symmetry-breaking)
    [
        # bounding the number of moves per cube
        [
            [Hamming(x[i][:-1], x[i][1:]) >= 1 for i in range(1, nCubes) if start[i] != goal[i]],
            [Hamming(x[i][:-1], x[i][1:]) <= nPiles for i in range(1, nCubes)]
        ],

        # preventing do-undo moves
        [
            If(
                ~done[t],
                Then=[
                    move[t].src != move[t + 1].src,
                    move[t].dst != move[t + 1].src,
                    move[t].dst != move[t + 1].dst,
                    move[t].src != move[t].dst
                ]
            ) for t in range(1, horizon - 1)
        ],

        # computing locked cubes
        [
            locked[i][t] == both(
                x[i][t] == goal[i],
                locked[goal[i]][t] if goal[i] != 0 else None
            ) for i in range(1, nCubes) for t in range(horizon)
        ],

        # not moving locked cubes
        [
            If(
                locked[i][t],
                Then=[
                    x[i][t + 1] == goal[i],
                    move[t + 1].src != i
                ]
            ) for i in range(1, nCubes) for t in range(horizon - 1)
        ],

        # objective lower bound
        [
            either(
                done[t],
                n - Sum(locked[:, t]) + t <= z
            ) for t in range(1, horizon)
        ]
    ],

    # computing the objective value
    z == horizon - Sum(done),
)

minimize(
    # minimizing the number of steps to achieve the goal
    z
)

""" Comments
1) [done[i] == (x[1:, i] == goal) for i in range(horizon)]
  is equivalent to:
   [done[i] == conjunction(x[j, i] == goal[j - 1] for j in range(1, n + 1)) for i in range(horizon)]  
2) The constraints about objective lower bound  seems penalizing
3) x[1:, t - 1] == x[1:, t]
 is equivalent to  [(x[i][t - 1] == x[i][t]) for i in range(1, nCubes)]
4) Hamming(x[i][:-1], x[i][1:]) >= 1
 is equivalent to
   [Sum(x[i][t - 1] != x[i][t] for t in range(1, horizon)) >= 1
"""

# # when finished, the configuration remains the same
# [(done[t - 1] == 0) | (x[i][t - 1] == x[i][t]) for t in range(1, horizon) for i in range(1, nCubes)],
#
# # ensuring the coherence of moves
# [
#     [done[t - 1] | ((x[i][t - 1] != x[i][t]) == (i == mv[t][0])) for t in range(1, horizon) for i in range(nCubes)],
#     [done[t - 1] | (nb[mv[t][0], t - 1] == 0) for t in range(1, horizon)],  # moved block must be at top
# ],

# # when finished, the state remains equal to the goal configuration
# [done[t] == (x[1:, t] == goal) for t in range(horizon)],

# locked[i][t] == (
#     x[i][t] == 0 if goal[i] == 0
#     else both(x[i][t] == goal[i], locked[goal[i]][t])
# ) for i in range(1, nCubes) for t in range(horizon)

# testing with tables as below?

# def table(i):
#     tbl = []
#     tbl.extend([(1, v, v, ANY) for v in range(nCubes)])
#     for j in range(nCubes):
#         if j != i:
#             tbl.extend([(0, v, v, j) for v in range(nCubes)])
#         else:
#             tbl.extend([(0, v, w, j) for v in range(nCubes) for w in range(nCubes) if v != w])
#     return tbl

# [(done[t - 1], x[i][t - 1], x[i][t], move[t].src) in table(i) for t in range(1, horizon) for i in range(nCubes)],
