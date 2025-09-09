# Problem: NursingWorkload

Balanced Nursing Workload Problem.
See Problem 069 at CSPLib.

## Data Example
  2zones1.json

## Model
  constraints: [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python NursingWorkload.py -data=<datafile.json>
  python NursingWorkload.py -data=<datafile.txt> -parser=NursingWorkload_Parser.py
```

## Links
  - https://www.csplib.org/Problems/prob069/
  - https://www.cril.univ-artois.fr/XCSP22/competitions/cop/cop

## Tags
  realistic, csplib, xcsp22
