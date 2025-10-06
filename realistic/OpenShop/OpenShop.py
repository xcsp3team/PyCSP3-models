"""
An open shop problem is identical to a job-shop problem with the exception that there is no ordering on the tasks of a job.
A job is a sequence of tasks.
A task involves processing by a single machine for some duration.
A machine can operate on at most one task at a time, for each job at most one task can be performed at a time.
Tasks cannot be interrupted.
The goal is to schedule each job to minimise the finishing time (makespan).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
The original MZN model was proposed by Diarmuid Grimes (adapted from Ralph Becket model).
Instances were taken from benchmarks proposed by Taillard, Gueret and Prin, and Brucker et al.; see links below.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  gp10-4.json

## Model
  constraints: Cumulative, NoOverlap

## Execution
  python OpenShop.py -data=<datafile.json>
  python OpenShop.py -data=<datafile.dzn> -parser=OpenShop_ParserZ.py

## Links
  - https://en.wikipedia.org/wiki/Open-shop_scheduling
  - https://www.sciencedirect.com/science/article/abs/pii/037722179390182M
  - https://link.springer.com/article/10.1023/A:1018930613891
  - https://www.sciencedirect.com/science/article/pii/S0166218X96001163
  - https://www.minizinc.org/challenge/2014/results/

## Tags
  realistic, mzn14
"""

from pycsp3 import *

nMachines, durations = data or load_json_data("gp10-4.json")

nJobs = len(durations)
Time = range(sum(sum(row) for row in durations) + 1)

J, M = range(nJobs), range(nMachines)

# x[j][m] is the starting time of job j on machine (task) m
x = VarArray(size=[nJobs, nMachines], dom=Time)

# z is the make-span
z = Var(dom=Time)

satisfy(
    # tasks on the same job cannot overlap
    [
        NoOverlap(
            origins=(x[j][m1], x[j][m2]),
            lengths=(durations[j][m1], durations[j][m2])
        ) for j in J for m1, m2 in combinations(M, 2)
    ],

    # tasks on the same machine cannot overlap
    [
        NoOverlap(
            origins=(x[j1][m], x[j2][m]),
            lengths=(durations[j1][m], durations[j2][m])
        ) for j1, j2 in combinations(J, 2) for m in M
    ],

    # tasks on the same job cannot overlap
    [
        Cumulative(
            Task(
                origin=x[j][m],
                length=durations[j][m],
                height=1
            ) for m in M
        ) <= 1 for j in J
    ],

    # tasks on the same machine cannot overlap
    [
        Cumulative(
            Task(
                origin=x[j][m],
                length=durations[j][m],
                height=1
            ) for j in J
        ) <= 1 for m in M
    ],

    # the finishing time must be no earlier than the finishing time of any task
    [
        x[j][m] + durations[j][m] <= z
        for j in J for m in M
    ]
)

minimize(
    z
)
