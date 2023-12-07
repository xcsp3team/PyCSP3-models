# Problem Dubois
## Description
This problem has been conceived by Olivier Dubois, and submitted to the second DIMACS Implementation Challenge.
Dubois's generator produces contradictory 3-SAT instances that seem very difficult to be solved by any general method.
Given an integer n, called the degree, Dubois's process allows us to construct a 3-SAT contradictory instance with 3 * n variables and 2 * n clauses,
each of them having 3 literals.


## Data
A number n, each clause of the problem has 3\*n variables and 2\*n clauses.

## Model(s)

A model can be found in this jupyter notebook [GitHub page](https://github.com/xcsp3team/pycsp3/blob/master/problems/csp/academic/Dubois.py).


  constraints: [Extension](http://pycsp.org/documentation/constraints/Extension)

## Command Line
```
  python3 Dubois.py
  python3 Dubois.py -data=10
```

## Tags
 academic notebook