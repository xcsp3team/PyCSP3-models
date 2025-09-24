# Problem: RamseyPartition

See http://www.mathematik.uni-bielefeld.de/~sillke/PUZZLES/partion3-ramsey

Partition the integers 1 to n into three sets, such that for no set are
there three different numbers with two adding to the third.
Given a grid containing some pairs of identical numbers, connect each pair of similar numbers by drawing a line sith horizontal or vertical segments,
while paying attention to not having crossed lines.

## Data Example
   two integers q and n

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [NValues](https://pycsp.org/documentation/constraints/NValues)

## Execution
```
  python RamseyPartition.py -data=[number,number]
  python RamseyPartition.py -data=[number,number] -variant=equ
```


## Links
  - http://www.mathematik.uni-bielefeld.de/~sillke/PUZZLES/partion3-ramsey
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  academic, xcsp25
