"""
Diameter Constrained Minimum Spanning Tree.
Given an undirected graph G=(V,E) and an integer k find a spanning tree of G of minimum cost such that its diameter is not greater than k.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016/2022 Minizinc challenges.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  s-v20-a50-d4.json

## Model
  constraints: Sum

## Execution
  python DC_MST.py -data=<datafile.json>
  python DC_MST.py -data=<datafile.dzn> -parser=DC_MST_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2022/results2022.html

## Tags
  realistic, mzn16, mzn22
"""

from pycsp3 import *

diameter, edges, n, weights = data
radius, m = diameter // 2, len(weights)
assert n <= m

# x[j] is 1 iff the jth edge belongs to the tree
x = VarArray(size=m, dom={0, 1})

# h[i] is the height of the ith node
h = VarArray(size=n, dom=range(radius + 1))

# p[i] is the parent of the ith node
p = VarArray(size=n, dom=range(n))

# r is the root of the tree
r = Var(dom=range(m))

satisfy(
    # ensuring n-1 edges
    Sum(x) == n - 1
)

if diameter % 2 == 1:
    # ra is the node root a
    ra = Var(dom=range(n))

    # rb is the node root b
    rb = Var(dom=range(n))

    satisfy(
        # linking edge and node roots
        [
            ra == edges[r][0],
            rb == edges[r][1]
        ],

        # tag(symmetry-breaking)
        ra < rb,

        # ensuring the edge root is selected
        [
            (
                If(ra == a, rb == b, Then=x[j] == 1),
                If(rb == a, ra == b, Then=x[j] == 1)
            ) for j, (a, b) in enumerate(edges)
        ],

        # setting special values for node roots
        [
            [h[ra] == 0, h[rb] == 0],
            [p[ra] == ra, p[rb] == rb]
        ],

        # constraining the height of nodes that are not roots
        [
            If(
                ra != i, rb != i,
                Then=[
                    h[i] > 0,
                    h[i] == h[p[i]] + 1
                ]
            ) for i in range(n)
        ],

        #  computing heights and parents of nodes
        [((h[a] == 0) & (h[b] == 0)) | (x[j] == 0) | ((h[a] == h[b] + 1) & (p[a] == b)) | ((h[b] == h[a] + 1) & (p[b] == a)) for j, (a, b) in enumerate(edges)]
    )

else:
    satisfy(
        # ensuring that the root is a node
        r < n,

        # setting special values for the root
        [h[r] == 0, p[r] == r],

        #  constraining the height of nodes that are not roots
        [
            If(
                r != i,
                Then=[
                    h[i] > 0,
                    h[i] == h[p[i]] + 1
                ]
            ) for i in range(n)
        ],

        #  computing heights and parents of nodes
        [(x[j] == 0) | ((h[a] == h[b] + 1) & (p[a] == b)) | ((h[b] == h[a] + 1) & (p[b] == a)) for j, (a, b) in enumerate(edges)]
    )

pairs = [(a1, b1, a2, b2) for j1, (a1, b1) in enumerate(edges) for j2, (a2, b2) in enumerate(edges) if weights[j1] < weights[j2]]

satisfy(
    # edge e1 dominated by edge e2 in all the following situations  tag(redundant)
    [
        [If(h[b1] <= h[b2], Then=p[a1] != b2) for a1, b1, a2, b2 in pairs if a1 == a2],
        [If(h[a1] <= h[a2], Then=p[b1] != a2) for a1, b1, a2, b2 in pairs if b1 == b2],
        [If(h[b1] <= h[a2], Then=p[a1] != a2) for a1, b1, a2, b2 in pairs if a1 == b2]
    ],

    # linking parenthood and edges  tag(redundant)
    [
        (
            If(p[a] == b, Then=x[j] == 1),
            If(p[b] == a, Then=x[j] == 1)
        ) for j, (a, b) in enumerate(edges)
    ]
)

minimize(
    # minimizing the weighted tree
    x * weights
)
