"""
The problem is to find communities in a graph with maximum modularity value while satisfying the fact that some pairs of nodes must be assigned
to same or different communities.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

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
  realistic, mzn17, mzn24
"""

from pycsp3 import *

assert not variant() or variant("mzn24")

m, together, separate, graph, W = data or load_json_data("strike-s2-k8.json")  # m is the maximum number of searched communities

n = len(graph)  # number of nodes


def domain_z():
    if not variant():
        return range(sum(W[i][j] for i, j in combinations(n, 2)) + 1)
    return range(sum(W[i][j] for i, j in combinations(n, 2) if W[i][j] < 0), sum(W[i][j] for i, j in combinations(n, 2) if W[i][j] > 0) + 1)  # for mzn24


# x[i] is the community of the ith node
x = VarArray(size=n, dom=range(m))

# z is the weighted sum of nodes belonging to the same communities
z = Var(dom=domain_z)

satisfy(
    # considering nodes that must belong to the same community
    [x[i - 1] == x[j - 1] for i, j in together],

    # considering nodes that must not belong to the same community
    [x[i - 1] != x[j - 1] for i, j in separate],

    # tag(symmetry-breaking)
    Precedence(x),

    # computing z
    z == Sum((x[i] == x[j]) * W[i][j] for i, j in combinations(n, 2))
)

maximize(
    # maximizing (an expression of) z
    2 * z + sum(W[i][i] for i in range(n))
)

""" Comments
1) Precedence(x) is equivalent to Precedence(x, values=range(maxCommunities))

2) The Cardinality constraint is not useful at all (at least, as expressed in the original MZN model)
   Cardinality(x, occurrences={v: range(n + 1) for v in range(maxCommunities)})
"""
