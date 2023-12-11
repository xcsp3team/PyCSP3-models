# Problem FAPP
## Description
See Challenge ROADEF 2001 (FAPP: Problème d'affectation de fréquences avec polarization)

## Data Example
  ex2.json

## Model
  Two variants manage in a slightly different manner the way distances are computed:
  - a main variant involving logical constraints
  - a variant 'sum' forcing the presence of Sum constraints

  constraints: [NoOverlap](http://pycsp.org/documentation/constraints/NoOverlap), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python FAPP.py -data=<datafile.json>
  python FAPP.py -data=<datafile.json>
```

## Links
  - https://www.roadef.org/challenge/2001/fr/

## Tags
  realistic
