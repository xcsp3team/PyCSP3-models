"""
A knight's tour is a sequence of moves of a knight on a chessboard such that the knight visits every square exactly once.
If the knight ends on a square that is one knight's move from the beginning square,
the tour is closed (or re-entrant); otherwise, it is open.

## Data
  A unique integer, the order of the problem instance

## Model
  constraints: Circuit

## Execution
  python KnightTour2.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Knight%27s_tour
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, recreational, xcsp22
"""

from pycsp3 import *

n = data or 8


def domain_x(i):
    r, c = i // n, i % n
    t = [(r - 2, c - 1), (r - 2, c + 1), (r - 1, c - 2), (r - 1, c + 2), (r + 1, c - 2), (r + 1, c + 2), (r + 2, c - 1), (r + 2, c + 1)]
    return {k * n + l for (k, l) in t if 0 <= k < n and 0 <= l < n}


# x[i] is the cell number that comes in the tour (by the knight) after cell i
x = VarArray(size=n * n, dom=domain_x)

satisfy(
    # the knights form a circuit (tour)
    Circuit(x),

    # the first move is set  tag(symmetry-breaking)
    x[0] == n + 2
)
