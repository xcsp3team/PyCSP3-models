"""
Job-shop Scheduling

## Data Example
  e0ddr1-0.json

## Model
  constraints: Maximum, NoOverlap

## Execution
  python SchedulingJS.py -data=<datafile.json>

## Links
  - https://en.wikipedia.org/wiki/Job_shop_scheduling

## Tags
  realistic
"""
from pycsp3 import *

jobs = data or load_json_data("e0ddr1-0.json")

durations, resources, release_dates, due_dates = zip(*jobs)
assert all(len(t) == len(durations[0]) for t in durations) and all(len(t) == len(durations[0]) for t in resources)

n, m = len(jobs), len(jobs[0].durations)

horizon = max(due_dates) if all(v != -1 for v in due_dates) else sum(sum(t) for t in durations)

# s[i][j] is the start time of the jth operation for the ith job
s = VarArray(size=[n, m], dom=range(horizon))

satisfy(
    # operations must be ordered on each job
    [Increasing(s[i], lengths=durations[i]) for i in range(n)],

    # respecting release dates
    [s[i][0] > release_dates[i] for i in range(n) if release_dates[i] > 0],

    # respecting due dates
    [s[i][-1] <= due_dates[i] - durations[i][-1] for i in range(n) if 0 <= due_dates[i] < horizon - 1],

    # no overlap on resources
    [
        NoOverlap(
            tasks=[
                Task(
                    origin=s[i][resources[i].index(j)],
                    length=durations[i][resources[i].index(j)]
                ) for i in range(n)
            ]
        ) for j in range(m)
    ]
)

minimize(
    # minimizing the makespan
    Maximum(s[i][-1] + durations[i][-1] for i in range(n))
)

""" Comments
1) The group of overlap constraints could be equivalently written:
 [NoOverlap(origins=[s[i][[resources[i].index(j)] for i in range(n)], lengths=[durations[i][[resources[i].index(j)] for i in range(n)]) for j in range(m)]
"""
