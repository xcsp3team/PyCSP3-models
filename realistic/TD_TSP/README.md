# Problem: TD_TSP

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2015/2017 Minizinc challenges.
For the original MZN model, no licence was explicitly mentioned (MIT Licence is assumed).

## Data Example
  10-24-10.json

## Model
  constraints: [Channel](https://pycsp.org/documentation/constraints/Channel), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python TD_TSP.py -data=<datafile.json>
  python TD_TSP.py -data=<datafile.dzn> -parser=TD_TSP_ParserZ.py
```

## Links
  - https://www.minizinc.org/challenge/2017/results/

## Tags
  realistic, mzn15, mzn17
