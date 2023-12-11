"""
Multi-Skilled Project Scheduling Problem

This is a variation of the basic resource-constrained project scheduling problem.
A set of activities must be executed so that the project duration is minimised while satisfying:
  - precedence relations between some activities expressing that an activity can only be run after its preceding activity's execution is finished,
  - skills requirements of activities on workers who have the capability to  perform the activity,
  - workers availability, i.e., a worker can perform only one activity in each time period.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  easy-01.json

## Model
  constraints: Cumulative, Sum

## Execution
  python MSPSP.py -data=<datafile.json>
  python MSPSP.py -data=<datafile.dzn> -parser=MSPSP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn12
"""

from pycsp3 import *

skills, durations, requirements, successors = data
nWorkers, nTasks, nSkills = len(skills), len(durations), len(requirements)

rc = [len([j for j in range(nWorkers) if i in skills[j]]) for i in range(nSkills)]
possibleWorkers = [[j for j in range(nWorkers) if len([k for k in skills[j] if requirements[k][i] > 0]) > 0] for i in range(nTasks)]
WTasks = [[i for i in range(nTasks) if len([k for k in skills[j] if requirements[k][i] > 0]) > 0] for j in range(nWorkers)]
RTasks = [[i for i in range(nTasks) if requirements[k][i] > 0] for k in range(nSkills)]
overlap_attention = [(i, j) for i, j in combinations(nTasks, 2) if j not in successors[i] and i not in successors[j]
                     and len([k for k in range(nSkills) if requirements[k][i] + requirements[k][j] > rc[k]]) > 0]
horizon = sum(durations)  # trivial upper bound

# s[i] is the starting time of the ith task
s = VarArray(size=nTasks, dom=range(horizon + 1))

# w[j][i] is 1 if the jth worker is assigned to the ith task
w = VarArray(size=[nWorkers, nTasks], dom={0, 1})

# z is the project duration
z = Var(range(horizon + 1))

satisfy(
    # respecting precedence relations
    [s[i] + durations[i] <= s[j] for i in range(nTasks) for j in successors[i]],

    # ensuring skill requirements are met
    [Sum(w[j][i] for j in possibleWorkers[i] if k in skills[j]) >= R for i in range(nTasks) for k in range(nSkills) if (R := requirements[k][i]) > 0],

    # discarding some workers
    [w[j][i] == 0 for i in range(nTasks) for j in range(nWorkers) if j not in possibleWorkers[i]],

    # non-overlapping constraints for the workers  tag(redundant-constraints)
    [
        Cumulative(
            Task(origin=s[i], length=durations[i], height=w[j][i]) for i in WTasks[j]
        ) <= 1 for j in range(nWorkers) if len(WTasks[j]) > 1
    ],

    # avoiding tasks that cannot be performed at the same time to overlap
    [before | after for i, j in overlap_attention if (before := s[i] + durations[i] <= s[j], after := s[j] + durations[j] <= s[i])],

    # cumulative skill constraints
    [
        Cumulative(
            Task(origin=s[i], length=durations[i], height=requirements[k][i]) for i in RTasks[k]
        ) <= rc[k] for k in range(nSkills) if len(RTasks[k]) > 1 and sum(requirements[k][RTasks[k]]) > rc[k]
    ],

    # constraining the objective value
    [s[i] + durations[i] <= z for i in range(nTasks) if len(successors[i]) == 0]
)

minimize(
    # minimizing the project duration
    z
)

""" Comments
1) sum(requirements[k][RTasks[k]])
 is equivalent to:
   sum(requirements[k][i] for i in RTasks[k])
2) [before | after for i, j in overlap_attention if (before := s[i] + durations[i] <= s[j], after := s[j] + durations[j] <= s[i])],
 is equivalent to:
   [(s[i] + durations[i] <= s[j]) | (s[j] + durations[j] <= s[i]) for i, j in overlap_attention]
"""
