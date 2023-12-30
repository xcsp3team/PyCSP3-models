"""
The problem is to find communities in a graph with maximum modularity value while satisfying the fact that some pairs of nodes must be assigned
to same or different communities.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  strike-s2-k8.json

## Model
  constraints: Precedence, Sum

## Execution
  python CommunityDetection_z1.py -data=<datafile.json>
  python CommunityDetection_z1.py -data=<datafile.dzn> -parser=CommunityDetection_ParserZ.py

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-66158-2_31
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn17
"""

from pycsp3 import *

m, together, separate, graph, W = data  # m is the maximum number of searched communities
n = len(graph)  # number of nodes

# x[i] is the community of the ith node
x = VarArray(size=n, dom=range(m))

# z is the weighted sum of nodes belonging to the same communities
z = Var(range(sum(W[i][j] for i in range(n) for j in range(i)) + 1))

satisfy(
    # considering nodes that must belong to the same community
    [x[i - 1] == x[j - 1] for i, j in together],

    # considering nodes that must not belong to the same community
    [x[i - 1] != x[j - 1] for i, j in separate],

    # tag(symmetry-breaking)
    Precedence(x),

    # computing z
    z == Sum((x[i] == x[j]) * W[i][j] for i in range(n) for j in range(i))
)

maximize(
    # maximizing (an expression of) z
    2 * z + sum(W[i][i] for i in range(n))
)

""" Comments
1) Precedence(x) is equivalent to Precedence(x, values=range(maxCommunities))

2) the Cardinality constraint is not useful at all (at least, as expressed in the original MZN model)
   Cardinality(x, occurrences={v: range(n + 1) for v in range(maxCommunities)})
"""
