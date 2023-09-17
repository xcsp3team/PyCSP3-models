# Problem Bibd
## Description


This is the [problem 28](http://www.csplib.org/Problems/prob028) of the CSPLib:

Balanced Incomplete Block Design (BIBD) generation is a standard combinatorial problem from design theory, originally used in the design of
statistical experiments but since finding other applications such as cryptography.
It is a special case of Block Design, which also includes Latin Square problems.
BIBD generation is described in most standard textbooks on combinatorics.
A BIBD is defined as an arrangement of $v$ distinct objects into $b$ blocks such that each block contains exactly $k$ distinct objects,
each object occurs in exactly $r$ different blocks, and every two distinct objects occur together in exactly $\lambda$ blocks.
Another way of defining a BIBD is in terms of its incidence matrix, which is a $v$ by $b$ binary matrix with exactly $r$ ones per row, $k$ ones per column, and with a scalar product of $\lambda$ between any pair of distinct rows.
A BIBD is therefore specified by its parameters $(v,b,r,k,\lambda)$.




### Example

An example of a solution for (7,7,3,3,1) is:
```
    0 1 1 0 0 1 0
    1 0 1 0 1 0 0
    0 0 1 1 0 0 1
    1 1 0 0 0 0 1
    0 0 0 0 1 1 1
    1 0 0 1 0 1 0
    0 1 0 1 1 0 0
```

## Data
Data is specified by a list \[$v$,$b$,$r$,$k$,$\lambda$], corresponding to:
 - $v$: the number of objects
 - $b$: the number of blocks
 - $k$: the number of distinct objects per block
 - $r$: each object occurs in exactly $r$ different blocks
 - every two distinct objects occur together in exactly $\lambda$ blocks


## Model(s)

There are two variants:
 - a main variant
 - another one (called aux) with auxiliary variables.

You can also find a step-by-step modeling process in this [Jupyter notebook](https://pycsp.org/documentation/models/CSP/Bibd/).

  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum), [LexIncreasing](http://pycsp.org/documentation/constraints/LexIncreasing)



## Command Line

```
python Bibd.py
python Bibd.py -data=[9,0,0,3,9]
python Bibd.py -data=[9,0,0,3,9] -variant=aux
```

## Tags
 academic notebook
