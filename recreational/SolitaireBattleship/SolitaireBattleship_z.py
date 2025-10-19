"""
Solitaire Battleships
A puzzle where we are given a partially filled-in board and the number of ships in each row and column and have to fill it with ships.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Peter Stuckey.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  12-12-5-1.json

## Model
  constraints: Sum

## Execution
  python SolitaireBattleship_z.py -data=<datafile.json>
  python SolitaireBattleship_z.py -data=<datafile.dzn> -parser=SolitaireBattleship_ParserZ.py

## Links
  - http://www.csee.umbc.edu/courses/671/fall09/resources/smith06.pdf
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  recreational, mzn10, mzn11, mzn12, mzn14, mzn16
"""

from pycsp3 import *

ships, hints, rsums, csums = data or load_json_data("12-12-5-1.json")

n, maxShip = len(hints), len(ships)

submarine, destroyer, cruiser, battleship = range(4)
WATER, SUB, LEFT, RIGHT, TOP, BOT, MID = pieces = range(7)  # Sub for submarine, left right top bottom of ship, middle of ship
nPieces = len(pieces)

cells = [(i, j) for i in range(1, n + 1) for j in range(1, n + 1)]


def pred(s, i, j):
    term1 = conjunction(
        x[i][j] == LEFT,
        x[i][j + s - 1] == RIGHT,
        x[i][j + 1: j + s - 1] == MID  # equivalent to [x[i][k] == MID for k in range(j + 1, j + s - 1)]
    ) if j + s - 1 <= n else False
    term2 = conjunction(
        x[i][j] == TOP,
        x[i + s - 1][j] == BOT,
        x[:, j][i + 1: i + s - 1] == MID  # equivalent to [x[k][j] == MID for k in range(i + 1, i + s - 1)]
    ) if i + s - 1 <= n else False
    return term1 | term2


# x[i][j] is the piece (state) put in cell with coordinates (i,j)
x = VarArray(size=[n + 2, n + 2], dom=lambda i, j: {WATER} if i in {0, n + 1} or j in {0, n + 1} else pieces)

# occ[i][j] is 1 if the cell at coordinates (i,j) is occupied
occ = VarArray(size=[n + 2, n + 2], dom={0, 1})

# cnt[k] is the number (count) of cells with piece k
cnt = VarArray(size=nPieces, dom=range(n * n + 1))

satisfy(
    # respecting hints
    [x[i][j] == hints[i - 1][j - 1] - 1 for i, j in cells if hints[i - 1][j - 1] != 0],

    # determining which cells are occupied
    [occ[i][j] == (x[i][j] != WATER) for i in range(n + 2) for j in range(n + 2)],

    # ensuring gaps between ships
    [
        (
            If(x[i][j] != WATER, Then=x[i + 1][j + 1] == WATER),
            If(x[i][j] != WATER, Then=x[i + 1][j - 1] == WATER),
            If(x[i][j] in {SUB, LEFT, RIGHT, TOP}, Then=x[i - 1][j] == WATER),
            If(x[i][j] in {SUB, LEFT, RIGHT, BOT}, Then=x[i + 1][j] == WATER),
            If(x[i][j] in {SUB, LEFT, TOP, BOT}, Then=x[i][j - 1] == WATER),
            If(x[i][j] in {SUB, RIGHT, TOP, BOT}, Then=x[i][j + 1] == WATER)
        ) for i, j in cells
    ],

    # ensuring coherent successive pieces
    [
        Match(
            x[i][j],
            Cases={
                LEFT: x[i][j + 1].among(RIGHT, MID),  # Do not use in inside Match!
                RIGHT: x[i][j - 1].among(LEFT, MID),
                TOP: x[i + 1][j].among(BOT, MID),
                BOT: x[i - 1][j].among(TOP, MID),
                MID: [  # this is a conjunction
                    occ[i - 1][j] == occ[i + 1][j],
                    occ[i][j - 1] == occ[i][j + 1],
                    occ[i - 1][j] + occ[i][j - 1] == 1
                ]
            }
        ) for i, j in cells
    ],

    # counting pieces
    [cnt[k] == Sum(x[i][j] == k for i, j in cells) for k in range(nPieces)],

    # checking the number of pieces
    [
        cnt[SUB] == ships[submarine],
        cnt[LEFT] == cnt[RIGHT],
        cnt[TOP] == cnt[BOT],
        cnt[LEFT] + cnt[TOP] == sum(ships[destroyer:]),
        cnt[MID] == sum(ships[s] * (s - 1) for s in range(cruiser, maxShip))
    ],

    # ensuring connected ships
    [Sum(pred(s + 1, i, j) for i, j in cells) == ships[s] for s in range(destroyer, maxShip)],

    # respecting sums on rows and columns
    [
        [Sum(occ[i]) == rsums[i - 1] for i in range(1, n + 1)],
        [Sum(occ[:, j]) == csums[j - 1] for j in range(1, n + 1)]
    ]
)

""" Comments
0) WARNING : do not use in with Match, because it becomes difficult to handle the stuff posted for the 'in' operator
   Currently, we don't handle it.
1) Some equivalent ways to write groups of constraints above is : 
    # ensuring gaps between ships
    [
        [(x[i][j] == WATER) | (x[i + 1][j + 1] == WATER) for i, j in cells],
        [(x[i][j] == WATER) | (x[i + 1][j - 1] == WATER) for i, j in cells],
        [If(belong(x[i][j], (SUB, LEFT, RIGHT, TOP)), Then=x[i - 1][j] == WATER) for i, j in cells],
        [If(belong(x[i][j], (SUB, LEFT, RIGHT, BOT)), Then=x[i + 1][j] == WATER) for i, j in cells],
        [If(belong(x[i][j], (SUB, LEFT, TOP, BOT)), Then=x[i][j - 1] == WATER) for i, j in cells],
        [If(belong(x[i][j], (SUB, RIGHT, TOP, BOT)), Then=x[i][j + 1] == WATER) for i, j in cells]
    ],
    
    # ensuring coherent successive pieces
    [
        [(x[i][j] != LEFT) | (x[i][j + 1] == RIGHT) | (x[i][j + 1] == MID) for i, j in cells],
        [(x[i][j] != RIGHT) | (x[i][j - 1] == LEFT) | (x[i][j - 1] == MID) for i, j in cells],
        [(x[i][j] != TOP) | (x[i + 1][j] == BOT) | (x[i + 1][j] == MID) for i, j in cells],
        [(x[i][j] != BOT) | (x[i - 1][j] == TOP) | (x[i - 1][j] == MID) for i, j in cells],
        [(x[i][j] != MID) | ((f[i - 1][j] == f[i + 1][j]) & (f[i][j - 1] == f[i][j + 1]) & (f[i - 1][j] + f[i][j - 1] == 1)) for i, j in cells]
    ],
"""

# MID: (occ[i - 1][j] == occ[i + 1][j]) & (occ[i][j - 1] == occ[i][j + 1]) & (occ[i - 1][j] + occ[i][j - 1] == 1)
