"""
Related papers:
 - Mathematical methods of organizing and planning production, L. V. Kantorovich, Management Science, 6(4):366–422, 1960
 - From High-Level Model to Branch-and-Price Solution in G12, J. Puchinger, P. Stuckey, M. Wallace, and S. Brand, CPAIOR 2008: 218-232

## Data Example
  small.json

## Model
  constraints: Lex, Sum

## Execution
  python Cutstock.py -data=<datafile.json>
  python Cutstock.py -data=<datafile.dzn> -parser=Cutstock_ParserZ.py

## Links
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  recreational, xcsp25
"""

from pycsp3 import *

nPieces, pieceLength, items = data
lengths, demands = zip(*items)
nItems = len(data.items)

# p[i] is 1 iff the ith piece of the stock is used
p = VarArray(size=nPieces, dom={0, 1})

# r[i][j] is the number of items of type j built using stock piece i
r = VarArray(size=[nPieces, nItems], dom=lambda i, j: range(max(demands) + 1))

satisfy(
    # not exceeding possible demands
    [r[i][j] <= demands[j] for i in range(nPieces) for j in range(nItems)],

    # each item demand must be exactly satisfied
    [Sum(r[:, j]) == demand for j, demand in enumerate(demands)],

    # each piece of the stock cannot provide more than its length
    [r[i] * lengths <= p[i] * pieceLength for i in range(nPieces)],

    # tag(symmetry-breaking)
    [
        Decreasing(p),
        LexDecreasing(r)  # to be removed for MiniCOP track
    ]
)

minimize(
    # minimizing the number of used pieces
    Sum(p)
)
