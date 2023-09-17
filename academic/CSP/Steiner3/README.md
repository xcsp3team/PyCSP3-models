# Problem Steiner3
## Description
This is the [problem 044](https://www.csplib.org/Problems/prob044/) of the CSPLib:

"*The ternary Steiner problem of order n consists of finding a set of n.(n−1)/6 triples of distinct integer
elements in {1...n} such that any two triples have at most one common element.*"


### Example
A solution for n=7 is

((1, 2, 3), (1, 4, 5), (1, 6, 7), (2, 4, 6), (2, 5, 7), (3, 4, 7), (3, 5, 6))

## Data
A number n, the number of integers.

## Model(s)

  constraints: [Increasing](http://pycsp.org/documentation/constraints/Increasing), [Extension](http://pycsp.org/documentation/constraints/Extension)

## Command Line
```
python Steiner3.py
python Steiner3.py -data=6
```

## Tags
 academic
