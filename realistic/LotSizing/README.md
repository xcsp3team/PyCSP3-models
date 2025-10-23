# Problem: LotSizing

Discrete Lot Sizing problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019/2020 Minizinc challenge.
The original MZN model was proposed by Andrea Rendl-Pitrey (Satalia).
MIT Licence.

## Data Example
  pigment15a.json

## Model
  constraints: [AllDifferent](https://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](https://pycsp.org/documentation/constraints/Cardinality), [Count](https://pycsp.org/documentation/constraints/Count), [Element](https://pycsp.org/documentation/constraints/Element), [Sum](https://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python LotSizing.py -data=<datafile.json>
  python LotSizing.py -data=<datafile.dzn> -parser=LotSizing_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob058/
  - https://www.minizinc.org/challenge/2020/results/

## Tags
  realistic, csplib, mzn19, mzn20
