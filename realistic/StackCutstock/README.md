# Problem: StackCutstock

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  d03.json

## Model
  constraints: [Cumulative](https://pycsp.org/documentation/constraints/Cumulative), [Maximum](https://pycsp.org/documentation/constraints/Maximum), [Minimum](https://pycsp.org/documentation/constraints/Minimum), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python StackCutstock.py -data=<datafile.json>
  python StackCutstock.py -data=<datafile.dzn> -parser=StackCutstock_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, mzn19
