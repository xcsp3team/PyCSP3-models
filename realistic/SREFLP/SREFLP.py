"""
The Single-Row Facility Layout Problem (SRFLP) is an ordering problem considering a set of departments in a facility,
with given lengths and pairwise traffic intensities.
Its goal is to find a linear ordering of the departments minimizing the weighted sum of the distances between department pairs.
See CP paper below.

## Data Example
  Cl07.json

## Model
  constraints: AllDifferent, Element, Sum, Table

## Execution
  python SREFLP.py -data=<datafile.json>
  python SREFLP.py -data=<datafile.txt> -parser=SREFLP_Parser.py

## Links
  - https://drops.dagstuhl.de/storage/00lipics/lipics-vol235-cp2022/LIPIcs.CP.2022.14/LIPIcs.CP.2022.14.pdf
  - https://github.com/vcoppe/csrflp-dd
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  realistic, xcsp23
"""

from pycsp3 import *

lengths, traffics = data
n = len(lengths)

ordered_lengths = sorted(lengths)

pairs = [(i, j) for i, j in combinations(n, 2) if i + 1 < j]

# x[i] is the department at the ith position
x = VarArray(size=n, dom=range(n))

# y[i] is the length of the department at the ith position
y = VarArray(size=n, dom=lengths)

# d[i][j] is the end-to-start distance between the ith and the jth departments
d = VarArray(size=[n, n], dom=lambda i, j: range(sum(ordered_lengths[:j - i - 1]), sum(ordered_lengths[i - j + 1:]) + 1) if i + 1 < j else None)

satisfy(
    # ensuring a linear ordering of the departments
    AllDifferent(x),

    # computing lengths
    [
        (x[i], y[i]) in [
            (j, lengths[j]) for j in range(n)
        ] for i in range(n)
    ],

    # computing distances
    [d[i][j] == Sum(y[i + 1:j]) for i, j in pairs]
)

if not variant():
    minimize(
        # minimizing weighted end-to-start distances
        Sum(d[i][j] * traffics[x[i], x[j]] for i, j in pairs)
    )

elif variant("mini"):
    z = VarArray(size=[n, n], dom=lambda i, j: traffics if i + 1 < j else None)

    m, M = min(v for row in traffics for v in row), max(v for row in traffics for v in row)

    w = VarArray(size=[n, n], dom=lambda i, j: range(sum(ordered_lengths[:j - i - 1]) * m, sum(ordered_lengths[i - j + 1:]) * M + 1) if i + 1 < j else None)

    satisfy(
        [(z[i][j], x[i], x[j]) in [(traffics[v1][v2], v1, v2) for v1 in range(n) for v2 in range(n)] for i, j in pairs],

        [w[i][j] == d[i][j] * z[i][j] for i, j in pairs]
    )

    minimize(
        # minimizing weighted end-to-start distances
        Sum(w)
    )

""" Comments
1) An alternative for computing distance is:
 [d[i][j] == (y[i + 1] if i + 2 == j else (y[i + 1] + y[i + 2]) if i + 3 == j else (d[i][j - 1] + y[j - 1])) for i, j in pairs]
"""
