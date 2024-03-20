"""
Road Network Maintenance Problem.

The aim is to determine which worksheets to execute on which day so that the road network is not perturbed too much.
Each worksheet is a contiguous set of daily tasks on roads: specified by a road and number of workers.
Worksheets have an importance defining how important they are to execute.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  easy-0200-50.json

## Model
  constraints: Cardinality, Cumulative, Maximum, Sum

## Execution
  python Nside.py -data=<datafile.json>
  python Nside.py -data=<datafile.dzn> -parser=Nside_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
"""

from pycsp3 import *

nDays, costs, centerWorkers, worksheets, blocks, arcs = data  # costs if for perturbation costs
work_center, mandatory, importance, est, lst, durations, roads, workers = zip(*worksheets)

nRoads, nCenters, nWorksheets = len(costs) - 1, len(centerWorkers), len(mandatory)
centerWorksheets = [[i for i in range(nWorksheets) if work_center[i] == c] for c in range(nCenters)]

W, D = range(nWorksheets), range(nDays)

# g[i] is 1 if the ith worksheet is executed
g = VarArray(size=nWorksheets, dom={0, 1})

# d[i] is the start time (debut) of the ith worksheet
d = VarArray(size=nWorksheets, dom=range(nDays))

# e[i] is the end time of the ith worksheet
e = VarArray(size=nWorksheets, dom=range(nDays))

satisfy(
    # computing end time of each worksheet
    [e[i] == d[i] + durations[i] for i in W],

    # fixing unused variables
    [(g[i] == 0) == (d[i] == est[i]) for i in W],

    # guaranteeing worksheet Earliest Starting Time
    [est[i] <= d[i] for i in W],

    # guaranteeing worksheet Latest Starting Time
    [d[i] <= lst[i] for i in W],

    # ensuring mandatory worksheets
    [g[i] >= mandatory[i] for i in W],

    # respecting precedences between worksheets
    [g[i] * e[i] <= d[j] + nDays * (1 - g[j]) for (i, j) in arcs],

    # maximal number of roads simultaneously blocked
    [
        Cardinality(
            within=[(d[i] + a + 1) * g[i] for i in W for a in range(durations[i]) if roads[i][a] in blocked_roads],
            occurrences={v + 1: range(limit + 1) for v in D}
        ) for (limit, blocked_roads) in blocks
    ],

    # not exceeding the capacity of work centers
    [
        Cumulative(
            tasks=[Task(origin=d[i] + a, length=g[i], height=workers[i][a]) for i in centerWorksheets[c] for a in range(durations[i])]
        ) <= centerWorkers[c]
        for c in range(nCenters) if len(centerWorksheets[c]) > 0
    ]
)

if not variant():
    maximize(
        g * importance - Maximum(Sum(g[i] * costs[roads[i][a] + 1][k] * (k == d[i] + a) for i in W for a in range(durations[i])) for k in D)
    )

elif variant('test'):

    tmp = VarArray(size=[nDays, nWorksheets], dom=lambda k, i: {costs[roads[i][a] + 1][k] for a in range(len(roads[i]))})

    satisfy(
        tmp[k][i] == g[i] * Sum(costs[roads[i][a] + 1][k] * (k == d[i] + a) for a in range(durations[i])) for k in D for i in W
    )

    maximize(
        g * importance - Maximum(Sum(tmp[k]) for k in D)
    )

"""
1) this part of the MZn model is not useful : Fits in schedule
    [e[i] <= nDays  for i in W]
2) the test variant does not seem efficient
3) for ACE, -di=0 -valh=Last
"""

# perterb_obj_ub = max(max(row) for row in perterb) * nDays
