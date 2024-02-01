# Problem Roster

The model, below, is close to (can be seen as the close translation of) the one submitted to the Minizinc challenges.
Instances (and the model) wre developed in the context of the ESPRIT PROJECT 22165 CHIC-2, with contributions from:
  - IC-Parc, Imperial College, London,
  - Bouygues research, Paris,
  - EuroDecision, Paris,
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  05.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python Roster.py -data=<datafile.json>
  python Roster.py -data=<datafile.dzn> -parser=Roster_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2023/results2023.html

## Tags
  realistic, mzn09, mzn11, mzn15, mzn23
