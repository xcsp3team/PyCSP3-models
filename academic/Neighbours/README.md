# Problem Neighbours

From the IBM Challenge "Ponder This".

There are people living in the separate squares of a rectangular grid.
Each resident's neighbours are those who live in the squares that have a common edge with that resident's square.
Each resident of the grid is assigned a natural number k in the range 1..5
with the condition that the numbers 1, 2, ..., k-1 are present in the squares of his/her neighbors.
Find a configuration (assignment of numbers) of all neighbours, so that the sum of their numbers are maximised.

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
The original MZN model was proposed by Peter J. Stuckey, with a Licence that sems to be like a MIT Licence.

## Data
  two integers (n,m)

## Model
  There are two variants:
    - a main one with intensional constraints,
    - a 'table" variant with extensional constraints

  Constraints: Count, Lex, Sum, Table

## Execution
```
  python Neighbours.py -data=[number,number]
```

## Links
  - https://research.ibm.com/haifa/ponderthis/challenges/December2012.html
  - https://www.minizinc.org/challenge2021/results2021.html

## Tags
  academic, mzn18, mzn21
