"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  small.json

## Model
  constraints: Sum

## Execution
  python RosterShifts.py -data=<datafile.json>

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
"""

from pycsp3 import *

nShifts, nEmployees, nExpertises, contract, employee_expertises, start_time, stop_time, req_expertise, time_units_per_hour = data

W = 1 + max(max(contract), max(stop_time[s] - start_time[s] for s in range(nShifts)))  # % Weight factor for objective to be lexicographical

assigned = VarArray(size=[nEmployees, nShifts], dom={0, 1})


def limit(e):
    return sum(stop_time[s] - start_time[s] for s in range(nShifts)) - contract[e]


def overlapping(s1, s2):
    return start_time[s1] < stop_time[s2] and start_time[s2] < stop_time[s1]


def identical_shifts(s1, s2):
    return start_time[s1] == start_time[s2] and stop_time[s1] == stop_time[s2] and req_expertise[s1] == req_expertise[s2]


contract_diff = VarArray(size=nEmployees, dom=lambda e: range(-contract[e], limit(e) + 1 - contract[e]))

satisfy(
    # No double assignments
    [Sum(assigned[:, s]) <= 1 for s in range(nShifts)],

    # No overlapping assignments
    [assigned[e][s1] + assigned[e][s2] <= 1 for s1, s2 in combinations(nShifts, 2) if overlapping(s1, s2) for e in range(nEmployees)],

    # Appropriate expertise required
    [assigned[e][s] == 0 for e in range(nEmployees) for s in range(nShifts) if req_expertise[s] not in employee_expertises[e]],

    # Not allowed to work more than 130% of your contract
    [10 * Sum(assigned[e][s] * (stop_time[s] - start_time[s]) for s in range(nShifts)) <= 13 * contract[e] for e in range(nEmployees) if contract[e] > 0],

    [contract_diff[e] == Sum(assigned[e][s] * (stop_time[s] - start_time[s]) for s in range(nShifts)) - contract[e] for e in range(nEmployees)],

    # tage(symmetry-breaking)
    [Sum(assigned[:, s2]) <= Sum(assigned[:, s1]) for s1, s2 in combinations(nShifts, 2) if identical_shifts(s1, s2)]
)

maximize(
    W * Sum(assigned) - Sum(abs(contract_diff[e]) for e in range(nEmployees))
)
