"""
Taken from the original Minizinc model:
"There are two warehouses, A and B. Each warehouse has a fixed set of customers.
No customer is served by both warehouses - so the two sets are disjoint.
Each warehouse has a truck. There is a table of distances from customer to warehouse and between the customers.

A truck is allowed to deliver not only to customers of its own warehouse, but also to customers of the other warehouse.
To make this possible there is a "depot" where one truck can leave some goods for the other truck to pick up and deliver to the customer.
The choice of depot is a decision variable ranging over customer and warehouse locations.

Naturally before delivering to a customer of another warehouse, the truck must first visit the depot to collect the goods for delivery to the customer.
The other truck must also visit the depot, of course, to drop off the goods.
There are no time constraints, and therefore no restriction on which truck visits the depot first.
The objective is to minimise the maximum of the distances travelled by the trucks."

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011/2016 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  ratt-99-5.json

## Model
  constraints: AllDifferent, Count, Element, Maximum

## Execution
  python DepotPlacement.py -data=<datafile.json>
  python DepotPlacement.py -data=<datafile.dzn> -parser=DepotPlacement_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  real, mzn10, mzn11, mzn16
"""

from pycsp3 import *

nClientsPerWarehouse, distances = data

tourLength = nClientsPerWarehouse + 1
nLocations = tourLength * 2  # number of customers plus two warehouses
WA, WB = 0, tourLength  # locations of warehouse A and B
tourSize = tourLength + 1  # possibility of visiting one extra client

# the location of the depot
depot = Var(range(nLocations))

# xa[i] is the ith visited location in tour A
xa = VarArray(size=tourSize, dom=range(nLocations))

# xb[i] is the ith visited location in tour B
xb = VarArray(size=tourSize, dom=range(nLocations))

# da[i] is the distance in tour A from the ith visited location to the next one
da = VarArray(size=tourSize, dom=distances)

# db[i] is the distance in tour B from the ith visited location to the next one
db = VarArray(size=tourSize, dom=distances)

satisfy(
    # computing distances for tour A
    [da[i] == distances[xa[i]][xa[i + 1]] for i in range(tourSize)],

    # computing distances for tour B
    [db[i] == distances[xb[i]][xb[i + 1]] for i in range(tourSize)],

    # all locations are visited by at least one truck (for tours A and B)
    [Exist(xa + xb, value=i) for i in range(nLocations)],

    # each tour visits different locations
    [
        AllDifferent(xa[1:]),
        AllDifferent(xb[1:])
    ],

    # warehouses must be visited first
    [xa[0] == WA, xb[0] == WB],

    # coming back to the warehouses is possible from second location  tag(symmetry-breaking)
    [
        [xa[i] != WA for i in range(2, tourSize)],
        [xb[i] != WB for i in range(2, tourSize)]
    ],

    # warehouses cannot be visited by different trucks  tag(redundant-constraint)
    [
        [xa[i] != WB for i in range(tourSize)],
        [xb[i] != WA for i in range(tourSize)]
    ],

    # depot constraints (visiting the depot before an extern location)
    [
        [
            If(
                xa[i] >= tourLength, xa[i] != depot,
                Then=Exist(xa[:i], value=depot)
            ) for i in range(1, tourSize)
        ],
        [
            If(
                xb[i] < tourLength, xb[i] != depot,
                Then=Exist(xb[:i], value=depot)
            ) for i in range(1, tourSize)]
    ]
)

minimize(
    Maximum(Sum(da), Sum(db))
)

"""
1) there is auto-adjusting of indexing, so:
  distances[xa[i]][xa[i + 1]]
is 
  distances[xa[i]][xa[(i + 1]) % tourSize]
"""
