"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Ties Westendorp, under the MIT Licence.

## Data Example
  small-4.json

## Model
  constraints: Sum

## Execution
  python RosterSickness.py -data=<datafile.json>
  python RosterSickness.py -data=<datafile.dzn> -parser=RosterSickness_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn22
"""

from pycsp3 import *

shifts, employees = data
starts, stops, required = zip(*shifts)
contracts, expertises, assigned = zip(*employees)
nShifts, nEmployees = len(shifts), len(employees)

W = 1 + max(max(contracts), max(stops[s] - starts[s] for s in range(nShifts)))  # weight factor for building a lexicographical objective

ES = [(e, s) for e in range(nEmployees) for s in range(nShifts)]

O1, O2 = [], [[] for _ in range(nShifts)]
for s1 in range(nShifts):
    for s2 in range(s1 + 1, nShifts):
        if starts[s1] < stops[s2] and starts[s2] < stops[s1]:
            O1.append((s1, s2))
            O2[s1].append(s2)
            O2[s2].append(s1)

# x[i][j] is 1 if the ith employee works in the jth shift
x = VarArray(size=[nEmployees, nShifts], dom={0, 1})

# y[i] is the difference between the contract and the achieved working time
y = VarArray(size=nEmployees, dom=lambda e: range(-contracts[e], max(4 * contracts[e], 500) + 1))  # hard coding: constants 4 and 500

satisfy(
    # setting some assignments
    [x[e][s] == 1 for e, s in ES if assigned[e][s]],

    # setting some non-assignments
    [x[e][s] == 0 for e, s in ES if any(assigned[f][s] for f in range(nEmployees) if e != f)],

    # at most one assignment
    [Sum(x[:, s]) <= 1 for s in range(nShifts)],

    # no overlapping assignments (a)
    [x[e][s1] + x[e][s2] <= 1 for e in range(nEmployees) for s1, s2 in O1 if not assigned[e][s1] and not assigned[e][s2]],

    # appropriate expertise required
    [x[e][s] == 0 for e, s in ES if not (assigned[e][s] or required[s] in expertises[e])],

    # no overlapping assignments (b)
    [Sum(x[e][t] for t in O2[s]) <= max(1, sum(assigned[e][t] for t in O2[s])) for e, s in ES],

    # computing the differences between working times and the contracts
    [y[e] == Sum(x[e][s] * (stops[s] - starts[s]) for s in range(nShifts)) - contracts[e] for e in range(nEmployees)]
)

maximize(
    W * Sum(x) - Sum(abs(y[e]) for e in range(nEmployees))
)
