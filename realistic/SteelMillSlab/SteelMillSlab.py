"""
Problem 038 on CSPLib.

Steel is produced by casting molten iron into slabs.

## Data Example
  bench-2-0.json

## Model
  constraints: Sum, Table

## Execution
  python SteelMillSlab.py -data=<datafile.json>
  python SteelMillSlab.py -data=<datafile.json> -variant=01

## Links
  - https://www.csplib.org/Problems/prob038/

## Tags
  realistic, notebook, csplib
"""

from pycsp3 import *

assert not variant() or variant("01")

capacities, orders = data or load_json_data("bench-2-0.json")

sizes, colors = zip(*orders)

possibleLosses = [min(v for v in [0] + capacities if v >= i) - i for i in range(max(capacities) + 1)]
allColors = sorted(set(colors))
colorGroups = [[i for i, order in enumerate(orders) if order.color == color] for color in allColors]
nOrders, nSlabs, nColors = len(orders), len(orders), len(allColors)

# sb[i] is the slab used to produce the ith order
sb = VarArray(size=nOrders, dom=range(nSlabs))

# ld[j] is the load of the jth slab
ld = VarArray(size=nSlabs, dom=range(max(capacities) + 1))

# ls[j] is the loss of the jth slab
ls = VarArray(size=nSlabs, dom=possibleLosses)

if not variant():
    satisfy(
        # computing (and checking) the load of each slab
        [ld[j] == sizes * [sb[i] == j for i in range(nOrders)] for j in range(nSlabs)],

        # computing the loss of each slab
        [
            Table(
                scope=(ld[j], ls[j]),
                supports=enumerate(possibleLosses)
            ) for j in range(nSlabs)
        ],

        # no more than two colors for each slab
        [
            Sum(
                disjunction(sb[i] == j for i in g) for g in colorGroups
            ) <= 2 for j in range(nSlabs)
        ]
    )

elif variant("01"):
    # y[j][i] is 1 iff the jth slab is used to produce the ith order
    y = VarArray(size=[nSlabs, nOrders], dom={0, 1})

    # z[j][c] is 1 iff the jth slab is used to produce an order of color c
    z = VarArray(size=[nSlabs, nColors], dom={0, 1})

    satisfy(
        # linking variables sb and y
        [y[j][i] == (sb[i] == j) for j in range(nSlabs) for i in range(nOrders)],

        # linking variables sb and z
        [
            If(
                sb[i] == j,
                Then=z[j][c]
            ) for j in range(nSlabs) for i in range(nOrders) if (c := allColors.index(orders[i].color),)
        ],

        # computing (and checking) the load of each slab
        [ld[j] == y[j] * sizes for j in range(nSlabs)],

        # computing the loss of each slab
        [
            Table(
                scope=(ld[j], ls[j]),
                supports=enumerate(possibleLosses)
            ) for j in range(nSlabs)
        ],

        # no more than two colors for each slab
        [Sum(z[j]) <= 2 for j in range(nSlabs)]
    )

satisfy(
    # tag(redundant)
    Sum(ld) == sum(sizes),

    # tag(symmetry-breaking)
    [
        Decreasing(ld),

        [sb[i] <= sb[j] for i, j in combinations(nOrders, 2) if orders[i] == orders[j]]
    ]
)

minimize(
    # minimizing summed up loss
    Sum(ls)
)

""" Comments
1) For computing (and checking) the load of each slab
   the reverse side ? eq(z[s]{c] = 1 => or(...) is not really necessary but could it be helpful?
"""
