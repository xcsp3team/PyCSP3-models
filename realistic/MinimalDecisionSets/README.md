# Problem MinimalDecisionSets
## Description
The model, below, is close to (can be seen as the close translation of) the one submitted to the 2020 Minizinc challenge.
No Licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  breast-cancer-train4.json

## Model
  constraints: [Count](http://pycsp.org/documentation/constraints/Count), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python MinimalDecisionSets.py -data=<datafile.json>
  python MinimalDecisionSets.py -data=<datafile.dzn> -parser=MinimalDecisionSets_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2020/results2020.html

## Tags
  real, mzn20
