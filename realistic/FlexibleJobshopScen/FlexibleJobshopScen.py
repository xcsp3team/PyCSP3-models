"""
From CSPLib, Problem 077 (and proposed by David Hemmi, Guido Tack and Mark Wallace):

    "The stochastic assignment and scheduling problem is a two-stage stochastic optimisation problem with recourse.
    A set of jobs, each composed of multiple tasks, is to be scheduled on a set of machines.
    Precedence constraints ensure that tasks, which belong to the same job are executed sequentially.
    Once the processing of a task has started, it can not be interrupted (non preemptive scheduling).
    The tasks may be restricted to a sub-set of machines. No more that one task may be executed concurrently on a machine.
    The task processing time depends on the selected machine, e.g. certain machines can finish a task faster than others.
    Furthermore, the processing times are subject to uncertainty, e.g. random variables.
    Scenarios are used to describe the uncertainty.
    A scenario describes a situation where all processing times are known and a complete schedule can be created.
    We assume that all processing times are known at the beginning of the second stage.

    The problem is composed of two stages.
    In the first stage, all the tasks have to be allocated to a machine. Once the tasks are allocated, their processing time is revealed.
    In the second stage a schedule for each machine is created, with respect to the observed processing times.
    The objective is to find a task to machine assignment minimizing the expected (average) makespan over all scenarios.
    Flexible Job Shop Scheduling is more general than Job Shop Scheduling as some tasks can be run an alternative machines.
    The goal remains to find a feasible schedule minimising the makespan.
    Each job is composed of tasks and each task must be executed by exactly one among several optional operations.
    Machines and durations are given for optional operations."

The model, below, is close to (can be seen as the close translation of) the one present at CSPLib.
The MZN model was proposed by Andreas Schutt (Copyright 2013 National ICT Australia).

## Data Example
  easy01.json

## Model
  constraints: Cumulative, Sum, Count

## Execution
  python FlexibleJobshopScen.py -data=<datafile.json>
  python FlexibleJobshopScen.py -data=<datafile.dzn> -parser=FlexibleJobshop_ParserZ.py
  python FlexibleJobshopScen.py -data=[datafile.dzn,"20"] -parser=FlexibleJobshop_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob077/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, csplib, xcsp25
"""

from pycsp3 import *

first_scen, last_scen, nMachines, tasks, options, option_machines, weights, durations = data
nAllScenarios, nJobs, nTasks, nOptions = len(durations), len(tasks), len(options), len(option_machines)

assert first_scen == 0 and 0 < last_scen < nAllScenarios
nScenarios = last_scen + 1

siblings = [next(tasks[i] for i in range(nJobs) if t in tasks[i]) for t in range(nTasks)]
minDurations = [[min(durations[s][options[t]]) for t in range(nTasks)] for s in range(nScenarios)]
maxDurations = [[max(durations[s][options[t]]) for t in range(nTasks)] for s in range(nScenarios)]
minStarts = [[sum(minDurations[s][k] for k in siblings[t] if k < t) for t in range(nTasks)] for s in range(nScenarios)]
maxStarts = [[sum(durations[s]) - sum(minDurations[s][k] for k in siblings[t] if k >= t) for t in range(nTasks)] for s in range(nScenarios)]

taskForOperation = [next(t for t in range(nTasks) if o in options[t]) for o in range(nOptions)]

t_max = [sum(max(durations[s][o] for o in options[t]) for t in range(nTasks)) for s in range(nScenarios)]

# x[s][t] is the starting time of the task t in the scenario s
x = VarArray(size=[nScenarios, nTasks], dom=lambda s, t: range(minStarts[s][t], maxStarts[s][t] + 1))

# d[s][t] is the duration of the task t in the scenario s
d = VarArray(size=[nScenarios, nTasks], dom=lambda s, t: range(minDurations[s][t], maxDurations[s][t] + 1))

# b[o] is 1 iff the optional operation o (for some task) is executed
b = VarArray(size=nOptions, dom={0, 1})

# z[s] is the duration of scenario s
z = VarArray(size=nScenarios, dom=range(max(t_max) + 1))

satisfy(
    # respecting precedence relations
    [x[s][t] + d[s][t] <= x[s][t + 1] for s in range(nScenarios) for i in range(nJobs) for t in tasks[i][:-1]],

    # computing durations of tasks
    [
        b[o] == 1 if len(options[t]) == 1 else If(b[o], Then=d[s][t] == durations[s][o])
        for o in range(nOptions) for s in range(nScenarios) if [t := taskForOperation[o]]
    ],

    # managing optional operations
    [
        [Sum(b[o] for o in T) <= 1 for t in range(nTasks) if len(T := options[t]) > 1],
        [Exist(b[o] for o in T) for t in range(nTasks) if len(T := options[t]) > 1],
        [b[min(T)] == ~b[max(T)] for t in range(nTasks) if len(T := options[t]) == 2]
    ],

    # cumulative resource constraints
    [
        Cumulative(
            tasks=[Task(origin=x[s][taskForOperation[o]], length=durations[s][o], height=b[o]) for o in range(nOptions) if option_machines[o] == m]
        ) <= 1 for m in range(nMachines) for s in range(nScenarios)
    ],

    # computing the objective
    [x[s][tasks[i][-1]] + d[s][tasks[i][-1]] <= z[s] for s in range(nScenarios) for i in range(nJobs)]

)

minimize(
    # minimizing the weighted combination of make-spans
    Sum(weights[s] * z[s] for s in range(nScenarios))
)
