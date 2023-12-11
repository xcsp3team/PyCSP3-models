"""
The benzenoid generation problem is defined as follows: given a set of structural properties P,
generate all the benzenoids which satisfy each property of P.
For instance, these structural properties may deal with the number of carbons, the number of
hexagons or a particular structure for the hexagon graph.
Here, we are interested in generating benzenoids with n hexagons (including benzenoids with ‘holes’).

See the PhD thesis by Adrien Varet (2022, Aix Marseille University).

## Data
  an integer, the order of the coronenoide

## Model
  constraints: Count, Lex, Precedence, Sum, Table

## Execution
  python Benzenoide.py -data=number

## Links
  - https://www.theses.fr/2022AIXM0508
  - https://link.springer.com/article/10.1007/s10601-022-09328-x
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.ptypes import TypeHexagonSymmetry

n = data or 8  # order of the coronenoide
w = 2 * n - 1  # maximal width
widths = [w - abs(n - i - 1) for i in range(w)]

symmetries = [sym.apply_on(n) for sym in TypeHexagonSymmetry]  # if sym.is_rotation()]


def valid(*t):
    return [(i, j) for i, j in t if 0 <= i < w and 0 <= j < widths[i]]


neighbors = [[valid(
    (i, j - 1), (i, j + 1),
    (i - 1, j - (1 if i < n else 0)), (i - 1, j + (0 if i < n else 1)),
    (i + 1, j - (1 if i >= n - 1 else 0)), (i + 1, j + (0 if i >= n - 1 else 1)))
    for j in range(widths[i])] for i in range(w)]


def T1(i, j):
    r = len(neighbors[i][j])
    return [(0, 0, *[ANY] * r), (1, 1, *[ANY] * r)] + \
        [(2, 1, *[1 if j == i else ANY for j in range(r)]) for i in range(r)] + \
        [(v, 1, *[v - 1 if j == i else {0}.union(range(v - 1, n + 1)) for j in range(r)]) for v in range(3, n + 1) for i in range(r)]


T2 = [(1, 1, 1, 1, 1, 1, 1)] + [(ANY, *[0 if j == i else ANY for j in range(6)]) for i in range(6)]

# x[i][j] is 1 iff the hexagon at row i and column j is selected
x = VarArray(size=[w, w], dom=lambda i, j: {0, 1} if j < widths[i] else None)

# y[i][j] is the distance (+1) wrt the root of the connected tree
y = VarArray(size=[w, w], dom=lambda i, j: range(n + 1) if j < widths[i] else None)

satisfy(
    # only one root
    Count(y, value=1) == 1,

    # ensuring connectedness
    [(y[i][j], x[i][j], y[neighbors[i][j]]) in T1(i, j) for i in range(w) for j in range(widths[i])],

    # exactly n hexagons
    Sum(x) == n,

    # ensuring no holes
    [(x[i][j], x[neighbors[i][j]]) in T2 for i in range(w) for j in range(widths[i]) if len(neighbors[i][j]) == 6],

    # tag(symmetry-breaking)
    [
        [LexDecreasing(x, [x[row] for row in sym]) for sym in symmetries],

        [Precedence(y, values=(1, v)) for v in range(2, n + 1)]

        # # at least one hexagon on the left
        # Sum(x[:, 0]) > 0,  # x[0][0] == 1
        #
        # # at least one hexagon on the top left
        # Sum(x[0] + x[1:n, 0]) > 0,

        # at least one hexagon on the two rightmost columns
        # Sum(x[i][widths[i]-2:] for i in range(w)) > 0
    ]
)

minimize(
    Sum(x[i][j] * ((n - i) * w + (n - j)) for i in range(w) for j in range(w) if j < widths[i])
)

""" Comments
1) for being compatible with the competition mini-track, we use:
  z = VarArray(size=[w, w], dom=lambda i, j: {0, 1} if j < widths[i] else None)

  satisfy(
    # only one root
    [
        [(z[i][j], y[i][j]) in [(1, 1)] + [(0, v) for v in range(n + 1) if v != 1] for i in range(w) for j in range(widths[i])],
        Sum(z) == 1
    ],
2) Note that:
 y[neighbors[i][j]]
   is a shortcut for:
 [y[k][l] for k, l in neighbors[i][j]] 
3) Data for the XCSP23 competition are : [6,7,8,9,10,11,12,13,14,15] 
"""

# [(y[i][j], y[k][l]) in [(ne(1), ANY), (1, 2)] for i in range(n) for j in range(widths[i])
#     for k, l in neighbors[i][j] if i < k or i == k and j < l]


# def sym(n, v):
#     d = {(n - 1, n - 1): (n - 1, n - 1)}  # center
#     for ring in range(2, n + 1):
#         skip = v * (ring - 1)  # test for 60
#         offset = n - ring
#         t = rings[ring]
#         for idx, (i, j) in enumerate(t):
#             k, l = t[(idx + skip) % len(t)]
#             d[(i + offset, j + offset)] = (k + offset, l + offset)
#     return d


# [(y[i][j], y[k][l]) in [(0, ANY), (ANY, 0), (1, 2), (2, 2), (2, 3)] + [(v, (v - 1, v, v + 1)) for v in range(3, n + 1)]
#  for i in range(n) for j in range(widths[i]) for k, l in neighbors[i][j] if i < k or i == k and j < l],
