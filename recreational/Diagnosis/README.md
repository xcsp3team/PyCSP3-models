# Problem Diagnosis

See Problem 042 on csplib.

Model-based diagnosis can be seen as taking as input a partially parameterized structural description of a system and a set of observations about that system.
Its output is a set of assumptions which, together with the structural description, logically imply the observations,
or that are consistent with the observations.

## Data Example
  example.json

## Model
  constraints: [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Diagnosis.py -data=<datafile.json>
```

## Links
 - https://www.csplib.org/Problems/prob042/

## Tags
  recreational, notebook, csplib
