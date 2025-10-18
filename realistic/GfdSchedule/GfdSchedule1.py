"""
A Scheduling problem, such that:
 - items are grouped by kinds
 - items are processed by groups using facilities
 - items must be processed after some 'produced days'
 - the maximum number of processed-items/day is fixed
 - the objective:
   a) items may be processed before 'deadLineDay'
   b) minimizing groups (minimizing use of facilities)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n025f5d20m10k3.json

## Model
  constraints: Count, Element, NValues, Sum

## Execution
  python GfdSchedule1.py -data=<datafile.json>
  python GfdSchedule1.py -data=<datafile.dzn> -parser=GfdSchedule_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2015/results/

## Tags
  realistic, mzn15
"""

from pycsp3 import *

nFacilities, maxItemsPerDay, maxDay, items = data or load_json_data("n025f5d20m10k3.json")

kinds, facilities, producedDays, deadlineDays = zip(*items)

nItems, nGroups = len(kinds), len(kinds)
I = range(nItems)

# for any kind k, we record a pair (b,t) for the base and the set t of items having kind t
kind_items = [(len([i for i in I if kinds[i] < k]), [i for i in I if kinds[i] == k]) for k in range(min(kinds), max(kinds) + 1)]

ub_dlp = sum(maxDay - deadlineDays[i] for i in I)

# group[i] is the group of the ith item
group = VarArray(size=nItems, dom=range(nGroups))

# facility[j] is the facility of the jth group (-1 if group number not used)
facility = VarArray(size=nGroups, dom=range(-1, nFacilities))

# gpd[j] is the process day of the jth group
gpd = VarArray(size=nGroups, dom=range(maxDay + 1))

# ipd[i] is the process day of the ith item
ipd = VarArray(size=nItems, dom=range(1, maxDay + 1))

# gf[j][k] is 1 if the kth facility is used by the jth group
gf = VarArray(size=[nGroups, nFacilities], dom={0, 1})

# z1 is the deadline penalty
z1 = Var(dom=range(ub_dlp + 1))

# z2 is the number of assigned groups
z2 = Var(dom=range(1, nItems + 1))

# z is the overall objective value
z = Var(dom=range(1, ub_dlp * 100 + nItems + 1))

satisfy(
    # computing item process days
    [ipd[i] == gpd[group[i]] for i in I],

    # items of different kinds cannot be assigned to the same group
    [group[i] != group[j] for i, j in combinations(I, 2) if kinds[i] != kinds[j]],

    # limiting group number selection range
    [group[i] in range(b, b + len(t)) for b, t in kind_items for i in t],

    # handling non-used groups (numbers)
    [
        NotExist(
            within=group,
            value=j
        ) == both(facility[j] == -1, gpd[j] == 0)
        for j in range(nGroups)
    ],

    # setting group order  tag(symmetry-breaking)
    [
        [group[i] < b + k + 1 for b, t in kind_items for k, i in enumerate(t)],
        [
            If(
                facility[b + j1] == -1,
                Then=facility[b + j2] == -1
            ) for b, t in kind_items for j1, j2 in combinations(len(t), 2)
        ]
    ],

    # items must be assigned to groups that are compatible wrt their facilities
    [facility[group[i]] in facilities[i] for i in I],

    # determining which facilities are used by groups
    [gf[j][k] == (facility[j] == k) for j in range(nGroups) for k in range(nFacilities)],

    # groups using the same facility cannot be processed the same day
    [
        If(
            facility[j1] != -1, facility[j2] != -1, facility[j1] == facility[j2],
            Then=gpd[j1] != gpd[j2]
        ) for j1, j2 in combinations(nGroups, 2)
    ],

    # items must be assigned to groups that are compatible wrt their processed days
    [producedDays[i] < gpd[group[i]] for i in I],

    # respecting the limit of items per day
    [Count(within=ipd, value=d) <= maxItemsPerDay for d in range(1, maxDay + 1)],

    # computing the deadline penalty
    z1 == Sum((ipd[i] > deadlineDays[i]) * (ipd[i] - deadlineDays[i]) for i in I),

    # computing the number of assigned groups
    z2 == NValues(group)
)

minimize(
    z
)

""" Comments
1) Following the MZN model in 2015, the objective is not connected to the rest of the variables. Hence the optimum is always 1. This is fixed in 2016.
"""
