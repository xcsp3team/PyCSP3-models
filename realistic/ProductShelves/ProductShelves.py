"""
From Danyal Mirza (Ericsson): In a warehouse, a number of products are to be placed on some shelves such that the minimum amount of shelves is used.
These products are all shaped like 3-dimensional boxes, with dimensions length, width and height.
The shelves are also shaped like 3-dimensional boxes with dimensions length, width and height and the number of shelves are finite.
Neither the shelves and the products are allowed to be rotated.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2025 Minizinc challenge.
The original model was written by Danyal Mirza  from Ericsson (MIT Licence).

## Data Example
  toy.json

## Model
  constraints: Lex, Maximum, NoOverlap, Precedence, Table

## Execution
  python ProductShelves.py -data=<datafile.json>
  python ProductShelves.py -data=<datafile.dzn> -parser=ProductShelves_ParserZ.py

## Links
  - https://www.minizinc.org/challenge/2025/results/

## Tags
  realistic, mzn25
"""

from pycsp3 import *

nShelves, dimensions, nProductsToBuild = data or load_json_data("toy.json")

maxLength = max(v for dim in dimensions.products for v in dim)
productOf = flatten([i] * v for i, v in enumerate(nProductsToBuild))  # product per item
nProducts, nItems, nDimensions = len(dimensions.products), len(productOf), 3  # Length, Width, Height

# x[i] is the shelf where is placed the ith item
x = VarArray(size=nItems, dom=range(nShelves))

# ilen[i][s][d] is the length of the ith item on the sth shelf along dimension d (0 if not on the shelf s)
ilen = VarArray(size=[nItems, nShelves, nDimensions], dom=range(maxLength + 1))

# ipos[i][s][d] is the starting position of the ith item on the sth shelf along dimension d
ipos = VarArray(size=[nItems, nShelves, nDimensions], dom=range(max(dimensions.shelves) + 1))

# z is the number of loaded shelves (minus 1)
z = Var(dom=range(nShelves))

satisfy(

    # setting all rows in products_sizes_3d to their respective sizes if they exist in shelf i, [0, 0, 0] otherwise
    [
        Table(
            scope=(x[i], ilen[i][s]),  # , ipos[i][s]),
            supports=[(s, dimensions.products[p]), (ne(s), 0, 0, 0)]  # [(s, dimensions.products[p], ANY, ANY, ANY), (ne(s), 0, 0, 0, 0, 0, 0)]
        ) for s in range(nShelves) for i in range(nItems) if (p := productOf[i],)
    ],

    # ensuring all products in each shelf to no overlap
    [
        NoOverlap(
            origins=ipos[:, s, :],
            lengths=ilen[:, s, :]
        ) for s in range(nShelves)
    ],

    # ensuring items are placed within the dimensions of the shelves
    [
        ipos[i][s][d] + ilen[i][s][d] <= dimensions.shelves[d]
        for s in range(nShelves) for i in range(nItems) for d in range(nDimensions)
    ],

    # tag(symmetry-breaking)
    [
        Precedence(x),

        [Increasing(x[i] for i in range(nItems) if productOf[i] == p) for p in range(nProducts)],

        [LexIncreasing(ipos[i][s] for i in range(nItems) if productOf[i] == p) for s in range(nShelves) for p in range(nProducts)]
    ],

    # computing the value of the objective
    z == Maximum(x)
)

minimize(
    z + 1
)

""" Comments
1) Are we totally sure of the way the last symmetry-breaking (group of) constraint has been translated from mzn? Even if that seems correct.
"""

# java -Xmx30000M ace ProductShelves-ps-50-06.xml -rr -ev -di=0 -g_noa=0
