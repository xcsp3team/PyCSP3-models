# Problem Dubois

## Description
This problem has been conceived by Olivier Dubois, and submitted to the second DIMACS Implementation Challenge.
Dubois's generator produces contradictory 3-SAT instances that seem very difficult to be solved by any general method.
Given an integer n, called the degree, Dubois's process allows us to construct a 3-SAT contradictory instance with 3 * n variables and 2 * n clauses,
each of them having 3 literals.


## Data
A number n, each clause of the problem has 3\*n variables and 2\*n clauses.

## Model(s)

A model can be found in this [GitHub page](https://github.com/xcsp3team/pycsp3/blob/master/problems/csp/academic/Dubois.py).


*Involved Constraints*: [Extension](https://pycsp.org/documentation/constraints/Extension/).



## Command Line


```shell
  python3 Dubois.py
  python3 Dubois.py -data=10
 ```

## Some Results

| Data | Number of Solutions |
|------|---------------------|
| 8    | 0                   | 
| 10   | 0                   | 
| 15   | 0                   | 
