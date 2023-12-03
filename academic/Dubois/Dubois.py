"""
This problem has been conceived by Olivier Dubois, and submitted to the second DIMACS Implementation Challenge.
Dubois's generator produces contradictory 3-SAT instances that seem very difficult to be solved by any general method.
Given an integer n, called the degree, Dubois's process allows us to construct a 3-SAT contradictory instance with 3 * n variables and 2 * n clauses,
each of them having 3 literals.

## Data
  A number n, each clause of the problem has 3*n variables and 2*n clauses.

## Model
  a model can be found in this jupyter notebook [GitHub page](https://github.com/xcsp3team/pycsp3/blob/master/problems/csp/academic/Dubois.py).

  constraints: Table

## Execution
  python Dubois.py -data=number

## Tags
  academic, notebook
"""
from pycsp3 import *

n = data or 8

T1 = {(0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1)}
T2 = {(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)}

x = VarArray(size=3 * n, dom={0, 1})

satisfy(
    (x[2 * n - 2], x[2 * n - 1], x[0]) in T1,

    [(x[i], x[2 * n + i], x[i + 1]) in T1 for i in range(n - 2)],

    [(x[n - 2 + i], x[3 * n - 2], x[3 * n - 1]) in T1 for i in range(2)],

    [(x[i], x[4 * n - 3 - i], x[i - 1]) in T1 for i in range(n, 2 * n - 2)],

    (x[2 * n - 2], x[2 * n - 1], x[2 * n - 3]) in T2
)
