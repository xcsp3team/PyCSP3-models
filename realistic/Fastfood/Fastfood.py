"""
## Data Example
  ff01.json

## Model
  constraints: Minimum, Sum, Table

## Execution
  python Fastfood.py -data=<datafile.json>
  python Fastfood.py -data=<datafile.json> -variant=table
  python Fastfood.py -data=<datafile.dzn> -parser=Fastfood_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2012/results2012.html

## Tags
  realistic
"""

from pycsp3 import *

assert not variant() or variant("table")

nDepots, restaurants = data or load_json_data("ff01.json")

positions = [restaurant.position for restaurant in restaurants]

nRestaurants = len(restaurants)
R, D = range(nRestaurants), range(nDepots)

# NOTE: below, cp_array is necessary for being able to use the constraint Element in the main variant
distances = cp_array([abs(positions[j] - positions[i]) for j in R] for i in R)

# d[i][j] is the distance between the ith restaurant and the jth depot
d = VarArray(size=[nRestaurants, nDepots], dom=lambda i, j: distances[i])

if not variant():
    # x[j] is the index of the restaurant used as the jth depot
    x = VarArray(size=nDepots, dom=range(nRestaurants))

    satisfy(
        # linking positions of depots with their distances to the restaurants
        distances[i][x[j]] == d[i][j] for i in R for j in D
    )

elif variant("table"):
    # x[j] is the position of the jth depot
    x = VarArray(size=nDepots, dom=positions)

    satisfy(
        # linking positions of depots with their distances to the restaurants
        Table(
            scope=(x[j], d[i][j]),
            supports={(p, abs(p - positions[i])) for p in positions}
        ) for i in R for j in D
    )

satisfy(
    # tag(symmetry-breaking)
    Increasing(x, strict=True)
)

minimize(
    Sum(Minimum(d[i]) for i in R)
)

""" Comments
1) because we build the 2-dimensional list 'distances" in the model (we don't load it from the data file)
   and because this list is involved in a constraint Element (in the main variant), we need to call cp_array 
2) the constraints Table can be equivalently posted by:
  (x[j], d[i][j]) in {(p, abs(p - positions[i])) for p in positions} for i in R for j in D
"""
