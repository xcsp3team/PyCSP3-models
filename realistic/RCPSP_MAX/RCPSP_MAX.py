"""
Resource-constrained Project Scheduling Problems with minimal and maximal time lags (RCPSP-max).
We have resources, activities, and precedence constraints.
Resources have a specific capacity and activities require some resources for their execution.
The objective is to find an optimal schedule minimizing the project duration.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010 Minizinc challenge.
The MZN model was proposed by the University of Melbourne and NICTA, Copyright (C) 2010.
The Licence seems to be like a MIT Licence.

## Data Example
  psp-j20-34.json

## Model
  constraints: Cumulative

## Execution
  python RCPSP_MAX.py -data=<datafile.json>
  python RCPSP_MAX.py -data=<datafile.dzn> -parser=RCPSP_MAX_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2010/results/

## Tags
  realistic, mzn10
"""

from pycsp3 import *

capacities, durations, requirements, precedences = data or load_json_data("psp-j20-34.json")

nTasks, nResources = len(durations), len(capacities)
T, R = range(nTasks), range(nResources)

# trivial upper bound for the project duration
horizon = sum(max([durations[i]] + [d for (j, d, _) in precedences if j == i]) for i in T) + 1

P = [(i, j) for i, j in combinations(T, 2) if any(requirements[r][i] + requirements[r][j] > capacities[r] for r in R)]
P1 = [(i, j) for i, j in P if any(k == i and l == j and -durations[j] < d < durations[i] for (k, d, l) in precedences)]
P2 = [(i, j) for i, j in P if any(k == j and l == i and -durations[i] < d < durations[j] for (k, d, l) in precedences)]
P3 = [(i, j) for i, j in P if (i, j) not in P1 and (i, j) not in P2]

# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon))

# z is the make-span
z = Var(dom=range(horizon))

satisfy(
    # ensuring some precedence relations
    [s[i] + d <= s[j] for (i, d, j) in precedences],

    # redundant non-overlapping constraints
    (
        [s[i] + durations[i] <= s[j] for i, j in P1],

        [s[j] + durations[j] <= s[i] for i, j in P2],

        [
            either(
                s[i] + durations[i] <= s[j],
                s[j] + durations[j] <= s[i]
            ) for i, j in P3
        ]
    ),

    # cumulative resource constraints
    [
        Cumulative(
            Task(
                origin=s[i],
                length=durations[i],
                height=requirements[r][i]
            ) for i in T
        ) <= capacities[r] for r in R
    ],

    # constraining the objective value
    [s[i] + durations[i] <= z for i in T]
)

minimize(
    z
)
