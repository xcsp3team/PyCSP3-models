"""
See "Solving the Wastewater Treatment Plant Problem with SMT", by Miquel Bofill, Víctor Muñoz, Javier Murillo. CoRR abs/1609.05367 (2016)

## Data
  ex04400.json

## Model
  constraints: AllDifferent, Sum

## Execution:
  python WWTPP.py -data=<datafile.json>
  python WWTPP.py -data=<datafile.json> -variant=short

## Links
 - https://arxiv.org/abs/1609.05367

## Tags
  realistic
"""

from pycsp3 import *

assert not variant() or variant("short")

nIndustries, nPeriods, plantCapacity, tankFlow, tankCapacity, sd, spans = data or load_json_data("ex04400.json")  # sd for schedule flow of discharge


def table_compatibility(i, j):
    if j in {nPeriods - 1, nPeriods} or (j - 1 == 0 and sd[i][0] == 0):
        return {(0, 0)}
    tf, tc = tankFlow[i], tankCapacity[i]
    tbl = {(0, ANY)} | {(tf, v) for v in range(tf, tc + 1)} | {(v, v) for v in range(1, min(tf, tc + 1))}
    return tbl if variant("short") else to_ordinary_table(tbl, [tf + 1, tc + 1])


# b[i][j] is the flow stored in buffer i at the end of period j
b = VarArray(size=[nIndustries, nPeriods], dom=lambda i, j: {0} if (j == 0 and sd[i][0] == 0) or j == nPeriods - 1 else range(tankCapacity[i] + 1))

# d[i][j] is the flow discharged from buffer (or industry) i during time period j
d = VarArray(size=[nIndustries, nPeriods], dom=lambda i, j: {0} if j == 0 else range(tankFlow[i] + 1))

# c[i][j] is the actual capacity requirement of industry i during time period j
c = VarArray(size=[nIndustries, nPeriods], dom=lambda i, j: {0, sd[i][j]} if sd[i][j] != 0 else None)

satisfy(
    # not exceeding the Wastewater Treatment Plant
    [
        Sum(
            c[:, j],
            d[:, j]
        ) <= plantCapacity for j in range(nPeriods)
    ],

    # managing scheduled discharge flows at period 0
    [
        Sum(
            b[i][0],
            c[i][0]
        ) == sd[i][0] for i in range(nIndustries) if sd[i][0] != 0
    ],

    # managing scheduled discharge flows at all periods except 0
    [
        Sum(
            b[i][j],
            -b[i][j - 1],
            d[i][j],
            c[i][j]
        ) == sd[i][j] for i in range(nIndustries) for j in range(1, nPeriods)
    ],

    # ensuring compatibility between stored and discharge flows
    [(d[i][j], b[i][j - 1]) in table_compatibility(i, j) for i in range(nIndustries) for j in range(1, nPeriods)],

    # spanning constraints
    [
        Table(
            scope=c[i][start:stop],
            supports={tuple([0] * (stop - start)), tuple(sd[i][start:stop])}
        )
        for (i, start, stop) in spans
    ]
)

""" Comments
1) When managing scheduled discharge flows, we have a list with four cells for variables and integers.
 However, when there is the special value None (at the fourth position in both lists), the two lists will be automatically reduced to three cells.
 
2) One could also write the more complex expression:
  [[b[i][j], b[i][j - 1], d[i][j], c[i][j]] * [1, -1, 1, 1 if c[i][j] else None] == sd[i][j] for i in range(nIndustries) for j in range(1, nPeriods)],
"""
