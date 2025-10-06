"""
## Data Example
  caterpillar13.json

## Model
  constraints: Maximum, Table

## Execution
  python CyclicBandwidth.py -data=<datafile.json>
  python CyclicBandwidth.py -data=<datafile.json> -variant=aux
  python CyclicBandwidth.py -data=<datafile.json> -variant=table
  python CyclicBandwidth.py -data=<datafile.txt> -parser=CyclicBandwith_Parser.py

## Links
  - https://www.sciencedirect.com/science/article/abs/pii/S0305054814003177
  - https://www.tamps.cinvestav.mx/~ertello/cbmp.php
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, xcsp22
"""

from pycsp3 import *

assert not variant() or variant("aux") or variant("table")

n, edges = data or (5, [[0, 1], (0, 4), (1, 2), (1, 3), (2, 3), (2, 4)])

edges = [tuple(t) for t in edges]  # because from JSON, we get lists and not tuples (which may be a problem with some conditions)

# x[i] is the label of the ith node
x = VarArray(size=n, dom=range(n))

satisfy(
    AllDifferent(x)
)

if not variant():
    minimize(
        Maximum(min(abs(x[i] - x[j]), n - abs(x[i] - x[j])) for i, j in edges)
    )


elif variant("aux"):

    # y[i][j] is the distance between the labels of nodes i and j (if an edge exists)
    y = VarArray(size=[n, n], dom=lambda i, j: range(1, n) if (i, j) in edges else None)

    satisfy(
        # computing distances
        y[i][j] == abs(x[i] - x[j]) for i, j in edges
    )

    minimize(
        Maximum(min(y[i][j], n - y[i][j]) for i, j in edges)
    )

elif variant("table"):
    T = [(min(abs(v1 - v2), n - abs(v1 - v2)), v1, v2) for v1 in range(n) for v2 in range(n) if v1 != v2]

    # y[i][j] is the minimum distance computed from the labels of nodes i and j (if an edge exists)
    y = VarArray(size=[n, n], dom=lambda i, j: range(1, n) if (i, j) in edges else None)

    satisfy(
        # computing minimum distances
        (y[i][j], x[i], x[j]) in T for i, j in edges
    )

    minimize(
        Maximum(y)
    )

""" Comments
1) With an aggressive ub, optimality is proved:
  java ace CyclicBandwidth-path300.xml -ale=4 -ub=3
  java ace CyclicBandwidth-aux-path300.xml -ub=2
"""
