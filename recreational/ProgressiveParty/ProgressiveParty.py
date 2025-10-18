"""
See Problem 013 on CSPLib.

The problem is to timetable a party at a yacht club.
Certain boats are to be designated hosts, and the crews of the remaining boats in turn visit the
host boats for several successive half-hour periods. The crew of a host boat remains on board
to act as hosts while the crew of a guest boat together visits several hosts. Every boat can only
hold a limited number of people at a time (its capacity) and crew sizes are different. The total
number of people aboard a boat, including the host crew and guest crews, must not exceed the
capacity. A table with boat capacities and crew sizes can be found below; there were six time
periods. A guest boat cannot not revisit a host and guest crews cannot meet more than once.
The problem facing the rally organizer is that of minimizing the number of host boats.

## Data Example
  12-05.json

## Model
  constraints: AllDifferent, Channel, Element, Sum

## Execution
  python ProgressiveParty.py -data=<datafile.json>
  python ProgressiveParty.py -data=<datafile.txt> -parser=ProgressiveParty_Parser.py
  python ProgressiveParty.py -parser=ProgressiveParty_rally-red.py <number> <number>

## Links
  - https://www.csplib.org/Problems/prob013/
  - https://link.springer.com/article/10.1007/BF00143880
  - https://www.cril.univ-artois.fr/XCSP23/competitions/cop/cop

## Tags
  recreational, csplib, xcsp23
"""

from pycsp3 import *

nPeriods, boats = data or load_json_data("12-05.json")

capacities, crews = zip(*boats)

nBoats = len(boats)
B, P = range(nBoats), range(nPeriods)


def minimal_number_of_hosts():
    nPersons = sum(crews)
    cnt, acc = 0, 0
    for capacity in sorted(capacities, reverse=True):
        if acc >= nPersons:
            return cnt
        acc += capacity
        cnt += 1
    assert False, "should not be reached"


# h[b] indicates if the boat b is a host boat
h = VarArray(size=nBoats, dom={0, 1})

# s[b][p] is the scheduled (visited) boat by the crew of boat b at period p
s = VarArray(size=[nBoats, nPeriods], dom=range(nBoats))

# g[b1][p][b2] is 1 if s[b1][p] = b2
g = VarArray(size=[nBoats, nPeriods, nBoats], dom={0, 1})

satisfy(
    # identifying host boats
    [h[b] == (s[b][p] == b) for b in B for p in P],

    # identifying host boats (from visitors)
    [h[s[b][p]] == 1 for b in B for p in P],

    # channeling variables from arrays s and g
    [Channel(g[b][p], s[b][p]) for b in B for p in P],

    # boat capacities must be respected
    [g[:, p, b] * crews <= capacities[b] for b in B for p in P],

    # a guest boat cannot revisit a host
    [AllDifferent(s[b], excepting=b) for b in B],

    # guest crews cannot meet more than once
    [Sum(s[b1][p] == s[b2][p] for p in P) <= 1 for b1, b2 in combinations(B, 2)],

    # ensuring a minimum number of hosts  tag(redundant)
    Sum(h) >= minimal_number_of_hosts()
)

minimize(
    # minimizing the number of host boats
    Sum(h)
)

""" Comments
1) Here is an alternative way of posting the 2nd group:
 [If(s[b1][p] == b2, Then=h[b2]) for b1 in B for b2 in B if b1 != b2 for p in P],

2) Here is a less compact way of posting the 4th group:
 [[g[i][p][b] for i in B] * crews <= capacities[b] for b in B for p in P],

3) In the Constraints paper cited above, additional constraints (not taken into account here) on host boats allow us 
   to prove easily optimality for the instance red42.
"""
