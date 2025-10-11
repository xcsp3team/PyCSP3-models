"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The original MZN model was proposed by Ties Westendorp, under the MIT Licence.

## Data Example
  small-4.json

## Model
  constraints: Sum

## Execution
  python RosterSickness.py -data=<datafile.json>
  python RosterSickness.py -data=<datafile.dzn> -parser=RosterSickness_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2022/results/

## Tags
  realistic, mzn22
"""

from pycsp3 import *

shifts, employees = data or load_json_data("small-4.json")

starts, stops, required = zip(*shifts)
contracts, expertises, assigned = zip(*employees)

nShifts, nEmployees = len(shifts), len(employees)
E, S = range(nEmployees), range(nShifts)

W = 1 + max(max(contracts), max(stops[s] - starts[s] for s in S))  # weight factor for building a lexicographical objective

O1, O2 = [], [[] for _ in S]
for s1, s2 in combinations(S, 2):
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
    [x[e][s] == 1 for e in E for s in S if assigned[e][s]],

    # setting some non-assignments
    [x[e][s] == 0 for e in E for s in S if any(assigned[f][s] for f in E if e != f)],

    # at most one assignment
    [Sum(x[:, s]) <= 1 for s in S],

    # no overlapping assignments (a)
    [x[e][s1] + x[e][s2] <= 1 for e in E for s1, s2 in O1 if not assigned[e][s1] and not assigned[e][s2]],

    # appropriate expertise required
    [x[e][s] == 0 for e in E for s in S if not (assigned[e][s] or required[s] in expertises[e])],

    # no overlapping assignments (b)
    [Sum(x[e][t] for t in O2[s]) <= max(1, sum(assigned[e][t] for t in O2[s])) for e in E for s in S],

    # computing the differences between working times and the contracts
    [y[e] == Sum(x[e][s] * (stops[s] - starts[s]) for s in S) - contracts[e] for e in E]
)

maximize(
    W * Sum(x) - Sum(abs(y[e]) for e in E)
)
