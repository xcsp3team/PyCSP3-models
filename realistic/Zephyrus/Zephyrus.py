"""
The deployment optimization problem is the problem of how to correctly deploy all the software components
needed by a cloud application on suitable VMs on the cloud at minimal cost.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2019 challenges.
The MZN model was proposed by Jacopo Mauro (under the terms of the ISC License)

## Data Example
  12-06-8-3.json

## Model
  constraints: Lex, Sum

## Execution
  python Zephyrus.py -data=<datafile.json>
  python Zephyrus.py -data=<datafile.dzn> -parser=Zephyrus_ParserZ.py

## Links
  - https://bitbucket.org/jacopomauro/zephyrus2/src/master/
  - https://www.duo.uio.no/handle/10852/51754
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn16, mzn19
"""

from pycsp3 import *

matrix, locations, components = data
costs, resources = zip(*locations)
requiring, providing, conflicts, consuming = zip(*components)
nLocations, nComponents, nPorts, nMultiPorts, nResources = len(locations), len(components), len(requiring[0]), len(providing[0]), 1  # len(resources[0])
assert nComponents == 4 and nPorts == 4 and nMultiPorts == 5 and nResources == 1

C, MP, P, L = range(nComponents), range(nMultiPorts), range(nPorts), range(nLocations)
MAX_INT = 4096

maxRequ = [[sum(requiring[j][p] for p in P if matrix[m][p] == 1) for j in C] for m in MP]


def conflicting(i, j=None):
    return any(conflicts[j if j is not None else i][p] == 1 and any(matrix[m][p] == 1 and providing[i][m] != 0 for m in MP) for p in P)


bindings = VarArray(size=[nMultiPorts, nPorts, nComponents, nComponents], dom=range(MAX_INT + 1))

# x[i] is the number of the ith component being deployed
x = VarArray(size=nComponents, dom=range(MAX_INT + 1))

# y[j][i] is the number of the ith component in the jth location
y = VarArray(size=[nLocations, nComponents], dom=range(MAX_INT + 1))

# total is the total number of deployed components
total = Var(dom=range(MAX_INT + 1))

# z[j] is 1 if the jth location is used
z = VarArray(size=nLocations, dom={0, 1})

satisfy(
    # computing the total number of deployed components
    total == Sum(x),

    # zero binding when a multi-port does not provide a port
    [bindings[m, p, :, :] == 0 for m in MP for p in P if matrix[m][p] == 0],

    # ensuring right values of bindings
    [
        [bindings[m, :, i, :] == 0 for m in MP for i in C if providing[i][m] == 0],

        [If(x[i] == 0, Then=bindings[m, p, i, j] == 0) for m in MP for i in C if providing[i][m] == -1 for p in P for j in C],

        [Sum(bindings[m, :, i, :]) <= x[i] * providing[i][m] for m in MP for i in C if providing[i][m] not in (-1, 0)]
    ],

    # ensuring port requirements of components
    [Sum(bindings[:, p, :, j]) == x[j] * requiring[j][p] for p in P for j in C],

    # at most one component if a port is conflicting
    [x[i] <= 1 for i in C if conflicting(i)],

    # avoiding the deployment of conflicting components
    [If(x[i] > 0, Then=x[j] == 0) for i in C for j in C if i != j and conflicting(i, j)],

    # unicity constraints
    [
        [
            If(
                x[i] >= maxRequ[m][i],
                Then=Sum(bindings[m, :, i, i]) <= maxRequ[m][i] * x[i] - maxRequ[m][i]
            ) for m in MP for i in C if maxRequ[m][i] != 0
        ],

        [Sum(bindings[m, :, i, i]) == 0 for m in MP for i in C if maxRequ[m][i] == 0],

        [
            If(
                x[i] < maxRequ[m][i],
                Then=[If(x[i] == v, Then=Sum(bindings[m, :, i, i]) <= v * (v - 1)) for v in range(1, maxRequ[m][i] + 1)]
            ) for m in MP for i in C],

        [
            If(
                x[i] >= maxRequ[m][j],
                Then=Sum(bindings[m, :, i, j]) <= maxRequ[m][j] * x[j]
            ) for m in MP for i in C for j in C if i != j and maxRequ[m][j] != 0
        ],

        [Sum(bindings[m, :, i, j]) == 0 for m in MP for i in C for j in C if i != j and maxRequ[m][j] == 0],

        [
            If(
                x[i] < maxRequ[m][j],
                Then=[If(x[i] == v, Then=Sum(bindings[m, :, i, j]) <= v * x[j]) for v in range(maxRequ[m][j] + 1)]
            ) for m in MP for i in C for j in C if i != j
        ]
    ],

    # deciding locations
    [
        [(Sum(y[j]) == 0) == (z[j] == 0) for j in L],
        [Sum(y[:, i]) == x[i] for i in C],
        [y[j] * consuming <= resources[j] for j in L],
        Sum(z) <= total
    ],

    # tag(symmetry-breaking)
    [
        (
            LexIncreasing(y[j1], y[j2]),
            If(z[j1], Then=z[j2])
        ) for j1, j2 in [(j1, j2) if costs[j1] > costs[j2] else (j2, j1) for j1, j2 in combinations(nLocations, 2) if resources[j1] == resources[j2]]
    ],

    (Sum(y[:, 0]) > 0) | (Sum(y[:, 1]) > 0),

    [
        (
            y[j][2] < 2,
            y[j][3] < 2
        ) for j in L
    ]
)

minimize(
    # minimizing the cost of used locations
    z * costs
)

"""
1) note that:
   [bindings[m, :, i, :] == 0 for m in MP for i in C if providing[i][m] == 0],
 is shorter to write than:
   [bindings[m, p, i, j] == 0 for m in MP for i in C if providing[i][m] == 0 for p in P for j in C],

2) we must try if there is a difference in term of efficiency when combining 
    [(comps_num[i] < max_req[m][i]) | (Sum(bindings[m, :, i, i]) <= max_req[m][i] * comps_num[i] - max_req[m][i]) for m in MP for i in
     C if max_req[m][i] != 0],

    [Sum(bindings[m, :, i, i]) == 0 for m in MP for i in C if max_req[m][i] == 0],
as in the original model

3) in 2015, instances were given in flat format
"""
