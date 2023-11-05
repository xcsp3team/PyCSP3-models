"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  L03-T6G5L5.json

## Model
  constraints: Sum

## Execution
  python UnitCommitment.py -data=sm-10-13-00.json
  python UnitCommitment.py -data=sm-10-13-00.dzn -dataparser=UnitCommitment_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  real, mzn23
"""

from pycsp3 import *

gen_max, dispatch_cost, gen_min, init_commitment, startup_cost, shutdown_cost, max_ramp_rate, demand, shed_cost, min_down, max_num_start = data
horizon, nGenerators, nLoads = len(gen_max[0]), len(gen_max), len(demand)
maxg = max(v for row in gen_max for v in row)

# x[i][t] is 1 if the ith generator is committed at time t
x = VarArray(size=[nGenerators, horizon], dom={0, 1})

# gl[i][t] is the level of the ith generator at time t
gl = VarArray(size=[nGenerators, horizon], dom=range(maxg // 2 + 1))

# ll[j][t] is the loss of the jth load at time t
ll = VarArray(size=[nLoads, horizon], dom=lambda l, t: range(demand[l][t] + 1))

# up[i][t] is 1 if the ith generator is up at time t
up = VarArray(size=[nGenerators, horizon], dom={0, 1})

# dn[i][t] is 1 if the ith generator is down at time t
dn = VarArray(size=[nGenerators, horizon], dom={0, 1})

satisfy(
    # ensuring dispatching conditions
    [
        (
            gl[i][t] <= gen_max[i][t] * x[i][t],
            gl[i][t] >= gen_min[i][t] * x[i][t]
        ) for i in range(nGenerators) for t in range(horizon)
    ],

    # initialization
    [
        x[:, 0] == init_commitment,
        up[:, 0] == 0,
        dn[:, 0] == 0
    ],

    # start-up/shut-down commitment logic
    [
        (
            up[i][t] == x[i][t] & ~x[i][t - 1],
            dn[i][t] == x[i][t - 1] & ~x[i][t]
        ) for i in range(nGenerators) for t in range(1, horizon)
    ],

    # copper plate one-bus simplified power-flow model
    [Sum(gl[:, t]) == Sum(demand[l][t] - ll[l][t] for l in range(nLoads)) for t in range(horizon)],

    # ramping constraints
    [
        (
            If(up[i][t] == 0, Then=gl[i][t] - gl[i][t - 1] <= max_ramp_rate[i]),
            If(dn[i][t] == 0, Then=gl[i][t] - gl[i][t - 1] >= -1 * max_ramp_rate[i])
        ) for i in range(nGenerators) for t in range(1, horizon)
    ],

    # minimum downtime constraints
    [
        If(
            dn[i][t],
            Then=[~x[i][j] for j in range(t + 1, min(horizon, t + min_down[i] + 1))]
        ) for i in range(nGenerators) for t in range(horizon)
    ],

    # Maximum generator start-up constraints (U.S. DoE emission)
    [Sum(up[i]) <= max_num_start[i] for i in range(nGenerators)]
)

minimize(
    dispatch_cost * gl +
    Sum(startup_cost[i] * Sum(up[i]) for i in range(nGenerators)) +
    Sum(shutdown_cost[i] * Sum(dn[i]) for i in range(nGenerators)) +
    Sum(shed_cost[j] * Sum(ll[j]) for j in range(nLoads))
)

"""
 1) domains are very large if we define domains with maxg and post:
     # Loss of load max
    [ll[j][t] <= demand[j][t] for j in range(nLoads) for t in range(horizon)],
"""
