# Problem: TilingRythmicCanons

Given a period n and a rhythm A subset of Zn, the Aperiodic Tiling Complements Problem consists in finding all its aperiodic complements B,
i.e., all subsets B of Zn such that A ⊕ B = Zn.

## Data example
  {'t': 16, 'n': 420, 'D': [60, 84, 140, 210], 'A': [0, 12, 24, 36, 48, 70, 82, 94, 106, 118]}

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [NValues](https://pycsp.org/documentation/constraints/NValues)

## Execution
```
  python TilingRythmicCanons.py -data=<datafile.json>
```

## Links
  - https://link.springer.com/article/10.1007/s10601-024-09375-6

## Tags
  realistic, xcsp25


Version 1 : with non 01 variables
