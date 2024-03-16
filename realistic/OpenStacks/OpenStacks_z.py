"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2011/2015 Minizinc challenges.
The MZN model was proposed by Peter J. Stuckey.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  pb-20-20-1.json

## Model
  constraints: AllDifferent, Element, Maximum, Sum

## Execution
  python OpenStacks.py -data=<datafile.json>
  python OpenStacks.py -data=<datafile.dzn> -parser=OpenStacks_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  realistic, mzn09, mzn11, mzn15
"""

from pycsp3 import *

orders = data
nCustomers, nProducts = len(orders), len(orders[0])

quantities = [sum(orders[i]) for i in range(nCustomers)]  # total quantities per customer

# x[i] is the schedule of the ith product
x = VarArray(size=nProducts, dom=range(nProducts))

# y[i][t] is the quantity of products built for customer i at time t
y = VarArray(size=[nCustomers, nProducts + 1], dom=range(max(quantities) + 1))

satisfy(
    # scheduling products
    AllDifferent(x),

    # no product built at time 0
    [y[i][0] == 0 for i in range(nCustomers)],

    # computing the quantity of products built at any time
    [y[i][t] == y[i][t - 1] + orders[i][x[t - 1]] for t in range(1, nProducts + 1) for i in range(nCustomers)]
)

minimize(
    Maximum(
        Sum(
            both(
                y[i][j - 1] < quantities[i],
                y[i][j] > 0
            ) for i in range(nCustomers)
        ) for j in range(1, nProducts + 1)
    )
)
