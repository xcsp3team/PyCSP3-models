"""
This is a cyclic resource-constrained project scheduling problem with generalised precedence relations
constrained to scarce cumulative resources and tasks which are repeated infinitely.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2014 Minizinc challenges.
The original model has: Copyright (C) 2011 The University of Melbourne and NICTA

## Data Example
  easy-4.json

## Model
  constraints: Cumulative, Maximum, Minimum

## Execution
  python CyclicRCPSP.py -data=<datafile.json>
  python CyclicRCPSP.py -data=<datafile.dzn> -parser=CyclicRCPSP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  realistic, mzn11, mzn14
"""

from pycsp3 import *

capacities, requirements, precedences = data
nResources, nTasks, nPrecedences = len(capacities), len(requirements), len(precedences)

d = [0] + [1] * (nTasks - 2) + [0]  # tasks have a unit duration, except for the artificial source and sink tasks
horizon = sum(precedences[i][2] for i in range(nPrecedences))  # maximal period

# resources per task
resources = [[i for i in range(nTasks) if requirements[i][r] > 0 and d[i] > 0] for r in range(nResources)]

# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon + 1))

# k[i] is the iteration of the ith task
k = VarArray(size=nTasks, dom=range(nTasks + 1))

# b[j] is 1 if the jth precedence relation is respected (wrt latency)
b = VarArray(size=nPrecedences, dom={0, 1})

# z is the make-span of one iteration
z = Var(dom=range(horizon + 1))

satisfy(
    # computing the make-span
    z == 1 + Maximum(s[i] - k[i] * s[-1] for i in range(nTasks - 1)) - Minimum(s[i] - k[i] * s[-1] for i in range(nTasks - 1)),

    # generalised precedence constraints
    [
        (
            b[p] == (s[i] + latency <= s[j]),
            k[i] + ~b[p] <= k[j] + distance
        ) for p, (i, j, latency, distance) in enumerate(precedences)
    ],

    # redundant non-overlapping constraints  tag(redundant-constraints)
    [(s[i] + d[i] <= s[j]) | (s[j] + d[j] <= s[i]) for i, j in combinations(nTasks, 2)
     if any(requirements[i][r] + requirements[j][r] > capacities[r] for r in range(nResources))],

    # cumulative resource constraints
    [
        Cumulative(
            tasks=[(s[i], d[i], requirements[i][r]) for i in resources[r]]
        ) <= capacities[r] for r in range(nResources) if sum(requirements[i][r] for i in resources[r]) > capacities[r]
    ],

    # computing the value of the last iteration
    k[-1] == Maximum(k[:-1]),

    # ensuring the last task starts after all other ones
    [s[i] + d[i] <= s[-1] for i in range(nTasks - 1)],

    # tag(symmetry-breaking)
    [
        s[0] == 0,
        k[0] == 0
    ]
)

minimize(
    # minimizing the schedule period, and then the make-span of one iteration
    s[-1] * horizon + z
)
