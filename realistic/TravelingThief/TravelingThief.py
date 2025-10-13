"""
Travelling Thief Problem

One has to visit all cities while picking items.
One has to maximize the value of the knapsack items and minimize the rental of the knapsack,
which depends on the travel time taking into account that the travel speed decreases with the weight of the items.
Note that there are no items in first city and there are always the same number of items in each other city.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
For the original MZn model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n10-k03-c5000-l10000-u10100-r46.json

## Model
  constraints: AllDifferent, Sum

## Execution
  python TravelingThief.py -data=sm-10-13-00.json
  python TravelingThief.py -data=sm-10-13-00.dzn -parser=TravelingThief_ParserZ.py

## Links
  - https://sites.google.com/view/ttp-gecco2023/home
  - https://www.minizinc.org/challenge/2023/results/

## Tags
  realistic, mzn23
"""

from pycsp3 import *

capacity, min_speed, max_speed, renting_ratio, distances, items = data or load_json_data("n10-k03-c5000-l10000-u10100-r46.json")

profits, weights, cities = cp_array(zip(*items))  # be careful (cp-array needed; otherwise tuples)

nCities, nItems = len(distances), len(items)
assert nItems % (nCities - 1) == 0, "not all cities have the same amount of items"
nSteps = nCities
itemsPerCity = nItems // (nCities - 1)  # number of items in each city

nu = (max_speed - min_speed) // capacity  # # velocity of the traveller at any point in time (which depends on the weight)
city_items = cp_array(([0] * itemsPerCity if c == 0 else [i for i in range(nItems) if items[i].city == c]) for c in range(nCities))  # maps cities to its items

# x[i] is 1 if the ith item is picked
x = VarArray(size=nItems, dom={0, 1})

# y[t] is the city visited at time t
y = VarArray(size=nSteps, dom=range(nCities))

# wgt[t] is the weight of the knapsack at time t
wgt = VarArray(size=nSteps, dom=range(capacity + 1))

# vel[t] is the velocity of the traveler at time t
vel = VarArray(size=nSteps, dom=range(min_speed, max_speed + 1))

satisfy(
    # computing velocities
    [vel[t] == max_speed - nu * wgt[t] for t in range(nCities)],

    # ensuring no city can be visited twice
    AllDifferent(y),

    # at time 0, the first city is 0 and the knapsack is empty
    [
        y[0] == 0,
        wgt[0] == 0
    ],

    # not exceeding the capacity of the knapsack
    x * weights <= capacity,

    # computing weights
    [
        wgt[t] == wgt[t - 1] + Sum(x[i] * weights[i] for j in range(itemsPerCity) if [i := city_items[:, j][y[t]]])
        for t in range(1, nCities)
    ]
)

maximize(
    100 * (x * profits) -
    renting_ratio * Sum(distances[y[t]][y[t + 1]] // vel[t] for t in range(nCities))
)

""" Comments
1) distances[y[t]][y[t + 1]]
 is a shortcut for 
   distances[y[t]][y[(t + 1) % nCities]]
 as by default, there is auto-adjustment of array indexing
"""
