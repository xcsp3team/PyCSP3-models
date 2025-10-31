"""
From Wikipedia:
    Open-shop scheduling is an optimization problem in computer science and operations research.
    It is a variant of optimal job scheduling.
    In a general job-scheduling problem, we are given n jobs J1, J2, ..., Jn of varying processing times,
    which need to be scheduled on m machines with varying processing power, while trying to minimize the makespan
    - the total length of the schedule (that is, when all the jobs have finished processing).
    In the specific variant known as open-shop scheduling, each job consists of a set of operations O1, O2, ..., On
    which need to be processed in an arbitrary order.

## Data Example
  GP-os-01.json

## Model
  constraints: AllDifferent, Element, Maximum, NoOverlap

## Execution
  python SchedulingOS.py -data=<datafile.json>

## Links
  - https://en.wikipedia.org/wiki/Open-shop_scheduling
  - https://dl.acm.org/doi/10.1145/321978.321985
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

durations = data or load_json_data("GP-os-01.json")  # durations[i][j] is the duration of operation/machine j for job i

horizon = sum(sum(t) for t in durations) + 1

n, m = len(durations), len(durations[0])
N, M = range(n), range(m)

# s[i][j] is the start time of the jth operation for the ith job
s = VarArray(size=[n, m], dom=range(horizon))

# d[i][j] is the duration of the jth operation of the ith job
d = VarArray(size=[n, m], dom=lambda i, j: durations[i])

# mc[i][j] is the machine used for the jth operation of the ith job
mc = VarArray(size=[n, m], dom=range(m))

# sd[i][k] is the start (dual) time of the kth machine when used for the ith job
sd = VarArray(size=[n, m], dom=range(horizon))

satisfy(
    # operations must be ordered on each job
    [Increasing(s[i], lengths=d[i]) for i in N],

    # each machine must be used for each job
    [AllDifferent(mc[i]) for i in N],

    [
        Table(
            scope=(mc[i][j], d[i][j]),
            supports=enumerate(durations[i])
        ) for j in M for i in N
    ],

    # tag(channeling)
    [sd[i][mc[i][j]] == s[i][j] for j in M for i in N],

    # no overlap on resources
    [
        NoOverlap(
            origins=sd[:, j],
            lengths=durations[:, j]
        ) for j in M
    ],

    # tag(redundant)
    [s[i][-1] + d[i][-1] >= sum(durations[i]) for i in N]
)

minimize(
    # minimizing the makespan
    Maximum(s[i][-1] + d[i][-1] for i in N)
)
