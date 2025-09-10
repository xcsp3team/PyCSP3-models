"""
An Aztec diamond of order n consists of 2n centered rows of unit squares, of respective lengths 2, 4, ..., 2n-2, 2n, 2n-2, ..., 4, 2.
An Aztec diamond of order n has exactly 2^(n*(n+1)/2) tilings by dominos.

The model, below, correspond to an optimization variant of Aztec Diamond, used for the 2024 competition.

## Data
  A unique integer, the order of the diamond

## Model
  constraints: Cardinality, Sum, Table

## Execution
  python AztecDiamondSym.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Aztec_diamond
  - https://www.cril.univ-artois.fr/XCSP24/competitions/cop/cop

## Tags
  academic, recreational, xcsp24
"""

from pycsp3 import *

n = data


def n_dominos(k):
    return 6 if k == 2 else n_dominos(k - 1) + 2 * k


nDominos = n_dominos(n)

T3 = [(v, v, ANY) for v in range(nDominos)] + [(v, ANY, v) for v in range(nDominos)]
T5 = [(v, v, ANY, ANY, ANY) for v in range(nDominos)] + [(v, ANY, v, ANY, ANY) for v in range(nDominos)] + \
     [(v, ANY, ANY, v, ANY) for v in range(nDominos)] + [(v, ANY, ANY, ANY, v) for v in range(nDominos)]


def valid(i, j):
    if i < 0 or i >= n * 2 or j < 0 or j >= n * 2:
        return False
    if i < n - 1 and (j < n - 1 - i or j > n + i):
        return False
    if i > n and (j < i - n or j > 3 * n - i - 1):
        return False
    return True


def top_left(i, j):
    return valid(i, j) and not valid(i, j - 1) and not valid(i - 1, j)


def top_right(i, j):
    return valid(i, j) and not valid(i, j + 1) and not valid(i - 1, j)


def bot_left(i, j):
    return valid(i, j) and not valid(i, j - 1) and not valid(i + 1, j)


def bot_right(i, j):
    return valid(i, j) and not valid(i, j + 1) and not valid(i + 1, j)


# x[i][j] is the number of the domino in cell (i,j)
x = VarArray(size=[2 * n, 2 * n], dom=lambda i, j: range(nDominos) if valid(i, j) else None)

m = [[x[i][j]] + [x[k][q] for k, q in [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)] if valid(k, q)]
     for i in range(2 * n) for j in range(2 * n) if valid(i, j)]

scp3, scp5 = [t for t in m if len(t) == 3], [t for t in m if len(t) == 5]

satisfy(
    # ensuring valid positioning of dominos (over sequences of length 3)
    [scp in T3 for scp in scp3],

    # ensuring valid positioning of dominos (over sequences of length 5)
    [scp in T5 for scp in scp5]
)

if not variant():
    satisfy(
        # ensuring the two pieces of each domino occurs twice
        Cardinality(x, occurrences={v: 2 for v in range(nDominos)}),
    )

    minimize(
        Sum(x[i][j] * (abs(n - i) * abs(n - j)) for i in range(2 * n) for j in range(2 * n) if valid(i, j))
    )

elif variant("mini"):
    flat_x = flatten(x)
    nf = len(flat_x)

    satisfy(
        [flat_x in [tuple(v if j == i else ANY for j in range(nf)) for i in range(nf)] for v in range(nDominos)]
    )

    minimize(
        Sum(x[n - n // 2:n + n // 2, n - n // 2:n + n // 2])
    )

"""
1) Data used for the 2024 competition are : [3, 4, 5, 6, 7, 8, 9, 10, 12, 15 ]
"""

# symmetry-breaking : [Increasing(x[i]) for i in range(2 * n)] [Increasing(x[:, i]) for i in range(2 * n)],
# but not all symmetries

# for i in range(n * 2):
#     print(
#         ['tl' if top_left(i, j) else 'tr' if top_right(i, j) else 'bl' if bot_left(i, j) else 'br' if bot_right(i, j) else '*' if valid(i, j) else ' ' for j in
#          range(n * 2)])

# Sum(x) == nDominos * (nDominos - 1)
