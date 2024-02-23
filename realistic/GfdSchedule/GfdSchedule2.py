"""
A Scheduling problem, such that:
 - items are grouped by kinds
 - items are processed by groups using facilities
 - items must be processed after some 'produced days'
 - the maximum number of processed-items/day is fixed
 - the objective:
   a) items may be processed before 'deadLineDay'
   b) minimizing groups (minimizing use of facilities)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2018/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n025f5d20m10k3.json

## Model
  constraints: Cumulative, Count, Element, Sum

## Execution
  python GfdSchedule2.py -data=<datafile.json>
  python GfdSchedule2.py -data=<datafile.dzn> -parser=GfdSchedule_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn16, mzn18, mzn22
"""

from pycsp3 import *

nFacilities, maxItemsPerDay, maxDay, items = data
kinds, facilities, producedDays, deadlineDays = zip(*items)
nItems, nGroups = len(kinds), len(kinds)

# for any kind k, we record a pair (b,t) for the base and the set t of items having kind t
items_per_kinds = [(len([i for i in range(nItems) if kinds[i] < k]), [i for i in range(nItems) if kinds[i] == k]) for k in range(min(kinds), max(kinds) + 1)]

# group[i] is the group of the ith item
group = VarArray(size=nItems, dom=range(nGroups))

# facility[j] is the facility of the jth group (-1 if group number not used)
facility = VarArray(size=nGroups, dom=range(-1, nFacilities))

# gpd[j] is the process day of the jth group
gpd = VarArray(size=nGroups, dom=range(maxDay + 1))

# ipd[i] is the process day of the ith item
ipd = VarArray(size=nItems, dom=range(1, maxDay + 1))

satisfy(
    # computing item process days
    [ipd[i] == gpd[group[i]] for i in range(nItems)],

    # items of different kinds cannot be assigned to the same group
    [group[i] != group[j] for i, j in combinations(nItems, 2) if kinds[i] != kinds[j]],

    # limiting group number selection ranges
    [group[i] in range(b, b + len(t)) for b, t in items_per_kinds for i in t],

    # handling non-used groups
    [NotExist(group, value=j) == both(facility[j] == -1, gpd[j] == 0) for j in range(nGroups)],

    # setting group order  tag(symmetry-breaking)
    [
        [group[i] < b + k + 1 for b, t in items_per_kinds for k, i in enumerate(t)],
        [If(facility[j1] == -1, Then=facility[j2] == -1) for b, t in items_per_kinds for j1, j2 in combinations(range(b, b + len(t)), 2)]
    ],

    # assigning items to groups that are compatible wrt their facilities
    [facility[group[i]] in facilities[i] for i in range(nItems)],

    # groups using the same facility cannot be processed the same day
    [
        Cumulative(
            origins=gpd,
            lengths=1,
            heights=[facility[j] == i for j in range(nGroups)]
        ) <= 1 for i in range(nFacilities)
    ],

    # assigning items to groups that are compatible wrt their processed days
    [producedDays[i] < gpd[group[i]] for i in range(nItems)],

    # respecting the limit of items per day
    [Count(ipd, value=d) <= maxItemsPerDay for d in range(1, maxDay + 1)]
)

minimize(
    # minimizing the sum of deadline penalties and then, the number of used groups
    Sum(max(0, ipd[i] - deadlineDays[i]) for i in range(nItems)) * 100 + NValues(group)
)

"""
1) It is possible to introduce the variable deadlinePenalty, and to post:
  deadlinePenalty == Sum((ipd[i] > deadlineDay[i]) * (ipd[i] - deadlineDay[i]) for i in range(nItems))
2) in Minizinc challenge 2015, a slightly different model was used as not involving Cumulative (and the unconnected objective)
"""
