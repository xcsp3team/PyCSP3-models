"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2013 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  11.json

## Model
  constraints: Cumulative

## Execution
  python RCPSPz.py -data=<datafile.json>
  python RCPSPz.py -data=<datafile.dzn> -parser=RCPSP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  real, mzn08, mzn13
"""

from pycsp3 import *

capacities, durations, requirements, successors = data
nResources, nTasks = len(capacities), len(durations)
horizon = sum(durations) + 1

# x[i] is the starting time of the ith task
x = VarArray(size=nTasks, dom=range(horizon))

# z is the total end time (makespan)
z = Var(range(horizon))

satisfy(
    # precedence relations
    [x[i] + durations[i] <= x[j] for i in range(nTasks) for j in successors[i]],

    # redundant non-overlapping constraints  tag(redundant-constraints)
    [(x[i] + durations[i] <= x[j]) | (x[j] + durations[j] <= x[i]) for i, j in combinations(nTasks, 2)
     if any(requirements[r, i] + requirements[r, j] > capacities[r] for r in range(nResources))],

    # cumulative resource constraints
    [
        Cumulative(
            tasks=[(x[i], durations[i], requirements[r][i]) for i in range(nTasks)]
        ) <= capacities[r] for r in range(nResources)
    ],

    # constraining the objective value
    [x[i] + durations[i] <= z for i in range(nTasks)]
)

minimize(
    z
)
