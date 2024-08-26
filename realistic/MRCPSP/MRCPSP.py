"""
Multi-mode Resource-constrained Project Scheduling (MRCPSP)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2023 challenges.
The MZN model was proposed by Ria Szeredi and Andreas Schutt (Copyright: Data61, CSIRO).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  j30-15-5.json

## Model
  constraints: Cumulative, Element, Sum

## Execution
  python MRCPSP.py -data=<datafile.json>
  python MRCPSP.py -data=<datafile.dzn> -parser=MRCPSP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn16, mzn23
"""

from pycsp3 import *

capacities, types, modes, successors, durations, requirements = data
nResources, nTasks, nModes = len(capacities), len(modes), len(durations)

renewable = [k for k in range(nResources) if types[k] == 1]  # renewable resources
non_renewable = [k for k in range(nResources) if types[k] == 2]  # non-renewable resources

UB = sum(max(durations[m] for m in modes[i]) for i in range(nTasks))


def activities_in_disjunction(i, j, k):
    return any(requirements[k, mi] + requirements[k, mj] > capacities[k] for mi in modes[i] for mj in modes[j])


def activities_in_disjunction_renew(i, j):
    return any(activities_in_disjunction(i, j, k) for k in renewable)


def modes_in_disjunction(mi, mj):
    return any(requirements[k, mi] + requirements[k, mj] > capacities[k] for k in renewable)


def activities_in_disjunction_in_all_modes(i, j):
    return all(modes_in_disjunction(mi, mj) for mi in modes[i] for mj in modes[j])


pairs = [(i, j) for i, j in combinations(nTasks, 2) if activities_in_disjunction_renew(i, j)]

# am[i] is 1 if the ith mode (optional activity) is activated
am = VarArray(size=nModes, dom={0, 1})

# x[i] is the starting time of the ith task
x = VarArray(size=nTasks, dom=range(UB + 1))

# d[i] is the duration of the ith task
d = VarArray(size=nTasks, dom=lambda i: {durations[i] for i in modes[i]})

# r[k][i] is the requirement (quantity) of the kth resource for the ith task
r = VarArray(size=[nResources, nTasks], dom=lambda k, i: {requirements[k, m] for m in modes[i]})

# tm[i] is the mode of the ith task
tm = VarArray(size=nTasks, dom=lambda i: modes[i])

satisfy(
    # activity and mode constraints
    (
        [am[tm[i]] == 1 for i in range(nTasks)],
        [Sum(am[modes[i]]) == 1 for i in range(nTasks)],
        [d[i] == durations[tm[i]] for i in range(nTasks)],
        [r[k][i] == requirements[k][tm[i]] for k in range(nResources) for i in range(nTasks)]
    ),

    # respecting precedence relations
    [x[i] + d[i] <= x[j] for i in range(nTasks) for j in successors[i]],

    # handling renewable resources
    [Cumulative(origins=x, lengths=d, heights=r[k]) <= capacities[k] for k in renewable],

    # handling non-renewable resources
    [Sum(r[k]) <= capacities[k] for k in non_renewable],

    # redundant non-overlapping constraints  tag(redundant)
    (
        [(x[i] + d[i] <= x[j]) | (x[j] + d[j] <= x[i]) for i, j in pairs if activities_in_disjunction_in_all_modes(i, j)],

        [
            If(
                r[k][i] + r[k][j] > capacities[k],
                Then=(x[i] + d[i] <= x[j]) | (x[j] + d[j] <= x[i])
            ) for i, j in pairs if not activities_in_disjunction_in_all_modes(i, j) for k in renewable if activities_in_disjunction(i, j, k)
        ]
    )
)

minimize(
    # minimizing the make-span
    Maximum(x[i] + d[i] for i in range(nTasks) if len(successors[i]) == 0)
)
