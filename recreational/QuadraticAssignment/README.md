# Problem: QuadraticAssignment

The Quadratic Assignment Problem (QAP) has remained one of the great challenges in combinatorial optimization (from QAPLIB).

## Data Example
  example.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Sum](https://pycsp.org/documentation/constraints/Sum), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python QuadraticAssignment.py -data=<datafile.json>
  python QuadraticAssignment.py -data=<datafile.txt> -parser=QuadraticAssignment_Parser.py
```

## Links
  - https://en.wikipedia.org/wiki/Quadratic_assignment_problem
  - https://coral.ise.lehigh.edu/data-sets/qaplib/

## Tags
  recreational
