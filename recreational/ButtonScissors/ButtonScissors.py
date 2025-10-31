"""
From LPCP contest 2021 (Problem 2):
    There is a supply of buttons attached to patches, and we have to cut them out in order to complete some very expensive suits.
    Buttons in the same patch are also of mixed color, and therefore they must be properly separated after detaching.
    We have to detach buttons of the same color with a cut on cardinal directions or along diagonals.
    A cut must involve at least two buttons, and all buttons along the cut are detached, so they must have the same color.
    Given a patch with buttons, find a sequence of cuts that detaches all buttons.

## Data Example
  01.json

## Model
  constraints: Count, Maximum

## Execution
  python ButtonScissors.py -data=<datafile.json>
  python ButtonScissors.py -data=<datafile.txt> -parser=ButtonsScissors_Parser.py

## Links
  - https://github.com/lpcp-contest/lpcp-contest-2021/tree/main/problem-2
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, lpcp21, xcsp25
"""

from pycsp3 import *

nColors, patch = data or load_json_data("01.json")

n = len(patch)

nDiagonalTypes = 2 * n - 3  # number of possible downward diagonals (and, similarly, number of upward diagonals); diagonals with at least 2 cells
nCodes = 2 * n + 2 * nDiagonalTypes

Attack = namedtuple("Attack", ["code", "between"])


def attack(k1, k2):
    # returns a pair composed of an attack code, followed by a list of the cells between k1 and k2
    # (together with a Boolean indicating if it has the same value as the end cells)
    i1, j1, i2, j2 = k1 // n, k1 % n, k2 // n, k2 % n
    if k1 >= k2:
        return None  # we only need to reason with k1 < k2
    if patch[i1][j1] != patch[i2][j2]:
        return None
    if i1 == i2:  # same row
        return Attack(i1, [(i1 * n + j, patch[i1][j] == patch[i1][j1]) for j in range(min(j1, j2) + 1, max(j1, j2))])
    if j1 == j2:  # same column
        return Attack(n + j1, [(i * n + j1, patch[i][j1] == patch[i1][j1]) for i in range(min(i1, i2) + 1, max(i1, i2))])
    if abs(i1 - i2) == abs(j1 - j2):  # same diagonal
        assert i1 < i2
        if j1 < j2:  # downward diagonal
            return Attack(2 * n + (j1 - i1 + n - 2), [((i1 + k) * n + j1 + k, patch[i1 + k][j1 + k] == patch[i1][j1]) for k in range(1, i2 - i1)])
        else:  # upward diagonal
            return Attack(2 * n + nDiagonalTypes + i2 + j2 - 1, [((i2 - k) * n + j2 + k, patch[i2 - k][j2 + k] == patch[i1][j1]) for k in range(1, i2 - i1)])
    return None


attacks = [[attack(k1, k2) for k2 in range(n * n)] for k1 in range(n * n)]
P = [(k1, k2) for k1, k2 in combinations(n * n, 2) if attacks[k1][k2]]
nMaxCuts = len(P)

# x[i][j] is the time at which the cell is cut
x = VarArray(size=n * n, dom=range(nMaxCuts))

# c[i][j] is the code of the cut for cell (i,j)
c = VarArray(size=n * n, dom=range(nCodes))

satisfy(
    # unreachable cells cannot be cut together
    [x[k1] != x[k2] for k1, k2 in combinations(n * n, 2) if (k1, k2) not in P],

    # ensuring that cuts can be performed
    [
        either(
            x[k1] != x[k2],
            x[k3] <= x[k1] if same else x[k3] < x[k1]
        ) for k1, k2 in P for k3, same in attacks[k1][k2].between
    ],

    # cells cut together (at the same time) must have the same cut code
    [
        either(
            x[k1] != x[k2],
            both(c[k1] == c[k2], c[k1] == attacks[k1][k2].code)
        ) for k1, k2 in P
    ],

    # a cut must involve at least two buttons
    [Count(within=x, value=v) != 1 for v in range(nMaxCuts)]
)

minimize(
    # minimizing the number of cuts
    Maximum(x)
)
