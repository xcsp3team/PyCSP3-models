
# Problem Number Partitioning

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


*Involved Constraints*: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent/), [Increasing](https://pycsp.org/documentation/constraints/Increasing/),
[Intension](https://pycsp.org/documentation/constraints/Intension/)
[Sum](https://pycsp.org/documentation/constraints/Sum/).



## Command Line


```shell
  python NumberPartitioning.py
  python NumberPartitioning.py -data=10
 ```

## Some Results

| Data | Number of Solutions |
|------|---------------------|
| 6    | 0                   |
| 8    | 1                   |
| 10   | 0                   |
