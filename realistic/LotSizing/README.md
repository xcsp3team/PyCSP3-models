# Problem LotSizing

Discrete Lot Sizing problem.

The model, below, is close to (can be seen as the close translation of) the one submitted to the 2019 Minizinc challenge.
The MZN model was proposed by Andrea Rendl-Pitrey (Satalia).
MIT Licence.

## Data Example
  pigment15a.json

## Model
  constraints: [AllDifferent](http://pycsp.org/documentation/constraints/AllDifferent), [Cardinality](http://pycsp.org/documentation/constraints/Cardinality), [Count](http://pycsp.org/documentation/constraints/Count), [Element](http://pycsp.org/documentation/constraints/Element), [Sum](http://pycsp.org/documentation/constraints/Sum)

## Execution
```
  python LotSizing.py -data=<datafile.json>
  python LotSizing.py -data=<datafile.dzn> -parser=LotSizing_ParserZ.py
```

## Links
  - https://www.csplib.org/Problems/prob058/
  - https://www.minizinc.org/challenge2019/results2019.html

## Tags
  realistic, csplib, mzn19, mzn20
