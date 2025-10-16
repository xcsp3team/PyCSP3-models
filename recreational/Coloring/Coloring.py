"""
In its simplest form, it is a way of coloring the vertices of a graph such that no two adjacent vertices are of the same color.

## Data Example
  rand01.json

## Model
 constraint: Maximum

## Execution:
  python Coloring.py -data=<datafile.json>
  python Coloring.py -data=<datafile.json> -variant=csp

## Links
 - https://en.wikipedia.org/wiki/Graph_coloring
 - https://www.cril.univ-artois.fr/XCSP23/competitions/csp/csp

## Tags
  recreational, xcsp23
"""

from pycsp3 import *

assert not variant() or variant("csp")

nNodes, nColors, edges = data or load_json_data("rand01.json")

# x[i] is the color assigned to the ith node of the graph
x = VarArray(size=nNodes, dom=range(nColors))

satisfy(
    # two adjacent nodes must be colored differently
    x[i] != x[j] for (i, j) in edges
)

if not variant():
    minimize(
        # minimizing the greatest used color index (and, consequently, the number of colors)
        Maximum(x)
    )

elif variant("csp"):
    satisfy(
        # tag(symmetry-breaking)
        x[i] <= i for i in range(min(nNodes, nColors))
    )
