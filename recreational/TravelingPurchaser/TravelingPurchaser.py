"""
See, e.g., "Solving the asymmetric traveling purchaser problem" by J. Riera-Ledesma, J. Salazar González, Annals OR 144(1): 83-97 (2006)
See similar model (called ttp) proposed by Kathryn Francis for the 2012 Minizinc Competition

## Data Example
  7-5-30-1.json

## Model
  constraints: Circuit, Sum

## Execution
  python TravelingPurchaser.py -data=<datafile.json>

## Links
  - https://www.csplib.org/Problems/prob013/

## Tags
  recreational
"""

from pycsp3 import *

distances, prices = data
nCities, nProducts = len(distances), len(prices)

# s[i] is the city succeeding to the ith city (itself if not part of the route)
s = VarArray(size=nCities, dom=range(nCities))

# d[i] is the distance (seen as a travel cost) between the ith city and its successor
d = VarArray(size=nCities, dom=lambda i: {v for v in distances[i] if v >= 0})

# l[i] is the purchase location of the ith product (last city has nothing for sale)
l = VarArray(size=nProducts, dom=range(nCities - 1))

# c[i] is the purchase cost of the ith product
c = VarArray(size=nProducts, dom=lambda i: set(prices[i]))

satisfy(
    # linking distances to successors
    [distances[i][s[i]] == d[i] for i in range(nCities)],

    # linking purchase locations to purchase costs
    [prices[i][l[i]] == c[i] for i in range(nProducts)],

    # purchasing a product at a city is only possible if you visit that city
    [
        If(
            s[i] == i,
            Then=l[j] != i
        ) for i in range(nCities) for j in range(nProducts)
    ],

    Circuit(s),

    # last city must be visited (we start here)
    s[nCities - 1] != nCities - 1
)

minimize(
    Sum(d) + Sum(c)
)
