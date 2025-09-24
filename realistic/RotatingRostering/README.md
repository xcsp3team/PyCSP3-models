# Problem: RotatingRostering

This problem is taken from real life rostering challenges (like nurse rostering).
The task is it to find a shift assignment for every employee for every day.
A rotation system is used to decrease the size of the problem.
Thus, only the rostering for one employee is calculated and all other employees gain a rotated version of the rostering.
So Employee 2 has in the first week the rostering of Employee 1 in the second week.
Employee 3 has in the first week the rostering of Employee 2 in the second week and Employee 1 in the third week etc.

See problem 087 at CSPLib.

## Data
  008-2-3.json

## Model
  constraints: [AllEqual](https://pycsp.org/documentation/constraints/AllEqual), [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Count](https://pycsp.org/documentation/constraints/Count), [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python RotatingRostering.py -data=<datafile.json>
  python RotatingRostering.py -data=<datafile.txt> -parser=RotatingRostering_ParserE.py
```

## Links
  - https://www.csplib.org/Problems/prob087/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/csp/csp

## Tags
  realistic, csplib, xcsp25
