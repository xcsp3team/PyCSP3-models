"""
An instance of the subgraph isomorphism problem is defined by a pattern graph Gp = (Vp, Ep) and a target graph Gt = (Vt, Et):
the objective is to determine whether Gp is isomorphic to some subgraph(s) in Gt.

## Data Example
  A-01.json

## Model
  constraints: AllDifferent, Table

## Execution:
  python Subisomorphism.py -data=<datafile.json>
  python Subisomorphism.py -parser=Subisomorphism_Parser.py -data=[filename1,filename2]

## Links
  - https://www.sciencedirect.com/science/article/pii/S0004370210000718
   - https://www.cril.univ-artois.fr/XCSP24/competitions/csp/csp

## Tags
  recreational, notebook, xcsp24
"""

from pycsp3 import *

n, m, pattern_edges, target_edges = data or load_json_data("A-01.json")  # n = nPatternNodes, m = nTargetNodes

# T = target_edges + [(j, i) for (i, j) in target_edges]

p_degrees = [len([edge for edge in pattern_edges if i in edge]) for i in range(n)]
t_degrees = [len([edge for edge in target_edges if i in edge]) for i in range(m)]

pattern_loops = [i for (i, j) in pattern_edges if i == j]
target_loops = [i for (i, j) in target_edges if i == j]

target_edges = target_edges + [(j, i) for (i, j) in target_edges]  # we add symmetric edges

# x[i] is the target node to which the ith pattern node is mapped
x = VarArray(size=n, dom=range(m))

satisfy(
    # ensuring injectivity
    AllDifferent(x),

    # preserving edges
    [(x[i], x[j]) in target_edges for (i, j) in pattern_edges],

    # being careful of self-loops
    [x[i] in target_loops for i in pattern_loops],

    # tag(redundant)
    [
        Table(
            scope=x[i],
            conflicts={j for j in range(m) if t_degrees[j] < p_degrees[i]}
        ) for i in range(n)
    ]
)
