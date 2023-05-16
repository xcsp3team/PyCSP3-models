
# Problem Opd

## Description
This is the [problem 065](https://www.csplib.org/Problems/prob065/) of the CSPLib:

An OPD problem ⟨v,b,r⟩ is to find a matrix of v rows and b columns of 0-1 values such that each row sums to r, 
and the maximum, denoted $\lambda$, of the dot products beween all pairs of distinct rows is minimal. 
Equivalently, the objective is to find v subsets of cardinality r drawn from a given set of b elements, 
such that the largest intersection of any two of the v sets has minimal cardinality, denoted $\lambda$.

### Example
The optimum for \[4,4,4] is 4 and a solution is 

```
    1 1 1 1 
    1 1 1 1 
    1 1 1 1 
    1 1 1 1  
```


## Data
A triplet \[v,b,r] as defined above.

## Model(s)


There are two variants, one with auxilliary variables, one without.

*Involved Constraints*: [Intension](https://pycsp.org/documentation/constraints/Intension/), [LexIncreasing](https://pycsp.org/documentation/constraints/LexIncreasing/), [Sum](https://pycsp.org/documentation/constraints/Sum/).


## Command Line

```
python Opd.py
python Opd.py -data=[4,6,4]
python Opd.py -data=[4,6,4] -variant=aux
```

## Some Results



| Data     | Optimum |
|----------|---------|
| \[4,4,4] | 4       |
| \[4,6,4] | 3       |
| \[6,7,6] | 5       |
