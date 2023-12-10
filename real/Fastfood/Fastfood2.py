"""
## Data Example
  02.json

## Model
  constraints: Minimum, Sum, Table

## Execution
  python Fastfood.py -data=<datafile.json>
  python Fastfood.py -data=<datafile.json> -variant=table
  python Fastfood.py -data=<datafile.dzn> -parser=Fastfood_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  real
"""

from pycsp3 import *

nDepots, restaurants = data
nRestaurants = len(restaurants)
positions = [restaurant.position for restaurant in restaurants]
# NOTE: below, cp_array is necessary for being able to use the constraint Element in the main variant
distances = cp_array([abs(positions[j] - positions[i]) for j in range(nRestaurants)] for i in range(nRestaurants))

# d[i][j] is the distance between the ith restaurant and the jth depot
d = VarArray(size=[nRestaurants, nDepots], dom=lambda i, j: distances[i])

if not variant():
    # x[j] is the index of the restaurant used as the jth depot
    x = VarArray(size=nDepots, dom=range(nRestaurants))

    satisfy(
        # linking positions of depots with their distances to the restaurants
        distances[i][x[j]] == d[i][j] for i in range(nRestaurants) for j in range(nDepots)
    )

elif variant("table"):
    # x[j] is the position of the jth depot
    x = VarArray(size=nDepots, dom=positions)

    satisfy(
        # linking positions of depots with their distances to the restaurants
        (x[j], d[i][j]) in {(p, abs(p - positions[i])) for p in positions} for i in range(nRestaurants) for j in range(nDepots)
    )

satisfy(
    # tag(symmetry-breaking)
    Increasing(x, strict=True)
)

minimize(
    Sum(Minimum(d[i]) for i in range(nRestaurants))
)
