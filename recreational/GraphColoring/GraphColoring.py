"""

## Data Example
  1-fullins-3.json

## Model
  There are two variants wrt the objective function.

  constraints: Maximum, Sum

## Execution
  python GraphColoring.py -data=<datafile.json>
  python GraphColoring.py -data=<datafile.json> -variant=sum

## Links
  - https://turing.cs.hbg.psu.edu/txn131/graphcoloring.html

## Tags
  recreational
"""

from pycsp3 import *

n, edges, colorings, multiColorings = data  # n is the number of nodes -- multi-coloring not taken into account for the moment
colorings = colorings if colorings else []

# c[i] is the color assigned to the ith node
c = VarArray(size=n, dom=range(n))

satisfy(
    [abs(c[i] - c[j]) >= d for (i, j, d) in edges],

    # nodes with preassigned colors
    [c[i] == colors[0] for (i, colors) in colorings if len(colors) == 1],

    # nodes with subsets of prefixed colors
    [c[i] in colors for (i, colors) in colorings if len(colors) > 1]
)

if not variant():
    minimize(
        # minimizing the greatest used color index (and, consequently, the number of colors)
        Maximum(c)
    )
elif variant("sum"):
    minimize(
        # minimizing the sum of colors assigned to nodes
        Sum(c)
    )

""" Comments
1) When d is 1, abs(x - y) >= d is automatically simplified into x != y
"""
