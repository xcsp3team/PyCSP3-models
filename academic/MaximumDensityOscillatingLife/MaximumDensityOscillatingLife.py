"""
From CP'10 paper whose URL is given below:
    Conway’s Game of Life was invented by John Horton Conway.
    The game is played on a square grid. Each cell in the grid is in one of two states (alive or dead).
    The state of the board evolves over time: for each cell, its new state is determined by its
    previous state and the previous state of its eight neighbours (including diagonal neighbours).
    Oscillators are patterns that return to their original state after a number of steps (referred to as the period).
    A period 1 oscillator is named a still life. Here we consider the problem of finding oscillators of various periods.

## Data
  two numbers n and h

## Model
  constraints: AllDifferentList, Sum, Table

## Execution
  python MaximumDensityOscillatingLife.py -data=[number,number]

## Links
  - https://link.springer.com/chapter/10.1007/978-3-642-15396-9_19
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, xcsp24
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry

n, horizon = data or (5, 5)

symmetries = [sym.apply_on(n + 2) for sym in TypeSquareSymmetry]

# x[t][i][j] is 1 iff the cell at row i and col j is alive at time t
x = VarArray(size=[horizon, n + 2, n + 2], dom=lambda t, i, j: {0} if i in (0, n + 1) or j in (0, n + 1) else {0, 1})

T = ([(ANY, *[0] * 8, 0)] +
     [(ANY, *[1 if k == k1 else 0 for k in range(8)], 0) for k1 in range(8)] +
     [(ANY, *[0 if k in (k1, k2, k3, k4) else 1 for k in range(8)], 0) for k1, k2, k3, k4 in combinations(8, 4)] +
     [(ANY, *[0 if k in (k1, k2, k3) else 1 for k in range(8)], 0) for k1, k2, k3 in combinations(8, 3)] +
     [(ANY, *[0 if k in (k1, k2) else 1 for k in range(8)], 0) for k1, k2 in combinations(8, 2)] +
     [(ANY, *[0 if k == k1 else 1 for k in range(8)], 0) for k1 in range(8)] +
     [(ANY, *[1] * 8, 0)] +
     [(ANY, *[1 if k in (k1, k2, k3) else 0 for k in range(8)], 1) for k1, k2, k3 in combinations(8, 3)] +
     [(0, *[1 if k in (k1, k2) else 0 for k in range(8)], 0) for k1, k2 in combinations(8, 2)] +
     [(1, *[1 if k in (k1, k2) else 0 for k in range(8)], 1) for k1, k2 in combinations(8, 2)]
     )

satisfy(
    # imposing rules of the game
    [(x[t][i][j], x[t].around(i, j), x[t + 1][i][j]) in T for t in range(horizon) for i in range(1, n + 1) for j in range(1, n + 1)],

    # forbidding identical states
    AllDifferentList(x[t][1:n + 1, 1:n + 1] for t in range(horizon)),  # .to_table(),

    # tag(symmetry-breaking)
    [
        [x[0] <= x[0][symmetry] for symmetry in symmetries],

        [x[0] <= x[i] for i in range(1, horizon)]
    ]
)

maximize(
    # maximizing the number of alive cells
    Sum(x)
)

""" Comments
1) For the mini-tracks, we use to_table() on AllDifferentLists and we discard symmetry breaking

2) Data used for the 2024 Competition: [(5,2), (5,3), (5,4), (5,5), (5,6), (6,2), (6,3), (6,4), (6,5), (6,6), (7,2), (7,3), (7,4), (7,5), (7,6)]
"""
