"""
Time-changing Graph Coloring Problem.

The problem is to minimize the number of steps for converting an initial coloring to an end coloring
by applying at most "k" changes of colors at each step, while always maintaining a valid coloring.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2017 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  k05-05.json

## Model
  constraints: Count, Sum

## Execution
  python TimeChangingGraphColoring.py -data=<datafile.json>
  python TimeChangingGraphColoring.py -data=<datafile.dzn> -parser=TimeChangingGraphColoring_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2017/results2017.html

## Tags
  real, mzn17
"""

from pycsp3 import *

k, edges, initial_coloring, final_coloring = data
n, m = len(initial_coloring), len(edges)  # n is the number of nodes, and m is the number of edges

nColors = max(max(initial_coloring), max(final_coloring)) + 1
nSteps = 10

# x[t][i] is the color of node i at time t
x = VarArray(size=[nSteps, n], dom=range(nColors))

# z is the number of steps to to convert the initial coloring into the end coloring by applying at most 'k' changes of colors
# at each step, while always maintaining a valid coloring.
z = Var(dom=range(1, nSteps))

satisfy(
    # setting the initial coloring
    x[0] == initial_coloring,

    # setting the final coloring
    x[z] == final_coloring,

    # ensuring a valid coloring at each step
    [x[t][a] != x[t][b] for t in range(nSteps) for (a, b) in edges],

    # ensuring a valid change from one step to the next one
    [
        If(
            t < z,
            Then=Sum(x[t][i] != x[t + 1][i] for i in range(n)) <= k,
            Else=x[t] == x[t + 1]
        ) for t in range(nSteps - 1)
    ]
)

minimize(
    (k * nSteps + 1) * (z + 1) + Sum(Hamming(x[t], x[t + 1]) for t in range(nSteps - 1))
)

"""
1) Sum(Hamming(x[t], x[t + 1]) for t in range(nSteps - 1)
is equivalent to:
 Sum(x[t][i] != x[t + 1][i] for t in range(nSteps - 1) for i in range(n))
2) with a good assumption, as in:
  java ace TimeChangingGraphColoring-k10_34.xml -ub=434
 the instance is closed in a few seconds
"""
