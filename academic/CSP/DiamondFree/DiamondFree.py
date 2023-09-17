"""

This is the [problem 050](https://www.csplib.org/Problems/prob050/) of the CSPLib. You can find a short description
below:

Given a graph with set n vertices. The problem is produce all unique degree sequences $d_1,...d_n$, such that

 - $d_i\geq d_i+1$
 - each degree $d_i>0$
 - and $d_i$ is modulo 3
 - the sum of the degrees is modulo 12
 - there exists a simple diamond-free graph with that degree sequence, i.e.  for every set of four vertices the number of edges between those vertices is at most four.

### Example

For n=9, a solution is
```
  6 6 6 3 3 3 3 3 3   # the degree of vertices

  0 0 0 1 1 1 1 1 1
  0 0 0 1 1 1 1 1 1
  0 0 0 1 1 1 1 1 1
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
  1 1 1 0 0 0 0 0 0
```

A representation of the graph is here:

![diamondfree](https://pycsp.org/assets/figures/diamondfree.png)

## Data
A number n, the number of nodes of the graph.

## Model(s)

constraints: Sum, Intension, Decreasing, LexIncreasing

## Command Line

python DiamondFree.py
python DiamondFree.py -data=10

## Tags
 academic
"""

from pycsp3 import *

n = data or 8

# x is the adjacency matrix
x = VarArray(size=[n, n], dom=lambda i, j: {0, 1} if i != j else {0})

# y[i] is the degree of the ith node
y = VarArray(size=n, dom={i for i in range(1, n) if i % 3 == 0})

# s is the sum of all degrees
s = Var(dom={i for i in range(n, n * (n - 1) + 1) if i % 12 == 0})

satisfy(
    # ensuring the absence of diamond in the graph
    [Sum(x[i][j], x[i][k], x[i][l], x[j][k], x[j][l], x[k][l]) <= 4 for i, j, k, l in combinations(n, 4)],

    # ensuring that the graph is undirected (symmetric)
    [x[i][j] == x[j][i] for i, j in combinations(n, 2)],

    # computing node degrees
    [Sum(x[i]) == y[i] for i in range(n)],

    # computing the sum of node degrees
    Sum(y) == s,

    # tag(symmetry-breaking)
    [Decreasing(y), LexIncreasing(x)]
)
