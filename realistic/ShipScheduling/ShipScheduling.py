"""
From the ICAPS conference paper (whose reference is given below):
"Ship scheduling deals with assigning arrival and departure times to a fleet of ships,
as well as the amount and sometimes type of cargo that is carried on each ship.
One consideration in ship scheduling which does not occur in other transportation problems is that most ports have
restrictions on the draft of ships that may safely enter the port.
Draft is the distance between the waterline and the ship’s keel, and is a function of the amount of cargo loaded onto the ship."

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2011/2012/2014 Minizinc challenges.
The MZN model was proposed by Elena Kelareva.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-Ships.json

## Model
  constraints: Element, Sum

## Execution
  python ShipScheduling.py -data=<datafile.json>
  python ShipScheduling.py -data=<datafile.dzn> -parser=ShipScheduling_ParserZ.py

## Links
  - https://ojs.aaai.org/index.php/ICAPS/article/view/13494
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic, mzn11, mzn12, mzn14
"""

from pycsp3 import *

berthSwaps, minSeparations, sailingDrafts, nTugs, ships, inShips, outShips, tugAllowances = data
inBerths, outBerths, gapBerths = zip(*berthSwaps)
earliest, tonnesPerCmDraft, tugSets, tugTurnarounds = zip(*ships)
nShips, horizon, nBerthSwaps, maxTugSets = len(ships), len(sailingDrafts), len(berthSwaps), len(tugSets[0])

assert nShips > 0 and horizon > 0 and all(0 < v <= horizon for v in earliest)

minDraft = min(v for row in sailingDrafts for v in row)
maxDraft = max(v for row in sailingDrafts for v in row)
maxTugsRequiredPerShip = max(v for row in tugSets for v in row)

# x[i] is the starting time of the ith ship
x = VarArray(size=nShips, dom=range(1, horizon))

# s[i] is 1 if the ith ship sails
s = VarArray(size=nShips, dom={0, 1})

# d[i] is the draft for the ith ship
d = VarArray(size=nShips, dom=range(minDraft, maxDraft + 1))

# tb[i][t][k] is the number of tugs of the kth set that are used at time t for ship i
tb = VarArray(size=[nShips, horizon, maxTugSets], dom=range(maxTugsRequiredPerShip + 1))

# tbe[i] is the number of extra tugs for the ith ship
tbe = VarArray(size=nShips, dom=range(maxTugsRequiredPerShip + 1))

# tbts[t] is the number of tugs used at time t
tbts = VarArray(size=horizon, dom=range(nShips * maxTugSets * maxTugsRequiredPerShip + 1))

satisfy(
    # computing sailing drafts
    [d[i] == sailingDrafts[x[i]][i] for i in range(nShips)],

    # a ship cannot sail if its max draft is 0
    [If(d[i] == 0, Then=s[i] == 0) for i in range(nShips)],

    # no ship can sail before its earliest allowable sailing time.
    [If(s[i] == 1, Then=x[i] >= earliest[i]) for i in range(nShips)],

    # managing shared berths
    [x[outBerths[i]] <= x[inBerths[i]] + gapBerths[i] for i in range(nBerthSwaps)],

    # managing separation times between all pairs of ships
    [
        If(
            s[i] == 1, s[j] == 1,
            Then=either(
                x[j] - x[i] >= minSeparations[i][j],
                x[i] - x[j] >= minSeparations[j][i]
            )
        ) for i, j in combinations(nShips, 2)
    ],

    # computing the number of tubs used at time t
    [tbts[t] == Sum(tb[:, t, :]) for t in range(horizon)],

    # computing the number of tugs used at each time slot for each ship
    [
        [
            If(
                s[i] == 1, t >= x[i], t < x[i] + tugTurnarounds[i][k],
                Then=tb[i][t][k] == tugSets[i][k]
            ) for i in range(nShips) for t in range(horizon) for k in range(maxTugSets)
        ],
        [
            If(
                disjunction(
                    s[i] == 0,
                    t < x[i],
                    t >= x[i] + tugTurnarounds[i][k]
                ),
                Then=tb[i][t][k] == 0
            ) for i in range(nShips) for t in range(horizon) for k in range(maxTugSets)
        ]
    ],

    # checking that we have enough tugs at any time
    [
        [Sum(tb[i][t] for i in inShips) <= nTugs for t in range(horizon)] if len(inShips) > 0 else None,
        [Sum(Sum(tb[i][t]) + tbe[i] * (t == x[i]) for i in outShips) <= nTugs for t in range(horizon)] if len(outShips) > 0 else None
    ],

    # adding an extra tug allowance to ensure that incoming tugs have time to move to the next ship
    [
        If(
            x[i] < x[j], x[i] + max(tugTurnarounds[i]) + tugAllowances[i][j] > x[j],
            Then=tbe[j] == sum(tugSets[i])
        ) for i in inShips for j in outShips
    ],

    # the number of extra tugs is 0 for incoming ships
    [tbe[i] == 0 for i in inShips],

    # the number of extra tugs is 0 for outgoing ships that are not shortly after an incoming ship
    [
        If(
            disjunction(
                x[i] > x[j],
                x[i] + max(tugTurnarounds[i]) + tugAllowances[i][j] <= x[j]
            ),
            Then=tbe[j] == 0
        ) for i in inShips for j in outShips
    ]
)

maximize(
    Sum(s[i] * d[i] * tonnesPerCmDraft[i] for i in range(nShips))
)

"""
1) Note that:
 If(len(outShips) > 0,
    Then=[Sum(Sum(tb[i][t]) + tbe[i] * (t == x[i]) for i in outShips) <= nTugs for t in range(horizon)]
 )
is equivalent to:
 [Sum(Sum(tb[i][t]) + tbe[i] * (t == x[i]) for i in outShips) <= nTugs for t in range(horizon)] if len(outShips) > 0 else None
"""
