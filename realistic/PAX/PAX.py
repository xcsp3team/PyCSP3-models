"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  pp-20-1c.json

## Model
  constraints: Count, Sum

## Execution
  python PAX.py -data=<datafile.json>
  python PAX.py -data=<datafile.dzn> -parser=PAX_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn19
"""

from pycsp3 import *

objType, forwardTW, backwardTW, stationLines, maxPAX, services, trips = data or load_json_data("pp-20-1c.json")

serviceLines, schedules = zip(*services)

nStations, nServices, nPassengers = len(stationLines), len(services), len(trips)
St, Sr, P = range(nStations), range(nServices), range(nPassengers)


def compatible_services(k):
    # for passenger k, these are the compatible services within the defined TW, or to the next available service reaching its destination
    time, src, dst = trips[k]
    S = set(stationLines[src]).intersection(set(stationLines[dst]))
    t = [i for i in Sr if schedules[i][src] > 0 and schedules[i][dst] > 0 and serviceLines[i] in S]
    t1 = [i for i in t if time - forwardTW <= schedules[i][src] <= time + backwardTW]
    j = next((i for i in t if schedules[i][src] >= time), -1)  # just the first element
    return set(t1 + ([j] if j != -1 else []))


def cost(y):
    v1, v2, v3 = (528 - 264), (528 - 264) + (662 - 528) * 5, (528 - 264) + (662 - 528) * 5 + (799 - 662) * 10
    if objType == 1:
        return ift(y < 265, 0, ift(y < 529, 10, ift(y < 663, 100, ift(y < 800, 1000, 10000))))
    return ift(y < 265, 0, ift(y < 529, y - 264, ift(y < 663, v1 + (y - 528) * 5, ift(y < 800, v2 + (y - 662) * 10, v3 + (y - 799) * 100))))


# x[k] is the service used by the kth passenger
x = VarArray(size=nPassengers, dom=range(nServices))

# p[i][j] is the number of passengers for the jth station of the ith service
p = VarArray(size=[nServices, nStations], dom=range(maxPAX + 1))

satisfy(
    # ensuring passengers are assigned to compatible services
    [x[k] in compatible_services(k) for k in P],

    # no passenger for an absent service
    [p[i][j] == 0 for i in Sr for j in St if schedules[i][j] == 0],

    # computing the number of passengers onboard each service departing every station
    [
        p[i][j] == Count(
            within=[x[k] for k in P if trips[k][1] <= j < trips[k][2]],
            value=i
        ) for i in Sr for j in St if schedules[i][j] != 0
    ]
)

minimize(
    Sum(cost(p[i][j]) for i in Sr for j in St)
)

""" Comments
1) Hybrid tables possible for the cost computation
2) In data (dzn files), we replaced 1..3 by {1,2,3} for simplifying parsing
"""
