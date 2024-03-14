"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2022 Minizinc challenge.
The MZN model was proposed by Peter J. Stuckey, under the MIT Licence.
Compared to the Minizinc model, we do not use set variables.

## Data Example
  007.json

## Model
  constraints: Cardinality, Lex, Minimum, Sum

## Execution
  python Vaccine.py -data=sm-10-13-00.json
  python Vaccine.py -data=sm-10-13-00.dzn -dataparser=Vaccine_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn22
"""

from pycsp3 import *

nVaccines, groups, ageBounds, limits, health_information, exposure_information = data
ageBounds = [range(bounds.lb, bounds.ub + 1) for bounds in ageBounds]
ages, genders, healths, exposures, sizes = zip(*groups)
min_size, max_diff, max_share = limits
nGroups, nGenders = len(groups), 3

infos = [health_information[healths[i]] * exposure_information[exposures[i]] for i in range(nGroups)]
similar_groups = [[ii for ii in range(nGroups) if ii < i and healths[i] == healths[ii] and exposures[i] == exposures[ii]] for i in range(nGroups)]

# x[i][j] is 1 if the jth vaccine is used for the ith group
x = VarArray(size=[nGroups, nVaccines], dom={0, 1})

# y[j] is the number of persons vaccinated with the jth vaccine
y = VarArray(size=nVaccines, dom=range(sum(sizes) + 1))

# z[j] is the cost (information) associated with the jth vaccine
z = VarArray(size=nVaccines, dom=range(nGroups * max(infos) + 1))

# ng[k][j] is the number of groups of gender k with the jth vaccine
ng = VarArray(size=[nGenders, nVaccines], dom=range(nGroups + 1))

satisfy(
    # maximum number of vaccines for each group
    [Sum(x[i]) <= sizes[i] // min_size for i in range(nGroups)],

    # imposing limits wrt vaccines and ages
    [
        Cardinality(
            [x[i][j] * ages[i] for i in range(nGroups)],
            occurrences={a + 1: bounds for a, bounds in enumerate(ageBounds)}
        ) for j in range(nVaccines)
    ],

    # computing the total number of vaccinated persons
    [y[v] == Sum(x[g][v] * (sizes[g] // (1 + Sum(x[g][j] for j in range(nVaccines) if j != v))) for g in range(nGroups)) for v in range(nVaccines)],

    # ensuring no too large difference between sizes of persons with different vaccines
    [abs(y[v1] - y[v2]) <= max_diff for v1, v2 in combinations(nVaccines, 2)],

    # computing numbers of vaccinated groups wrt gender
    [ng[k][j] == Sum(x[i][j] for i in range(nGroups) if genders[i] == k) for k in range(nGenders) for j in range(nVaccines)],

    # imposing balance between numbers of vaccinated groups wrt gender
    [ng[k][j1] == ng[k][j2] for k in range(nGenders) for j1, j2 in combinations(nVaccines, 2)],

    # imposing limits on common vaccines
    [Sum(both(x[i1][j] == x[i2][j], x[i1][j]) for j in range(nVaccines)) <= max_share for i1, i2 in combinations(nGroups, 2)],

    # computing costs (information) of vaccines
    [z[j] == Sum(x[i][j] * ift(Exist(x[ii][j] for ii in similar_groups[i]), Then=1, Else=infos[i]) for i in range(nGroups)) for j in range(nVaccines)],

    # tag(symmetry-breaking)
    [LexIncreasing(x[:, j], x[:, j + 1]) for j in range(nVaccines - 1)]
)

maximize(
    Minimum(z)
)

"""
1) solution for 857:
  x == [[0, 0, 0, 0, 1, 1], [0, 0, 1, 1, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0], [1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 0, 0], [1, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0],
       [1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 1]],
2) y seems to be an approximation
"""

# ig = VarArray(size=[nVaccines, nGroups], dom={0, 1})
# [ig[v][g] == Exist(x[g1][v] for g1 in range(nGroups) if g1 < g and healths[g] == healths[g1] and exposures[g] == exposures[g1]) for v in range(nVaccines)
#  for g in range(nGroups)],
