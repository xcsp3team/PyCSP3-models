# Problem NumberPartitioning
## Description
This is the [problem 049](https://www.csplib.org/Problems/prob049/) of the CSPLib:

This problem consists in finding a partition of numbers 1...n  into two sets A and B such that:
 - A and B have the same cardinality
 - sum of numbers in A = sum of numbers in B
 - sum of squares of numbers in A = sum of squares of numbers in B

### Example

A solution for n=8 : A = {1, 4, 6, 7} and B = {2,3,5,7}

## Data
A number n.

## Model(s)
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Increasing](http://pycsp.org/documentation/constraints/Increasing), [Intension](http://pycsp.org/documentation/constraints/Intension), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Command Line
```
  python NumberPartitioning.py
  python NumberPartitioning.py -data=10
```

## Tags
 academic csplib
