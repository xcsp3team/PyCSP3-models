"""
The travelling salesman problem (TSP) asks the following question: "Given a list of cities and the distances between each pair of cities,
what is the shortest possible route that visits each city exactly once and returns to the origin city?" (from wikipedia).

## Data Example
  10-20-0.json

## Model
  constraints: Sum, Table

## Execution
  python TravelingSalesman.py -data=<datafile.json>
  python TravelingSalesman.py -data=<datafile.json> -variant=table

## Links
  - https://en.wikipedia.org/wiki/Travelling_salesman_problem

## Tags
  recreational
"""

from pycsp3 import *

distances = data
nCities = len(distances)

# c[i] is the ith city of the tour
c = VarArray(size=nCities, dom=range(nCities))

# d[i] is the distance between the cities i and i+1 chosen in the tour
d = VarArray(size=nCities, dom=distances)

satisfy(
    # Visiting each city only once
    AllDifferent(c)
)

if not variant():
    satisfy(
        # computing the distance between any two successive cities in the tour
        distances[c[i]][c[i + 1]] == d[i] for i in range(nCities)
    )

elif variant("table"):
    T = {(i, j, distances[i][j]) for i in range(nCities) for j in range(nCities) if i != j}

    satisfy(
        # computing the distance between any two successive cities in the tour
        (c[i], c[i + 1], d[i]) in T for i in range(nCities)
    )

minimize(
    # minimizing the travelled distance
    Sum(d)
)

""" Comments
1) Writing dom=distances is equivalent (and more compact) than writing dom={v for row in distances for v in row}

2) Index auto-adjustment is used with c[i+1] (equivalent to c[(i+1) % nCities)
"""
