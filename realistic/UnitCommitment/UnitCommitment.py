"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  L03-T6G5L5.json

## Model
  constraints: Sum

## Execution
  python UnitCommitment.py -data=sm-10-13-00.json
  python UnitCommitment.py -data=sm-10-13-00.dzn -parser=UnitCommitment_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
"""

from pycsp3 import *

generators, loads = data or load_json_data("L03-T6G5L5.json")

min_capacities, max_capacities, dispatch_costs, init_commitments, startup_costs, shutdown_costs, max_ramp_rates, min_downtimes, max_startups = generators
demand, shed_cost, = loads

horizon, nGenerators, nLoads = len(max_capacities[0]), len(max_capacities), len(demand)
G, L, H = range(nGenerators), range(nLoads), range(horizon)

max_g = max(max(row) for row in max_capacities)

# x[i][t] is 1 if the ith generator is committed at time t
x = VarArray(size=[nGenerators, horizon], dom={0, 1})

# gl[i][t] is the level of the ith generator at time t
gl = VarArray(size=[nGenerators, horizon], dom=range(max_g // 2 + 1))

# ll[j][t] is the loss of the jth load at time t
ll = VarArray(size=[nLoads, horizon], dom=lambda j, t: range(demand[j][t] + 1))

# up[i][t] is 1 if the ith generator is up at time t
up = VarArray(size=[nGenerators, horizon], dom={0, 1})

# dn[i][t] is 1 if the ith generator is down at time t
dn = VarArray(size=[nGenerators, horizon], dom={0, 1})

satisfy(
    # ensuring dispatching conditions
    [
        (
            gl[i][t] <= max_capacities[i][t] * x[i][t],
            gl[i][t] >= min_capacities[i][t] * x[i][t]
        ) for i in G for t in H
    ],

    # initialization
    [
        x[:, 0] == init_commitments,
        up[:, 0] == 0,
        dn[:, 0] == 0
    ],

    # start-up/shut-down commitment logic
    [
        (
            up[i][t] == x[i][t] & ~x[i][t - 1],
            dn[i][t] == x[i][t - 1] & ~x[i][t]
        ) for i in G for t in H[1:]
    ],

    # copper plate one-bus simplified power-flow model
    [Sum(gl[:, t]) == Sum(demand[k][t] - ll[k][t] for k in L) for t in H],

    # ramping constraints
    [
        (
            If(up[i][t] == 0, Then=gl[i][t] - gl[i][t - 1] <= max_ramp_rates[i]),
            If(dn[i][t] == 0, Then=gl[i][t] - gl[i][t - 1] >= -1 * max_ramp_rates[i])
        ) for i in G for t in H[1:]
    ],

    # minimum downtime constraints
    [
        If(
            dn[i][t],
            Then=[~x[i][j] for j in range(t + 1, min(horizon, t + min_downtimes[i] + 1))]
        ) for i in G for t in H
    ],

    # Maximum generator start-up constraints (U.S. DoE emission)
    [Sum(up[i]) <= max_startups[i] for i in G]
)

minimize(
    dispatch_costs * gl +
    Sum(startup_costs[i] * Sum(up[i]) for i in G) +
    Sum(shutdown_costs[i] * Sum(dn[i]) for i in G) +
    Sum(shed_cost[j] * Sum(ll[j]) for j in L)
)

""" Comments
1) Domains are very large if we define domains with max_g and post:
     # Loss of load max
    [ll[j][t] <= demand[j][t] for j in range(nLoads) for t in range(horizon)],
"""
