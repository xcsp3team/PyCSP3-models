# Problem QuadraticAssignment
## Description
The Quadratic Assignment Problem (QAP) has remained one of the great challenges in combinatorial optimization (from QAPLIB).

## Data
  example.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Sum](http://pycsp.org/documentation/constraints/Sum), [Table](http://pycsp.org/documentation/constraints/Table)

## Execution
```
  python QuadraticAssignment.py -data=QuadraticAssignment_qap.json
  python QuadraticAssignment.py -data=QuadraticAssignment_example.txt -dataparser=QuadraticAssignment_Parser.py
```

## Links
  - https://en.wikipedia.org/wiki/Quadratic_assignment_problem
  - https://coral.ise.lehigh.edu/data-sets/qaplib/

## Tags
  recreational
