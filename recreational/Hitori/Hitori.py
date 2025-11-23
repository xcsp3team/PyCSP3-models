"""
Hitori

You have to shade some of the cells of a given grid according to the following rules:
 1. No number should appear unshaded more than once in a row or a column.
 2. Two shaded cells cannot be adjacent horizontally or vertically.
 3. All non-shaded cells should be connected in a single group by vertical or horizontal motion.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenges.
For the original mzn model, no Licence was explicitly mentioned (MIT Licence assumed).

Important: this PyCSP3 model is rather different from the mzn model as connectedness is encoded differently.


## Data Example
  h11-1.json

## Model
  constraints: AllDifferent, Count, Sum, Table

## Execution
  python Hitori.py -data=<datafile.json>
  python Hitori.py -data=<datafile.dzn> -parser=Hitori_ParserZ.py

## Links
  - https://www.puzzle-hitori.com/
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  recreational, mzn25
"""

from pycsp3 import *

clues = data or [[4, 2, 4, 3, 1], [3, 2, 1, 2, 2], [4, 5, 3, 1, 2], [2, 2, 5, 3, 3], [1, 3, 4, 5, 4]]

n = len(clues)
N = range(n)


def table(r):
    return [(-1, *[ANY] * r), (0, *[ANY] * r)] + [tuple([v] + [v - 1 if k == q else ANY for q in range(r)]) for v in range(1, 2 * n) for k in range(r)]


# shaded[i][j] is 1 if the cell (i,j) of the grid is shaded
shaded = VarArray(size=[n, n], dom={0, 1})

# x[i][j] is the value in the cell (i,j) of the grid ; 0 if shaded
x = VarArray(size=[n, n], dom=range(n + 1))

# the x-coordinate of the root of the covering tree
rootx = Var(dom=range(n))

# the y-coordinate of the root of the covering tree
rooty = Var(dom=range(n))

# rootd[i][j] is the distance between the cell (i,j) (if not shaded) and the root ; -1 if shaded
rootd = VarArray(size=[n, n], dom=range(-1, 4 * n))

satisfy(
    # computing x
    [x[i][j] == ift(shaded[i][j], 0, clues[i][j]) for i in N for j in N],

    # if two identical clues are adjacent then all equal clue values in the row/col have to be shaded
    [
        [
            [shaded[i][k] == 1 for k in N if k not in (j, j + 1) and clues[i][k] == clues[i][j]]
            for i in N for j in N[:- 1] if clues[i][j] == clues[i][j + 1]
        ],
        [
            [shaded[k][j] == 1 for k in N if k not in (i, i + 1) and clues[k][j] == clues[i][j]]
            for i in N[:- 1] for j in N if clues[i][j] == clues[i + 1][j]
        ]
    ],

    #  a cell between two identical cells cannot be shaded
    [
        [shaded[i][j] == 0 for i in N[1:- 1] for j in N if clues[i - 1][j] == clues[i + 1][j]],
        [shaded[i][j] == 0 for i in N for j in N[1:- 1] if clues[i][j - 1] == clues[i][j + 1]]
    ],

    # handling simple corners
    [
        [shaded[0][0] == 1 if clues[0][0] == clues[0][1] == clues[1][0] else None],
        [shaded[0][-1] == 1 if clues[0][-1] == clues[0][-2] == clues[1][-1] else None],
        [shaded[-1][0] == 1 if clues[-1][0] == clues[-1][1] == clues[-2][0] else None],
        [shaded[-1][-1] == 1 if clues[-1][-1] == clues[-2][-1] == clues[-1][-2] else None],
    ],

    # no number should appear unshaded more than once in a row or a column
    [
        [AllDifferent(x[i], excepting=0) for i in N],
        [AllDifferent(x[:, j], excepting=0) for j in N]
    ],

    # no adjacent shaded cells
    [
        [either(shaded[i][j] == 0, shaded[i][j + 1] == 0) for i in N for j in N[:- 1]],
        [either(shaded[i][j] == 0, shaded[i + 1][j] == 0) for i in N[:- 1] for j in N]
    ],

    # ensuring a single root
    Count(rootd, value=0) == 1,

    # setting the root
    rootd[rootx][rooty] == 0,  # distance 0

    # setting the distance of shaded cells to -1
    [(rootd[i][j] == -1) == shaded[i][j] for i in N for j in N],

    # ensuring connectedness (covering tree)
    [scp in T for i in N for j in N if (scp := rootd.cross(i, j), T := table(len(scp) - 1))]
)

maximize(
    shaded * clues
)

""" Comments
1) shaded * clues  
 is equivalent to  
   Sum(shaded[i][j] * clues[i][j] for i in range(n) for j in range(n))
"""

# # #  never black out clues that appear once in row and column  // commented in MZN
# [shaded[i][j] == 0 for i in range(n) for j in range(n) if
#  len([k for k in range(n) if clues[i][j] == clues[i][k]]) == len([k for k in range(n) if clues[i][j] == clues[k][j]]) == 1],


# [x[i][j] == (~filled[i][j]) * clues[i][j] for i in range(n) for j in range(n)],
# [x[i][j] == ((filled[i][j] == 0) * clues[i][j]) for i in range(n) for j in range(n)],
# [x[i][j] == ift(filled[i][j], 0, clues[i][j]) for i in range(n) for j in range(n)],
