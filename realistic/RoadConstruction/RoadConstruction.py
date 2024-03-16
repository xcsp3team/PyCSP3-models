"""
Road construction problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2014 Minizinc challenge.
The MZN model was proposed by Rehan Abdul Aziz.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  09.json

## Model
  constraints: Minimum, Sum, Table

## Execution
  python RoadConstruction.py -data=<datafile.json>
  python RoadConstruction.py -data=<datafile.dzn> -parser=RoadConstruction_ParserZ.py

## Links
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  realistic, mzn14, mzn17
"""

from pycsp3 import *

budget, distances, costs = data
n = len(distances)

M = 1000000

# x[i][j][k] is the smallest distance between nodes i and j, computed after k reasoning steps
x = VarArray(size=[n, n, n], dom=lambda i, j, k: range(M + 1) if i < j else None)

# y[i][j] is 1 if a road is constructed between nodes i and j
y = VarArray(size=[n, n], dom=lambda i, j: {0, 1} if i < j else None)

satisfy(
    # initially computing the smallest distance between pairs of nodes
    [
        (x[i][j][0], y[i][j]) in {(M, 0), (distances[i][j], 1)} for i, j in combinations(n, 2)
    ],

    # iteratively computing the smallest distance between pairs of nodes
    [
        x[i][j][s + 1] == Minimum(
            x[i][j][s], [x[i][k][s] + x[min(j, k)][max(j, k)][s] for k in range(i + 1, n) if j != k]
        ) for i, j in combinations(n, 2) for s in range(n - 1)
    ],

    # not exceeding the budget
    Sum(
        costs[i][j] * y[i][j] for i, j in combinations(n, 2)
    ) <= budget
)

minimize(
    # minimizing the distance between pairs of nodes
    Sum(x[i][j][-1] for i, j in combinations(n, 2))
)

"""
1) One should be able to compute M from data instead of the arbitrary value of M
"""
