"""
Constrained Community Detection Problem

The problem is to find communities in a graph with maximum modularity value while satisfying the fact that some pairs of nodes must be assigned
to same or different communities.
See CP paper cited below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2021 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  n050-e2500-s10-d5-c4-p90.json

## Model
  constraints: Precedence, Sum

## Execution
  python CommunityDetection.py -data=<datafile.json>

## Links
  - https://link.springer.com/chapter/10.1007/978-3-319-66158-2_31
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  realistic, notebook, mzn21
"""

from pycsp3 import *

graph, m, together, separate = data or load_json_data("n050-e2500-s10-d5-c4-p90.json")  # m is the maximum number of searched communities
n = len(graph)  # number of nodes


def modularity_matrix():
    degrees = [sum(graph[i]) for i in range(n)]  # node degrees
    sum_degrees = sum(degrees)  # multiplier used to avoid fractions
    return [[sum_degrees * graph[i][j] - degrees[i] * degrees[j] for j in range(n)] for i in range(n)]


W = modularity_matrix()

# x[i] is the community of the ith node
x = VarArray(size=n, dom=range(m))

satisfy(
    # considering nodes that must belong to the same community
    [x[i - 1] == x[j - 1] for i, j in together],

    # considering nodes that must not belong to the same community
    [x[i - 1] != x[j - 1] for i, j in separate],

    # tag(symmetry-breaking)
    Precedence(x)
)

maximize(
    # maximizing the weighted sum of nodes belonging to the same communities
    Sum((x[i] == x[j]) * W[i][j] for i, j in combinations(n, 2) if W[i][j] != 0)
)

""" Comments
1) Precedence(x) is equivalent to Precedence(x, values=range(m))
2) The Cardinality constraint (not posted here) is not useful at all:
   Cardinality(x, occurrences={v: range(n + 1) for v in range(maxCommunities)})
3) The heuristic chs is efficient with symmetry-breaking 
"""
