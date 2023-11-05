# Problem CostasArray_z
## Description
An order-n Costas array is a permutation on {1,...,n} such that the distances in each row of the triangular difference table are distinct.
For example, the permutation {1,3,4,2,5} has triangular difference table {2,1,-2,3}, {3,-1,1}, {1,2}, and {4}.
Since each row contains no duplications, the permutation is therefore a Costas array.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2010/2011/2015 Minizinc challenges.
The MZN model was proposed by Barry O'Sullivan (Cork Constraint Computation Centre, Ireland).
No Licence was explicitly mentioned (MIT Licence assumed).

## Data
  a number n

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent)

## Execution
  python CostasArray_z.py -data=[number]

## Links
  - https://mathworld.wolfram.com/CostasArray.html
  - https://www.minizinc.org/challenge2015/results2015.html

## Tags
  academic, mzn10, mzn11, mzn15
