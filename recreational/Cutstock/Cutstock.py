"""

Related papers:
 - "*Mathematical methods of organizing and planning production*", L. V. Kantorovich, Management Science, 6(4):366–422, 1960
 - "*From High-Level Model to Branch-and-Price Solution in G12*", J. Puchinger, P. Stuckey, M. Wallace, and S. Brand, CPAIOR 2008: 218-232

## Data
 - nPieces, pieceLengths: the number and the sizes of pieces
 - items (tuple): each item has a length and a demand.

An example is given in the json file.

## Model
  constraints: Lex, Sum

## Execution
  python Cutstock.py -data=<datafile.json>

## Tags
  recreational
"""

from pycsp3 import *

nPieces, pieceLength, items = data
lengths, demands = zip(*items)
nItems = len(data.items)

# p[i] is 1 iff the ith piece of the stock is used
p = VarArray(size=nPieces, dom={0, 1})

# r[i][j] is the number of items of type j built using stock piece i
r = VarArray(size=[nPieces, nItems], dom=lambda i, j: range(demands[j] + 1))

satisfy(
    # each item demand must be exactly satisfied
    [Sum(r[:, j]) == demand for j, demand in enumerate(demands)],

    # each piece of the stock cannot provide more than its length
    [r[i] * lengths <= p[i] * pieceLength for i in range(nPieces)],

    # tag(symmetry-breaking)
    [Decreasing(p), LexDecreasing(r)]
)

minimize(
    # minimizing the number of used pieces
    Sum(p)
)
