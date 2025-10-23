# Problem: FlexibleJobshopScen

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
The original MZN model was proposed by Andreas Schutt (Copyright 2013 National ICT Australia).

## Data Example
  see data files from the 2025 competition

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python FlexibleJobshopScen.py -data=<datafile.json>
  python FlexibleJobshopScen.py -data=<datafile.dzn> -parser=FlexibleJobshop_ParserZ.py
  python FlexibleJobshopScen.py -data=[datafile.dzn,"20"] -parser=FlexibleJobshop_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob077/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, csplib, xcsp25
