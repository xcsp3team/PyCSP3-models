"""
The ROADEF conference is the largest French-speaking event aimed at bringing together researchers from various domains, including combinatorial optimization,
 operational research, constraint programming and industrial engineering.
This event is organized annually and welcomes around 600 participants.
ROADEF includes plenary sessions, tutorials in semi-plenary sessions, and multiple parallel sessions.
The conference also involves many working groups consisting of researchers collaborating on a national and potentially international level
 on specific themes covered by the conference, with each parallel session usually being organized by one or more of these working group.
The problem si to schedule ROADEF parallel sessions into available time slots while avoiding clashes among research working groups.

## Data Example
  2021.json

## Model
  constraints: Cardinality, Lex, Sum, Table

## Execution
  python RoadefPlanning2.py -data=<datafile.json>
  python RoadefPlanning2.py -data=[datafile.json,number]

## Links
  - https://drops.dagstuhl.de/storage/00lipics/lipics-vol307-cp2024/LIPIcs.CP.2024.34/LIPIcs.CP.2024.34.pdf
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
"""

from pycsp3 import *

nSessions, nSlots, papers_range, nGroups, nSessionPapers, slot_capacities, session_groups, forbidden, nRooms = data or (*load_json_data("2021.json"), 6)

assert nSessions == len(nSessionPapers) == len(session_groups) and nSlots == len(slot_capacities)
slot_capacities.sort()  # easier for reasoning and posting some constraints
decrement(forbidden)  # because we start indexing at 0
NO = nSlots

I, T = range(nSessions), range(nSlots)

# pairs (i,j) of sessions shared by a positive number v of working groups
conflicts = [(i, j, v) for i, j in combinations(I, 2) if (v := len(set(session_groups[i]).intersection(set(session_groups[j])))) > 0]

# table used for channeling
channel_table = [(t, v) for t in T for v in range(papers_range[0], slot_capacities[t] + 1)] + [(NO, 0)]

maxSlots = [next(t if (t + 1) * papers_range[0] > k else t + 1 for t in T if sum(slot_capacities[:t + 1]) >= k)
            for i, k in enumerate(nSessionPapers)]
gap = nRooms * sum(slot_capacities) - sum(nSessionPapers)
min_nb_rooms = [max(0, nRooms - (gap // slot_capacities[t] + (1 if gap % slot_capacities[t] != 0 else 0))) for t in T]


def range_no():
    g = sum(sum(slot_capacities[: maxSlots[i]]) for i in I) - sum(nSessionPapers)
    min_nb_no = max(0, g // papers_range[-1]) + (1 if g // papers_range[-1] != 0 else 0)
    g = sum(sum(slot_capacities[-maxSlots[i]:]) for i in I) - sum(nSessionPapers)
    max_nb_no = g // papers_range[0] + (1 if g // papers_range[0] != 0 else 0)
    return range(min_nb_no, max_nb_no + 1)


def similar_sessions():
    avoidable_groups = [g for g in range(nGroups) if len([i for i in I if g in session_groups[i]]) == 1]
    m = [[g for g in session_groups[i] if g not in avoidable_groups] for i in I]
    return [(i, j) for i, j in combinations(I, 2) if nSessionPapers[i] == nSessionPapers[j] and m[i] == m[j]]


# x[i][k] is the kth slot used for session i (NO if unused slot)
x = VarArray(size=[nSessions, maxSlots], dom=range(nSlots + 1))  # if k < maxSlots[i] else None)

# y[i][k] is the number of papers presented in the kth slot used for session i (0 if unused slot)
y = VarArray(size=[nSessions, maxSlots], dom=[0] + papers_range)

satisfy(

    # channeling variables
    [
        Table(
            scope=(x[i][k], y[i][k]),
            supports=channel_table
        ) for i in I for k in range(maxSlots[i])
    ],

    # allocating the right number of papers for each session
    [Sum(y[i]) == nSessionPapers[i] for i in I],

    # not exceeding the possible number of parallel sessions
    Cardinality(
        within=x,
        occurrences={t: range(min_nb_rooms[t], nRooms + 1) for t in T} | {NO: range_no()}
    ),

    # forbidding some slots
    [x[i][k] != t for (i, t) in forbidden for k in range(maxSlots[i])],

    # ensuring different slots (while ordering them)
    [
        If(
            x[i][k + 1] != NO,
            Then=x[i][k] < x[i][k + 1]
        ) for i in I for k in range(maxSlots[i] - 1)
    ],

    # tag(symmetry-breaking)
    [x[i] <= x[j] for i, j in similar_sessions()]
)

minimize(
    Sum(
        both(
            x[i][k1] != NO,
            x[i][k1] == x[j][k2]
        ) * v
        for i, j, v in conflicts for k1 in range(maxSlots[i]) for k2 in range(maxSlots[j])
    )
)

# THE MOST EFFECTIVE MODEL

""" Comments
1) the range used for NO should be double checked
2) value 2 removed from the end of the array np of instance 2023 (seems a mistake)
3) Compilation example: python3 RoadefPlaning2.py -data=[2024.json,k=15]
4) ACE-rr is quite competitive wrt the MaxSAt approach presented at CP'04, as ACE can prove unsatisfiability or finds an optimal solution within 10 seconds 
   (optimality proof is not achieved for 4 instances however, as it can be seen at https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop)           
"""
# No need for y = VarArray(size=[nSessions, maxSlots], dom=lambda i, k: [0] + papers_range if k < maxSlots[i] else None)

# [Count(x, value=t) <= nRooms for t in range(nSlots)],
# BinPacking(x, sizes=1, limits=[nRooms] * nSlots + [200]),
