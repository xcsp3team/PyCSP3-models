"""
Capacitated Vehicle Routing problem with Time Windows, Service Times and Pickup and deliveries.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The MZN model was proposed by Haakon H. Rød (with a Copyright that seems to be like a MIT Licence),
based on Andrea Rendl's work from 2015 and the Routing model used by the LNS solver for VRPs in Google's OR Tools.

## Data
  toy-D-2v-4l-w-reload.json

## Model
  constraints: Circuit, Element, Sum

## Execution
  python VrpSubmission.py -data=file.json

## Links
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn21
"""

from pycsp3 import *

nVehicles, nCustomers, capacities, windows, demands, pds, travelTimes = data
pds = [t[1] - 1 for t in pds]

n = 2 * nVehicles + nCustomers
horizon = max(windows[:, 1]) + max(max(travelTimes[i] for i in range(n))) + 1  # the maximal of time that we got
r1, r2, r3 = range(nCustomers), range(nCustomers, nCustomers + nVehicles), range(nCustomers + nVehicles, nCustomers + 2 * nVehicles)

# succ[i] is the node that succeeds to the ith node
succ = VarArray(size=n, dom=range(n))

# pred[i] is the node that precedes the ith node
pred = VarArray(size=n, dom=range(n))

# veh[i] is the vehicle that visits the ith node
veh = VarArray(size=n, dom=range(nVehicles))

# load[i] is the load when arriving at the ith node
load = VarArray(size=n, dom=range(max(capacities) + 1))

# arr[i] is the arrival time at the ith node
arr = VarArray(size=n, dom=range(horizon))

# dep[i] is the departure time of the ith node
dep = VarArray(size=n, dom=range(horizon))

# slack[i] is the recreative time allowed at the ith node
slack = VarArray(size=n, dom=range(horizon))

# z = Var(range(horizon))

satisfy(
    # predecessors of start nodes are end nodes and successors of end nodes are start nodes
    (
        [pred[i] == (n - 1 if i == nCustomers else i + nVehicles - 1) for i in r2],
        [succ[i] == (nCustomers if i == n - 1 else i - nVehicles + 1) for i in r3]
    ),

    # associating each start/end nodes with a vehicle
    (
        [veh[i] == i - nCustomers for i in r2],
        [veh[i] == i - nCustomers - nVehicles for i in r3]
    ),

    # linking predecessors and successors
    (
        [succ[pred[i]] == i for i in range(n)],
        [pred[succ[i]] == i for i in range(n)]
    ),

    Circuit(succ),
    Circuit(pred),

    # vehicles remain the same along a tour
    (
        (
            veh[pred[i]] == veh[i],
            veh[succ[i]] == veh[i]
        ) for i in r1
    ),

    # managing pickups and deliveries
    (
        (
            veh[i] == veh[pds[i]],
            arr[i] >= arr[pds[i]]
        ) for i in r1 if pds[i] != i
    ),

    # time constraints
    [arr[i] + slack[i] + travelTimes[i][succ[i]] == arr[succ[i]] for i in range(nCustomers + nVehicles)],

    # time window constraints
    (
        (
            arr[i] >= windows[i][0],
            arr[i] <= windows[i][1]
        ) for i in r1
    ),

    # load constraints
    (
        [load[i] + demands[i] == load[succ[i]] for i in r1],
        [load[i] == load[succ[i]] for i in r2],
        [load[i] <= capacities[veh[i]] for i in r1]
    ),

    # z == Sum(arr[r3]) - Sum(arr[r2])
)

minimize(
    Sum(arr[r3]) - Sum(arr[r2])  # z
)

""" Comments
1) avoiding the introduction of the variable z may improve the performance of the solvers
2)  java ace VrpSubmission-toy-D-2v-4l-w-reload.xml  -trace  
  => filtering process very long at some moment 
3) the array dep is not used
"""
