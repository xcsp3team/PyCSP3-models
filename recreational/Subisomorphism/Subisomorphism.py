"""
An instance of the subgraph isomorphism problem is defined by a pattern graph Gp = (Vp, Ep) and a target graph Gt = (Vt, Et):
the objective is to determine whether Gp is isomorphic to some subgraph(s) in Gt.

## Data Example
  A-01.json

## Model
  constraints: AllDifferent, Table

## Execution:
  python Subisomorphism.py -data=<datafile.json>

## Links
  - https://www.sciencedirect.com/science/article/pii/S0004370210000718

## Tags
  recreational, notebook
"""

from pycsp3 import *

n, m, p_edges, t_edges = data


def structures():
    both_way_table = {(i, j) for (i, j) in t_edges} | {(j, i) for (i, j) in t_edges}
    p_degrees = [len([edge for edge in p_edges if i in edge]) for i in range(n)]
    t_degrees = [len([edge for edge in t_edges if i in edge]) for i in range(m)]
    degree_conflicts = [{j for j in range(m) if t_degrees[j] < p_degrees[i]} for i in range(n)]
    return [i for (i, j) in p_edges if i == j], [i for (i, j) in t_edges if i == j], both_way_table, degree_conflicts


p_loops, t_loops, T, conflicts = structures()

# x[i] is the target node to which the ith pattern node is mapped
x = VarArray(size=n, dom=range(m))

satisfy(
    # ensuring injectivity
    AllDifferent(x),

    # preserving edges
    [(x[i], x[j]) in T for (i, j) in p_edges],

    # being careful of self-loops
    [x[i] in t_loops for i in p_loops],

    # tag(redundant-constraints)
    [x[i] not in C for i, C in enumerate(conflicts)]
)
