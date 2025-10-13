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

## Data Example
  t020m10r03-1.json

## Model
  constraints: Cumulative, Maximum, NoOverlap

## Execution
  python TestScheduling.py -data=<datafile.json>
  python TestScheduling.py -data=<datafile.pl> -parser=TestScheduling_Parser.py

## Links
  - https://www.csplib.org/Problems/prob073/
  - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  realistic, csplib, xcsp24
"""

from pycsp3 import *

nMachines, nResources, tests = data or load_json_data("t020m10r03-1.json")

durations, machines, resources = zip(*tests)  # information split over the tests

nTests = len(tests)
horizon = sum(durations) + 1  # computing a better upper bound?

tests_by_single_machines = [t for t in [[i for i in range(nTests) if len(machines[i]) == 1 and m in machines[i]] for m in range(nMachines)] if len(t) > 1]
tests_by_resources = [t for t in [[i for i in range(nTests) if r in resources[i]] for r in range(nResources)] if len(t) > 1]


def conflicting_tests():
    def possibly_conflicting(i, j):
        return len(machines[i]) == 0 or len(machines[j]) == 0 or len(set(machines[i] + machines[j])) != len(machines[i]) + len(machines[j])

    pairs = [(i, j) for i, j in combinations(nTests, 2) if possibly_conflicting(i, j)]
    for t in tests_by_single_machines + tests_by_resources:
        for i, j in combinations(t, 2):
            if (i, j) in pairs:
                pairs.remove((i, j))  # because will be considered in another posted constraint
    return pairs


# s[i] is the starting time of the ith test
s = VarArray(size=nTests, dom=range(horizon))

# m[i] is the machine used for the ith test
m = VarArray(size=nTests, dom=lambda i: range(nMachines) if len(machines[i]) == 0 else machines[i])

satisfy(
    # no overlapping on machines
    [
        If(
            m[i] == m[j],
            Then=either(
                s[i] + durations[i] <= s[j],
                s[j] + durations[j] <= s[i]
            )
        ) for i, j in conflicting_tests()
    ],

    # no overlapping on single pre-assigned machines
    [
        NoOverlap(
            tasks=[
                Task(
                    origin=s[i],
                    length=durations[i]
                ) for i in t
            ]
        ) for t in tests_by_single_machines
    ],

    # no overlapping on resources
    [
        NoOverlap(
            tasks=[
                Task(
                    origin=s[i],
                    length=durations[i]
                ) for i in t
            ]
        ) for t in tests_by_resources
    ],

    # no more than the available number of machines used at any time  tag(redundant-constraints)
    Cumulative(
        origins=s,
        lengths=durations,
        heights=[1] * nTests
    ) <= nMachines
)

minimize(
    # minimizing the makespan
    Maximum(s[i] + durations[i] for i in range(nTests))
)

""" Comments
1) The first group of NoOverlap constraints could be alternatively written:
  [NoOverlap((s[i], durations[i]) for i in t) for t in tests_by_single_machines],
  or [NoOverlap(origins=[s[i] for i in t], lengths=[durations[i] for i in t]) for t in tests_by_single_machines],
"""
