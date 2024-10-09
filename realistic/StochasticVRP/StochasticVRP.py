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

distances = cp_array([distances[p + j * nNodes:p + (j + 1) * nNodes] for j in range(nNodes)] for k in range(nSetups) if (p := k * (nNodes * nNodes),))

AllDepots = range(nCustomers, nCustomers + 2 * nVehicles)
StartDepots = range(nCustomers, nCustomers + nVehicles)
EndDepots = range(nCustomers + nVehicles, nCustomers + 2 * nVehicles)

# nxt[k][i] is the successor of the ith node in the kth setup
nxt = VarArray(size=[nSetups, nNodes], dom=range(nNodes))

# prv[k][i] is the predecessor of the ith node in the kth setup
prv = VarArray(size=[nSetups, nNodes], dom=range(nNodes))

# veh[i] is the vehicle at the ith node
veh = VarArray(size=nNodes, dom=range(nVehicles))

# arr[k][i] is the arrival time at the ith node in the kth setup
arr = VarArray(size=[nSetups, nNodes], dom=range(timeBudget + 1))

satisfy(
    # pre-assigning a few variables
    [
        [prv[k][i] == v for k in range(nSetups) for i in StartDepots if (v := i + nVehicles - 1 + (nVehicles if i == nCustomers else 0),)],
        [nxt[k][i] == v for k in range(nSetups) for i in EndDepots if (v := i - nVehicles + 1 - (nVehicles if i == nNodes - 1 else 0),)],

        [veh[i] == i - nCustomers for i in StartDepots],
        [veh[i] == i - nCustomers - nVehicles for i in EndDepots],

        [arr[k][i] == 0 for k in range(nSetups) for i in StartDepots]
    ],

    # ensuring coherence between succeeding and preceding nodes
    [
        (
            nxt[k][prv[k][i]] == i,
            prv[k][nxt[k][i]] == i
        ) for k in range(nSetups) for i in range(nNodes)
    ],

    # ensuring we have a circuit
    [
        (
            Circuit(nxt[k]),
            Circuit(prv[k])
        ) for k in range(nSetups)
    ],

    # ensuring we keep the same vehicle
    [
        (
            veh[prv[k][i]] == veh[i],
            veh[nxt[k][i]] == veh[i]
        ) for k in range(nSetups) for i in range(nCustomers)
    ],

    # restraining arrival times
    [
        arr[k][i] + services[i] + distances[k][i][nxt[k][i]] <= arr[k][nxt[k][i]] for k in range(nSetups) for i in range(nCustomers + nVehicles)
    ]
)

minimize(
    Sum(weights[i] * Maximum(arr[i]) for i in range(nSetups))
)

""" Comments
1) note that data have been transferred in JSON
"""
