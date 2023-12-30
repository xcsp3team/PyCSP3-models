"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2017 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  10-24-10.json

## Model
  constraints: Channel, Element, Sum

## Execution
  python TD_TSP.py -data=<datafile.json>
  python TD_TSP.py -data=<datafile.dzn> -parser=TD_TSP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn15, mzn17
"""

from pycsp3 import *

durations, nSteps, granularity, times = data
nVisits = len(durations)
horizon = nSteps * (granularity - 1) + 1

# x[i] is the position in the tour of the ith client to be visited
x = VarArray(size=nVisits + 1, dom=range(nVisits + 1))

# nxt[i] is the client that comes after the ith visit
nxt = VarArray(size=nVisits + 1, dom=range(nVisits + 1))

# prv[i] is the client that comes before the ith visit
prv = VarArray(size=nVisits + 1, dom=range(nVisits + 1))

# at[i] is the time when is visited the ith client
at = VarArray(size=nVisits + 1, dom=range(horizon + 1))

satisfy(
    Channel(nxt, prv),

    # fixing some variables
    [
        x[0] == 0,
        x[-1] == nVisits,
        at[0] == 0,
        prv[0] == nVisits,
        nxt[-1] == 0
    ],

    # ensuring a proper tour
    [
        [nxt[i] != i for i in range(nVisits + 1)],
        [prv[i] != i for i in range(nVisits + 1)]
    ],

    # ensuring coherence of positions
    [
        [x[nxt[i]] == x[i] + 1 for i in range(nVisits)],
        [x[i] == x[prv[i]] + 1 for i in range(1, nVisits + 1)]
    ],

    # taking into account travel time constraints
    [
        [at[i] >= at[j] + durations[j] + times[:, i, :][j][at[j] // granularity] for i in range(1, nVisits + 1) if (j := prv[i])],
        [at[nxt[i]] >= at[i] + durations[i] + times[i][nxt[i]][at[i] // granularity] for i in range(nVisits)]
    ],

    # imposing some conditions on last visit time  tag(redundant-constraints)
    [
        at[-1] - Sum(times[i][nxt[i]][at[i] // granularity] for i in range(nVisits)) >= sum(durations),
        at[-1] - Sum(times[:, i, :][prv[i]][at[prv[i]] // granularity] for i in range(1, nVisits + 1)) >= sum(durations)
    ]
)

if variant("plus"):
    # y[i] is the client visited at the ith position
    y = VarArray(size=nVisits + 1, dom=range(nVisits + 1))  # only for search

    # redundant constraints regarding the search variables  tag(search)
    satisfy(
        Channel(x, y),
        y[0] == 0,
        y[-1] == nVisits,
        [nxt[y[j]] == y[j + 1] for j in range(nVisits)],
        [prv[y[j + 1]] == y[j] for j in range(nVisits)]
    )

minimize(
    # minimizing time visit of the last client
    at[-1]
)

"""
1) note that constraints about prec and forbid are not posted because there are not present in the data (2015 and 2017)
"""
