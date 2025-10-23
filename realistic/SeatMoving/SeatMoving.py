"""
The problem is to move a person from a start position to a goal position.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
The original MZN model was proposed by Toshimitsu Fujiwara - no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  sm-10-12-00.json

## Model
  constraints: AllDifferent, Element, Sum, Table

## Execution
  python SeatMoving.py -data=sm-10-13-00.json
  python SeatMoving.py -data=sm-10-13-00.dzn -parser=SeatMoving_ParserZ.py

## Links
  - www.minizinc.org/challenge/2021/results/

## Tags
  realistic, mzn18, mzn21
"""

from pycsp3 import *

nPersons, seats, swaps = data or load_json_data("sm-10-12-00.json")

start, goal = zip(*seats)

nSeats = len(seats)
horizon = (2 * nSeats) // (nSeats - nPersons + 1) + 1  # maximum number of steps
H, P = range(horizon), range(nPersons)

# x[t][i] is the person at the ith seat at time t (-1 means 'empty seat')
x = VarArray(size=[horizon, nSeats], dom=range(-1, nPersons))

# y[t][j] is the seat for the jth person at time t
y = VarArray(size=[horizon, nPersons], dom=range(nSeats))

# z1 is the number of steps for reaching the goal
z1 = Var(dom=range(horizon + 1))

# z2 is the sum of moving costs
z2 = Var(dom=range(nPersons * horizon + 1))


def move(t, j):
    if not swaps[j]:
        return x[t][y[t + 1][j]] == -1
    return either(
        y[t][j] == y[t + 1][x[t][y[t + 1][j]]],
        x[t][y[t + 1][j]] == -1
    )


satisfy(
    # binding initial and last seating
    [
        x[0] == start,
        x[-1] == goal
    ],

    # binding persons and seats
    [x[t][y[t][j]] == j for t in H for j in P],

    # ensuring different persons at any time
    [AllDifferent(x[t], excepting=-1) for t in H],

    # tag(redundant)
    [AllDifferent(y[t]) for t in H],

    # computing overall moving cost
    z2 == Sum(y[t][j] != y[t + 1][j] for t in H[:-1] for j in P),

    # not moving after all seats are fixed
    [
        If(
            z1 <= t,
            Then=x[t] == goal
        ) for t in H
    ],

    # managing allowed moves
    [
        If(
            y[t][j] != y[t + 1][j],
            Then=move(t, j)
        ) for t in H[:-1] for j in P
    ]
)

minimize(
    z1 * nPersons * horizon + z2
)

""" Comments
1) Minizinc 2018 and 2021: same model/file except a compact way of defining the upper bound of the objective; does not change anything
"""
