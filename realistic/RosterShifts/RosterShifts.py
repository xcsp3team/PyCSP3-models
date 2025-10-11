"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  small.json

## Model
  constraints: Sum

## Execution
  python RosterShifts.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn23
"""

from pycsp3 import *

nShifts, nEmployees, _, contract, employee_expertises, start_time, stop_time, req_expertise, _ = data or load_json_data("small.json")

E, S = range(nEmployees), range(nShifts)

W = 1 + max(max(contract), max(stop_time[s] - start_time[s] for s in S))  # % Weight factor for objective to be lexicographical


def limit(e):
    return sum(stop_time[s] - start_time[s] for s in S) - contract[e]


def overlapping(s1, s2):
    return start_time[s1] < stop_time[s2] and start_time[s2] < stop_time[s1]


def identical_shifts(s1, s2):
    return start_time[s1] == start_time[s2] and stop_time[s1] == stop_time[s2] and req_expertise[s1] == req_expertise[s2]


assigned = VarArray(size=[nEmployees, nShifts], dom={0, 1})

contract_diff = VarArray(size=nEmployees, dom=lambda e: range(-contract[e], limit(e) + 1 - contract[e]))

satisfy(
    # No double assignments
    [Sum(assigned[:, s]) <= 1 for s in S],

    # No overlapping assignments
    [assigned[e][s1] + assigned[e][s2] <= 1 for s1, s2 in combinations(S, 2) if overlapping(s1, s2) for e in E],

    # Appropriate expertise required
    [assigned[e][s] == 0 for e in E for s in S if req_expertise[s] not in employee_expertises[e]],

    # Not allowed to work more than 130% of your contract
    [10 * Sum(assigned[e][s] * (stop_time[s] - start_time[s]) for s in S) <= 13 * contract[e] for e in E if contract[e] > 0],

    [contract_diff[e] == Sum(assigned[e][s] * (stop_time[s] - start_time[s]) for s in S) - contract[e] for e in E],

    # tage(symmetry-breaking)
    [Sum(assigned[:, s2]) <= Sum(assigned[:, s1]) for s1, s2 in combinations(S, 2) if identical_shifts(s1, s2)]
)

maximize(
    W * Sum(assigned) - Sum(abs(contract_diff[e]) for e in E)
)
