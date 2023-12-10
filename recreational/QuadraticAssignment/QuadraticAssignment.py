"""
The Quadratic Assignment Problem (QAP) has remained one of the great challenges in combinatorial optimization (from QAPLIB).

## Data
  example.json

## Model
  constraints: AllDifferent, Sum, Table

## Execution
  python QuadraticAssignment.py -data=QuadraticAssignment_qap.json
  python QuadraticAssignment.py -data=QuadraticAssignment_example.txt -dataparser=QuadraticAssignment_Parser.py

## Links
  - https://en.wikipedia.org/wiki/Quadratic_assignment_problem
  - https://coral.ise.lehigh.edu/data-sets/qaplib/

## Tags
  recreational
"""

from pycsp3 import *

weights, distances = data  # facility weights and location distances
all_distances = {d for row in distances for d in row}
n = len(weights)

table = {(i, j, distances[i][j]) for i in range(n) for j in range(n) if i != j}

# x[i] is the location assigned to the ith facility
x = VarArray(size=n, dom=range(n))

# d[i][j] is the distance between the locations assigned to the ith and jth facilities
d = VarArray(size=[n, n], dom=lambda i, j: all_distances if i < j and weights[i][j] != 0 else None)

satisfy(
    # all locations must be different
    AllDifferent(x),

    # computing the distances
    [(x[i], x[j], d[i][j]) in table for i, j in combinations(range(n), 2) if weights[i][j] != 0]
)

minimize(
    # minimizing summed up distances multiplied by flows
    d * weights
)

""" Comments
1) d * weights is possible because d is of type 'ListVar' and because None values (and associated coeffs) will be discarded

2) weights * d is also possible because weights is of type 'ListInt' and because None values (and associated coeffs) will be discarded

3) one can also write of course:
 Sum(d[i][j] * weights[i][j] for i, j in combinations(range(n), 2) if weights[i][j] != 0)

4) the model is only valid for symmetric instances (the obtained bound must then be multiplied by two)   
   TODO a more general model (for non systematically symmetric instances)
"""
