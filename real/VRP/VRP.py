"""
The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The MZN model was proposed by Jakob Puchinger.
No Licence was explicitly mentioned (MIT Licence assumed).

## Data Example
  A-n38-k5.json

## Model
  constraints: Count, Sum

## Execution
  python VRP.py -data=<datafile.json>
  python VRP.py -data=<datafile.dzn> -parser=VRP_ParserZ.py

## Links
  - https://en.wikipedia.org/wiki/Vehicle_routing_problem
  - https://www.minizinc.org/challenge2013/results2013.html

## Tags
  real, mzn09, mzn11, mzn12, mzn13
"""

from pycsp3 import *

capacity, demands, distances = data
n = len(demands)  # number of nodes (including 0 for the depot)
k = n - 1  # because n has been incremented in the parser

# x[i][j] is 1 iff the arc (i,j) is part of a route
x = VarArray(size=[n, n], dom=lambda i, j: {0} if i == j else {0, 1})

# u[i] is the vehicle load after visiting the ith node (used for subtour elimination)
u = VarArray(size=n, dom=lambda i: {0} if i == 0 else range(capacity + 1))

satisfy(
    # exactly one incoming arc for each node j other than the depot
    [Count(x[:, j], value=1) == 1 for j in range(1, n)],

    # exactly one outgoing arc for each node i other than the depot
    [Count(x[i], value=1) == 1 for i in range(1, n)],

    # no more than 'k' vehicles leaving the depot
    Sum(x[:, 0]) <= k,

    # no more than 'k' vehicles arriving to the depot
    Sum(x[0]) <= k,

    # Miller-Tucker-Zemlin subtour elimination
    [Sum(u[i], -u[j], capacity * x[i][j]) <= capacity - demands[j] for i in range(1, n) for j in range(1, n) if i != j],

    # satisfying demand at each node
    [u[i] >= demands[i] for i in range(1, n)]
)

minimize(
    x * distances
)

"""
1) Compared to the minizinc model, we avoid handling the trivial cases of x[i][i]
2) Note that:
  Sum(u[i], -u[j], capacity * x[i][j])
is equivalent to:
  [u[i], u[j], x[i][j]] * [1, -1, capacity] 


"""
