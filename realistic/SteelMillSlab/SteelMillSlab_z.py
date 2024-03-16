"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017/2019 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  13-0.json

## Model
  constraints:  BinPacking, Count, Sum

## Execution
  python SteelMillSlab_z.py -data=<datafile.json>
  python SteelMillSlab_z.py -data=<datafile.dzn> -parser=SteelMillSlab_ParserZ.py

## Links
  - https://www.csplib.org/Problems/prob038/
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, csplib, mzn17, mzn19
"""

from pycsp3 import *

slabSizes, orders = data
colors, sizes = zip(*orders)
nOrders, nColors = len(orders), len(set(colors))
nSlabs, slabSizeLimit = nOrders, max(slabSizes) + 1

# gaps between each possible required size s and the closest slab with a size greater than s
gaps = cp_array(min(c - s for c in slabSizes if c >= s) for s in range(slabSizeLimit))

# x[k] is the slab for the kth order
x = VarArray(size=nOrders, dom=range(nSlabs))

# y[i] is the size (load) of the ith slab
y = VarArray(size=nSlabs, dom=range(slabSizeLimit))

satisfy(
    # each slab can contain at most 2 colors
    [
        Sum(
            Exist(x[k] == i for k in range(nOrders) if colors[k] == c) for c in range(nColors)
        ) <= 2 for i in range(nSlabs)
    ],

    # computing loads of slabs
    BinPacking(x, sizes=sizes, loads=y),

    # tag(symmetry-breaking)
    (
        [
            If(
                y[i] == 0,
                Then=y[i + 1] == 0
            ) for i in range(nSlabs - 1)
        ],

        [x[k] <= x[l] for k, l in combinations(nOrders, 2) if sizes[k] == sizes[l] or colors[k] == colors[l]]
    )
)

minimize(
    # minimizing total weight of steel produces
    Sum(gaps[y[i]] for i in range(nSlabs))
)

"""
 [Precedence(x), Decreasing(y)] for symmetry-breaking ?
"""
