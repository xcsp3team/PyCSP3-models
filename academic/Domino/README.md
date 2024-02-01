# Problem Domino

This problem is described in the paper cited below.
Informally the Domino problem is an undirected constraint graph with a cycle and a trigger constraint.

## Data
  a pair (n,d), where n is the number of variables and d the size of the domain

## Model
  There are two variants: a main one and a variant 'table" with constraints in extension.

  constraints: [AllEqual](http://pycsp.org/documentation/constraints/AllEqual), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python Domino.py
  python Domino.py -data=[number,number]
  python Domino.py -data=[number,number] -variant=table
```

## Links
  - https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.103.1730&rep=rep1&type=pdf

## Tags
  academic
