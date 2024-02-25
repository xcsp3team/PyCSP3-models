"""
Discrete Lot Sizing problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by Andrea Rendl-Pitrey (Satalia).
MIT Licence.

## Data Example
  pigment15a.json

## Model
  constraints: AllDifferent, Cardinality, Count, Element, Sum

## Execution
  python LotSizing.py -data=<datafile.json>
  python LotSizing.py -data=<datafile.dzn> -parser=LotSizing_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob058/
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, csplib, mzn19, mzn20
"""

from pycsp3 import *

nPeriods, inventoryCost, changeCosts, nbOfOrders, orders = data
duePeriods, itemTypes = zip(*orders)
nOrders, nItemTypes = len(orders), len(nbOfOrders)


#  returns the order number of the k-th order of item_type
def order_number(item_type, k):
    return sum(nbOfOrders[:item_type]) + k


# x[t] is the order produced at time t (possibly, none with special value nOrders)
x = VarArray(size=nPeriods, dom=range(nOrders + 1))

# y[i] is the time at which the order is produced
y = VarArray(size=nOrders, dom=range(nPeriods))

# ip[i] is the inventory period required for order i (i.e. the number of periods the order is completed before its due date)
ip = VarArray(size=nOrders, dom=range(max(duePeriods) + 1))

# cc[t] is the cost for changing the machine setup from time t to t+1
cc = VarArray(size=nPeriods - 1, dom=changeCosts)

# po[i] is the ith produced order
po = VarArray(size=nPeriods, dom=range(nOrders + 1))

satisfy(
    # each order must be produced (only once)
    Cardinality(x, occurrences={i: 1 for i in range(nOrders)} | {nOrders: nPeriods - nOrders}),  # needs Python 3.9

    # any order must be produced before its due date
    [x[t] != i for i in range(nOrders) for t in range(nPeriods) if duePeriods[i] < t],

    # linking variables of arrays x and y
    [x[y[i]] == i for i in range(nOrders)],

    # tag(redundant-constraints)
    AllDifferent(y),

    # sets the number of periods that inventory is necessary for each order
    [ip[i] == duePeriods[i] - y[i] for i in range(nOrders)],

    # computing production order (without holes that may be present in x); useful to impose the change_cost constraints
    [
        po[0] == x[0],
        [
            If(
                x[t] == nOrders,
                Then=po[t] == po[t - 1],
                Else=po[t] == x[t]
            ) for t in range(1, nPeriods)
        ]
    ],

    # tag(redundant-constraints)
    [Count(po, value=i) in range(1, 2 + (nPeriods - nOrders)) for i in range(nOrders)],

    # computing change costs (the change cost is applied when changing from one item type to another)
    [cc[t] == changeCosts[po[t]][po[t + 1]] for t in range(nPeriods - 1)],

    # completing orders of same type in a fixed order  tag(symmetry-breaking)
    [y[order_number(it, k)] < y[order_number(it, k + 1)] for it in range(nItemTypes) for k in range(nbOfOrders[it] - 1)]
)

minimize(
    # minimizing the sum of the total change costs and inventory costs
    Sum(cc) + Sum(ip) * inventoryCost
)
