"""
Flexible Job Shop Scheduling is more general than Job Shop Scheduling as some tasks can be run an alternative machines.
The goal remains to find a feasible schedule minimising the makespan.
Each job is composed of tasks and each task must be executed by exactly one among several optional operations.
Machines and durations are given for optional operations.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013 Minizinc challenge.
The MZN model was proposed by Andreas Schutt (Copyright 2013 National ICT Australia).

## Data Example
  easy01.json

## Model
  constraints: Cumulative, Maximum, Sum, Count

## Execution
  python FlexibleJobshop.py -data=<datafile.json>
  python FlexibleJobshop.py -data=<datafile.dzn> -parser=FlexibleJobshop_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  real, mzn13
"""

from pycsp3 import *

nMachines, tasks, operations, machines, durations = data
nJobs, nTasks, nOperations = len(tasks), len(operations), len(machines)

siblings = [next(tasks[i] for i in range(nJobs) if t in tasks[i]) for t in range(nTasks)]
minDurations = [min(durations[operations[t]]) for t in range(nTasks)]
maxDurations = [max(durations[operations[t]]) for t in range(nTasks)]
minStarts = [sum(minDurations[k] for k in siblings[t] if k < t) for t in range(nTasks)]
maxStarts = [sum(durations) - sum(minDurations[k] for k in siblings[t] if k >= t) for t in range(nTasks)]

taskForOperation = [next(t for t in range(nTasks) if o in operations[t]) for o in range(nOperations)]

# x[t] is the starting time of the task t
x = VarArray(size=nTasks, dom=lambda t: range(minStarts[t], maxStarts[t] + 1))

# d[t] is the duration of the task t
d = VarArray(size=nTasks, dom=lambda t: range(minDurations[t], maxDurations[t] + 1))

# b[o] is 1 iff the optional operation o (for some task) is executed
b = VarArray(size=nOperations, dom={0, 1})

satisfy(
    # respecting precedence relations
    [x[t] + d[t] <= x[t + 1] for i in range(nJobs) for t in tasks[i][:-1]],

    # computing durations of tasks
    [
        b[o] == 1 if len(operations[t]) == 1 else If(b[o], Then=d[t] == durations[o])
        for o in range(nOperations) if [t := taskForOperation[o]]
    ],

    # managing optional operations
    [
        [Sum(b[o] for o in T) <= 1 for t in range(nTasks) if len(T := operations[t]) > 1],
        [Exist(b[o] for o in T) for t in range(nTasks) if len(T := operations[t]) > 1],
        [b[min(T)] == ~b[max(T)] for t in range(nTasks) if len(T := operations[t]) == 2]
    ],

    # cumulative resource constraints
    [
        Cumulative(
            Task(origin=x[taskForOperation[o]], length=durations[o], height=b[o]) for o in range(nOperations) if machines[o] == m
        ) <= 1 for m in range(nMachines)
    ]
)

minimize(
    # minimizing the make-span
    Maximum(x[tasks[i][-1]] + d[tasks[i][-1]] for i in range(nJobs))
)

""" Comments
1) The two first groups of the block "managing optional operations" can be simplified as:
 [ExactlyOne(b[o] for o in operations[t]) for t in range(nTasks) if len(operations[t]) > 1],
   but we kept the form as given in the MZN model.
2) The block "computing durations of tasks" cab be written:
 [(b[o] == 0) | (d[taskForOperation[o]] == durations[o]) for o in range(nOperations) if len(operations[taskForOperation[o]]) > 1],
 [b[o] == 1 for o in range(nOperations) if len(operations[taskForOperation[o]]) == 1]
"""
