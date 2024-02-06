# Problem Superpermutation

In combinatorial mathematics, a superpermutation on n symbols is a string that contains each permutation of n symbols
as a substring. While trivial superpermutations can simply be made up of every permutation listed together,
superpermutations can also be shorter (except for the trivial case of n = 1) because overlap is allowed.
For instance, in the case of n = 2, the superpermutation 1221 contains all possible permutations (12 and 21),
but the shorter string 121 also contains both permutations.

It has been shown that for 1 ≤ n ≤ 5, the smallest superpermutation on n symbols has length 1! + 2! + ... + n!.
The first four smallest superpermutations have respective lengths 1, 3, 9, and 33, forming the strings 1, 121,
123121321, and 123412314231243121342132413214321.
However, for n = 5, there are several smallest superpermutations having the length 153.

## Data
  An integer n

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
  - python Superpermutation.py -data=number
  - python Superpermutation.py -data=number -variant=table

## Links
  - https://en.wikipedia.org/wiki/Superpermutation
  - https://www.cril.univ-artois.fr/XCSP22/competitions/csp/csp

## Tags
  academic, xcsp22
