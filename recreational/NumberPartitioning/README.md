# Problem NumberPartitioning
## Description
This problem consists in finding a partition of the set of numbers {1, 2, ..., n} into two sets A and B such that:
  - A and B have the same cardinality
  - the sum of numbers in A is equal to the sum of numbers in B
  - the sum of squares of numbers in A is equal to the sum of squares of numbers in B
See Problem 049 on CSPLib.

## Data
  an integer n

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python NumberPartitioning.py -data=[number]

## Links
  - https://www.csplib.org/Problems/prob049/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
