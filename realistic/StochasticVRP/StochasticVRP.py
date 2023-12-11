"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  s2-v2-c7.json

## Model
  constraints: Circuit, Element, Sum

## Execution
  python StochasticVRP.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn14, mzn19
"""

from pycsp3 import *

nVehicles, nCustomers, timeBudget, services, distances, weights = data
nNodes, nSetups = nCustomers + 2 * nVehicles, len(weights)

distances = cp_array([distances[k * (nNodes * nNodes) + j * nNodes:k * (nNodes * nNodes) + (j + 1) * nNodes] for j in range(nNodes)] for k in range(nSetups))

AllDepots = range(nCustomers, nCustomers + 2 * nVehicles)
StartDepots = range(nCustomers, nCustomers + nVehicles)
EndDepots = range(nCustomers + nVehicles, nCustomers + 2 * nVehicles)

# x[k][i] is the successor of the ith node in the kth setup
x = VarArray(size=[nSetups, nNodes], dom=range(nNodes))

# y[k][i] is the predecessor of the ith node in the kth setup
y = VarArray(size=[nSetups, nNodes], dom=range(nNodes))

# vh[i] is the vehicle at the ith node
vh = VarArray(size=nNodes, dom=range(nVehicles))

# at[k][i] is the arrival time at the ith node in the kth setup
at = VarArray(size=[nSetups, nNodes], dom=range(timeBudget + 1))

satisfy(
    # pre-assigning a few variables
    [
        [y[k][i] == i + nVehicles - 1 for k in range(nSetups) for i in range(nCustomers + 1, nCustomers + nVehicles)],
        [y[k][nCustomers] == nCustomers + 2 * nVehicles - 1 for k in range(nSetups)],

        [x[k][i] == i - nVehicles + 1 for k in range(nSetups) for i in range(nCustomers + nVehicles, nCustomers + 2 * nVehicles - 1)],
        [x[k][-1] == nCustomers for k in range(nSetups)],

        [vh[i] == i - nCustomers for i in StartDepots],
        [vh[i] == i - nCustomers - nVehicles for i in EndDepots],

        [at[k][i] == 0 for k in range(nSetups) for i in StartDepots]
    ],

    # ensuring coherence between succeeding and preceding nodes
    [
        [x[k][y[k][i]] == i for k in range(nSetups) for i in range(nNodes)],
        [y[k][x[k][i]] == i for k in range(nSetups) for i in range(nNodes)]
    ],

    # ensuring we have a circuit
    [
        [Circuit(x[k]) for k in range(nSetups)],
        [Circuit(y[k]) for k in range(nSetups)]
    ],

    # ensuring we keep the same vehicle
    [
        [vh[y[k][i]] == vh[i] for k in range(nSetups) for i in range(nCustomers)],
        [vh[x[k][i]] == vh[i] for k in range(nSetups) for i in range(nCustomers)]
    ],

    # restraining arrival times
    [
        [at[k][i] + services[i] + distances[k][i][x[k][i]] <= at[k][x[k][i]] for k in range(nSetups) for i in range(nCustomers)],
        [at[k][i] + services[i] + distances[k][i][x[k][i]] <= at[k][x[k][i]] for k in range(nSetups) for i in StartDepots]
    ]
)

minimize(
    Sum(weights[i] * Maximum(at[i]) for i in range(nSetups))
)

"""
1) note that data have been transferred in JSON
"""
