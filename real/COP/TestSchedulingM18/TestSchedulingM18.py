"""
This problem was presented as the Industrial Modelling Challenge at the conference CP2015.

From CSPLib: "The problem arises in the context of a testing facility.
A number of tests have to be performed in minimal time.
Each test has a given duration and needs to run on one machine.
While a test is running on a machine, no other test can use that machine.
Some tests can only be assigned to a subset of the machines, for others you can use any available machine.
For some tests, additional, possibly more than one, global resources are needed.
While those resources are used for a test, no other test can use the resource.
The objective is to finish the set of all tests as quickly as possible."

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Gustav Björdal (in 2018).
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  t030m10r03-15.json

## Model
  constraints: Cumulative, Maximum, Minimum, NoOverlap, Precedence, Table

## Execution
  python TestSchedulingM18.py -data=<datafile.json>
  python TestSchedulingM18.py -data=<datafile.dzn> -parser=TestSchedulingM18_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob073/
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, csplib, mzn18, mzn23
"""

from pycsp3 import *

nMachines, capacities, tests = data
durations, machines, resources = zip(*tests)
nResources, nTests = len(capacities), len(tests)

# lb and ub are minimal and maximal values for the make-span
lb = max(sum(durations[t] for t in range(nTests) if r in resources[t]) for r in range(nResources))
ub = max(sum(durations[t] for t in range(nTests) if m in machines[t]) for m in range(nMachines))
symmetricalMachines = [j for j in range(nMachines) if len([i for i in range(nTests) if j in machines[i] and len(machines[i]) < nMachines]) == 0]

# x[i] is the machine used for the ith test
x = VarArray(size=nTests, dom=range(nMachines))

# s[i] is the starting time of the ith test
s = VarArray(size=nTests, dom=range(ub - max(durations) + 1))

# z is the make-span
z = Var(dom=range(lb, ub + 1))

satisfy(
    # executing tests on valid machines
    [x[i] in machines[i] for i in range(nTests)],

    # avoiding tests to overlap when run on the same machine
    [
        Cumulative(
            tasks=[Task(origin=s[i], length=durations[i], height=x[i] == m) for i in range(nTests)]
        ) <= 1 for m in range(nMachines)
    ],

    # avoiding tests to overlap when using the same resource
    [
        NoOverlap(
            tasks=[Task(origin=s[i], length=durations[i]) for i in range(nTests) if r in resources[i]]
        ) for r in range(nResources)
    ],

    # tag(symmetry-breaking)
    Precedence(x, values=symmetricalMachines),

    # tag(redundant-constraint)
    Minimum(s) == 0,

    # computing the objective value
    z == Maximum(s[i] + durations[i] for i in range(nTests))
)

minimize(
    z
)
