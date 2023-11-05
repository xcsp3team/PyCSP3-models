"""
Steiner Tree Problem: find a tree in a graph containing all the "terminal" nodes while minimizing its weight.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2018 Minizinc challenge.
The MZN model was proposed by Diege de Una.
No Licence was explicitly mentioned (so, MIT Licence is currently assumed).

## Data Example
  es10fst03.json

## Model
  constraints: Count, Sum

## Execution
  python SteinerTree.py -data=<datafile.json>
  python SteinerTree.py -data=<datafile.dzn> -parser=SteinerTree_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2018/results2018.html

## Tags
  real, mzn18
"""

from pycsp3 import *

endNodes, terminals, weights = data
n, m = len(endNodes[0]), len(endNodes)

pairs = [[i for i in range(n) if endNodes[e][i]] for e in range(m)]
fr = [min(pairs[e]) for e in range(m)]
to = [max(pairs[e]) for e in range(m)]
dfr = fr + to  # duplicated fr
dto = to + fr  # duplicated to

NO = n  # for indicating "no parent"

# x[i] is 1 if the ith node is selected (part of the tree)
x = VarArray(size=n, dom={0, 1})

# y[j] is 1 if the ith edge is selected (part of the tree)
y = VarArray(size=m, dom={0, 1})

# dy[k] is 1 if the kth duplicated edge is selected
dy = VarArray(size=2 * m, dom={0, 1})

# dst[i] is the distance of the ith node wrt the root
dst = VarArray(size=n, dom=range(n))

# prt[i] is the parent of the ith node (or special value n)
prt = VarArray(size=n, dom=range(n + 1))

# the node being the tree root
root = Var(dom=range(n))

satisfy(
    # all terminal nodes must be part of the tree
    [x[i] == 1 for i in terminals],

    # the number of edges in the tree is one less than the number of nodes (ensuring that all nodes are connected to each other)  tag(redundant-constraint)
    Sum(x) - Sum(y) == 1,

    # ensuring that the selected directed edges agree with undirected edges
    [y[e] == dy[e] | dy[m + e] for e in range(m)],

    # there is a root, at distance 0 and with no parent
    [
        x[root] == 1,
        dst[root] == 0,
        prt[root] == NO,
    ],

    # non-selected nodes have no parent, and are at distance 0 ; selected nodes have a parent (except the root)
    [
        If(
            x[i] == 0,
            Then=[
                prt[i] == NO,
                dst[i] == 0
            ],
            Else=If(i != root, Then=prt[i] != NO)
        ) for i in range(n)
    ],

    # each node with a parent is selected as well as its parent, is 1 unit distant from its parent, and involves some edges being selected
    [
        If(
            prt[i] != NO,
            Then=[
                x[i],
                x[prt[i]],
                dst[i] == dst[prt[i]] + 1,
                Exist(
                    both(
                        dy[e],
                        dfr[e] == prt[i]
                    )
                    for e in range(2 * m) if dto[e] == i
                )
            ]
        ) for i in range(n)
    ],

    # each selected edge must be part of the parent relation
    [
        If(
            dy[e] == 1,
            Then=prt[dto[e]] == dfr[e]
        ) for e in range(2 * m)
    ],

    # redundant relationship of trees
    Sum(x) - Sum(dy) == 1,

    # ensuring coherence between duplicated edges and nodes
    (
        If(
            dy[e],
            Then=[
                x[dfr[e]],
                x[dto[e]]
            ]
        ) for e in range(2 * m)
    )
)

minimize(
    # minimizing weighted selected edges
    weights * y
)

"""
1) It is better to write Sum(x) - Sum(y) == 1 than Sum(x) == Sum(y) + 1 because it avoids the introduction of auxiliary variables
In the future, we may avoid that (when compiling).
"""
