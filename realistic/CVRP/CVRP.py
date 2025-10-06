"""
See Problem 086 on CSPLib, and VVRLib.

## Data Example
  A-n32-k5.json

## Model
  constraints: AllDifferent, Cardinality, Element, Sum

## Execution
  python CVRP.py -data=<datafile.json>

## Links
  - https://www.csplib.org/Problems/prob086/
  - http://vrp.galgos.inf.puc-rio.br/index.php/en/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22
"""

from pycsp3 import *

nNodes, capacity, demands, distances = data or load_json_data("A-n32-k5.json")


def max_tour():
    t = sorted(demands)
    i, s = 1, 0
    while i < nNodes and s < capacity:
        s += t[i]
        i += 1
    return i - 2


nVehicles = nNodes // 4  # This is a kind of hard coding, which can be at least used for Set A (Augerat, 1995)
nSteps = max_tour()
n0s = nVehicles * nSteps - nNodes + 1

V, S, N = range(nVehicles), range(nSteps), range(nNodes)

# c[i][j] is the jth customer (step) during the tour of the ith vehicle
c = VarArray(size=[nVehicles, nSteps], dom=N)

# d[i][j] is the demand of the jth customer during the tour of the ith vehicle
d = VarArray(size=[nVehicles, nSteps], dom=demands)

satisfy(
    AllDifferent(c, excepting=0),

    # ensuring that all demands are satisfied
    Cardinality(
        within=c,
        occurrences={v: n0s if v == 0 else 1 for v in N}
    ),

    # no holes permitted during tours
    [
        If(
            c[i][j] == 0,
            Then=c[i][j + 1] == 0
        ) for i in V for j in S[:-1]
    ],

    # computing the collected demands
    [demands[c[i][j]] == d[i][j] for i in V for j in S],

    # not exceeding the capacity of each vehicle
    [Sum(d[i]) <= capacity for i in V],

    # tag(symmetry-breaking)
    Decreasing(c[:, 0])
)

minimize(
    # minimizing the total traveled distance by vehicles
    Sum(distances[0][c[i][0]] for i in V)
    + Sum(distances[c[i][j]][c[i][j + 1]] for i in V for j in S[:-1])
    + Sum(distances[c[i][-1]][0] for i in V)
)

""" Comments
1) We can check the solution for the instance A-n32-k5 with:
 [c[2][k] == v for k, v in enumerate([21, 31, 19, 17, 13, 7, 26])],
 [c[4][k] == v for k, v in enumerate([12, 1, 16, 30])],
 [c[1][k] == v for k, v in enumerate([27, 24])],
 [c[0][k] == v for k, v in enumerate([29, 18, 8, 9, 22, 15, 10, 25, 5, 20])],
 [c[3][k] == v for k,v in enumerate([14, 28, 11, 4, 23, 3, 2, 6])]
 
2) The AllDifferent constraint is redundant
"""
