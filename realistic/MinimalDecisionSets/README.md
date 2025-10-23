# Problem: MinimalDecisionSets

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  breast-cancer-train4.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MinimalDecisionSets.py -data=<datafile.json>
  python MinimalDecisionSets.py -data=<datafile.dzn> -parser=MinimalDecisionSets_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2020/results/

## Tags
  realistic, mzn20
