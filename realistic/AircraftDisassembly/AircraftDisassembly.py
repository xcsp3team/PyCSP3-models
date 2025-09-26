"""
Aircraft Disassembly Scheduling

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenges.
The original MZN model is by Allen Zhon (No Licence was explicitly mentioned - MIT Licence assumed), while being inspired by:
  - the CP Optimizer [model](https://github.com/cftmthomas/AircraftDisassemblyScheduling) for Aircraft Disassembly Scheduling
  - the MiniZinc [model](https://github.com/youngkd/MSPSP-InstLib) for Multi-Skill Project Scheduling Problem

## Data Example
  600-01.json

## Model
  constraints: Cumulative, Maximum, Sum

## Execution
  python AircraftDisassembly.py -data=<datafile.json>
  python AircraftDisassembly.py -data=<datafile.dzn> -parser=AircraftDisassembly_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-031-60599-4_13
  - https://github.com/cftmthomas/AircraftDisassemblyScheduling
  - https://www.minizinc.org/challenge2024/results2024.html

## Tags
  realistic, mzn24
"""
from pycsp3 import *

horizon, precedences, unrelated_precedences, resources, mass, location_capacities, activities, unavailable = data

useful_resources, durations, skill_requirements, required_mass, locations, occupancies = activities
_, costs, skill_mastery = resources
M, comp_prod, maxDiff = mass

nActivities, nResources, nSkills = len(useful_resources), len(costs), len(skill_requirements[0])
nUnavailable, nUnrelatedActivities, nLocations = len(unavailable.resources), len(unrelated_precedences), len(location_capacities)
A, R, S = range(nActivities), range(nResources), range(nSkills)

skill_capacities = [sum(skill_mastery[:, s]) for s in S]  # capacity of each skill
consumption = [[(required_mass[j] if locations[j] in comp_prod[i, 0] else -required_mass[j] if locations[j] in comp_prod[i, 1] else 0) for j in A] for i in M]
resAct = [[i for i in A if consumption[m][i] != 0] for m in M]  # set of "non-zero" activities for each mass balanced

# x[i] is the starting time of the ith activity
x = VarArray(size=nActivities, dom=range(horizon + 1))

assign = VarArray(size=[nActivities, nResources], dom={0, 1})  # assignment of resources to actioccupancyvities

contrib = VarArray(size=[nActivities, nResources, nSkills], dom={0, 1})  # skill contribution assignment

overlap = VarArray(size=nUnrelatedActivities, dom={0, 1})  # overlapping of unrelated activities

# order variables describe the relative precedence between pairs of activities
act_leq_act = VarArray(size=[nActivities, nActivities], dom={0, 1})

satisfy(
    # Precedence constraint
    [x[i] + durations[i] <= x[j] for (i, j) in precedences],

    # Unary resource constraint
    [
        If(
            overlap[u],
            Then=x[i] + durations[i] <= x[j],
            Else=x[j] + durations[j] <= x[i]
        ) for u, (i, j) in enumerate(unrelated_precedences) if any(skill_requirements[i][s] + skill_requirements[j][s] > skill_capacities[s] for s in S)
    ],

    # Unary resource constraint
    [
        (
            (overlap[u] == 0) == either(x[i] + durations[i] <= x[j], x[j] + durations[j] <= x[i]),
            [
                If(
                    assign[i][r], assign[j][r],
                    Then=overlap[u] == 0
                ) for r in set(useful_resources[i]).intersection(set(useful_resources[j]))
            ]
        ) for u, (i, j) in enumerate(unrelated_precedences) if not any(skill_requirements[i][s] + skill_requirements[j][s] > skill_capacities[s] for s in S)
    ],

    # Resource unavailable constraint
    [
        If(
            assign[a][unavailable.resources[i]],
            Then=either(x[a] + durations[a] <= unavailable.starts[i], x[a] >= unavailable.ends[i])
        ) for i in range(nUnavailable) for a in A
    ],

    # Skill constraint: Skill requirements are satisfied
    [Sum(contrib[a][r][s] for r in useful_resources[a]) == skill_requirements[a][s] for a in A for s in S if skill_requirements[a][s] > 0],

    # Non-Multi-Tasking constraint: Maximum of one contribution by each activity
    [Sum(contrib[a][r][s] for s in S if skill_mastery[r][s] == 1 and skill_requirements[a][s] > 0) <= 1 for a in A for r in useful_resources[a]],

    # Skill constraint: Resources only use skills they have mastered
    [contrib[a][r][s] <= skill_mastery[r][s] for a in A for r in useful_resources[a] for s in S],

    # Linking constraint: resources only contribute to activities they are assigned
    [contrib[a][r][s] <= assign[a][r] for a in A for r in useful_resources[a] for s in S if skill_requirements[a][s] > 0],

    # Location constraint: limit the maximum number of technicians allowed to work there at the same time.
    [
        Cumulative(
            origins=x,
            lengths=durations,
            heights=occupancies
        ) <= location_capacities[i] for i in range(nLocations)
    ],

    [act_leq_act[i][j] == (x[i] <= x[j]) for i in A for j in A],

    # constraint for correct reservoir levels at the start of activities
    [
        (
            Sum(consumption[m][j] * act_leq_act[j][i] for j in resAct[m]) <= maxDiff[m],
            Sum(consumption[m][j] * act_leq_act[j][i] for j in resAct[m]) >= -maxDiff[m]
        ) for m in M for i in resAct[m]
    ],

    #  constraint for act_leq_act
    [
        either(
            act_leq_act[i][j],
            act_leq_act[j][i]
        ) for i, j in combinations(A, 2)
    ],
)

minimize(
    100000 * Maximum(x) + Sum(costs[r] * durations[a] * assign[a][r] for a in A for r in R)
)
