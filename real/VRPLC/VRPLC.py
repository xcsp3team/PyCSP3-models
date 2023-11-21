"""
The Vehicle Routing Problem with Location Congestion (VRPLC) adds cumulative scheduling constraints
on to the standard Pickup and Delivery Problem with Time Windows (PDPTW).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Edward Lam, and described in the 2016 paper of Constraints Journal (see below).
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  09-5-10-s1.json

## Model
  constraints: Circuit, Cumulative, Element, Sum

## Execution
  python VRPLC.py -data=<datafile.json>
  python VRPC.py -data=<datafile.dzn> -parser=VRPLC_ParserZ.py

## Links
  - https://link.springer.com/article/10.1007/s10601-016-9241-2
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, mzn18, mzn23
"""

from pycsp3 import *

horizon, nVehicles, vehicleCapacity, nLocations, locationCapacity, nPickups, times, requests = data
l, a, b, s, q = zip(*requests)
nNodes, n = len(times), len(requests)  # n is the number of requests (pickups and deliveries)

MainNodes = range(n + nVehicles)  # request and start nodes
Depots = range(n, nNodes)  # start and end nodes
qq = cp_array(list(q) + [0 for i in Depots])

# veh[i] is the vehicle visiting the ith node
veh = VarArray(size=nNodes, dom=range(nVehicles))

# succ[i] is the node that succeeds to the ith node
succ = VarArray(size=nNodes, dom=range(nNodes))

# load[i] is the load after visiting the ith node
load = VarArray(size=nNodes, dom=range(vehicleCapacity + 1))

# arr[i] is the arrival time at the ith node
arr = VarArray(size=nNodes, dom=range(horizon + 1))

# ser[i] is the starting time of service at the ith node
ser = VarArray(size=nNodes, dom=range(horizon + 1))

# dep[i] is the departure time of the ith node
dep = VarArray(size=nNodes, dom=range(horizon + 1))

satisfy(
    # ensuring a circuit
    Circuit(succ),

    # giant tour representation of routes
    (
        [succ[n + nVehicles + v] == n + v + 1 for v in range(nVehicles - 1)],
        succ[-1] == n
    ),

    # tracking vehicle along route
    (
        [veh[i] == veh[succ[i]] for i in MainNodes],
        [veh[n + v] == v for v in range(nVehicles)],
        [veh[n + nVehicles + v] == v for v in range(nVehicles)]
    ),

    # ordering time-related variables
    (
        (
            arr[i] <= ser[i],
            ser[i] + s[i] <= dep[i],
            a[i] <= ser[i],
            ser[i] <= b[i]
        ) for i in range(n)
    ),

    # setting time at start and end nodes
    [
        [arr[i] == ser[i] for i in Depots],
        [ser[i] == dep[i] for i in Depots]
    ],

    # accumulating time along route
    [dep[i] + times[i][succ[i]] == arr[succ[i]] for i in MainNodes],

    # accumulating load along route
    [load[i] + qq[succ[i]] == load[succ[i]] for i in MainNodes],

    # setting load at start and end nodes
    [load[i] == 0 for i in Depots],

    # delivery after pickup
    [dep[i] + times[i][nPickups + i] <= arr[nPickups + i] for i in range(nPickups)],

    # delivery on same vehicle as pickup
    [veh[i] == veh[nPickups + i] for i in range(nPickups)],

    # handling service resources
    [
        Cumulative(
            tasks=[Task(origin=ser[i], length=s[i], height=1) for i in range(n) if l[i] == ll]
        ) <= locationCapacity for ll in range(nLocations)
    ],

    # tag(symmetry-breaking)
    (
        [
            If(
                succ[n + v] == n + nVehicles + v,
                Then=succ[n + v + 1] == n + nVehicles + v + 1
            ) for v in range(nVehicles - 1)
        ],
        veh[0] == 0
    )
)

minimize(
    # minimizing the total travel distance
    Sum(times[i][succ[i]] for i in MainNodes)
)
