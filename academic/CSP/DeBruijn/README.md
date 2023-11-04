# Problem DeBruijn
## Description
In combinatorial mathematics, a de Bruijn sequence of order n on an alphabet A of size b is a cyclic sequence
in which every possible length-n string on A occurs exactly once as a substring.

## Data
  a pair (b,n) of integer values

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Minimum](http://pycsp.org/documentation/constraints/Minimum), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
  python Debruijn.py -data=[number,number]

## Links
  - https://en.wikipedia.org/wiki/De_Bruijn_sequence
  - http://www.hakank.org/common_cp_models/#debruijn
  - https://www.minizinc.org/challenge2008/results2008.html

## Tags
  academic, mzn08
