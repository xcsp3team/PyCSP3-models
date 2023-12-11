"""
The goal of the asymmetric travelling purchaser problem is to decide where to buy each of a set of products,
and in which order to visit the purchase locations, so as to minimize the total travel and purchase costs.
Travel costs are asymmetric, and cities are laid out on a grid with travel only allowed between horizontally and vertically adjacent cities.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2012/2016 Minizinc challenges.
The MZN model was proposed by Kathryn Francis.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-3-30-1.json

## Model
  constraints: Circuit, Element

## Execution
  python TPP.py -data=<datafile.json>
  python TPP.py -data=<datafile.dzn> -parser=TPP_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn12, mzn16
"""

from pycsp3 import *

nProducts, distances, prices = data
nCities, maxDistance, maxPrice = len(distances), max(max(row) for row in distances), max(max(row) for row in prices)

# x[i] is the city that succeeds to the ith city
x = VarArray(size=nCities, dom=range(nCities))

# tc[i] is the travel cost from going to the ith city to the next one
tc = VarArray(size=nCities, dom=range(maxDistance + 1))

# pl[j] is the purchase location of the jth product
pl = VarArray(size=nProducts, dom=range(nCities - 1))

# pc[j] is the purchase cost of the jth product
pc = VarArray(size=nProducts, dom=range(maxPrice + 1))

satisfy(
    # computing travel costs
    [tc[i] == distances[i][x[i]] for i in range(nCities)],

    # the purchase cost depends on the chosen purchase city
    [pc[j] == prices[pl[j]][j] for j in range(nProducts)],

    # purchasing a product at a city is only possible if you visit that city
    [x[pl[j]] != pl[j] for j in range(nProducts)],

    # a circuit is expected
    Circuit(x),

    # the last city must be visited (we start here)
    x[nCities - 1] != nCities - 1
)

minimize(
    # minimizing the total cost
    Sum(tc) + Sum(pc)
)
