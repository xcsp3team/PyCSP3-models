# Problem AztecDiamond
## Description
An Aztec diamond of order n consists of 2n centered rows of unit squares, of respective lengths 2, 4, ..., 2n-2, 2n, 2n-2, ..., 4, 2.
An Aztec diamond of order n has exactly 2^(n*(n+1)/2) tilings by dominos.

It is easy to build a solution, but finding a random solution is more complex.
A CP model is interesting as one can easily add side constraints to form Aztec diamonds with some specific properties.

## Data
  A unique integer, the order of the diamond

## Model
  constraints: [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python AztecDiamond.py -data=number

## Links
  - https://en.wikipedia.org/wiki/Aztec_diamond
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  recreational, xcsp22
