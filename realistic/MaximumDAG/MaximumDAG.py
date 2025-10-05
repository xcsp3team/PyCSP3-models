"""
Maximum Directed Acyclic Graph.
Given a directed graph G=(V,E) find the subgraph of G that is a DAG, while maximizing the number of edges.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2016 challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  25-01.json

## Model
  constraints: Maximum, Sum

## Execution
  python MaximumDAG.py -data=<datafile.json>
  python MaximumDAG.py -data=<datafile.dzn> -parser=MaximumDAG_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2016/results2016.html

## Tags
  realistic, mzn16
"""

from pycsp3 import *

tails, incidence_matrix = data or load_json_data("25-01.json")

n, m = len(incidence_matrix), len(tails)

# x[j] is 1 iff the jth edge is selected to be in the DAG
x = VarArray(size=m, dom={0, 1})

# d[i] is the distance of the ith node with respect to the root
d = VarArray(size=n, dom=range(m + 1))

satisfy(
    # root node (0) is at distance 0
    d[0] == 0,

    # computing other distances
    [
        d[i] == Maximum(
            (d[tails[j]] + 1) * x[j] for j in range(m) if incidence_matrix[i][j] == 1
        ) for i in range(1, n)
    ]
)

maximize(
    # maximizing the number of edges in the DAG
    Sum(x)
)
