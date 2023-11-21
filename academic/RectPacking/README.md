# Problem RectPacking
## Description
The rectangle (square) packing problem consists of n squares of size 1x1, 2x2, 3x3, ..., nxn,
to be put in an enclosing rectangle (container) without overlapping of the squares.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2009/2014 Minizinc challenges.
The MZN model has Copyright (C) 2009-2014 The University of Melbourne and NICTA.

## Data
  two integers (n,k)

## Model
  constraints: [Cumulative](http://pycsp.org/documentation/constraints/Cumulative), [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap)

## Execution
```
  python RectPacking.py -data=[number,number]
```

## Links
  - https://www.minizinc.org/challenge2014/results2014.html

## Tags
  academic, mzn09, mzn14
