# Problem Fapp
## Description
See Challenge ROADEF 2001 (FAPP: Problème d'affectation de fréquences avec polarization)

## Data
TODO

## Model
 Two variants manage in a slightly different manner the way distances are computed:
  - a main variant involving logical constraints
  - a variant 'sum' forcing the presence of Sum constraints

  constraints: [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python3 Fapp.py -data=Fapp_ex2.json
  python3 Fapp.py -data=Fapp_ex2.json -variant=short
```

## Links
  - https://www.minizinc.org/challenge2022/results2022.html
  - https://www.roadef.org/challenge/2001/fr/
## Tags
 recreational
