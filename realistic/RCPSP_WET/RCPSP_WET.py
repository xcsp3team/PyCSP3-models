"""
Resource-Constrained Project Scheduling Problems with Weighted Earliness/Tardiness objective (RCPSP/WET).

The objective is to find an optimal schedule so that tasks start as close as possible to
the given start time for each task, penalizing earliness or tardiness according to
the given weight for earliness and tardiness per task.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2017 challenges.
The original MZN model was proposed by University of Melbourne and NICTA (seems to be a MIT Licence).

## Data Example
  j30-27-5.json

## Model
  constraints: Cumulative, Sum

## Execution
  python RCPSP_WET.py -data=<datafile.json>
  python RCPSP_WET.py -data=<datafile.dzn> -parser=RCPSP_WET_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2017/results/

## Tags
  realistic, mzn16, mzn17
"""

from pycsp3 import *

resources, tasks, horizon = data or load_json_data("j30-27-5.json")

requirements, capacities = zip(*resources)
durations, successors, deadlines = zip(*tasks)

nTasks, nResources = len(tasks), len(resources)
T, R = range(nTasks), range(nResources)

relevantTasks = [[i for i in T if requirements[r][i] > 0 and durations[i] > 0] for r in R]

# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon))

satisfy(
    # enforcing precedence relations
    [s[i] + durations[i] <= s[j] for i in T for j in successors[i]],

    # cumulative resource constraints
    [
        Cumulative(
            Task(
                origin=s[i],
                length=durations[i],
                height=requirements[r][i]
            ) for i in relevantTasks[r]
        ) <= capacities[r] for r in R if sum(requirements[r][relevantTasks[r]]) > capacities[r]
    ],

    # redundant non-overlapping constraints  tag(redundant)
    [
        either(
            s[i] + durations[i] <= s[j],
            s[j] + durations[j] <= s[i]
        ) for i, j in combinations(T, 2) if any(requirements[r][i] + requirements[r][j] > capacities[r] for r in R)
    ],
)

minimize(
    # minimizing the weighted earliness/tardiness objective
    Sum(
        deadlines[i][1] * max(0, deadlines[i][0] - s[i]) + deadlines[i][2] * max(0, s[i] - deadlines[i][0]) for i in T
    )
)

"""
1) Note that:
 sum(requirements[r][relevantTasks[r]]) 
   is a shortcut for:
 sum(requirements[r][i] for i in relevantTasks[r])
"""
