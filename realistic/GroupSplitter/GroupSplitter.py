"""
A group of people want to do activities (Cinema then Restaurant) in subgroups
where the activities for subgroups are supposed to  match better members' preferences.
The aim of our model is to find the best activities and group combinations to recommend.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The original MZN model was proposed by Jacopo Mauro and Tong Liu - no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  execute 'python GroupSplitter.py -data=<datafile.dzn> -parser=GroupSplitter_ParserZ.py -export' to get a JSON file

## Model
  constraints: Count, Element, Sum, Table

## Execution
  python GroupSplitter.py -data=<datafile.json>
  python GroupSplitter.py -data=<datafile.dzn> -parser=GroupSplitter_ParserZ.py

## Links
  - http://amsdottorato.unibo.it/9068/1/main.pdf
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn17, mzn19, mzn25
"""

from pycsp3 import *

nGroups, minGroupSize, startAfter, maxWait, ratingBalance, prf1, prf2, nTimeSlots, act1, act2, distances = data

nUsers, nCells, nActivities1, nActivities2 = len(prf1), len(distances), len(act1), len(act2)
U = range(nUsers)

T1 = [tuple(j if i == 0 else act1[j][i - 1] for i in range(6)) for j in range(nActivities1)]
T2 = [tuple(j if i == 0 else act2[j][i - 1] for i in range(6)) for j in range(nActivities2)]
T3 = [(i, j, distances[i][j]) for i in range(nCells) for j in range(nCells)]

# x1[i] is the starting time of following the activity by the ith user in phase 1
x1 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# x2[i] is the starting time of following the activity by the ith user in phase 2
x2 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# g1[i] is the group of the ith user in phase 1
g1 = VarArray(size=nUsers, dom=range(nGroups))

# g2[i] is the group of the ith user in phase 2
g2 = VarArray(size=nUsers, dom=range(nGroups))

# ga1[j] is the activity followed by the jth group in phase 1
ga1 = VarArray(size=nGroups, dom=range(nActivities1))

# ga2[j] is the activity followed by the jth group in phase 2
ga2 = VarArray(size=nGroups, dom=range(nActivities2))

# ua1[i] is the activity followed by the ith user in phase 1
ua1 = VarArray(size=nUsers, dom=range(nActivities1))

# ua2[i] is the activity followed by the ith user in phase 2
ua2 = VarArray(size=nUsers, dom=range(nActivities2))

# dur1[i] is the duration of the activity followed by the ith user in phase 1
dur1 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# dur2[i] is the duration of the activity followed by the ith user in phase 2
dur2 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# avl1[i] is the availability (time) of the activity followed by the ith user in phase 1
avl1 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# avl2[i] is the availability (time) of the activity followed by the ith user in phase 2
avl2 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# end1[i] is the closing (time) of the activity followed by the  ith user in phase 1
end1 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# end2[i] is the closing (time) of the activity followed by the ith user in phase 2
end2 = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

# cell1[i] is the cell (place) where is situated the activity followed by the ith user in phase 1
cell1 = VarArray(size=nUsers, dom=range(1, nCells + 1))

# cell2[i] is the cell (place) where is situated the activity followed by the ith user in phase 2
cell2 = VarArray(size=nUsers, dom=range(1, nCells + 1))

# pr1[i] is the public rating of the activity followed by the ith user in phase 1
pr1 = VarArray(size=nUsers, dom=range(6))

# pr2[i] is the public rating of the activity followed by the ith user in phase 2
pr2 = VarArray(size=nUsers, dom=range(6))

# ur1[i] is the user rating by the ith user of the activity followed in phase 1
ur1 = VarArray(size=nUsers, dom=range(-2, 3))

# ur2[i] is the user rating by the ith user of the activity followed in phase 2
ur2 = VarArray(size=nUsers, dom=range(-2, 3))

# dt[i] is the time required by the ith user for going from activity 1 to activity 2
dt = VarArray(size=nUsers, dom=range(1, nTimeSlots + 1))

satisfy(
    # respecting the minimum size of a group
    [
        (
            Count(within=g1, value=i) >= minGroupSize,
            Count(within=g2, value=i) >= minGroupSize
        ) for i in range(nGroups) if nGroups > 1
    ],

    # linking variables with table constraints
    [
        [
            Table(
                scope=(ua1[i], avl1[i], end1[i], dur1[i], cell1[i], pr1[i]),
                supports=T1
            ) for i in U
        ],
        [
            Table(
                scope=(ua2[i], avl2[i], end2[i], dur2[i], cell2[i], pr2[i]),
                supports=T2
            ) for i in U
        ],
        [
            Table(
                scope=(ua1[i], ur1[i]),
                supports=enumerate(prf1[i])
            ) for i in U
        ],
        [
            Table(
                scope=(ua2[i], ur2[i]),
                supports=enumerate(prf2[i])
            ) for i in U
        ],
        [
            Table(
                scope=(cell1[i], cell2[i], dt[i]),
                supports=T3
            ) for i in U
        ]
    ],

    # user's activity is also group's activity
    [
        (
            ua1[i] == ga1[g1[i]],
            ua2[i] == ga2[g2[i]]
        ) for i in U
    ],

    # activity temporal constraints
    [
        (
            x1[i] >= avl1[i],
            x1[i] <= end1[i] - dur1[i],
            x2[i] >= avl2[i],
            x2[i] <= end2[i] - dur2[i],
            x2[i] >= x1[i] + dur1[i] + dt[i],
            x2[i] <= x1[i] + dur1[i] + maxWait
        ) for i in U
    ],

    # user 0 belongs always to the first group  tag(symmetry-breaking)
    [
        g1[0] == 0,
        g2[0] == 0
    ],

    # next user belongs to the group of the previous users or +1  tag(symmetry-breaking)
    [
        (
            g1[i] <= i,
            g2[i] <= i
        ) for i in U
    ],

    [x1[i] >= startAfter for i in U]
)

maximize(
    # maximizing the balanced ratings from public and users
    ratingBalance * Sum(ur1) + (10 - ratingBalance) * Sum(pr1) + (10 - ratingBalance) * Sum(pr2) + ratingBalance * Sum(ur2)
)
