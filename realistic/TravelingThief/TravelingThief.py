"""
Travelling Thief Problem

One has to visit all cities while picking items.
One has to maximize the value of the knapsack items and minimize the rental of the knapsack,
which depends on the travel time taking into account that the travel speed decreases with the weight of the items.
Note that there are no items in first city and there are always the same number of items in each other city.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2023 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n10-k03-c5000-l10000-u10100-r46.json

## Model
  constraints: AllDifferent, Sum

## Execution
  python TravelingThief.py -data=sm-10-13-00.json
  python TravelingThief.py -data=sm-10-13-00.dzn -dataparser=TravelingThief_ParserZ.py

## Links
  - https://sites.google.com/view/ttp-gecco2023/home
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn23
"""

from pycsp3 import *

cap, min_speed, max_speed, renting_ratio, distances, items = data
profits, weights, cities = cp_array(zip(*items))  # be careful (cp-array needed; otherwise tuples)
nCities, nItems = len(distances), len(items)
nSteps = nCities

itemsPerCity = nItems // (nCities - 1)  # number of items in each city
assert nItems % (nCities - 1) == 0, "not all cities have the same amount of items"

nu = (max_speed - min_speed) // cap  # # velocity of the traveller at any point in time (which depends on the weight)
city_items = cp_array(
    [([0] * itemsPerCity if c == 0 else [i for i in range(nItems) if items[i].city == c]) for c in range(nCities)])  # maps cities to its items

# x[i] is 1 if the ith item is picked
x = VarArray(size=nItems, dom={0, 1})

# y[t] is the city visited at time t
y = VarArray(size=nSteps, dom=range(nCities))

# wgt[t] is the weight of the knapsack at time t
wgt = VarArray(size=nSteps, dom=range(cap + 1))

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
    x * weights <= cap,

    # computing weights
    [wgt[t] == wgt[t - 1] + Sum(x[i] * weights[i] for j in range(itemsPerCity) if [i := city_items[:, j][y[t]]]) for t in range(1, nCities)]
)

maximize(
    100 * (x * profits) -
    renting_ratio * Sum(distances[y[t]][y[t + 1]] // vel[t] for t in range(nCities))
)

"""
1) distances[y[t]][y[t + 1]]
 is a shortcut for 
 distances[y[t]][y[(t + 1) % nCities]]
 as by default, there is auto-adjustment of array idnexing
"""
