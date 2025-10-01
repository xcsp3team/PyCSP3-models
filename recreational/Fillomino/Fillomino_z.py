"""
Fillomino is played on a rectangular grid, with some cells containing numbers.
The goal is to divide the grid into regions called polyominoes (by filling in their boundaries)
such that each given number n in the grid satisfies the following constraints:
  - each clue n is part of a polyomino of size n
  - no two polyominoes of matching size (number of cells) are orthogonally adjacent (share a side)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2011/2014 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  08.json

## Model
  constraints: Element, Sum

## Execution
  python Fillomino_z.py -data=<datafile.json>
  python Fillomino_z.py -data=<datafile.dzn> -parser=Fillomino_ParserZ.py

## Links
  - https://en.wikipedia.org/wiki/Fillomino
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  recreational, mzn09, mzn11, mzn14
"""

from pycsp3 import *

puzzle = data or load_json_data("08.json")

n, m = len(puzzle), len(puzzle[0])

horizon = min(9, n + m) + 1


def join(r, c):
    return [
        AllHold(  # TODO test AllHold vs conjunction
            when[r][c] == 1 + when[rr][cc],
            area[r][c] == area[rr][cc],
            what[r][c] == what[rr][cc]
        ) for rr, cc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)] if 0 <= rr < n and 0 <= cc < m
    ]


same_in_range = [
    [sum(puzzle[rr][cc] == puzzle[r][c] for rr in range(n) for cc in range(m) if (rr > r or rr == r and cc > c) and abs(rr - r) + abs(cc - c) < puzzle[r][c])
     for c in range(m)] for r in range(n)
]

# size[k] is the size of the area k
size = VarArray(size=n * m, dom=range(n * m + 1))

# area[i][j] is the area owning the cell at coordinates (i,j)
area = VarArray(size=[n, m], dom=range(n * m))

# when[i][j] is the time at which the cell at coordinates (i,j) is fixed
when = VarArray(size=[n, m], dom=range(horizon))

# what[i][j] is the number in cell at coordinates (i,j)
what = VarArray(size=[n, m], dom=range(1, 10))

satisfy(
    # setting clues
    [what[i][j] == puzzle[i][j] for i in range(n) for j in range(m) if puzzle[i][j] > 0],

    # setting unambiguous roots at time 0
    [
        (
            when[i][j] == 0,
            area[i][j] == i * m + j
        ) for i in range(n) for j in range(m) if puzzle[i][j] > 0 and same_in_range[i][j] == 0
    ],

    # each cell contains the number corresponding to the size of its area
    [what[i][j] == size[area[i][j]] for i in range(n) for j in range(m)],

    # each area size is the number of cells in that area
    [size[k] == Sum(area[i][j] == k for i in range(n) for j in range(m)) for k in range(n * m)],

    # each cell is either the root of an area or is an extension of a neighbouring cell
    [
        If(
            when[i][j] == 0,
            Then=area[i][j] == i * m + j,
            Else=AtLeastOne(join(i, j))  # TODO test AtLeastOne vs disjunction
        ) for i in range(n) for j in range(m)
    ],

    # the distance to the area root of a cell cannot be larger than the size of the area
    [when[i][j] <= size[area[i][j]] for i in range(n) for j in range(m)],

    # neighbouring areas must have different sizes
    [
        [(x != y) == (size[x] != size[y]) for i in range(n) for j in range(1, m) if (x := area[i][j - 1], y := area[i][j])],
        [(x != y) == (size[x] != size[y]) for i in range(1, n) for j in range(m) if (x := area[i - 1][j], y := area[i][j])]
    ]
)

""" Comments

1) Note that:
  [(x != y) == (size[x] != size[y]) for i in range(n) for j in range(1, m) if (x := area[i][j - 1]) and (y := area[i][j])]
is equivalent to:
  [(area[i][j - 1] != area[i][j]) == (size[area[i][j - 1]] != size[area[i][j]]) for i in range(n) for j in range(1, m)]

2) Instead of posting the If statement, we could write:
  [((when[i][j] == 0) & (area[i][j] == i * m + j)) | ((0 < when[i][j]) & disjunction(join(i, j))) for i in range(n) for j in range(m)],
"""

# java ace Fillomino-5x5-1.xml -s=all -valh=Asgs -p=AP
