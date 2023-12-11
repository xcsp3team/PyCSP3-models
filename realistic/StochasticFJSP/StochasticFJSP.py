"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  a1-s2-t15-j3-m3.json

## Model
  constraints: Sum

## Execution
  python StochasticFJSP.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  realistic, mzn14
"""

from pycsp3 import *

nTasks, _, nMachines, horizon, nAdditionalTasks, jobs, durations, machines, add_starts, add_ends, add_machines, weights = data
nSetups = len(weights)
assert nAdditionalTasks == 1

decrement([jobs, machines, add_machines])  # to adapt the model, we need to decrement some numbers

# m[i] is the machine used for the ith task
m = VarArray(size=nTasks, dom=range(nMachines))

# s[k][i] is the starting time of the ith task in the kth setup
s = VarArray(size=[nSetups, nTasks], dom=range(1, horizon + 1))

# z[k] is the make-span in the kth setup
z = VarArray(size=nSetups, dom=range(1, horizon + 1))

satisfy(
    # ordering tasks in same jobs
    [s[k][i1] + durations[i1] <= s[k][i2] for k in range(nSetups) for i1, i2 in combinations(nTasks, 2) if jobs[i1] == jobs[i2]],

    # avoiding the overlapping of tasks using the same machine
    [
        If(
            m[i1] == m[i2],
            Then=either(s[k][i1] + durations[i1] <= s[k][i2], s[k][i2] + durations[i2] <= s[k][i1])
        ) for k in range(nSetups) for i1 in range(nTasks) for i2 in range(nTasks) if i1 != i2 and any(v in machines[i2] for v in machines[i1])
    ],

    # using appropriate machines
    [m[i] != j for i in range(nTasks) for j in range(nMachines) if j not in machines[i]],

    # handling stochastic constraints generated for each setup
    [
        If(
            m[i] == add_machines[k],
            Then=either(s[k][i] + durations[i] < add_starts[k], s[k][i] > add_ends[k])
        ) for k in range(nSetups) for i in range(nTasks)
    ],

    # constraining make-spans
    [s[k][i] + durations[i] <= z[k] for k in range(nSetups) for i in range(nTasks)]
)

minimize(
    # minimizing weighted make-spans
    weights * z
)

"""
1) note that data have been converted to JSON, because the model/instances were half flat
"""
