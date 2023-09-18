"""

See [wikipedia](https://en.wikipedia.org/wiki/Graph_coloring): In its simplest form, it is a way of coloring the vertices of a graph such that no two adjacent vertices are of the same color.

## Data
 - nNodes, nColors: the number of nodes and colors
 - edges (tuples of tuples): the list of edges of the graph.

An example is given in the json file.
## Model
constraints: Maximum, Intension


## Command Line

```shell
python3 Coloring.py -data=Coloring_rand1.json [-solve]
```

"""

from pycsp3 import *

nNodes, nColors, edges = data

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
