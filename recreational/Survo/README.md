# Problem Survo
## Description
In a Survo puzzle, the task is to fill an m × n table with integers 1, 2, ..., m·n
so that each of these numbers appears only once and their row and column sums
are equal to integers given on the bottom and the right side of the table.
Often some of the integers are given readily in the table in order to guarantee
uniqueness of the solution and/or for making the task easier.

## Data Example
  01.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution:
```
  python Survo.py -data=<datafile.json>
```

## Links
 - https://en.wikipedia.org/wiki/Survo_puzzle

## Tags
  recreational
