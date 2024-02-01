# Problem NumberPartitioning

This is [Problem 049](https://www.csplib.org/Problems/prob049/) at CSPLib.

This problem consists in finding a partition of the set of numbers {1, 2, ..., n} into two sets A and B such that:
  - A and B have the same cardinality
  - the sum of numbers in A is equal to the sum of numbers in B
  - the sum of squares of numbers in A is equal to the sum of squares of numbers in B

## Data
  An integer n

## Example
  A solution for n=8 : A = {1, 4, 6, 7} and B = {2,3,5,7}

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  - python NumberPartitioning.py -data=number

## Links
  - https://www.csplib.org/Problems/prob049/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, recreational, csplib, xcsp22
