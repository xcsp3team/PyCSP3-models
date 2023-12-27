"""
This models a routing problem based on a little example of Mario's day.
Mario is an Italian Plumber and his work is mainly to find gold in the plumbing of all the houses of the neighborhood.
Mario is moving in the city using his kart that has a specified amount of fuel.
Mario starts his day of work from his house and always ends to his friend Luigi's house to have the supper.
The problem here is to plan the best path for Mario in order to earn the more money with the amount of fuel of his kart.

From a more general point of view, the problem is to find a path in a graph:
 - Path endpoints are given (from Mario's to Luigi's)
 - The sum of weights associated to arcs in the path is restricted (fuel consumption)
 - The sum of weights associated to nodes in the path has to be maximized (gold coins)

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2013/2014/2017 Minizinc challenges.
The MZN model was proposed by maury Ollagnier and Jean-Guillaume Fages.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  easy-2.json

## Model
  constraints: Circuit, Element, Sum

## Execution
  python Mario_z.py -data=<datafile.json>
  python Mario_z.py -data=<datafile.dzn> -parser=Mario_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  recreational, mzn13, mzn14, mzn17
"""

from pycsp3 import *

marioHouse, luigiHouse, fuelLimit, houses = data
fuels, golds = zip(*houses)  # using cp_array is not necessary since intern arrays have the right type (for the constraint Element)
nHouses = len(houses)

# s[i] is the house succeeding to the ith house (itself if not part of the route)
s = VarArray(size=nHouses, dom=range(nHouses))

# consumed fuel
fuel = Var(dom=range(fuelLimit + 1))

satisfy(
    # we cannot consume more than the available fuel
    Sum(fuels[i][s[i]] for i in range(nHouses)) == fuel,

    # Mario must make a tour (not necessarily complete)
    Circuit(s),

    # Mario's house succeeds to Luigi's house
    s[luigiHouse] == marioHouse
)

maximize(
    # maximizing collected gold
    Sum((s[i] != i) * golds[i] for i in range(nHouses) if golds[i] != 0)
)
