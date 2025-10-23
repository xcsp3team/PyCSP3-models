# Problem: PAX

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  pp-20-1c.json

## Model
  constraints: [Count](https://pycsp.org/documentation/constraints/Count), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python PAX.py -data=<datafile.json>
  python PAX.py -data=<datafile.dzn> -parser=PAX_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2019/results/

## Tags
  realistic, mzn19
