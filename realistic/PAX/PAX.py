"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  pp-20-1c.json

## Model
  constraints: Count, Sum

## Execution
  python PAX.py -data=<datafile.json>
  python PAX.py -data=<datafile.dzn> -parser=PAX_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
"""

from pycsp3 import *

objType, forwardTW, backwardTW, stationLines, maxPAX, services, trips = data
serviceLines, schedules = zip(*services)
nStations, nServices, nPassengers = len(stationLines), len(services), len(trips)


def compatible_services(k):
    # for passenger k, these are the compatible services within the defined TW, or to the next available service reaching its destination
    time, src, dst = trips[k]
    t = [s for s in range(nServices) if
         schedules[s][src] > 0 and schedules[s][dst] > 0 and serviceLines[s] in set(stationLines[src]).intersection(set(stationLines[dst]))]
    t1 = [s for s in t if time - forwardTW <= schedules[s][src] <= time + backwardTW]
    t2 = [s for s in t if schedules[s][src] >= time]
    return set(t1 + ([t2[0]] if len(t2) > 0 else []))


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
    [x[k] in compatible_services(k) for k in range(nPassengers)],

    # no passenger for an absent service
    [p[i][j] == 0 for i in range(nServices) for j in range(nStations) if schedules[i][j] == 0],

    # computing the number of passengers onboard each service departing every station
    [
        p[i][j] == Count(
            [x[k] for k in range(nPassengers) if trips[k][1] <= j < trips[k][2]],
            value=i
        ) for i in range(nServices) for j in range(nStations) if schedules[i][j] != 0
    ]
)

minimize(
    Sum(cost(p[i][j]) for i in range(nServices) for j in range(nStations))
)

"""
1) hybrid tables possible for the cost computation
2) in data, we replaced 1..3 by {1,2,3} for simplifying parsing
"""
