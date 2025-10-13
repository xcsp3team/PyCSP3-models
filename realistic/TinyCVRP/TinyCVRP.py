"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
For the original MZN model: MIT Licence.

## Data Example
  easy-04.json

## Model
  constraints: Maximum, Sum

## Execution
  python TinyCVRP.py -data=<datafile.json>
  python TinyCVRP.py -data=<datafile.dzn> -parser=TinyCVRP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn24
"""

from pycsp3 import *

capacities, demands, etas = data or load_json_data("easy-04.json")

nVehicles, nCustomers, nPlaces = len(capacities), len(demands) - 1, len(demands)
V, P = range(nVehicles), range(1, nPlaces)  # note that P starts at 1 (because it is the way we need it)

# visit[i][j] is 1 if the ith vehicle visits the jth place
visit = VarArray(size=[nVehicles, nPlaces], dom={0, 1})

# order[i][j] is the order the jth place is visited by the ith vehicle (0 if not visited)
order = VarArray(size=[nVehicles, nPlaces + 1], dom=range(nPlaces + 2))  # +1 to accommodate an explicit index for the vehicle's return to the depot

# last[i] is the last place visited by the ith vehicle
last = VarArray(size=nVehicles, dom=range(nPlaces))

satisfy(
    # not exceeding the capacity of each vehicle
    [demands * visit[i] <= capacities[i] for i in V],

    # visiting each customer location exactly once by one vehicle
    [Sum(visit[:, j]) == 1 for j in P],

    # handling start from depot
    [
        (
            visit[i][0] == 1,
            order[i][0] == 1
        ) for i in V
    ],

    # ensuring sequential order for visited locations (tour allocation)
    [
        If(
            visit[i][j] == 1,
            Then=order[i][j] > Maximum(order[i][k] * visit[i][k] for k in range(j)),
            Else=order[i][j] == 0
        ) for i in V for j in P
    ],

    # handling return to depot
    [
        order[i][-1] == Maximum(order[i][j] * visit[i][j] for j in P) + 1
        for i in V
    ],

    # computing the last customer of each vehicle
    [last[i] == Maximum(j * visit[i][j] for j in P) for i in V]
)

minimize(
    # minimizing the total ETA, including the return to the depot
    Sum(visit[i][j] * visit[i][k] * etas[j][k] for i in V for j, k in combinations(nPlaces, 2))
    + Sum(visit[i][last[i]] * etas[last[i]][0] for i in V)
)

# java ace TinyCVRP-hard-18.xml -rr -ale=4 => 6058 in 591s
