"""
Capacitated Vehicle Routing problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
The MZN model was proposed by Andrea Rendl (CP formulation adapted to use instances for MIP models).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  A-n37-k5.json

## Model
  constraints: Circuit, Element, Sum

## Execution
  python CVRP.py -data=<datafile.json>
  python CVRP.py -data=<datafile.dzn> -parser=CVRP_ParserZ.py

## Links
  - https://en.wikipedia.org/wiki/Vehicle_routing_problem
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  real, mzn15
"""

from pycsp3 import *

capacity, demands, distances = data

n = len(demands)  # n is the number of customers
nVehicles = n  # here, n is also the number of vehicles
timeBudget = sum(max(distances[i][:-1]) for i in range(n))
nNodes = n + 2 * nVehicles

AllDepots = range(n, n + 2 * nVehicles)  # all nodes including start and end nodes
StartDepots = range(n, n + nVehicles)
EndDepots = range(n + nVehicles, n + 2 * nVehicles)

# adapting demands and distances to giant tour representation
demands = demands + [0] * (nNodes - n)
distances = cp_array([distances[i + 1, j + 1] if i < n and j < n else distances[0, i + 1] if i < n <= j else distances[
    j + 1, 0] if j < n <= i else distances[0, 0] for j in range(nNodes)] for i in range(nNodes))

# x[i] is the successor of the ith node
x = VarArray(size=nNodes, dom=range(nNodes))

# y[i] is the predecessor of the ith node
y = VarArray(size=nNodes, dom=range(nNodes))

# vh[i] is the vehicle visiting the ith customer
vh = VarArray(size=nNodes, dom=range(nVehicles))

# ld[i] is the load of the vehicle when arriving at the ith node
ld = VarArray(size=nNodes, dom=range(capacity + 1))

# at[i] is the time at which the vehicle serving node i will arrive at i
at = VarArray(size=nNodes, dom=range(timeBudget + 1))

satisfy(
    # predecessors of start nodes are end nodes
    [y[i] == i + nVehicles - 1 + (nVehicles if i == n else 0) for i in StartDepots],

    # successors of end nodes are start nodes
    [x[i] == i - nVehicles + 1 - (nVehicles if i == n + 2 * nVehicles - 1 else 0) for i in EndDepots],

    # associating each start/end node with a vehicle
    (
        [vh[i] == i - n for i in StartDepots],
        [vh[i] == i - n - nVehicles for i in EndDepots]
    ),

    # vehicles leave the depot at time zero
    [at[i] == 0 for i in StartDepots],

    # vehicle load when starting at the depot
    [ld[i] == 0 for i in StartDepots],

    # linking predecessor and successor variables
    (
        [x[y[i]] == i for i in range(nNodes)],
        [y[x[i]] == i for i in range(nNodes)]
    ),

    # ensuring a circuit
    [
        Circuit(x),
        Circuit(y)
    ],

    # vehicle of node i is the same as the vehicle for the predecessor
    (
        [vh[y[i]] == vh[i] for i in range(n)],
        [vh[x[i]] == vh[i] for i in range(n)]
    ),

    # time constraints
    (
        [at[i] + distances[i][x[i]] <= at[x[i]] for i in range(n)],
        [at[i] + distances[i][x[i]] <= at[x[i]] for i in StartDepots]
    ),

    # load constraints
    (
        [ld[i] + demands[i] == ld[x[i]] for i in range(n)],
        [ld[i] == ld[x[i]] for i in StartDepots]
    )
)

minimize(
    Sum(at[depot] for depot in EndDepots)
)
