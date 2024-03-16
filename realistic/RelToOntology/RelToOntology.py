"""
The Relational-To-Ontology Mapping Problem is viewed here as a Steiner Tree Problem with side constraints.
See IJCAI paper below.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  3-09.json

## Model
  constraints: AllDifferent, Count, Element

## Execution
  python RelToOntology.py -data=<datafile.json>
  python RelToOntology.py -data=<datafile.dzn> -parser=RelToOntology_ParserZ.py

## Links
  - https://www.ijcai.org/proceedings/2018/0178.pdf
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  realistic, mzn17
"""

from pycsp3 import *

attributes, adjacency, dnodes, anodes, edges = data
tails, heads, edgeCosts = zip(*edges)
nAttributes, n, m = len(attributes), len(adjacency), len(edges)

match_lb, match_ub = min(min(domain) for (domain, _) in attributes), max(max(domain) for (domain, _) in attributes)
matrix = cp_array([next((e for e in range(m) if adjacency[i][e] == 1 and adjacency[j][e] == 1), -1) for j in range(n)] for i in range(n))


def possible_parents(i):
    return sorted(list({heads[j] if tails[j] == i else tails[j] for j in range(m) if adjacency[i][j] == 1}))


# x[i] is 1 if the ith node is selected in the tree
x = VarArray(size=n, dom={0, 1})

# y[j] is 1 if the jth edge is selected in the tree
y = VarArray(size=m, dom={0, 1})

# match[k] is the node associated with the kth attribute
match = VarArray(size=nAttributes, dom=range(match_lb, match_ub + 1))

# p[i] is the parent of the ith node
p = VarArray(size=n, dom=range(n))

root = Var(dom=range(n))

satisfy(
    # some attributes must be in the tree
    [x[i] == 1 for i in anodes],

    # enforcing treeness
    [
        [
            If(
                y[j],
                Then=[
                    x[tails[j]],
                    x[heads[j]]]
            ) for j in range(m)
        ],
        x[root] == 1,
        p[root] == root,
        [
            If(
                root != i, x[i] != 0,
                Then=[
                    p[i] in possible_parents(i),
                    y[matrix[i][p[i]]] == 1,
                    x[p[i]] == 1,
                    p[p[i]] != i
                ]
            ) for i in range(n)
        ],
        [
            If(
                x[i] == 0,
                Then=p[i] == i
            ) for i in range(n)
        ]
    ],

    # matching problem
    [
        [match[k] in attributes[k].domain for k in range(nAttributes)],

        [x[match[k]] == 1 for k in range(nAttributes)],

        AllDifferent(match)
    ],

    # matched nodes are in the tree
    [x[i] == Exist(match[k] == i for k in range(nAttributes)) for i in dnodes],

    # only one edge coming out of the match
    [x[i] == ExactlyOne(y[j] for j in range(m) if adjacency[i][j] == 1) for i in dnodes]
)

minimize(
    y * edgeCosts
    + Sum(
        matchCost[match[k]] for k, (_, matchCost) in enumerate(attributes)
    )
)

"""
1) Some groups of constraints might be advantageously posted using table constraints
"""
