"""
Resource-Constrained Project Scheduling Problems with Weighted Earliness/Tardiness objective (RCPSP/WET).

The objective is to find an optimal schedule so that tasks start as close as possible to
the given start time for each task, penalizing earliness or tardiness according to
the given weight for earliness and tardiness per task.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2017 challenges.
The MZN model was proposed by University of Melbourne and NICTA (seems to be a MIT Licence).

## Data Example
  j30-27-5.json

## Model
  constraints: Cumulative, Sum

## Execution
  python RCPSP_WET.py -data=<datafile.json>
  python RCPSP_WET.py -data=<datafile.dzn> -parser=RCPSP_WET_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn16, mzn17
"""

from pycsp3 import *

resources, tasks, horizon = data
requirements, capacities = zip(*resources)
durations, successors, deadlines = zip(*tasks)
nTasks, nResources = len(tasks), len(resources)

relevantTasks = [[i for i in range(nTasks) if requirements[r][i] > 0 and durations[i] > 0] for r in range(nResources)]

# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon))

satisfy(
    # enforcing precedence relations
    [s[i] + durations[i] <= s[j] for i in range(nTasks) for j in successors[i]],

    # cumulative resource constraints
    [
        Cumulative(
            tasks=[Task(origin=s[i], length=durations[i], height=requirements[r][i]) for i in relevantTasks[r]]
        ) <= capacities[r] for r in range(nResources) if sum(requirements[r][relevantTasks[r]]) > capacities[r]
    ],

    # redundant non-overlapping constraints  tag(redundant)
    [
        either(
            s[i] + durations[i] <= s[j],
            s[j] + durations[j] <= s[i]
        ) for i, j in combinations(nTasks, 2) if any(requirements[r][i] + requirements[r][j] > capacities[r] for r in range(nResources))
    ],
)

minimize(
    # minimizing the weighted earliness/tardiness objective
    Sum(
        deadlines[i][1] * max(0, deadlines[i][0] - s[i]) + deadlines[i][2] * max(0, s[i] - deadlines[i][0]) for i in range(nTasks)
    )
)

"""
1) Note that:
 sum(requirements[r][relevantTasks[r]]) 
   is a shortcut for:
 sum(requirements[r][i] for i in relevantTasks[r])
"""
