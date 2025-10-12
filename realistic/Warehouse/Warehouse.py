"""
See Problem 034 on CSPLib.

In the Warehouse Location problem (WLP), a company considers opening warehouses at some candidate locations in order to supply its existing stores.

## Data Example
  opl-example.json

## Model
  constraints: Element, Sum

## Execution
  python Warehouse.py -data=<datafile.json>
  python Warehouse.py -data=<datafile.json> -variant=compact
  python Warehouse.py -data=<datafile.txt> -parser=Warehouse_Parser.py
  python Warehouse.py -parser=Warehouse_Random.py 20 50 100 10 1000 0

## Links
  - https://www.csplib.org/Problems/prob034/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, notebook, csplib, xcsp22
"""

from pycsp3 import *
from pycsp3.dashboard import options

options.keep_sum = True  # to get a better formed XCSP instance

assert not variant() or variant("compact")

cost, capacities, costs = data or load_json_data("opl-example.json")  # cost is the fixed cost when opening a warehouse

nWarehouses, nStores = len(capacities), len(costs)

# w[i] is the warehouse supplying the ith store
w = VarArray(size=nStores, dom=range(nWarehouses))

satisfy(
    # capacities of warehouses must not be exceeded
    Count(w, value=j) <= capacities[j] for j in range(nWarehouses)
)

if not variant():
    # c[i] is the cost of supplying the ith store
    c = VarArray(size=nStores, dom=lambda i: costs[i])

    # o[j] is 1 if the jth warehouse is open
    o = VarArray(size=nWarehouses, dom={0, 1})

    satisfy(
        # the warehouse supplier of the ith store must be open
        [o[w[i]] == 1 for i in range(nStores)],

        # computing the cost of supplying the ith store
        [costs[i][w[i]] == c[i] for i in range(nStores)]
    )

    minimize(
        # minimizing the overall cost
        Sum(c) + Sum(o) * cost
    )

elif variant("compact"):
    minimize(
        # minimizing the overall cost
        Sum(costs[i][w[i]] for i in range(nStores)) + NValues(w) * cost
    )

""" Comments
1) When compiling the 'compact' variant, some auxiliary variables are automatically introduced
   in order to remain in the perimeter of XCSP3-core   
2) It is possible to replace the first group of constraints Count by:
      Cardinality(w, occurrences={j: range(capacities[j]+1) for j in range(nWarehouses)})
    or
      BinPacking(w, sizes=1, limits=capacities)
"""
