"""
See Problem 040 on CSPLib.

## Data Example
  A01.json

## Model
  constraints: Sum

## Execution
  python EchelonStock2.py -data=<datafile.json>
  python EchelonStock2.py -data=<datafile.txt> -parser=EchelonStock_Parser.py

## Links
  - https://www.csplib.org/Problems/prob040/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22
"""

from pycsp3 import *
from math import floor, gcd
from functools import reduce

children, hcosts, pcosts, demands = data or load_json_data("A01.json")

n, nPeriods, nLeaves = len(children), len(demands[0]), len(demands)

simplification = True
if simplification:
    gcd = reduce(gcd, {v for row in demands for v in row})
    demands = [[row[t] // gcd for t in range(nPeriods)] for row in demands]
    hcosts = [hcosts[i] * gcd for i in range(n)]

sum_dmds, all_dmds = [], []
for i in range(n):
    if i < nLeaves:
        sum_dmds.append(sum(demands[i]))
        all_dmds.append([sum(demands[i][t:]) for t in range(nPeriods)])
    else:
        sum_dmds.append(sum(sum_dmds[j] for j in children[i]))
        all_dmds.append([sum(all_dmds[j][t] for j in children[i]) for t in range(nPeriods)])


def ratio1(i, coeff=1):
    parent = next(j for j in range(n) if i in children[j])  # use a cache instead, if necessary (i., precompute parents)
    return floor(pcosts[i] // (coeff * (hcosts[i] - hcosts[parent])))


def ratio2(i, t_inf):
    return min(sum(demands[i][t_inf: t_sup + 1]) + ratio1(i, t_sup - t_inf + 1) for t_sup in range(t_inf, nPeriods))


def domain_x(i, t):  # ratio2 from IC4, and allDemands from IC6a
    return range(min(all_dmds[i][t], ratio2(i, t)) + 1) if i < nLeaves else range(all_dmds[i][t] + 1)


def domain_y(i, t):  # {0} from IC1, ratio1 from IC3 and allDemands from IC6b (which generalizes IC1)
    return {0} if t == nPeriods - 1 else range(min(all_dmds[i][t + 1], ratio1(i)) + 1) if i < n - 1 else range(all_dmds[i][t + 1] + 1)


# x[i][t] is the amount ordered at node i at period (time) t
x = VarArray(size=[n, nPeriods], dom=domain_x)

# y[i][t] is the amount stocked at node i at the end of period t
y = VarArray(size=[n, nPeriods], dom=domain_y)

satisfy(
    [y[i][0] == x[i][0] - demands[i][0] for i in range(nLeaves)],

    [y[i][t] == x[i][t] + y[i][t - 1] - demands[i][t] for i in range(nLeaves) for t in range(1, nPeriods)],

    [y[i][0] == x[i][0] - Sum(x[j][0] for j in children[i]) for i in range(nLeaves, n)],

    [y[i][t] == x[i][t] + y[i][t - 1] - Sum(x[j][t] for j in children[i]) for i in range(nLeaves, n) for t in range(1, nPeriods)],

    # IC2
    [(x[i][t] == 0) | disjunction(x[j][t] > 0 for j in children[i]) for i in range(nLeaves, n) for t in range(nPeriods)],

    # IC5
    [(y[i][t - 1] == 0) | (x[i][t] == 0) for i in range(n) for t in range(1, nPeriods)],

    # tag(redundant)
    [Sum(x[i]) == sum_dmds[i] for i in range(n)],

    [y[i][t - 1] + Sum(x[i][t:]) == all_dmds[i][t] for i in range(nLeaves) for t in range(1, nPeriods)]
)

minimize(
    Sum(hcosts[i] * y[i][t] for i in range(n) for t in range(nPeriods))
    + Sum(pcosts[i] * (x[i][t] > 0) for i in range(n) for t in range(nPeriods))
)

""" Comments
1) IC4, simple version is: [x[i][t] <= demands[i][t] + ratio(i) for i in range(nLeaves) for t in range(nPeriods)],
2) Using only one Sum when posting the objective generates a complex XCSP3 expression
"""
