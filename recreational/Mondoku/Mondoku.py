"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
The original mzn model was written by Mikael Zayenz Lagerkvist (MIT Licence).

## Data
  three integers denoting width, height and number of colors

## Model
  constraints: Cardinality, Maximum, Minimum, Precedence

## Execution
  python Mondoku.py -data=[number,number,number]

## Links
  - https://www.reddit.com/r/generative/comments/1fxp5ng/irregular_mondoku_art/
  - https://www.minizinc.org/challenge2025/results2025.html

## Tags
  academic, recreational, mzn25
"""

from pycsp3 import *

mzn25 = [(8, 8, 4), (10, 10, 6), (12, 12, 8), (14, 14, 8), (20, 18, 9)]

W, H, C = data or (8, 8, 4)  # width, height and number of  colors

# x[w][h] is the color in the matrix in cell (w,h)
x = VarArray(size=[W, H], dom=range(1, C + 1))

# across[w][h] is a color (index) if it is the start of a group across the grid (0 otherwise)
across = VarArray(size=[W, H], dom=range(0, C + 1))

# down[w][h] is a color (index) if it is the start of a group down the grid (0 otherwise)
down = VarArray(size=[W, H], dom=range(0, C + 1))

# occ_across[h][c] is the number of occurrences of color c across height h
occ_across = VarArray(size=[H, C], dom=range(W + 1))

# occ_down[w][c] is the number of occurrences of color c down width w
occ_down = VarArray(size=[W, C], dom=range(H + 1))

# diff_across[h] is the maximal difference of color occurrences across height h
diff_across = VarArray(size=H, dom=range(W + 1))

# diff_down[w] is the maximal difference of color occurrences down width w
diff_down = VarArray(size=W, dom=range(H + 1))

satisfy(

    # computing starts of groups (other values set to 0)
    [
        [
            across[0] == x[0],
            [across[w][h] == ift(x[w - 1][h] != x[w][h], x[w][h], 0) for w in range(1, W) for h in range(H)]
        ],

        [
            down[:, 0] == x[:, 0],
            [down[w][h] == ift(x[w][h - 1] != x[w][h], x[w][h], 0) for w in range(W) for h in range(1, H)]
        ]
    ],

    # ensuring all colors are present
    [
        [Cardinality(within=across[:, h], occurrences={0: W - C} | {v: 1 for v in range(1, C)}) for h in range(H)],
        [Cardinality(within=down[h], occurrences={0: H - C} | {v: 1 for v in range(1, C)}) for h in range(W)]
    ],

    # computing color occurrences
    [
        [Cardinality(within=x[:, h], occurrences={v: occ_across[h][v - 1] for v in range(1, C + 1)}) for h in range(H)],
        [Cardinality(within=x[w], occurrences={v: occ_down[w][v - 1] for v in range(1, C + 1)}) for w in range(W)]
    ],

    # computing maximal differences of color occurrences
    [
        [diff_across[h] == Maximum(occ_across[h]) - Minimum(occ_across[h]) for h in range(H)],
        [diff_down[w] == Maximum(occ_down[w]) - Minimum(occ_down[w]) for w in range(H)]
    ],

    # colors are interchangeable tag(symmetry-breaking)
    Precedence(x)
)

minimize(
    #  minimizing the maximum difference for any row or column (as one way to keep it all balanced)
    Maximum(diff_across + diff_down)
)
