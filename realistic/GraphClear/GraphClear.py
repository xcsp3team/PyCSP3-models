"""
Mobile robot graph-clear problem.

In a graph-clear problem, an undirected graph (N,E) with the node weight ai for each node i in N and the edge weight bij for each edge {i,j} in E is given.
In the beginning, all nodes are contaminated. In each step, one node can be made clean by sweeping it using ai robots and blocking each edge {i,j} using bij robots.
However, while sweeping a node, an already swept node becomes contaminated if it is connected by a path of unblocked edges to a contaminated node.
The optimal solution minimizes the maximum number of robots per step to make all nodes clean.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2024 Minizinc challenge.
For the original MZN model, no Licence was explicitly mentioned (MIT Licence assumed).
This MZN model was mentioned to be adapted from https://github.com/Kurorororo/didp-models/blob/main/graph-clear/graph_clear_cp.py

## Data Example
  n20-2022-14.json

## Model
  constraints: AllDifferent, Maximum, Sum

## Execution
  python GraphClear.py -data=<datafile.json>

## Links
  - https://robotics.ucmerced.edu/sites/g/files/ufvvjh1576/f/page/documents/iros2007c.pdf
  - https://link.springer.com/article/10.1007/s10601-018-9288-3
  - https://github.com/Kurorororo/didp-models/tree/main/graph-clear
  - https://www.minizinc.org/challenge/2024/results/

## Tags
  realistic, mzn24
"""

from pycsp3 import *

n, node_weights, edge_weights = data or load_json_data("n20-2022-14.json")

edges = [(i, j) for i in range(n) for j in range(n) if edge_weights[i][j] > 0]
m = len(edges)

c_block = sum(sum(row) for row in edge_weights)
c_sweep = max(node_weights[i] + sum(edge_weights[i][j] + edge_weights[j][i] for j in range(n)) for i in range(n))

var_t = VarArray(size=n, dom=range(n))
var_l = VarArray(size=m, dom=range(n))
var_u = VarArray(size=m, dom=range(n))
var_s = VarArray(size=n, dom=range(1, c_sweep + 1))
var_b = VarArray(size=n, dom=range(c_block + 1))
var_i = VarArray(size=[m, n], dom={0, 1})
var_z = Var(dom=range(1, max(node_weights) + c_block + 1))

satisfy(
    var_z == Maximum(var_s[i] + var_b[i] for i in range(n)),

    [
        If(
            var_t[i] == j,
            Then=var_s[j] == node_weights[i] + sum(edge_weights[i][k] + edge_weights[k][i] for k in range(n))
        ) for i in range(n) for j in range(n)
    ],

    AllDifferent(var_t),

    [
        If(
            var_t[i] < var_t[j],
            Then=[
                var_l[e] == var_t[i],
                var_u[e] == var_t[j]
            ]
        ) for e, (i, j) in enumerate(edges)
    ],

    [
        If(
            var_t[j] < var_t[i],
            Then=[
                var_l[e] == var_t[j],
                var_u[e] == var_t[i]
            ]
        ) for e, (i, j) in enumerate(edges)
    ],

    [
        If(
            var_l[e] <= t, var_u[e] >= t, var_t[i] != t, var_t[j] != t,
            Then=var_i[e][t] == 1
        ) for e, (i, j) in enumerate(edges) for t in range(n)
    ],

    [var_b[t] == Sum(edge_weights[i][j] * var_i[e][t] for e, (i, j) in enumerate(edges)) for t in range(n)]
)

minimize(
    var_z
)
