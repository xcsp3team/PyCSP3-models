# Problem: FAPP

See Challenge ROADEF 2001 (FAPP: Problème d'affectation de fréquences avec polarization)

## Data Example
  ex2.json

## Model
  Two variants manage in a slightly different manner the way distances are computed:
  - a main variant involving logical constraints
  - a variant 'aux' introducing auxiliary variubles

  constraints: [Table](https://pycsp.org/documentation/constraints/Table)

## Execution
```
  python FAPP.py -data=<datafile.json>
  python FAPP.py -data=<datafile.json> -variant=aux
  python FAPP.py -data=<datafile> -parser=FAPP_parser.py
```

## Links
  - https://www.roadef.org/challenge/2001/fr/
  - https://www.cril.univ-artois.fr/XCSP25/competitions/cop/cop

## Tags
  realistic, xcsp25
