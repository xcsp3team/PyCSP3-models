"""
Physician Scheduling During a Pandemic (see link to CPAIOR paper).

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
The original MZN model was proposed by Tobias Geibinger, Lucas Kletzander, Matthias Krainz, Florian Mischek, Nysret Musliu and Felix Winter (Copyright 2021).
The licence seems to be like a MIT Licence.

## Data Example
  03-0-34.json

## Model
  constraints: Cardinality, Count, NValues, Sum

## Execution
  python PhysicianSchedule.py -data=sm-10-13-00.json
  python PhysicianSchedule.py -data=sm-10-13-00.dzn -dataparser=PhysicianSchedule_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-030-78230-6_29
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  real, mzn21
"""

from pycsp3 import *

nDepartments, stations, shifts, weights, nSkills, demands, subsums, persons = data
departments, commons = cp_array(zip(*stations))
shiftLengths, forbiddenSequences = cp_array(zip(*shifts))
subDemand = cp_array(sub.demands for sub in subsums)
nStations, nShifts, nPersons, nDays = len(stations), len(shifts), len(persons), len(subDemand[0])
nWeeks = nDays // 7  # assumes starting on Monday and numDays divisible by 7
OFF = 0

sf = lambda t: sum(flatten(t))  # summing after flattening the argument array
sums0, sumsub = [nPersons - sf(demands[1:, 1:, d, 1:]) for d in range(nDays)], [sum(subDemand[:, d]) for d in range(nDays)]
# below, expected number of occurrences
Osh = [[sums0[d]] + [sf(demands[1:, s, d, 1:]) + sumsub[d] * (-1 if s == 1 else 1 if s == 2 else 0) for s in range(1, nShifts)] for d in range(nDays)]
Ost = [[sums0[d]] + [sf(demands[s, 1:, d, 1:]) for s in range(1, nStations)] for d in range(nDays)]
Osk = [[sums0[d]] + [sf(demands[1:, 1:, d, s]) for s in range(1, nSkills)] for d in range(nDays)]
assert all(len(t) == nShifts for t in Osh) and all(len(t) == nStations for t in Ost) and all(len(t) == nSkills for t in Osk)

# sh[i][j] is the shift for the ith person on the jth day
sh = VarArray(size=[nPersons, nDays], dom=range(nShifts))

# sk[i][j] is the skill for the ith person on the jth day
sk = VarArray(size=[nPersons, nDays], dom=range(nSkills))

# st[i][j] is the station for the ith person on the jth day
st = VarArray(size=[nPersons, nDays], dom=range(nStations))

# w[i] is 1 if the ith person is working at all
w = VarArray(size=nPersons, dom={0, 1})

# last[i][j] is the last station for the ith person on the jth day
last = VarArray(size=[nPersons, nDays + 1], dom=range(nStations))

# z1 is the number of working persons
z1 = Var(dom=range(nPersons + 1))

# z2 is the sum of preferences
z2 = Var(dom=range(3 * nPersons * nDays + 1))

# z3 is the weighted persons at risk that are working
z3 = Var(dom=range(nPersons * nDepartments + 1))

# z4 is the number of station changes
z4 = Var(dom=range(nPersons * nDays + 1))

satisfy(
    # ensuring the coherence of assignments
    [
        Sum(
            sh[i][j] == OFF,
            st[i][j] == OFF,
            sk[i][j] == OFF
        ) in {0, 3} for i in range(nPersons) for j in range(nDays)
    ],

    # ensuring at most 6 consecutive days without a day off
    [
        [Exist(sh[i][:max(0, 7 - persons[i].histDays)], value=OFF) for i in range(nPersons) if nDays >= 7],
        [Exist(sh[i][j:j + 7], value=OFF) for i in range(nPersons) for j in range(1, nDays - 6 + 1)]
    ],

    # here, two groups of the original model not posted because indexNight is empty in the 5 available instances

    # respecting a maximal number of hours per week
    [Sum(shiftLengths[sh[i][7 * j + k]] for k in range(7)) <= persons[i].maxHoursPerWeek for i in range(nPersons) for j in range(nWeeks)],

    # shifts 1 and 2: individual assignments on common stations
    [
        Sum(
            conjunction(
                st[i][j] == v1,
                sh[i][j] == v2,
                sk[i][j] == v3
            ) for i in range(nPersons)
        ) == demands[v1][v2][j][v3]
        for v1 in range(1, nStations) if commons[v1] == 1 for v2 in (1, 2) for j in range(nDays) for v3 in range(1, nSkills)
    ],

    # shift 1 may be subsumed by shift 2 on non-common stations
    [
        Sum(
            conjunction(
                st[i][j] == v1,
                sh[i][j] in {1, 2},
                sk[i][j] == v3
            ) for i in range(nPersons)
        ) == demands[v1][1][j][v3]
        for v1 in range(1, nStations) if commons[v1] == 0 for j in range(nDays) for v3 in range(1, nSkills)
    ],

    # shifts 3+: regular assignments
    [
        Sum(
            conjunction(
                st[i][j] == v1,
                sh[i][j] == v2,
                sk[i][j] == v3
            ) for i in range(nPersons)
        ) == demands[v1][v2][j][v3]
        for v1 in range(1, nStations) for v2 in range(3, nShifts) for j in range(nDays) for v3 in range(1, nSkills)
    ],

    # tag(redundant-constraints)
    [
        Count(
            both(
                st[i][j] == v1,
                sh[i][j] in ({1, 2} if commons[v1] == 0 and v2 == 1 else {v2})
            ) for i in range(nPersons) if persons[i].preferences[v1][v3] < 4
        ) >= demands[v1][v2][j][v3]
        for v1 in range(1, nStations) for v2 in range(1, nShifts) if v2 != 2 or commons[v1] == 1 for j in range(nDays) for v3 in range(1, nSkills)
    ],

    # demand for subsuming stations, hardcoded to shift index 2
    [
        Sum(
            conjunction(
                departments[st[i][j]] == subDp,
                commons[st[i][j]] == 0,
                sh[i][j] == 2,
                sk[i][j] in subSk
            ) for i in range(nPersons)
        ) == subDm[j] for (subDp, subSk, subDm) in subsums for j in range(nDays)
    ],

    # choosing allowed combinations of skills and stations
    [persons[i].preferences[st[i][j]][sk[i][j]] < 4 for i in range(nPersons) for j in range(nDays)],

    # avoiding forbidden shift sequences
    [
        (
            sh[i][0] not in forbiddenSequences[persons[i].histShift],
            [sh[i][j + 1] not in forbiddenSequences[sh[i][j]] for j in range(nDays - 1)]
        ) for i in range(nPersons)
    ],

    # handling forbidden days
    [sh[i][j] == OFF for i in range(nPersons) for j in persons[i].forbiddenDays],

    # determining who is working during the period
    [
        [w[i] == Exist(sh[i][j] > 0 for j in range(nDays)) for i in range(nPersons)],
        [w[i] == 1 for i in range(nPersons) if persons[i].requiredWork]
    ],

    # computing last assigned stations
    [
        (
            last[i][0] == (0 if commons[persons[i].histStation] == 1 else persons[i].histStation),
            [last[i][j + 1] == ift(commons[st[i][j]], Then=last[i][j], Else=st[i][j]) for j in range(nDays)]
        ) for i in range(nPersons)
    ],

    # working at most in two different departments
    [NValues([departments[persons[i].histStation]] + [departments[st[i][j]] for j in range(nDays)]) <= 2 for i in range(nPersons)],

    # computing the number of working persons
    z1 == Sum(w),

    # computing the sum of preferences
    z2 == Sum(persons[i].preferences[st[i][j]][sk[i][j]] for i in range(nPersons) for j in range(nDays)),

    # computing the weighted persons at risk that are working
    z3 == Sum(departments[last[i][-1]] * w[i] for i in range(nPersons) if persons[i].atRisk),

    # computing the number of changes
    z4 == Count(
        both(
            last[i][j - 1] > 0,
            last[i][j] != last[i][j - 1]
        ) for i in range(nPersons) for j in range(1, nDays + 1)
    ),

    # ensuring that shifts, stations and skills are covered
    [
        (
            Cardinality(sh[:, j], occurrences=Osh[j]),
            Cardinality(st[:, j], occurrences=Ost[j]),
            Cardinality(sk[:, j], occurrences=Osk[j])
        ) for j in range(nDays)
    ]
)

minimize(
    z1 * weights.person + z2 * weights.preference + z3 * weights.risk + z4 * weights.station
)

"""
1) Sometimes, Sum is used instead of Count (not sure it makes a big difference for the solvers)
 
2) we can replace:
 sh[i][j] in {1,2}
  by 
  (sh[i][j] == 1) | (sh[i][j] == 2)
  or 
    belong(sh[i][j],(1,2))
  
3) Instead of:
  [NValues([departments[persons[i].histStation]] + [departments[st[i][j - 1]] for j in range(1, nDays + 1)]) <= 2 for i in range(nPersons)],
 one could declare:   
   # dpt[i][j] is the station department for the ith person on the jth day
   dpt = VarArray(size=[nPersons, nDays + 1], dom=range(nDepartments + 1))
 and use:  
    # computing departments
    [
        [dpt[i][0] == departments[persons[i].histStation] for i in range(nPersons)],
        [dpt[i][j] == departments[st[i][j - 1]] for i in range(nPersons) for j in range(1, nDays + 1)]
    ],

    # at most, working in two different departments
    [NValues(dpt[i]) <= 2 for i in range(nPersons)],
    Would it be clearer?
    
4) Now,
    [[sh[i][0] not in forbiddenSequences[persons[i].histShift] for i in range(nPersons)]]
 is possible, instead of:
    [sh[i][0] not in T for i in range(nPersons) if len(T := forbiddenSequences[persons[i].histShift]) > 0]
    
5) Now,
   [sh[i][j + 1] not in forbiddenSequences[sh[i][j]] for i in range(nPersons) for j in range(nDays - 1)]
 is possible, instead of:
   [(sh[i][j], sh[i][j + 1]) in [(v, w) for v in range(nShifts) for w in range(nShifts) if w not in forbiddenSequences[v]] 
     for i in range(nPersons) for j in range(nDays - 1)]
     
6) Now,
    [persons[i].preferences[st[i][j]][sk[i][j]] < 4 for i in range(nPersons) for j in range(nDays)]
 is possible instead of:
    [(st[i][j], sk[i][j]) in [[(v, w) for v in range(nStations) for w in range(nSkills) if persons[i].preferences[v][w] < 4]
       for i in range(nPersons) for j in range(nDays)]
"""
