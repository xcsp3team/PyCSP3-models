"""
From LPCP contest 2021 (Problem 1):
    The problem is based on the Crazy Frog Puzzle.
    You have the control of a little frog, capable of very long jumps.
    The little frog just woke up in an SxS land, with few obstacles and a lot of insects.
    The frog can jump as long as you want, but only in the four cardinal directions (don't ask why) and you cannot land on any obstacle or already visited places.

Important: the model, below, has not been checked to exactly correspond to this statement (it was written for the 2025 XCSP3 competition).

## Data Example
  06.json

## Model
  constraints: AllDifferent, Circuit, Table

## Execution
  python CrazyFrog.py -data=<datafile.json>
  python CrazyFrog.py -data=<datafile.json> -variant=table

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2021/tree/main/problem-1
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  recreational, lpcp21, xcsp25
"""

from pycsp3 import *

assert not variant() or variant("table")

frog, grid = data or load_json_data("06.json")

n = len(grid)

zeros = [tuple(frog)] + [(i, j) for i in range(n) for j in range(n) if grid[i][j] == 0 and (i, j) != tuple(frog)]
nZeros = len(zeros)

compatible_zeros = [(k, l) for k in range(nZeros) for l in range(nZeros) if k != l and (zeros[k][0] == zeros[l][0] or zeros[k][1] == zeros[l][1])]

if not variant():
    # x[i] is the zero that follows the ith zero
    x = VarArray(size=nZeros, dom=lambda i: {l for k, l in compatible_zeros if k == i} | ({0} if i != 0 else set()))

    satisfy(
        # ensuring a circuit
        Circuit(x),
    )

elif variant('table'):

    # x[i] is the ith zero visited by the frog
    x = VarArray(size=nZeros, dom=range(nZeros))

    satisfy(
        x[0] == 0,

        AllDifferent(x),

        [(x[i], x[i + 1]) in compatible_zeros for i in range(nZeros - 1)]
    )

""" Comments
1) model to be checked wrt lpcpc21
2) Choco seems far more efficient than ACE on the main variant
"""
